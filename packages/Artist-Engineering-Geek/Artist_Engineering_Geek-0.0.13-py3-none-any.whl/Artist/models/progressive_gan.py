"""
Code mostly from https://github.com/rosinality/progressive-gan-pytorch
Vast majority of credit goes to github user rosinality for this right here, I don't want to just copy + paste and steal

https://i.kym-cdn.com/entries/icons/original/000/028/306/Screen_Shot_2019-01-24_at_3.23.42_PM.jpg
Professionals have standards
I'm going to copy + paste + credit the person I got this from
¯\_(ツ)_/¯
"""
from math import sqrt

import torch
from torch import nn
from torch.autograd import Variable
from torch.nn import functional as F
from torch.nn import init


def init_linear(linear):
    init.xavier_normal(linear.weight)
    linear.bias.data.zero_()


def init_conv(conv, glu=True):
    init.kaiming_normal(conv.weight)
    if conv.bias is not None:
        conv.bias.data.zero_()


class SpectralNorm:
    def __init__(self, name):
        self.name = name

    def compute_weight(self, module):
        weight = getattr(module, self.name + '_orig')
        u = getattr(module, self.name + '_u')
        size = weight.size()
        weight_mat = weight.contiguous().view(size[0], -1)
        if weight_mat.is_cuda:
            u = u.cuda()
        v = weight_mat.t() @ u
        v = v / v.norm()
        u = weight_mat @ v
        u = u / u.norm()
        weight_sn = weight_mat / (u.t() @ weight_mat @ v)
        weight_sn = weight_sn.view(*size)

        return weight_sn, Variable(u.data)

    @staticmethod
    def apply(module, name):
        fn = SpectralNorm(name)
        weight = getattr(module, name)
        del module._parameters[name]
        module.register_parameter(name + '_orig', nn.Parameter(weight.data))
        input_size = weight.size(0)
        u = Variable(torch.randn(input_size, 1) * 0.1, requires_grad=False)
        setattr(module, name + '_u', u)
        setattr(module, name, fn.compute_weight(module)[0])
        module.register_forward_pre_hook(fn)
        return fn

    def __call__(self, module, input):
        weight_sn, u = self.compute_weight(module)
        setattr(module, self.name, weight_sn)
        setattr(module, self.name + '_u', u)


def spectral_norm(module, name='weight'):
    SpectralNorm.apply(module, name)
    return module


class EqualLR:
    def __init__(self, name):
        self.name = name

    def compute_weight(self, module):
        weight = getattr(module, self.name + '_orig')
        fan_in = weight.data.size(1) * weight.data[0][0].numel()
        return weight * sqrt(2 / fan_in)

    @staticmethod
    def apply(module, name):
        fn = EqualLR(name)
        weight = getattr(module, name)
        del module._parameters[name]
        module.register_parameter(name + '_orig', nn.Parameter(weight.data))
        module.register_forward_pre_hook(fn)

        return fn

    def __call__(self, module, input):
        weight = self.compute_weight(module)
        setattr(module, self.name, weight)


def equal_lr(module, name='weight'):
    EqualLR.apply(module, name)

    return module


