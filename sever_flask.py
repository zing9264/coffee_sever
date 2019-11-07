# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
from robotclient import start_Robot
from image_module import predict

#全域變數溝通
brewflag=0 #設定是否可沖煮
coffee_weight=0 #儲存咖啡重
#圖片格式允許
ALLOWED_EXTENSIONS = set(['png','jpeg' ,'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
#
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/', methods=['GET'])  # 
def index():
    global brewflag #設定是否可沖煮
    brewflag=0
    coffee_weight=0
    return render_template('index.html')
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    global brewflag #設定是否可沖煮

    if request.method == 'POST':
        i=0
        for file in request.files.getlist("file"):
            print("file " ,file,type(file),file.filename)

            if not(file and allowed_file(file.filename)):
                    # Make the filename safe, remove unsupported chars
                return jsonify({"error": 1001, "msg": "請檢查圖檔類型，僅限png、PNG、jpg、JPG、bmp"})
            basepath = os.path.dirname(__file__)  #當前目錄
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            file.save(upload_path)
                # 使用Opencv轉換格式
            img = cv2.imread(upload_path)
            newname= "Demo_input.jpg"
            print(newname+"\n")
            cv2.imwrite(os.path.join(basepath, 'static/images/raw_photo',newname ), img)
            brewflag=1
            i = i+1
            break

        get_answer=[]
        for i in range(0,5):
            _="weight_"+str(i)
            print(request.form.get(_))
            j=int(request.form.get(_))
            get_answer.append(j)
        
        predict_answer=predict(correct_answer=get_answer)

        '''
        for i in range(len(f)):
        # Check if the file is one of the allowed types/extensions
            if not(f[i] and allowed_file(f[i].filename)):
                    # Make the filename safe, remove unsupported chars
                return jsonify({"error": 1001, "msg": "請檢查圖檔類型，僅限png、PNG、jpg、JPG、bmp"})
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/images', secure_filename(f[i].filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f[i].save(upload_path)
                # 使用Opencv转换一下图片格式和名称
            img = cv2.imread(upload_path)
            newname= "text_"+i+".jpg"
            print(newname+"\n")
            cv2.imwrite(os.path.join(basepath, 'static/images',newname ), img)
            brewflag=1
            i = i+1
            #particle_info = particle_analysis("static/images/test.jpg")
            #plot(particle_info)\
        '''    
        return render_template('upload_ok.html',robot_status="待機中" ,input_answer=get_answer,predict_answer=predict_answer,val1=time.time())
    brewflag=0
    return render_template('upload.html')

@app.route('/start_brew', methods=['GET'])  # 添加路由
def startbrew():
    global brewflag
   # if brewflag==1:
    start_Robot(1)
   # brewflag=0
    return render_template('upload_ok.html',robot_status="開始沖煮，等待沖泡完成",coffeeWeight=coffee_weight,val1=time.time())
 

if __name__ == '__main__':
    # app.debug = True
   app.run(host='10.42.0.1', port=8080, debug=True)
   #app.run(host='192.168.11.21', port=8080, debug=True)

 
   #app.run(host='192.168.43.99', port=8080, debug=True)
