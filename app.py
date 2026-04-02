from flask import Flask, render_template, request, jsonify
import requests
import os
import base64

app = Flask(__name__)

# ====================== 必须改成你自己的 ======================
API_KEY = "这里填你的百度API Key"
SECRET_KEY = "这里填你的百度Secret Key"
# ==============================================================

# 可调节参数
STYLE = "anime"  # 风格：anime/cartoon/sketch/oil_painting

# 创建静态文件夹
if not os.path.exists("static"):
    os.makedirs("static")

# 获取百度AI token
def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    res = requests.post(url, data=data).json()
    return res.get("access_token")

# 首页（显示学号姓名）
@app.route('/')
def index():
    # ========== 学号姓名 ==========
    student_id = "202335020614"
    student_name = "黄蕊"
    return render_template("index.html", id=student_id, name=student_name)

# AI风格转换接口
@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img_bytes = file.read()
        base64_img = base64.b64encode(img_bytes).decode()

        token = get_token()
        url = f"https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans?access_token={token}"

        data = {
            "image": base64_img,
            "style": STYLE
        }

        res = requests.post(url, data=data).json()

        if "error_code" in res:
            return jsonify({"status":"err","msg":res["error_msg"]})

        img_data = base64.b64decode(res["image"])
        with open("static/result.png","wb") as f:
            f.write(img_data)

        return jsonify({"status":"ok","url":"/static/result.png"})
    except Exception as e:
        return jsonify({"status":"err","msg":str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
