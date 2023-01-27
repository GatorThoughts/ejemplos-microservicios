#Esta aplicación simplemente recibe una imagen y la devuelve sin hacer ningún cambio

#Para manejar requests
from flask import Flask, request, send_file

#Para abrir la imagen
from PIL import Image

#Para manejar persistencia
import os


app = Flask(__name__)

#recuperar environment variable definida en Dockerfile
IMG_FOLDER = os.environ['IMG_VOL']
addr = 'http://downloadsvc.ingress.com'

@app.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'POST':

        #Obtener imagen de request
        file = request.files['image']

        #Abrir imagen y estandarizar su formato
        img = Image.open(file.stream).convert(mode='RGB')

        #Guardar negativo en el folder al que apunta la env var
        imgName = f'{IMG_FOLDER}/foo.png'
        img.save(imgName)

        #Redirigir al servicio de descarga
        return send_file(imgName, mimetype='png')

#Si es un get (acceso desde browser) mostrar form minimalista
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)