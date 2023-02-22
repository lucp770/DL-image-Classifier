from flask import Flask, render_template, request

from matplotlib import pyplot as plt

# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')
import json 

import inception

import imageio as iio
from PIL import Image


################# Application #########################

app = Flask(__name__)


models = [('CNN','#'),('AlexNet','https://pytorch.org/hub/pytorch_vision_alexnet/'),
('VGG','https://pytorch.org/hub/pytorch_vision_vgg/'),('ResNet','https://pytorch.org/hub/pytorch_vision_resnet'),
('SqueezeNet','https://pytorch.org/hub/pytorch_vision_squeezenet/') ,('DenseNet','https://pytorch.org/hub/pytorch_vision_densenet/'),
('Inception v3','https://pytorch.org/hub/pytorch_vision_inception_v3/')]

def setImage(imagem):
	global image
	image = imagem

def setModel(model):
	global currentModel
	currentModel = model;

@app.route("/")
def homepage():
	return render_template("main.html", models = models)

@app.route("/", methods = ['POST'])
def receive_image():
	# manipulate and transform the image in an array.
	# get the data stream from the post request
	image_data = request.get_data()

	image_data= iio.imread(image_data)
	# print(image)
	# image_data = Image.open(image_data)
	print(image_data)
	setImage(image_data);
	
	return "image received"

@app.route("/model", methods = ['POST'])
def processModel():
	data = request.get_json()
	data = data['selected model'];
	# print('\n parsed data : ', json.loads(data))
	setModel(data)
	return "model received"

@app.route("/classification", methods = ['POST'])
def classification():
	model_of_choice = currentModel
	image_to_classify = image
	print('\n \n modelo:',model_of_choice)
	if model_of_choice =='Inception v3':
		inception.Apply_model(image_to_classify);

	# else: print('nenhum modelo correspondente');
	# insert here the classification algorithm
	plt.imshow(image_to_classify)
	plt.show()

	return 'classification done'


if __name__ =="__main__":
	app.run(debug=True)



# 

# -implementar a classificação e um retorno para o usuario no método
# -usar modelos pre treinados para um resultado melhor e compara-los.
