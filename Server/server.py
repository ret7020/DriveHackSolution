from flask import Flask, request, render_template
from PIL import Image
import sys
import io
sys.path.append("../")
import text_based
from neural_net_based import Segmentator



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return '''
        <!doctype html>
        <title>Upload image</title>
        <h1>Upload image</h1>
        <form method=post enctype=multipart/form-data action='/upload'>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
'''

@app.route('/upload', methods=['POST'])
def upload():
    global recognizer, classes_names
    try:
        dt = request.data
        req = Image.open(io.BytesIO(dt))
        class_id = recognizer.recognzie(req)
        class_id_net = neuralnet.recognize(req)
        print(f"Tesseract: {class_id}; CNN: {class_id_net}")
        return classes_names[class_id]
    except:
        return "Некорректный файл"
        
if __name__ == '__main__':
    recognizer = text_based.TextBasedRec()
    neuralnet = Segmentator("epoch_12.t")
    classes_names = {0: "Счёт-фактура", 1: "Счёт на оплату", -1: "неопределён"}
    app.run(host="0.0.0.0", port=8080)
