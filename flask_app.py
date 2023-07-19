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


models = [('AlexNet','https://pytorch.org/hub/pytorch_vision_alexnet/'),
('VGG','https://pytorch.org/hub/pytorch_vision_vgg/'),('ResNet','https://pytorch.org/hub/pytorch_vision_resnet'),
('SqueezeNet','https://pytorch.org/hub/pytorch_vision_squeezenet/') ,('DenseNet','https://pytorch.org/hub/pytorch_vision_densenet/'),
('Inception v3','https://pytorch.org/hub/pytorch_vision_inception_v3/')]

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

	#Apply the model
	result = inception.Apply_Model(img,model)
	response = json.dumps(result)
	return response

if __name__ =="__main__":
	app.run(debug=True)

