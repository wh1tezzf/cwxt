import json

from flask import Flask, request, jsonify, render_template
from web import sumMoney, sumAmount
import pandas as pd

app = Flask(__name__)

ALLOWED_EXTS = {"xlsx"}

def check_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTS

@app.route("/")
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    return render_template("upload.html")

@app.route("/result",methods=['POST'])
def result():
    error = None
    dictionary = None
    if request.method == 'POST':
        if'file' not in request.files:
            error = "File not selected"
            return render_template('upload.html', error=error)
        file = request.files['file']
        filename = file.filename

        if filename == '':
            error = "Filename is empty"
            return render_template('upload.html', error=error)
        if check_file(filename) == False:
            error = "Please upload an excel file"
            return render_template('upload.html', error=error)

        doctor_dict = {'投资方分配金额': 0}
        df = pd.read_excel(file, sheet_name=None)
        ds = pd.read_excel(file, sheet_name='治疗检查')
        register = pd.DataFrame(df['挂号费'], columns=['接诊医生', '挂号费分配金额', '挂号费用'])
        exam = pd.DataFrame(df['治疗检查'], columns=['接诊医生', '治疗检查费分配金额', '实际金额'])
        glasses = pd.DataFrame(df['配镜'], columns= ['接诊医生','分配金额1','验光师','分配金额2','来源1','分配金额3','来源2','分配金额4', '实际金额'])

        # 检查费
        doctor_dict = sumMoney(exam['接诊医生'], exam['治疗检查费分配金额'], doctor_dict)
        doctor_dict = sumAmount(exam['接诊医生'], exam['实际金额'], 0.5, doctor_dict)

        # 挂号费
        doctor_dict = sumMoney(register['接诊医生'], register['挂号费分配金额'], doctor_dict)
        doctor_dict = sumAmount(register['接诊医生'], register['挂号费用'], 0.2, doctor_dict)
        # 配镜费
        doctor_dict = sumMoney(glasses['接诊医生'], glasses['分配金额1'], doctor_dict)
        doctor_dict = sumMoney(glasses['验光师'], glasses['分配金额2'], doctor_dict)
        doctor_dict = sumMoney(glasses['来源1'], glasses['分配金额3'], doctor_dict)
        doctor_dict = sumMoney(glasses['来源2'], glasses['分配金额4'], doctor_dict)
        doctor_dict = sumAmount(glasses['接诊医生'], glasses['实际金额'], 0.2, doctor_dict)
        return render_template('upload.html', dictionary=doctor_dict)


@app.route("/export", methods=['GET'])
def export_records():
    return


if __name__ == "__main__":
    app.run()
