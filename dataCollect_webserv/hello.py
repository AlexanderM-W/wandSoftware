from flask import Flask, redirect, url_for, render_template, send_file
import os
import zipfile



app = Flask(__name__)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/')
def index():
   try:
      return render_template('index.html')
   except Exception as e:
      return str(e)

@app.route('/return-files-wfringes/')
def wfringes():
   name = "/home/cm4/dataCollect_webserv/data/pics_wfringes"
   zip_name = name + ".zip"


   with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
      for folder_name, subfolders, filenames in os.walk(name):
         for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

   zip_ref.close()

   try:
      return send_file('/home/cm4/dataCollect_webserv/data/pics_wfringes', attachment_filename='pics_with_fringes.zip')
   except Exception as e:
      return str(e)


@app.route('/return-files-wofringes/')
def wofringes():
   name = "/home/cm4/dataCollect_webserv/data/pics_wofringes"
   zip_name = name + ".zip"


   with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
      for folder_name, subfolders, filenames in os.walk(name):
         for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

   zip_ref.close()

   try:
      return send_file('/home/cm4/dataCollect_webserv/data/pics_wofringes.zip', attachment_filename='pics_without_fringes.zip')
   except Exception as e:
      return str(e)

if __name__ == '__main__':
   app.run(debug = True, host = "0.0.0.0")