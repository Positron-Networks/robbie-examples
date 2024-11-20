from robbie import remote
from torchvision import datasets, transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR


class Net(nn.Module):
    """Define the CNN architecture."""

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output
    

    # Train the model by iterating through the data once
# If dry_run is set to True, it only goes through one batch of the data set
def train(model, device, train_loader, optimizer, epoch, log_interval, dry_run):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
            if dry_run:
                break



def check_performance(model, device, test_loader, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction="sum").item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    test_accuracy = 100.0 * correct / len(test_loader.dataset)

    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss, correct, len(test_loader.dataset), test_accuracy
        )
    )

@remote(tail=True, 
    funding_group_id="cecfc347-5680-4fb0-ae99-b029941b08dd",
    environment_id="cf4d655d-f72f-48b7-a8cd-0dbb7e5d34e9"
)
def perform_train(
    train_data,
    test_data,
    *,
    batch_size: int = 64,
    test_batch_size: int = 1000,
    epochs: int = 3,
    lr: float = 1.0,
    gamma: float = 0.7,
    no_cuda: bool = True,
    no_mps: bool = True,
    dry_run: bool = False,
    seed: int = 1,
    log_interval: int = 10,
):
    """PyTorch MNIST Example

    :param train_data: the training data set
    :param test_data: the test data set
    :param batch_size: input batch size for training (default: 64)
    :param test_batch_size: input batch size for testing (default: 1000)
    :param epochs: number of epochs to train (default: 14)
    :param lr: learning rate (default: 1.0)
    :param gamma: Learning rate step gamma (default: 0.7)
    :param no_cuda: disables CUDA training
    :param no_mps: disables macOS GPU training
    :param dry_run: quickly check a single pass
    :param seed: random seed (default: 1)
    :param log_interval: how many batches to wait before logging training status
    :return: the trained model
    """

    use_cuda = not no_cuda and torch.cuda.is_available()
    use_mps = not no_mps and torch.backends.mps.is_available()

    torch.manual_seed(seed)

    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    train_kwargs = {"batch_size": batch_size}
    test_kwargs = {"batch_size": test_batch_size}
    if use_cuda:
        cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    train_loader = torch.utils.data.DataLoader(train_data, **train_kwargs)
    test_loader = torch.utils.data.DataLoader(test_data, **test_kwargs)

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=lr)

    scheduler = StepLR(optimizer, step_size=1, gamma=gamma)

    # load the experiment run from the context

    print({"epochs": epochs, "lr": lr, "gamma": gamma})

    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, optimizer, epoch, log_interval, dry_run)
        check_performance(model, device, test_loader, epoch)
        scheduler.step()

    # log confusion matrix
    with torch.no_grad():
        data, target = next(iter(test_loader))
        data, target = data.to(device), target.to(device)
        output = model(data)
        pred = output.max(1, keepdim=True)[1]

    return model


def main():
    train_set = datasets.MNIST(
        "./data",
        train=True,
        transform=transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        ),
         download=True,
    )

    test_set = datasets.MNIST(
        "./data",
        train=False,
        transform=transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        ),
        download=True,
    )
    perform_train(train_set, test_set)


if __name__ == "__main__":
    main()