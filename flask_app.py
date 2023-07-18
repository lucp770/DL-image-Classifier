from flask import Flask, render_template, request
import base64


from matplotlib import pyplot as plt

# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')
import json 
import inception

import imageio.v2 as iio
from PIL import Image


################# Application #########################

app = Flask(__name__)


models = [('CNN','#'),('AlexNet','https://pytorch.org/hub/pytorch_vision_alexnet/'),
('VGG','https://pytorch.org/hub/pytorch_vision_vgg/'),('ResNet','https://pytorch.org/hub/pytorch_vision_resnet'),
('SqueezeNet','https://pytorch.org/hub/pytorch_vision_squeezenet/') ,('DenseNet','https://pytorch.org/hub/pytorch_vision_densenet/'),
('Inception v3','https://pytorch.org/hub/pytorch_vision_inception_v3/')]

# def setImage(imagem):
# 	global image
# 	image = imagem

# def setModel(model):
# 	global currentModel
# 	currentModel = model;

@app.route("/")
def homepage():
	return render_template("main.html", models = models)


@app.route("/classification", methods=['POST'])
def classifyImage():
	data = request.get_json()
	# parsedData = json.loads(imageData)
	imageData = data['image64Code']
	model = data['model']

	#transform the base64 data into an array
	img = iio.imread(base64.b64decode(imageData))
	if model =='Inception v3':
		result = inception.Apply_Inception_model(img)
	elif model =='AlexNet':
		result = inception.Apply_AlexNet_Model(img)
	elif model =='VGG':
		result = inception.Apply_VGG_Model(img)
	else: result  = 'none'
	response = json.dumps(result)
	return response



# @app.route("/", methods = ['POST'])
# def receive_image():
# 	# manipulate and transform the image in an array.
# 	# get the data stream from the post request
# 	image_data = request.get_data()

# 	image_data= iio.imread(image_data)
# 	# print(image)
# 	# image_data = Image.open(image_data)
# 	print(image_data)
# 	setImage(image_data)
	
# 	return "image received"

# @app.route("/model", methods = ['POST'])
# def processModel():
# 	data = request.get_json()
# 	data = data['selected model'];
# 	# print('\n parsed data : ', json.loads(data))
# 	setModel(data)
# 	return "model received"

# @app.route("/classification", methods = ['POST'])
# def classification():
# 	model_of_choice = currentModel
# 	image_to_classify = image
# 	print('\n \n modelo:',model_of_choice)
# 	if model_of_choice =='Inception v3':
# 		result = inception.Apply_model(image_to_classify);
# 	else: result  = 'none'

# 	print(' \n \n classification done: ', result);

# 	# else: print('nenhum modelo correspondente');
# 	# insert here the classification algorithm

# 	return result

if __name__ =="__main__":
	app.run(debug=True)

