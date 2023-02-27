import pickle

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

def save_as_byte_stream(labels_array):
	"""
	transform an array of labels, to a byte stream and save to a picke file.

	"""
	pickle.dump(labels_array, name);



# an example of use:
# get the file 
file = './labels'
# obtain the array of labels
array = red_data(file)
# save the array of labels in the folder, as a pickle file.
save_as_byte_stream(array);

