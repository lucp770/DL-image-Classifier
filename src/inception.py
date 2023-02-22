import torch
from torchvision import transforms
from matplotlib import pyplot as plt
from PIL import Image 

def Apply_model(processed_image):

	PIL_image = Image.fromarray(processed_image)
	print('\n \n Size: ', PIL_image.size)
	print('\n \n color: ', PIL_image.getcolors())

	model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', pretrained=True)
	model.eval()

	# ḍefine the preprocess and check the image result(before and after)
	# preprocess = transforms.Compose([transforms.Resize(299),
	# transforms.CenterCrop(299),
	# transforms.ToTensor(),
	# # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	# ])

	# transformed_image = preprocess(PIL_image);

	# plt.subplot(1,1,1)
	# plt.imshow(PIL_image)
	# plt.title('imagem antes do preprocess')

	# plt.subplot(1,1,2)
	# plt.imshow(PIL_image)
	# plt.title('imagem apos processamento')

	# plt.show()

if __name__  == '__main__':
	import torch
	model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', pretrained=True)
	model.eval()

	lazulifile = '../../../../Lazuli.png'

	image2 = Image.open(lazulifile)


	import urllib
	url, filename = ("https://github.com/pytorch/hub/raw/master/images/dog.jpg", "dog.jpg")
	try: urllib.URLopener().retrieve(url, filename)
	except: urllib.request.urlretrieve(url, filename)

	# sample execution (requires torchvision)
	from PIL import Image
	from torchvision import transforms
	input_image = Image.open(filename)
	preprocess = transforms.Compose([
	    transforms.Resize(299),
	    transforms.CenterCrop(299),
	    transforms.ToTensor(),
	    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	input_tensor = preprocess(input_image)
	input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

	print('size', input_image.size)

	print('\n ... trying to apply the preprocess to the image::')
	lazuli_tensor  = preprocess(image2)
	print(lazuli_tensor)

	print(input_tensor.shape)
	plt.imshow(image2)
	plt.show()

# preciso saber porque o preprocessor nao funciona na imagem Lazuli.png.
#  a documentação de normalize sugere que não funciona em imagens do tipo PIL, mas isso não parece ser verdade.
	# talvez o problema seja converter imagens png (como o logo da lazuli,)
	# TENTAR IMAGENS E/OU CONVERSÕES PARA JPG.
		