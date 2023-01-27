import hashlib
import os
from flask import Flask, request, send_file
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


from flask import Flask

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'POST':
        #Obtener la imagen del request
        file = request.files['image']
        #Abrirla y estandarizar su formato
        img = Image.open(file.stream).convert(mode='RGB')

        #Separar los valores por su color
        red     = []
        green   = []
        blue    = []

        for i in np.array(img):
            for j in i:
                red.append(j[0])
                green.append(j[1])
                blue.append(j[2])

        #Preparar espacio para 3 gráficos en una sola imagen
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

        #Crear 3 histogramas, uno por cada espacio
        ax1.hist(red,     bins=20, color='red'    )
        ax2.hist(green,   bins=20, color='green'  )
        ax3.hist(blue,    bins=20, color='blue'   )

        #Asignar un título para cada gráfico
        ax1.set_title('Rojo')
        ax2.set_title('Verde')
        ax3.set_title('Azul')

        #Ajustar separación
        fig.tight_layout()

        #Guardar figura temporalmente como fig.png
        fig_name = f'fig.png'
        plt.savefig(fig_name)

        #Abrir archivo en binario para pasarlo por SHA-256
        with open(fig_name, 'rb') as f:
            hash = hashlib.sha256(f.read()).hexdigest()

        #Guardar la imagen bajo el nombre de su hash
        hist = Image.open(fig_name)
        hist.save(f'{hash}.png')

        #Remover el archivo temporal
        os.remove(fig_name)

        #Descargar el archivo producido
        return send_file(f'{hash}.png', mimetype='png')
        
#Si es un get (acceso desde browser) mostrar form minimalista
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>'''


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)