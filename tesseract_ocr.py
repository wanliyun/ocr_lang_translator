#!/bin/env python
# -*- coding: utf-8 -*- 
import urllib
import urllib2
import urlparse
import hashlib
import re
import sys 
import os
import json
from PIL import Image
from PIL import ImageGrab
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import pytesseract
pytesseract.pytesseract.tesseract_cmd= os.getcwd() + "/Tesseract-OCR/tesseract.exe"

def OCR(filepath, lang_="vie"):
	im = Image.open(filepath)
	a = pytesseract.image_to_string(im, lang=lang_)
	a.encode("utf-8")
	return a