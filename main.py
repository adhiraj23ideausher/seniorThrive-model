from flask import Flask, request, jsonify
import json
from img_recog import caption_image, get_prompt_obj
from videos import search_videos
from products import get_products
from auth_image import caption_and_authenticate_image
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'msg': 'You can go to /docs to use this API :)'})

@app.route('/auth-image',methods=['POST'])
def auth_image():
    if not request.json or 'img_url' not in request.json or 'selection' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'Required fields not provided'}), 400
    img_url = request.json['img_url']
    selection = request.json['selection']
    is_valid = caption_and_authenticate_image(img_url,selection)
    return jsonify({'valid':is_valid})

@app.route('/scan', methods=['POST'])
def scan_image():
    if not request.json or 'img_url' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'No img_url provided'}), 400
    img_url = request.json['img_url']
    prompt = caption_image(img_url)
    res = get_prompt_obj(prompt)
    # clean_data = res.strip()[7:-3].strip()
    json_data = json.loads(res)
    for p in json_data:
        prod = get_products(p['products'])
        p['products'] = prod
    for p in json_data:
        vid = search_videos(p['videos'])
        p['videos'] = vid
    return jsonify({
        'prompt': json_data
    })
    

if __name__ == "__main__":
    app.run(debug=True)
