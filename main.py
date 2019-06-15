from bottle import route, run, template
from bottle import request
from bottle import static_file
from bottle import redirect
from tesseract_ocr import OCR
import uuid


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def root():
    redirect('/static/html/index.html')

url_baidu = "http://fanyi.baidu.com/v2transapi"
def translate_baidu(content, sign, token, f = "vie", t = "zh"):
	query = "query=" + urllib.quote(content) + "&from=" + f + "&to=" + t + \
		"&transtype=translang&simple_means_flag=3&sign="+sign+"&token="+token
	req = urllib2.Request(url_baidu, query)
	resp = urllib2.urlopen(req)
	content = resp.read()

	data = json.loads(content)
	result = data["trans_result"]["data"][0]["dst"]
	return result

@route("/translate", method = 'POST')
def do_translate():
    content = bottle.request.POST.get('content')
    sign = bottle.request.POST.get('sign')
    token = bottle.request.POST.get('token')
    return translate_baidu(content, sign, token)

#定义上传路径
save_path = './static/upload/'

#文件上传，overwrite=True为覆盖原有的文件，
#如果不加这参数，当服务器已存在同名文件时，将返回“IOError: File exists.”错误
@route('/upload', method = 'POST')
def do_upload():
    upload = request.files.get('filedata')
    savefilename = str(uuid.uuid1()) + "_" + upload.raw_filename 
    upload.raw_filename = savefilename
    upload.save(save_path,overwrite=True)  #把文件保存到save_path路径下
    return OCR(save_path + savefilename)

from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'


run(host='0.0.0.0', port=8080)