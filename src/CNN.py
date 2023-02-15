"""
This is a simple convolutional neural network for multiclass classification.
 
"""
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F#relu, tahn and other useful functions
from torch.utils.data import DataLoader#utilities for database managment, functions to create minibatches, etc
import torchvision.datasets as datasets#pytorch datasets such as mnist and cifar.
import torchvision.transforms as transforms#useful transformations for images (data augmentation functionalities)

class CNN(nn.Module):

	def __init__(self, in_channels=1, num_classes=10):
		super(CNN,self).__init__()
		self.conv1 = nn.Conv2d(in_channels = 1, out_channels = 8, kernel_size = (3,3), stride = (1,1), padding = (1,1))#maintains the size of the input
		self.pool = nn.MaxPool2d(kernel_size = (2,2), stride = (2,2))
		self.conv2 = nn.Conv2d(in_channels = 8, out_channels = 16, kernel_size=(3,3), stride =(1,1), padding = (1,1))
		self.fc = nn.Linear(16*7*7, num_classes)

	def forward(self,x):
		x = F.relu(self.conv1(x))
		x = self.pool(x)
		x = F.relu(self.conv2(x))
		x = self.pool(x)
		x = x.reshape(x.shape[0], -1)#flatten the other dimensions to insert in the fc layer
		x = self.fc(x)
		return x 

# set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu');

# set the hyperparameters ( is not necessary to set the input size, pytorch is inteligent)
learning_rate = 0.001
batch_size = 64
num_epochs = 1

# get the training data
train_data = datasets.MNIST(root ='dataset', train = True, download = True, transform = transforms.ToTensor());
train_loader = DataLoader(dataset = train_data,batch_size = batch_size, shuffle = True )

test_data = datasets.MNIST(root = 'dataset', train = False, download = True, transform = transforms.ToTensor())
test_loader = DataLoader(dataset = test_data, batch_size = batch_size, shuffle = True)

# create the model instance
model = CNN()#is not necessary to pass any parameter because we already configured standard values

# x = torch.rand(64,1,28,28)#the 1 here is for the number of channels
# print(model(x).shape)
loss_function= nn.CrossEntropyLoss();
optimizer = optim.Adam(model.parameters(), lr = learning_rate)

def execute_training_epoch():
	for idx, (data,targets) in enumerate(train_loader):
		data = data.to(device = device)
		targets = targets.to(device = device)
		output = model(data)
		loss = loss_function(output, targets)

		# backpropagation
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

def train_network():
	for epoch in range(num_epochs):
		execute_training_epoch()

def check_acurracy(loader, model):
	if loader.dataset.train: print('checking accuracy on training data... \n')
	else: print('checking accuracy on test data... \n')

	n_correctn_samples = 0
	model.eval()

	with torch.no_grad():
		for x,y in loader:#this time i did not enumerate
			x = x.to(device = device)
			y = y.to(device = device)
			_,max_score_index = model(x).max(1)
			#create a personalized way of doing this.

print('\n training the network .... \n')
train_network()
check_acurracy(test_loader,model)

