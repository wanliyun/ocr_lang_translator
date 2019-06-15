# -*- coding: utf-8 -*-
from bottle import route, run, template
from bottle import request
from bottle import static_file
from bottle import redirect
from tesseract_ocr import OCR
import uuid


from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def root():
    redirect('/static/html/index.html')

#定义上传路径
save_path = './static/upload/'


import os
if not os.path.exists(save_path):
    os.makedirs(save_path) 

#文件上传，overwrite=True为覆盖原有的文件，
#如果不加这参数，当服务器已存在同名文件时，将返回“IOError: File exists.”错误
@route('/upload', method = 'POST')
def do_upload():
    upload = request.files.get('filedata')
    savefilename = str(uuid.uuid1()) + "_" + upload.raw_filename 
    upload.raw_filename = savefilename
    upload.save(save_path,overwrite=True)  #把文件保存到save_path路径下
    return OCR(save_path + savefilename)

run(host='0.0.0.0', port=8080)