# %%

import torch
import torch.optim
from torch import nn
from torch.utils import data
import numpy as np
import itertools
from tqdm import tqdm

from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)

# %%

import torchvision

means = np.array([125.30691805, 122.95039414, 113.86538318]) / 255
stds = np.array([62.99321928, 62.08870764, 66.70489964]) / 255

train_transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.Pad(4),
        torchvision.transforms.RandomCrop(32),
    ]
)

train_data = torchvision.datasets.CIFAR10(root="./data", train=True)
train_x = train_data.data / 255.
train_y = train_data.targets
train_x = (train_x - means) / stds
train_x = np.transpose(train_x, [0, 3, 1, 2])
train_x = torch.Tensor(train_x)
train_y = torch.Tensor(train_y).to(torch.long)

valid_data = torchvision.datasets.CIFAR10(root="./data", train=False)
valid_x = valid_data.data / 255.
valid_y = valid_data.targets
valid_x = (valid_x - means) / stds
valid_x = np.transpose(valid_x, [0, 3, 1, 2])
valid_x = torch.Tensor(valid_x)
valid_y = torch.Tensor(valid_y).to(torch.long)


class TensorDataset(torch.utils.data.Dataset):
    def __init__(self, tensors, transform=None):
        self.tensors = tensors
        self.transform = transform

    def __getitem__(self, index):
        x = self.tensors[0][index]

        if self.transform:
            x = self.transform(x)

        y = self.tensors[1][index]
        return x, y

    def __len__(self):
        return self.tensors[0].shape[0]


train_load = torch.utils.data.DataLoader(
    TensorDataset((train_x, train_y), train_transform),
    batch_size=128,
    shuffle=True,
    pin_memory=True, )

valid_load = torch.utils.data.DataLoader(
    TensorDataset((valid_x, valid_y), None),
    batch_size=128,
    shuffle=False,
    pin_memory=True, )


# %%

class Metric:
    def __init__(self):
        self.value = 0
        self.n_samples = 0

    def __call__(self, new_value, n_samples=1):
        self.value += new_value * n_samples
        self.n_samples += n_samples

    def reset_states(self):
        self.value = 0
        self.n_samples = 0

    def result(self):
        if self.n_samples:
            return self.value / self.n_samples

    def __repr__(self):
        r = self.result()
        if r is None:
            return 'None'
        else:
            return str(float(r))


class Trainer:
    def __init__(
            self,
            model: nn.Module,
            train_ds,
            valid_ds,
            loss_fn,
            optimizer: torch.optim.Optimizer,
            scheduler,
            device,
    ):
        self.device = device
        self.model = model.to(device)
        self.train_ds = train_ds
        self.valid_ds = valid_ds
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.scheduler = scheduler

        self.metrics = {
            "train_loss": Metric(),
            "train_acc": Metric(),
            "valid_loss": Metric(),
            "valid_acc": Metric()
        }

    def train_epoch(self, use_pbar=False):
        self.model.train(True)
        self.metrics["train_loss"].reset_states()
        self.metrics["train_acc"].reset_states()

        if use_pbar:
            pbar = tqdm(self.train_ds)
        else:
            pbar = self.train_ds
        for x, y in pbar:
            loss, acc = self.train_step(x, y)
            self.scheduler.step()
            self.metrics["train_loss"](loss, len(x))
            self.metrics["train_acc"](acc, len(x))

    def valid_epoch(self):
        loss = 0
        n_el = 0
        self.model.train(False)
        self.metrics["valid_loss"].reset_states()
        self.metrics["valid_acc"].reset_states()

        with torch.no_grad():
            for x, y in self.valid_ds:
                x = x.to(self.device)
                y = y.to(self.device)
                outs = self.model(x)
                loss = self.loss_fn(outs, y)

                preds = torch.argmax(outs, dim=-1)
                acc = torch.mean((y == preds).to(torch.float32))
                self.metrics["valid_loss"](loss, len(x))
                self.metrics["valid_acc"](acc, len(x))

    def train_step(self, x, y):
        self.optimizer.zero_grad()
        x = x.to(self.device)
        y = y.to(self.device)
        outs = self.model(x)
        loss = self.loss_fn(outs, y)

        loss.backward()
        self.optimizer.step()
        preds = torch.argmax(outs, dim=-1)
        acc = torch.mean((y == preds).to(torch.float32))
        return loss, acc


from pytorch_functional import examples

model = examples.ResNet(
    input_shape=(3, 32, 32),
    n_classes=10,
    version=("WRN", 16, 4)
)

optim = torch.optim.SGD(
    model.parameters(),
    lr=0.1,
    momentum=0.9,
    weight_decay=1e-4
)
scheduler = torch.optim.lr_scheduler.StepLR(optim,
                                            step_size=24000,
                                            gamma=0.2)

trainer = Trainer(
    model=model,
    train_ds=train_load,
    valid_ds=valid_load,
    loss_fn=nn.CrossEntropyLoss(),
    optimizer=optim,
    scheduler=scheduler,
    device="cuda",
)

# %%

for idx in range(2):
    trainer.train_epoch()
    trainer.valid_epoch()
    print(idx, trainer.metrics, scheduler.get_last_lr())

# %%
