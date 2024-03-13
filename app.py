# from flask import Flask
# from flask import request
# from flask import send_from_directory
# from detect import detect
# import os
#
# UPLOAD_FOLDER = './upload'
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# styles = '''body {
#   background-image: linear-gradient(135deg, #AFA4A4 10%, #DC8C8C 100%);
#   background-size: cover;
#   background-repeat: no-repeat;
#   background-attachment: fixed;
#   font-family: "Open Sans", sans-serif;
#   color: #333333;
# }
#
# .box-form-detected {
#   margin: 0 auto;
#   margin-top: 30px;
#   width: 80%;
#   background: #FFFFFF;
#   border-radius: 10px;
#   overflow: hidden;
#   display: flex;
#   flex: 1 1 100%;
#   align-items: stretch;
#   justify-content: space-between;
#   box-shadow: 0 0 20px 6px #090b6f85;
# }
#
# .box-form {
#   margin: 0 auto;
#   margin-top: 30px;
#   width: 40%;
#   background: #FFFFFF;
#   border-radius: 10px;
#   overflow: hidden;
#   display: flex;
#   flex: 1 1 100%;
#   align-items: stretch;
#   justify-content: space-between;
#   box-shadow: 0 0 20px 6px #090b6f85;
# }
#
#   .box-form {
#     flex-flow: wrap;
#     text-align: center;
#     align-content: center;
#     align-items: center;
#   }
#
# .box-form div {
#   height: auto;
# }
# .box-form .left {
#   color: #FFFFFF;
#   background-size: cover;
#   background-repeat: no-repeat;
#   background-image: url("https://i.pinimg.com/736x/5d/73/ea/5d73eaabb25e3805de1f8cdea7df4a42--tumblr-backgrounds-iphone-phone-wallpapers-iphone-wallaper-tumblr.jpg");
#   overflow: hidden;
# }
# .box-form .left .overlay {
#   padding: 30px;
#   width: 100%;
#   height: 100%;
#   background: #5961f9ad;
#   overflow: hidden;
#   box-sizing: border-box;
# }
# .box-form .left .overlay h1 {
#   font-size: 10vmax;
#   line-height: 1;
#   font-weight: 900;
#   margin-top: 40px;
#   margin-bottom: 20px;
# }
# .box-form .left .overlay span p {
#   margin-top: 30px;
#   font-weight: 900;
# }
# .box-form .left .overlay span a {
#   background: #3b5998;
#   color: #FFFFFF;
#   margin-top: 10px;
#   padding: 14px 50px;
#   border-radius: 100px;
#   display: inline-block;
#   box-shadow: 0 3px 6px 1px #042d4657;
# }
# .box-form .left .overlay span a:last-child {
#   background: #1dcaff;
#   margin-left: 30px;
# }
# .box-form .right {
#   padding: 40px;
#   overflow: hidden;
# }
#
#   .box-form .right {
#     width: 100%;
#   }
#
# .box-form .right h5 {
#   font-size: 2vmax;
#   line-height: 0;
# }
# .box-form .right p {
#   font-size: 14px;
#   color: #B0B3B9;
# }
# .box-form .right .inputs {
#   overflow: hidden;
# }
# .box-form .right input {
#   width: 100%;
#   padding: 10px;
#   margin-top: 25px;
#   font-size: 16px;
#   border: none;
#   outline: none;
#   border-bottom: 2px solid #B0B3B9;
# }
# .main-header{
#   border-radius: 15px 50px;
#     background-image: linear-gradient(135deg, #FFF 10%, #DC8C8C 100%);
#   padding: 20px;
#   width: 90% ;
#   height: 60px;
#   margin: 0 auto;
# }
# .box-form .right .remember-me--forget-password {
#   display: flex;
#   justify-content: space-between;
#   align-items: center;
# }
# .box-form .right .remember-me--forget-password input {
#   margin: 0;
#   margin-right: 7px;
#   width: auto;
# }
# .box-form .right button {
#   float: right;
#   color: #fff;
#   font-size: 16px;
#   padding: 12px 35px;
#   border-radius: 50px;
#   display: inline-block;
#   border: 0;
#   outline: 0;
#   box-shadow: 0px 4px 20px 0px #49c628a6;
#   background-image: linear-gradient(135deg, #70F570 10%, #49C628 100%);
# }
#
# label {
#   display: block;
#   position: relative;
#   margin-left: 30px;
# }
#
# label::before {
#   content: ' \f00c';
#   position: absolute;
#   font-family: FontAwesome;
#   background: transparent;
#   border: 3px solid #70F570;
#   border-radius: 4px;
#   color: transparent;
#   left: -30px;
#   transition: all 0.2s linear;
# }
#
# label:hover::before {
#   font-family: FontAwesome;
#   content: ' \f00c';
#   color: #fff;
#   cursor: pointer;
#   background: #70F570;
# }
#
# label:hover::before .text-checkbox {
#   background: #70F570;
# }
#
# label span.text-checkbox {
#   display: inline-block;
#   height: auto;
#   position: relative;
#   cursor: pointer;
#   transition: all 0.2s linear;
# }
#
# label input[type="checkbox"] {
#   display: none;
# }
#
# select {
# border-radius : 5px;
# width: 50%
# }
#
# table {
#   font-family: arial, sans-serif;
#   border-collapse: collapse;
#   width: 100%;
# }
#
# td, th {
#   border: 1px solid lightgray;
#   text-align: center;
#   padding: 8px;
# }
#
# .number {
# text-align: right;
# }
#
# '''
#
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file1' not in request.files:
#             return 'there is no file1 in form!'
#         file1 = request.files['file1']
#
#         path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
#         file1.save(path)
#         model = request.form['model']
#         scale = request.form['scale']
#
#         print(model, scale)
#
#         # detections =  {'fix': [['hood', 'fix', 2731332]], 'replace': [
#         #     ['headlamp', 'replace', 98654325]]}
#         detections = detect(path, model, scale)
#
#         total_cost = 0
#         table_string = '''
#             <h2>COST ESTIMATION</h2>
#             <table><tr>
#                 <th>Part</th>
#                 <th>Fix/Replace</th>
#                 <th>Cost</th>
#             </tr>'''
#
#         for i in detections['fix']:
#             table_string += f'''<tr><td>{i[0]}</td><td>Fix</td><td class='number'>{i[2]}</td></tr>'''
#             total_cost += i[2]
#
#         # table_string += '''</table>
#         # <h2>REPLACE</h2><table>'''
#
#         for i in detections['replace']:
#             table_string += f'''<tr><td>{i[0]}</td><td>Replace</td><td class='number'>{i[2]}</td></tr>'''
#             total_cost += i[2]
#
#         table_string += f'''<tr><td></td><td><b>TOTAL</b></td><td class='number'><b >{total_cost}</b></td></tr>'''
#
#         table_string += '''</table>'''
#
# # This is for the 2nd page
#         return f'''<!DOCTYPE html>
#                     <html>
#                     <head>
#                         <title>Index</title>
#                     </head>
#                     <body>
#                         <header>
#       <div class="main-header">
#           <img src="static/logo.png" alt="logo Image" height="60">
#        </div>
#     </header>
#                     <div class="box-form-detected">
#
#
# 		            <div class="right">
#                     <img src="detected/output.jpg" alt="User Image">
#                      </div>
#                     </div>
#                     <div class="box-form">
#
#
# 		            <div class="right">
#                         {table_string}
#                     </div>
#                     </div>
#                     </body>
#                     <style>{styles}</style>
#                     </html>'''
#
#     return f'''
#     <!DOCTYPE html>
# <html lang="en" >
# <head>
#   <meta charset="UTF-8">
#   <title>Damage detection and cost estimation</title>
#   <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
#
#
# <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous"><link rel="stylesheet" href="./style.css">
#
# </head>
# <body>
#     <header>
#       <div class="main-header">
#           <img src="static/logo.png" alt="logo Image" height="60">
#        </div>
#     </header>
# <!-- partial:index.partial.html -->
# <div class="box-form">
#
#
# 		<div class="right">
# 		<h5>Damage cost estimation</h5>
# 		<form method="post" enctype="multipart/form-data">
#         <p>Select model</p>
#             <select name="model" id="model" required>
#             <option value="toyota">Toyota</option>
#             </select>
#             <input name='scale' type="number" placeholder="scale" required>
# 			<input type="file" name="file1" required>
# 			<input type="submit">
# 		  </form>
#
#
#
# </div>
# <!-- partial -->
#
# </body>
# <style>{styles}/styles>
# </html>
#     '''
#
#
# @app.route('/detected/<filename>')
# def send_uploaded_file(filename=''):
#     return send_from_directory('detected/', filename)
#
#
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import detect
from flask import send_from_directory

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        model = request.form.get('model')
        scale = float(request.form.get('scale'))
        result = detect.detect(file_path, model, scale)
        return jsonify(result)
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/detected/<filename>')
def send_uploaded_file(filename):
    return send_from_directory('detected/', filename)

@app.route('/results')
def send_results_file():
    return send_from_directory('detected/', 'results.txt')

@app.route('/')
def server_run():
    return "server running"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
