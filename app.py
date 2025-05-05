from flask import Flask, request, render_template, jsonify, send_from_directory
import tensorflow as tf
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


try:
    model = tf.keras.models.load_model('static/models/bird_classifier.keras')
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    model = None


class_names = [
    'ABBOTTS BABBLER', 'ABBOTTS BOOBY', 'ABYSSINIAN GROUND HORNBILL',
    'AFRICAN CROWNED CRANE', 'AFRICAN EMERALD CUCKOO', 'AFRICAN FIREFINCH',
    'AFRICAN OYSTER CATCHER', 'AFRICAN PIED HORNBILL', 'AFRICAN PYGMY GOOSE',
    'ALBATROSS', 'ALBERTS TOWHEE', 'ALEXANDRINE PARAKEET', 'ALPINE CHOUGH',
    'ALTAMIRA YELLOWTHROAT', 'AMERICAN AVOCET', 'AMERICAN BITTERN',
    'AMERICAN COOT', 'AMERICAN FLAMINGO', 'AMERICAN GOLDFINCH', 'AMERICAN KESTREL'
]


descriptions = {
    'ABBOTTS BABBLER': 'Кустарниковая птица с характерным криком, обитающая в Юго-Восточной Азии.',
    'ABBOTTS BOOBY': 'Морская птица с длинными крыльями, гнездится на тропических островах.',
    'ABYSSINIAN GROUND HORNBILL': 'Крупная птица с мощным клювом, обитающая в саваннах Африки.',
    'AFRICAN CROWNED CRANE': 'Элегантная птица с золотистой короной перьев, символ Африки.',
    'AFRICAN EMERALD CUCKOO': 'Ярко-изумрудная птица с контрастными полосами на хвосте.',
    'AFRICAN FIREFINCH': 'Маленькая птичка с ярко-красным оперением у самцов.',
    'AFRICAN OYSTER CATCHER': 'Крупная морская птица с ярко-красным клювом и ногами.',
    'AFRICAN PIED HORNBILL': 'Птица с черно-белым оперением и характерным хохолком.',
    'AFRICAN PYGMY GOOSE': 'Маленькая утка с яркими пятнами вокруг глаз.',
    'ALBATROSS': 'Одна из крупнейших летающих птиц с размахом крыльев до 3.5 метров.',
    'ALBERTS TOWHEE': 'Серо-коричневая птица с темной маской вокруг глаз.',
    'ALEXANDRINE PARAKEET': 'Ярко-зеленый попугай с характерным красным плечом.',
    'ALPINE CHOUGH': 'Горная ворона с красными ногами и изогнутым клювом.',
    'ALTAMIRA YELLOWTHROAT': 'Певчая птица с ярко-желтым горлом и маской на лице.',
    'AMERICAN AVOCET': 'Болотная птица с длинным изогнутым клювом и пестрым оперением.',
    'AMERICAN BITTERN': 'Массивная цапля с камуфляжным рисунком оперения.',
    'AMERICAN COOT': 'Черная водоплавающая птица с белым клювом и лопастными пальцами.',
    'AMERICAN FLAMINGO': 'Ярко-розовая птица с длинными ногами и характерным изогнутым клювом.',
    'AMERICAN GOLDFINCH': 'Маленькая птичка с ярко-желтым оперением у самцов.',
    'AMERICAN KESTREL': 'Самый маленький сокол в Северной Америке с полосатым хвостом.'
}


@app.route('/')
def index():

    examples = [f"{cls.replace(' ', '_')}.jpg" for cls in class_names]


    return render_template(
        'index.html',
        examples_with_desc=zip(examples, [descriptions[cls] for cls in class_names])
    )


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Модель не загружена'}), 500

    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Файл не загружен'}), 400

    try:

        img = Image.open(file).convert('RGB').resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        prediction = model.predict(np.expand_dims(img_array, axis=0))


        result_idx = np.argmax(prediction)
        result = class_names[result_idx]
        confidence = float(prediction[0][result_idx])
        description = descriptions.get(result, 'Информация отсутствует')

        return jsonify({
            'result': result,
            'description': description,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)