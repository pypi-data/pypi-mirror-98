import json
from os import cpu_count
from typing import List
from typing import Union

import numpy as np
import torch
from pytorch_lightning import LightningModule
from src.Artist.models.progressive_gan import Generator, Discriminator
from torch import Tensor
from torch.autograd import grad
from torch.optim import Optimizer
from torch.utils.data.dataloader import DataLoader
from torch.utils.data.dataset import Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision.utils import make_grid

from src.Artist.dataset import unsplash_downloader


class CustomDataset(Dataset):
    def __init__(self, art_type: str = "celeba", n=1000, iterations: List[int] = None, batch_sizes: List[int] = None,
                 step: int = 0, json_path: str = ""):
        path = json.load(open(json_path))["filepaths"]["image dirpath"]
        if iterations is None:
            iterations = [100000] * 6
        if batch_sizes is None:
            batch_sizes = [8] * 6

        self.path = unsplash_downloader(art_type, path, n)
        self.iterations = iterations
        self.batch_sizes = batch_sizes
        self.iteration = 0
        self.step = step
        self.dataset = None
        self.first_flag = True
        self.__generate_dataset__()

        super().__init__()

    def __generate_dataset__(self):
        size = 2 ** (self.step + 2)
        dataset = ImageFolder(
            root=self.path,
            transform=transforms.Compose([
                transforms.Resize(size + int(size * 0.1) + 1),
                transforms.RandomCrop(size),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor()
            ])
        )
        self.dataset = iter(dataset)

    def __len__(self):
        return sum(self.iterations)

    def __next_step__(self):
        if self.step < len(self.iterations) and not self.first_flag:
            self.step += 1
            self.iteration = 0
            self.__generate_dataset__()
        else:
            self.first_flag = False

    def __getitem__(self, item):
        beta = 2
        alpha = min(1., beta * (self.iteration / self.iterations[self.step]))

        # increment step if we're done with the current step
        if self.iteration >= self.iterations[self.step]: self.__next_step__()

        images, labels = [], []
        for index in range(self.batch_sizes[self.step]):
            try:
                image, label = next(self.dataset)
            except (OSError, StopIteration):
                # Iterating through this image folder is done, now reset it
                self.__generate_dataset__()
                image, label = next(self.dataset)
            images.append(image)
            labels.append(torch.Tensor([label]).type(torch.IntTensor))

        images = torch.stack(images)
        labels = torch.stack(labels)

        # increment iteration
        self.iteration += self.batch_sizes[self.step]

        # how many iterations left until next up-scaling?
        iterations_left = self.iterations[self.step] - self.iteration
        return images, labels, torch.Tensor([alpha]), torch.Tensor([self.step]), torch.tensor([iterations_left])


