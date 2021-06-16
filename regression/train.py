import torch
import os

from torchvision import transforms
from model import KeyPointModel
from datasets import KeyPointDatasets
from torch.utils.data import DataLoader
from visual import Visualizer

IMG_SIZE = 640,480


vis = Visualizer(env="keypoint")

def train(model, epoch, dataloader, optimizer, criterion):
    model.train()
    for itr, (image, label) in enumerate(dataloader):
        bs = image.shape[0]
        output = model(image)
        loss = criterion(output, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if itr % 4 == 0:
            print("epoch:%2d|step:%04d|loss:%.6f" % (epoch, itr, loss.item()/bs))
            vis.plot_many_stack({"train_loss": loss.item()*100/bs})


def test(model, epoch, dataloader, criterion):
    model.eval()
    sum_loss = 0.
    n_sample = 0
    for itr, (image, label) in enumerate(dataloader):
        output = model(image)
        loss = criterion(output, label)

        sum_loss += loss.item()
        n_sample += image.shape[0]
    print("TEST: epoch:%02d-->loss:%.6f" % (epoch, sum_loss/n_sample))
    vis.plot_many_stack({"test_loss": sum_loss*1000/n_sample})
    return sum_loss / n_sample


if __name__ == "__main__":

    total_epoch = 300
    bs = 10
    ########################################
    transforms_all = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((480,640)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4372, 0.4372, 0.4373],
                             std=[0.2479, 0.2475, 0.2485])
    ])

    datasets = KeyPointDatasets(root_dir=".\data", transforms=transforms_all)

    data_loader = DataLoader(datasets, shuffle=True,
                             batch_size=bs, collate_fn=datasets.collect_fn)

    model = KeyPointModel()

    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
    # criterion = torch.nn.SmoothL1Loss()
    criterion = torch.nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                step_size=30,
                                                gamma=0.1)

    for epoch in range(total_epoch):
        train(model, epoch, data_loader, optimizer, criterion)
        loss = test(model, epoch, data_loader, criterion)

        if epoch % 10 == 0:
            torch.save(model.state_dict(),
                       ".\weights\epoch_%d_%.3f.pt" % (epoch, loss*1000))
