# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
from robotclient import start_Robot
from ParticleAnalysis import particle_analysis
from plot import plot
#全域變數溝通
brewflag=0 #設定是否可沖煮
coffee_weight=0 #儲存咖啡重
#圖片格式允許
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/', methods=['GET'])  # 添加路由
def index():
    global brewflag #設定是否可沖煮
    global coffee_weight #儲存咖啡重
    brewflag=0
    coffee_weight=0
    return render_template('index.html')
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    global brewflag #設定是否可沖煮
    global coffee_weight #儲存咖啡重
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "請檢查圖檔類型，僅限png、PNG、jpg、JPG、bmp"})
 
        coffee_weight = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        brewflag=1
        particle_info = particle_analysis("static/images/test.jpg")
        plot(particle_info)
        return render_template('upload_ok.html',robot_status="待機中",coffeeWeight=coffee_weight,val1=time.time())
    brewflag=0
    return render_template('upload.html')

@app.route('/start_brew', methods=['GET'])  # 添加路由
def startbrew():
    global brewflag
    global coffee_weight #儲存咖啡重
   # if brewflag==1:
    start_Robot(1)
   # brewflag=0
    return render_template('upload_ok.html',robot_status="開始沖煮",coffeeWeight=coffee_weight,val1=time.time())
 

if __name__ == '__main__':
    # app.debug = True
    app.run(host='10.42.0.1', port=8080, debug=True)