class PixelNorm(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        return input / torch.sqrt(torch.mean(input ** 2, dim=1, keepdim=True) + 1e-8)


class SpectralNormConv2d(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__()

        conv = nn.Conv2d(*args, **kwargs)
        init.kaiming_normal(conv.weight)
        conv.bias.data.zero_()
        self.conv = spectral_norm(conv)

    def forward(self, input):
        return self.conv(input)


class EqualConv2d(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__()

        conv = nn.Conv2d(*args, **kwargs)
        conv.weight.data.normal_()
        conv.bias.data.zero_()
        self.conv = equal_lr(conv)

    def forward(self, _input):
        return self.conv(_input)


class ConvBlock(nn.Module):
    def __init__(self, in_channel, out_channel, kernel_size, padding, kernel_size2=None, padding2=None, pixel_norm=True,
                 spectral_norm=False):
        super().__init__()

        pad1 = padding
        pad2 = padding
        pad2 = padding2 if padding2 is not None else pad2

        kernel1 = kernel_size
        kernel2 = kernel_size
        if kernel_size2 is not None:
            kernel2 = kernel_size2

        if spectral_norm:
            self.conv = nn.Sequential(
                SpectralNormConv2d(in_channel, out_channel, kernel1, padding=pad1),
                nn.LeakyReLU(0.2),
                SpectralNormConv2d(out_channel, out_channel, kernel2, padding=pad2),
                nn.LeakyReLU(0.2)
            )
        else:
            if pixel_norm:
                self.conv = nn.Sequential(
                    EqualConv2d(in_channel, out_channel, kernel1, padding=pad1),
                    PixelNorm(),
                    nn.LeakyReLU(0.2),
                    EqualConv2d(out_channel, out_channel, kernel2, padding=pad2),
                    PixelNorm(),
                    nn.LeakyReLU(0.2)
                )
            else:
                self.conv = nn.Sequential(
                    EqualConv2d(in_channel, out_channel, kernel1, padding=pad1),
                    nn.LeakyReLU(0.2),
                    EqualConv2d(out_channel, out_channel, kernel2, padding=pad2),
                    nn.LeakyReLU(0.2)
                )

    def forward(self, input):
        out = self.conv(input)

        return out


class Generator(nn.Module):
    def __init__(self, code_dim=512 - 10, n_label=10):
        super().__init__()

        self.label_embed = nn.Embedding(n_label, n_label)
        self.code_norm = PixelNorm()
        self.label_embed.weight.data.normal_()
        self.progression = nn.ModuleList([
            ConvBlock(512, 512, 4, 3, 3, 1),
            ConvBlock(512, 512, 3, 1),
            ConvBlock(512, 512, 3, 1),
            ConvBlock(512, 512, 3, 1),
            ConvBlock(512, 256, 3, 1),
            ConvBlock(256, 128, 3, 1)
        ])

        self.to_rgb = nn.ModuleList([
            nn.Conv2d(512, 3, 1),
            nn.Conv2d(512, 3, 1),
            nn.Conv2d(512, 3, 1),
            nn.Conv2d(512, 3, 1),
            nn.Conv2d(256, 3, 1),
            nn.Conv2d(128, 3, 1)
        ])

    def forward(self, _input, label, step=0, alpha=-1):
        _input = self.code_norm(_input)
        label = self.label_embed(label)
        out = torch.cat([_input, label], 1).unsqueeze(2).unsqueeze(3)

        for i, (conv, to_rgb) in enumerate(zip(self.progression, self.to_rgb)):
            if i > 0 and step > 0:
                upsample = F.interpolate(out, scale_factor=2)
                out = conv(upsample)

            else:
                out = conv(out)

            if i == step:
                out = to_rgb(out)
                if i > 0 and 0 <= alpha < 1:
                    skip_rgb = self.to_rgb[i - 1](upsample)
                    out = (1 - alpha) * skip_rgb + alpha * out

                break

        return out


class Discriminator(nn.Module):
    def __init__(self, n_label=10):
        super().__init__()

        self.progression = nn.ModuleList([
            ConvBlock(128, 256, 3, 1, pixel_norm=False, spectral_norm=False),
            ConvBlock(256, 512, 3, 1, pixel_norm=False, spectral_norm=False),
            ConvBlock(512, 512, 3, 1, pixel_norm=False, spectral_norm=False),
            ConvBlock(512, 512, 3, 1, pixel_norm=False, spectral_norm=False),
            ConvBlock(512, 512, 3, 1, pixel_norm=False, spectral_norm=False),
            ConvBlock(513, 512, 3, 1, 4, 0, pixel_norm=False, spectral_norm=False)]
        )

        self.from_rgb = nn.ModuleList([
            nn.Conv2d(3, 128, 1),
            nn.Conv2d(3, 256, 1),
            nn.Conv2d(3, 512, 1),
            nn.Conv2d(3, 512, 1),
            nn.Conv2d(3, 512, 1),
            nn.Conv2d(3, 512, 1)]
        )

        self.n_layer = len(self.progression)

        self.linear = nn.Linear(512, 1 + n_label)

    def forward(self, _input, step=0, alpha=-1):
        for i in range(step, -1, -1):
            index = self.n_layer - i - 1

            if i == step:
                out = self.from_rgb[index](_input)

            if i == 0:
                mean_std = _input.std(0).mean()
                mean_std = mean_std.expand(_input.size(0), 1, 4, 4)
                out = torch.cat([out, mean_std], 1)

            out = self.progression[index](out)

            if i > 0:
                out = F.avg_pool2d(out, 2)

                if i == step and 0 <= alpha < 1:
                    skip_rgb = F.avg_pool2d(_input, 2)
                    skip_rgb = self.from_rgb[index + 1](skip_rgb)
                    out = (1 - alpha) * skip_rgb + alpha * out

        out = out.squeeze(2).squeeze(2)
        # print(input.size(), out.size(), step)
        out = self.linear(out)

        return out[:, 0], out[:, 1:]
