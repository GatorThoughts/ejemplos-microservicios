import os
from flask import Flask, send_file

IMG_FOLDER = os.environ['IMG_VOL']

app = Flask(__name__)


@app.route('/<hash>/download', methods=['GET'])
def download_file(hash):
    #Descargar el archivo desde el folder compartido
    return send_file(f'{IMG_FOLDER}/{hash}.png', mimetype='png', as_attachment=True)

@app.route('/', methods=['GET'])
def test_file():
    #Descargar el archivo desde el folder compartido
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