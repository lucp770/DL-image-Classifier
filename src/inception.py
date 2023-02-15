import torch
from torchvision import transforms
from matplotlib import pyplot as plt
from PIL import Image 

def Apply_model(processed_image):

	model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', pretrained=True)
	model.eval()

	# ḍefine the preprocess and check the image result(before and after)
	preprocess = transforms.Compose([transforms.Resize(299),
	transforms.CenterCrop(299),
	transforms.ToTensor(),
	transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	transformed_image = preprocess(processed_image);

	plt.subplot(1,1,1)
	plt.imshow(processed_image)
	plt.title('imagem antes do preprocess')

	plt.subplot(1,1,2)
	plt.imshow(transformed_image)
	plt.title('imagem apos processamento')

	plt.show()







# preciso usar PIL para processar a imagem e não iio.