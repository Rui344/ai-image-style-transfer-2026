# AI前沿人像风格迁移项目

## 👤 个人信息
- 学号：202335020614
- 姓名：黄蕊

## 📌 项目简介
基于轻量 Stable Diffusion 实现的网页端 AI 图像风格迁移工具，支持上传图片一键生成动漫/油画/写实等风格效果，可自由调参优化，支持本地/服务器多平台部署。

## 🛠️ 技术栈
- 后端：Python + Flask
- AI模型：Stable Diffusion
- 前端：HTML + CSS + JavaScript

## ⚙️ 可调参数
- `INFERENCE_STEPS`：推理步数，控制生成质量（越大越清晰，速度越慢）
- `GUIDANCE_SCALE`：风格强度，控制AI对提示词的贴合度
- `MODEL_ID`：模型地址，可替换成其他风格模型

## 🚀 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 运行项目：`python app.py`
3. 浏览器访问：`http://127.0.0.1:5000`
