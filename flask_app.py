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

@app.route("/")
def homepage():
	return render_template("main.html", models = models)

@app.route("/", methods = ['POST'])
def receive_image():
	# manipulate and transform the image in an array.

	# get the data stream from the post request
	image_data = request.get_data()
	# print(image_data);
	for i in request.files:
		print(i)
	
	# for i in dir(request):
	# 	print(i)

	# print('\n \n propriedades do request getdata')
	# for j in dir(image_data):
	# 	print(j)

	# convert the data stream to an array
	# image = iio.imread(data1)

	# now insert here the code for image classification
	
	return "<h1>Done !!</h1>"	

if __name__ =="__main__":
	app.run(debug=True)

# -futuristic syle with nice animations (background dargrey, text: light blue)
# 		-put the arrow dow in the menu v
# 		-put the menu going down

# -manipulate the image in the background so it transform in an array. V

# -no botao submit, incluir uma janela de carregamento no estilo futurista
# -elaborar modelo de ML baseado em CNN para classificação da imagem colocada pelo usuario
# -implementar a classificação e um retorno para o usuario no método 
# -usar modelos pre treinados para um resultado melhor e compara-los.
# -