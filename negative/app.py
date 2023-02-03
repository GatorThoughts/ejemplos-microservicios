#Para manejar requests
from flask import Flask, request, redirect

#Para manipulación de imágenes
from PIL import Image, ImageOps

#Para manejar persistencia
import os


app = Flask(__name__)

#recuperar environment variable definida en Dockerfile
IMG_FOLDER = os.environ['IMG_VOL']




#Usar localhost:[puerto asignado al servicio de descarga] para pruebas locales con Docker
addr = 'http://localhost:8001'

#Usar el nombre del servicio para deployments en kubernetes
#addr = 'http://downloadsvc.ingress.com'

@app.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'POST':

        #Obtener imagen de request
        file = request.files['image']

        #Abrir imagen y estandarizar su formato
        img = Image.open(file.stream).convert(mode='RGB')

        #Crear negativo
        negative = ImageOps.invert(img)

        #Guardar negativo en el folder al que apunta la env var
        negativeName = f'{IMG_FOLDER}/negativo.png'
        negative.save(negativeName)

        #Redirigir al servicio de descarga
        return redirect(f'{addr}/negativo/download')

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