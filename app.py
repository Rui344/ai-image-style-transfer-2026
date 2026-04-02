from flask import Flask, render_template, request, jsonify
import requests
import base64
import pygame
import time
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制16MB
# 允许的图片类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

# ==================== 填写你的信息 ====================
NAME = "黄蕊"
STUDENT_ID = "202335020614"
# 百度AI开放平台密钥
API_KEY = "gHLox0TOB0Eky1EJZveNbOMY"
SECRET_KEY = "fdN8mvwFnrHqwj8K4gy3hLuBRnCxNh5w"


# ======================================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 获取百度AI access_token
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    return requests.post(url, data=data).json()["access_token"]


# OCR文字识别
@app.route("/ocr", methods=["POST"])
def ocr():
    if 'img' not in request.files:
        return jsonify({"error": "未上传文件"})
    file = request.files['img']
    if file.filename == '':
        return jsonify({"error": "未选择文件"})
    if not allowed_file(file.filename):
        return jsonify({"error": "当前不支持该文件类型，请尝试其他文件"})

    token = get_access_token()
    img = file.read()
    img_b64 = base64.b64encode(img).decode()
    r = requests.post(
        f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}",
        data={"image": img_b64}
    )
    return jsonify(r.json())


# 图像物体识别
@app.route("/detect", methods=["POST"])
def detect():
    if 'img' not in request.files:
        return jsonify({"error": "未上传文件"})
    file = request.files['img']
    if file.filename == '':
        return jsonify({"error": "未选择文件"})
    if not allowed_file(file.filename):
        return jsonify({"error": "当前不支持该文件类型，请尝试其他文件"})

    token = get_access_token()
    img = file.read()
    img_b64 = base64.b64encode(img).decode()
    r = requests.post(
        f"https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={token}",
        data={"image": img_b64}
    )
    return jsonify(r.json())


# 语音合成
@app.route("/voice", methods=["POST"])
def voice():
    token = get_access_token()
    text = request.json["text"]
    r = requests.post(
        f"https://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=1&tok={token}&tex={text}"
    )
    with open("voice.mp3", "wb") as f:
        f.write(r.content)
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    time.sleep(2)
    return jsonify({"msg": "播放成功"})


@app.route("/")
def index():
    return render_template("index.html", name=NAME, sid=STUDENT_ID)


if __name__ == "__main__":
    app.run(debug=True)
