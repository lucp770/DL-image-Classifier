
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F#relu, tahn and other useful functions
from matplotlib import pyplot as plt

from torch.utils.data import DataLoader#utilities for database managment, functions to create minibatches, etc
import torchvision.datasets as datasets#pytorch datasets such as mnist and cifar.
import torchvision.transforms as transforms#useful transformations for images (data augmentation functionalities)


class NN(nn.Module):
	def __init__(self, input_size, num_classes):
		super(NN,self).__init__()#do not forget to include self in the parameters
		# first layer (50 units of hidden layer)
		self.fc1 = nn.Linear(input_size, 50)
		self.fc2 = nn.Linear(50, num_classes)

	def forward(self,x):
		x = F.relu(self.fc1(x))
		x = self.fc2(x)
		# we dont set a relu in the output because we are using CEL that applies the softmax

		return x
		
# lets make a simple test

def test_NN():
	#a function just to see with the network is executed with the right dimensions.
	model = NN(784,10)
	x = torch.randn(64,784)#create a mini-batch of 64 elements
	print(model(x).shape)#64x10 is expected

# set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# set the hyperparameters
input_size = 784
num_classes = 10
learning_rate = 0.001
batch_size = 64
num_epochs = 3

# load the data (MNIST)
train_dataset = datasets.MNIST(root = 'dataset', train = True, download = True, transform = transforms.ToTensor())

# train loader to manage the batches and shuffle the dataset after every epoch
train_loader = DataLoader(dataset = train_dataset, batch_size = batch_size, shuffle = True)
# the shuffle garantees that we dont have the same images in the batch in each epoch

test_dataset = datasets.MNIST(root = 'dataset', train = False, download = True, transform = transforms.ToTensor())
test_loader = DataLoader(dataset = test_dataset, batch_size = batch_size, shuffle = True)

# initialize the network
model = NN(input_size = input_size, num_classes = num_classes).to(device)

# set the loss function and optimizer
loss = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr = learning_rate)

def train_network():
	for epoch in range(num_epochs):
		# we apply enumerate to indexate the batch
		for batch_index, (data,targets) in enumerate(train_loader):
			# send the data to the device before the training step
			data = data.to(device = device)
			targets = targets.to(device=device)

			# print(data.shape)

			# since we are not using a 2D network we need to transform the data from
			# (64,1,28,28) to (64, 784)

			data = data.reshape(data.shape[0], -1)

			# apply the network to the data
			output = model(data)

			# calculate the loss
			out_loss = loss(output, targets)

			#backpropagation
			optimizer.zero_grad()#we need to set the gradients to zero in every batch
			out_loss.backward()#calculate the gradients
			optimizer.step()#update the wheights

#execute training
print('\n training the network .... \n')
train_network()

def check_accuracy(loader, model):
	if loader.dataset.train: print('checking accuracy in the training set .... ')
	else: print('checking accuracy in the training set .... ')

	num_correct = 0
	num_samples = 0
	model.eval()#change the model to evaluation mode
	 
	with torch.no_grad():#set pytorch to not compute the gradients, this is unnecesary computation in this step
			for x,y in loader:
				x = x.to(device =device)
				y = y.to(device = device)
				x = x.reshape(x.shape[0], -1)

				scores = model(x)
				#get what digit the model predict:
				_, predictions = scores.max(1)
				num_correct +=(predictions ==y).sum()
				num_samples += predictions.size(0)
	
			print(f'The model got right: {num_correct} / {num_samples} \n accuracy: {float(num_correct)/float(num_samples)*100:.2f}')
	model.train()#change the model back to training mode.

print('accuracy after {} epochs: \n '.format(num_epochs))
# check_accuracy(train_loader, model)
check_accuracy(test_loader, model)


print('\n \n here are 5 examples ....')
indexes = [int(i) for i in (torch.rand(6)*10)]
egs = []
aux=[]

# create a list with the examples.
for i in indexes:
	eg = test_dataset[i][0]
	egs.append(eg.squeeze())

	pred = eg.reshape(eg.shape[0], -1)#generate [1, 784]
	aux.append(pred.squeeze())

# make the predictions
y = [torch.argmax(model(e)) for e in aux]

eg = egs[0]

# # since we are not using a 2D network we need to transform the data from
# 			# (64,1,28,28) to (64, 784)

# 			data = data.reshape(data.shape[0], -1)
print('\n shape eg', eg.shape)

# print(egs)

# y =model(eg)


print('predictions', y)
# print('predictions max1', y.max(1))

# print(indexes)


def show_examples(egs, predictions):
	size = int(.5*len(egs))

	for idx in range(len(egs)):

		plt.subplot(size,size,idx+1)
		plt.imshow(egs[idx])
		plt.title('prediction: ' + str(int(predictions[idx])))
	plt.subplots_adjust(hspace = 0.8)

	plt.show()

show_examples(egs,y)

# print(test_dataset[0][0].squeeze().shape)





# https://pytorch.org/tutorials/beginner/introyt/modelsyt_tutorial.html