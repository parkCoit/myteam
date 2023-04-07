import os

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset

# Define the dataset class
class VideoDataset(Dataset):
    def __init__(self, video_dir, label_file, transform=None):
        self.video_dir = video_dir
        self.transform = transform
        with open(label_file, 'r') as f:
            self.labels = [int(gt) for gt in f.readline().split(',')]

    def __getitem__(self, index):
        video_ls = os.listdir('/app/models/data/3frame_videos_but_348')
        video_file = f'{self.video_dir}/{video_ls[index]}'
        # Load video data here using OpenCV or other video processing libraries
        cap = cv2.VideoCapture(video_file)
        video_data = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_data.append(frame)
        cap.release()
        video_data = np.array(video_data)
        print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{video_data[0][0][0]}")
        print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{video_data.shape}")

        if self.transform is not None:
            video_data2 = np.array( [[ 1, 2, 3],
                 [ 4, 2, 5],[ 4, 2, 5]] )
            video_data = self.transform(video_data2)
        label = self.labels[index]
        return video_data, label

    def __len__(self):
        return len(self.labels)

# Define the ResNet18-based model
class VideoClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        return self.resnet(x)
###################################################################
# Define the data transforms to be applied to each video
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load the training data
train_data = VideoDataset('/app/models/data/3frame_videos_but_348',
                          '/app/models/label/spell_1_truth.txt',
                          transform=transform)
train_loader = DataLoader(train_data, batch_size=16, shuffle=True)

# Initialize the model, loss function, and optimizer
model = VideoClassifier(num_classes=5)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

# Train the model
num_epochs = 10

for epoch in range(num_epochs):
    for i, (inputs, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        print(f'Epoch {epoch+1}, Batch {i+1}/{len(train_loader)}, Loss: {loss.item()}')

# Save the trained model
torch.save(model.state_dict(), '/app/models/model_save')
