"""
This is a simple convolutional neural network for multiclass classification.
 
"""
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F#relu, tahn and other useful functions

class CNN(nn.module):

	def __init__(self, n_channels=1, num_classes=10):
		super(CNN).__init__()
		self.conv1 = nn.Conv2d(in_Channels = n_channels, out_Channels = 8, kernel_size = (3,3), stride = (1,1), padidng = (1,1))#maintains the size of the input
		self.pool = nn.MaxPool2d(kernel_size = (2,2), stride = (2,2))
		self.conv2 = nn.Conv2d(in_Channels = 8, out_Channels = 16, kernel_size=(3,3), stride =(1,1), padidng = (1,1))
		self.fc = nn.Linear(16*7*7, num_classes)

	def forward(self,x):
		x = F.relu(self.conv1(x))
		x = self.pool(x)
		x = F.relu(self.conv2(x))
		x = self.pool(x)
		x = x.reshape(x.shape[0], -1)#flatten the other dimensions to insert in the fc layer
		x = self.fc(x)

		return x 

