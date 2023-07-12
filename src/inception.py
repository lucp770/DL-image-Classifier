import torch
from torchvision import transforms
from matplotlib import pyplot as plt
from PIL import Image
import json

def RGBA_processor(RGBA_image):
	"""preprocessing for RGBA image type:
		cut the image, to dimension 299 x 299, transform to tensor, normalize it """
	preprocess = transforms.Compose([transforms.Resize(299),
	transforms.CenterCrop(299),
	transforms.ToTensor(),
	transforms.Normalize(mean=[0.485, 0.456, 0.406,0.406], std=[0.229, 0.224, 0.225, 0.225]),
	])

	transformed_image = preprocess(RGBA_image);

	return transformed_image

def RGB_processor(RGB_image):
	"""preprocessing for RGB image type:
		normalize the image and return a torch.tensor """
	preprocess = transforms.Compose([transforms.Resize(299),
	transforms.CenterCrop(299),
	transforms.ToTensor(),
	transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	transformed_image = preprocess(RGB_image);

	return transformed_image

def get_labels(file):

	with open(file) as label_file:
		categories = json.load(label_file)
	return categories


def Apply_model(processed_image):

	PIL_image = Image.fromarray(processed_image)

	model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', weights='Inception_V3_Weights.DEFAULT')
	model.eval()

	if len(PIL_image.getbands())  == 3:
		input_tensor = RGB_processor(PIL_image)
	elif len(PIL_image.getbands()) == 4:
		input_tensor = RGBA_processor(PIL_image)
	else: print(' \n \n ERROR! : image type is not recognized \n ')

	input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

	# check if cuda is available
	if torch.cuda.is_available():
		# if it is, send the data and the model to the gpu
		input_tensor.to('cuda')
		model.to('cuda')

	with torch.no_grad():
		output = model(input_batch)

	output = output[0]#remove just the first element of the batch
	probabilities = torch.nn.functional.softmax(output, dim=0)#get the probabilities

	# Show top categories per image
	top5_prob, top5_idx = torch.topk(probabilities, 5)

	categories = get_labels('./src/labels/labels_imagenet')

	top5_categories = [categories[idx] for idx in top5_idx]
	top5_prob = (top5_prob*100).tolist()

	data_package  = {"categories" : top5_categories, "probabilities": top5_prob}

	# top5_categories = json.dumps(top5_categories)#transform to json
	data_package = json.dumps(data_package)

	return data_package

if __name__  == '__main__':
	import torch
	model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', pretrained=True)
	model.eval()

	lazulifile = '../../../../Lazuli.png'
	dogimage = './dog.jpg'

	image2 = Image.open(dogimage)

	# RGBA_processor(image2)

	# print (image2.getbands());
	if len(image2.getbands())  == 3:
		input_tensor = RGB_processor(image2)
	elif len(image2.getbands()) == 4:
		input_tensor = RGBA_processor(image2)
	else: print(' \n \n ERROR! : image type is not recognized \n ')

	input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

	print('tensor', input_tensor.shape)
	print('\n batch: ', input_batch.shape)

	# check if cuda is available
	if torch.cuda.is_available():
		# if it is, send the data and the model to the gpu
		input_tensor.to('cuda')
		model.to('cuda')
	with torch.no_grad():
		output = model(input_batch)

	output = output[0]#remove just the first element of the batch
	probabilities = torch.nn.functional.softmax(output, dim=0)#get the probabilities

	# Show top categories per image
	top5_prob, top5_idx = torch.topk(probabilities, 5)

	categories = get_labels('./labels/labels_imagenet')

	top5_categories = [categories[idx] for idx in top5_idx]
	print((top5_prob*100).tolist())

	# need to normalize the output to get the probabilities.
	# ['Samoyed', 'Arctic fox', 'white wolf', 'Pomeranian', 'keeshond']



		