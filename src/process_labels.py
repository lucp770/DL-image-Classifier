import os
import json

def red_data(file):
	"""
	read the data from a file with the labels, when the file is formated as :
	 https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt

	return an array with the labels.
	"""
	labels = []
	with open(file, 'r', encoding = 'utf-8') as file:
		for line in file:
			labels.append(line[:-1])#ignores the last element, the \n especial character
	return labels

def save_as_json(labels_array, filename):
	"""
	transform an array of labels, to a json file.
	save to /labels/<filename.json>
	"""
	out_file = open('./labels/' + filename, 'w')#open a file with name indicated in the writing mode
	json.dump(labels_array, out_file);


# an example of use:
# get the file 
file = './labels_imagenet'
# obtain the array of labels
array = red_data(file)
# save the array of labels in the folder, as a pickle file.
save_as_json(array,file);