class ProgressiveGAN(LightningModule):
    def __init__(self, art_type: str = "celeba", name: str = "Fatima", batch_sizes: List[int] = None, n_label: int = 1,
                 display_interval: int = 100, n: int = 1000, iterations: List[int] = None, display_length: int = 32,
                 initial_step: int = 0):
        super().__init__()
        iterations = [100000] * 6 if iterations is None else iterations
        batch_sizes = [8] * 6 if batch_sizes is None else batch_sizes

        self.name, self.art_type, self.code_size, self.index, self.display_length, self.display_interval = \
            name, art_type, 512 - n_label, 0, display_length, display_interval

        self.dataset = CustomDataset(
            batch_sizes=batch_sizes,
            art_type=art_type,
            n=n,
            iterations=iterations,
            step=initial_step
        )

        self.generator = Generator(self.code_size, n_label).cuda()
        self.discriminator = Discriminator(n_label).cuda()

        self.testing_seed = torch.randn(display_length, self.code_size)
        self.one, self.m_one = torch.tensor(1, dtype=torch.float).cuda(), torch.tensor(-1, dtype=torch.float).cuda()

    def __get_losses__(self, optimizer_idx: int, predictions: Union[List[torch.Tensor], torch.Tensor],
                       real_images: torch.Tensor, fake_images: torch.Tensor, step: int, alpha: float):
        if optimizer_idx == 0:
            discriminator_predictions = predictions
            generator_loss = -discriminator_predictions.mean()

            # Logging
            log = {"generator_loss": generator_loss}
            self.logger.log_metrics(log, self.global_step)
            self.log_dict(log, prog_bar=True)

            return generator_loss

        if optimizer_idx == 1:
            real_predictions = predictions[0]
            fake_predictions = predictions[1]

            real_predictions_loss = real_predictions.mean() - 0.001 * (real_predictions ** 2).mean()
            fake_predictions_loss = fake_predictions.mean()

            epsilon = torch.rand(real_images.shape[0], 1, 1, 1).to(self.device)
            x_hat = epsilon * real_images.data + (1 - epsilon) * fake_images.detach().data
            x_hat.requires_grad = True
            hat_predict = self.discriminator(x_hat, step=step, alpha=alpha)[0]
            grad_x_hat = grad(outputs=hat_predict.sum(), inputs=x_hat, create_graph=True)[0]
            grad_loss = ((grad_x_hat.view(grad_x_hat.shape[0], -1).norm(2, dim=1) - 1) ** 2).mean()

            discriminator_loss = torch.stack([real_predictions_loss, fake_predictions_loss, grad_loss])

            # Logging
            log = {"grad_prediction_losses": discriminator_loss[-1]}
            self.logger.log_metrics(log, self.global_step)
            self.log_dict(log, prog_bar=True)

            return discriminator_loss

    def training_step(self, batch, batch_idx, optimizer_idx):
        alpha = batch[2].item()
        step = int(batch[3].item())
        iterations_left = int(batch[4].item())
        labels = batch[1].squeeze().to(self.device)

        real_images = batch[0].squeeze().to(self.device)
        seed = torch.randn(real_images.shape[0], self.code_size).to(self.device)
        fake_images = self.generator(seed, label=labels, step=step, alpha=alpha)

        self.log_dict({"iterations_left": iterations_left, "step": step, "alpha": alpha}, prog_bar=True)

        if optimizer_idx == 0:
            # Training the generator
            discriminator_predictions = self.discriminator(fake_images, step=step, alpha=alpha)[0]
            loss = self.__get_losses__(optimizer_idx, discriminator_predictions, real_images, fake_images, step, alpha)

            if self.global_step % self.display_interval == 0:
                self.__display_samples__(real_images, step, alpha)
            return loss

        if optimizer_idx == 1:
            # Training the Discriminator
            real_predictions = self.discriminator(real_images, step=step, alpha=alpha)[0]
            fake_predictions = self.discriminator(fake_images.detach(), step=step, alpha=alpha)[0]

            predictions = [real_predictions, fake_predictions]
            loss = self.__get_losses__(optimizer_idx, predictions, real_images, fake_images, step, alpha)

            return loss

    def backward(self, loss: Tensor, optimizer: Optimizer, optimizer_idx: int, *args, **kwargs) -> None:
        if optimizer_idx == 0:
            loss.backward()

        if optimizer_idx == 1:
            loss[0].backward(self.m_one, retain_graph=True)
            loss[1].backward(self.one, retain_graph=True)
            loss[2].backward()

    def configure_optimizers(self):
        g_optimizer = torch.optim.Adam(self.generator.parameters(), lr=0.001, betas=(0.0, 0.99))
        d_optimizer = torch.optim.Adam(self.discriminator.parameters(), lr=0.001, betas=(0.0, 0.99))
        return [g_optimizer, d_optimizer], []

    def __display_samples__(self, real_images, step, alpha):
        with torch.no_grad():
            generated_images = self.generator(
                self.testing_seed.to(self.device),
                torch.from_numpy(np.array([0] * self.display_length)).to(self.device),
                step,
                alpha
            )
            self.logger.experiment.add_image(
                "{}'s artwork of {}".format(self.name, self.art_type),
                make_grid(generated_images),
                self.global_step
            )
            self.logger.experiment.add_image(
                "Sample Real Images".format(self.name, self.art_type),
                make_grid(real_images),
                self.global_step
            )

    def train_dataloader(self) -> DataLoader:
        # BATCH SIZE MUST BE 1, NO EXCEPTIONS WITHOUT COMPLETE REDOING OF THE CODE FROM SCRATCH
        # DON'T YOU FUCKING DARE CHANGE THIS BATCH SIZE UNLESS U WANT TO DESTROY THIS WHOLE CODE BASE
        return DataLoader(self.dataset, num_workers=cpu_count() - 2, batch_size=1)
