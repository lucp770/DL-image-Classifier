from flask import Flask, render_template, request

from matplotlib import pyplot as plt

# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')

import imageio as iio


################# Application #########################

app = Flask(__name__)


models = ['AlexNet','VGG','ResNet','SqueezeNet','DenseNet','Inception v3']
currentModel = 'None'
image =[]

def setImage(imagem):
	image = imagem
	print(image)

def setModel(model):
	currentModel = model;


@app.route("/")
def homepage():
	return render_template("main.html", models = models)

@app.route("/", methods = ['POST'])
def receive_image():
	# manipulate and transform the image in an array.
	# get the data stream from the post request
	image_data = request.get_data()

	image = iio.imread(image_data)
	# print(image)
	setImage(image);
	
	return "image received"

@app.route("/model", methods = ['POST'])
def processModel():
	data = request.get_data()
	
	return "model received"

if __name__ =="__main__":
	app.run(debug=True)



# -no botao submit, incluir uma janela de carregamento no estilo futurista
# -elaborar modelo de ML baseado em CNN para classificação da imagem colocada pelo usuario
# -implementar a classificação e um retorno para o usuario no método 
# -usar modelos pre treinados para um resultado melhor e compara-los.
# -