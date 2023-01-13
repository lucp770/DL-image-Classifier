from flask import Flask, render_template, request


# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')


################# Application #########################

app = Flask(__name__)

@app.route("/")
def homepage():
	return render_template("main.html")


@app.route("/", methods = ['POST'])
def receive_image():
		image = request.form.get('user-input')
		# manipulate and transform the image in an array.
		print(image)
		return "<h1>Done !!</h1>"	

if __name__ =="__main__":
	app.run(debug=True)

# -futuristic syle with nice animations (background dargrey, text: light blue)
# 		-put the arrow dow in the menu v
# 		-put the menu going down

# -manipulate the image in the background so it transform in an array.
# -no botao submit, incluir uma janela de carregamento no estilo futurista
# -elaborar modelo de ML baseado em CNN para classificação da imagem colocada pelo usuario
# -implementar a classificação e um retorno para o usuario no método 
# -usar modelos pre treinados para um resultado melhor e compara-los.
# -