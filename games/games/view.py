from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.conf import settings
from base64 import b64decode
from . import hf
from . import settings
import json
import os

def index(request):
    print(request.is_ajax())
    if request.is_ajax():
        '''
        判断是否为ajax请求。
        网站中的ajax请求有上传图片和下载图片。
        '''
        #data:接收到的图片文件
        data=dict(request.FILES)['content'][0]
        #将问津进行存储，并返回原图预览
        path = default_storage.save('static/img/test.png', ContentFile(data.read()))
        #为图片添加头像框并返回新图预览
        new_pic_path = hf.add_head_frame(path)
        print(new_pic_path)
        return HttpResponse(json.dumps({'code': True, 'img_path': '/' + path, 'new_img_path': '/' + new_pic_path}))
        #return HttpResponse(json.dumps({'code': True, 'img_path': '/' + path}))
    else:
        '''
        非ajax请求，加载网页
        '''
        return render(request, 'index.html', {})

def submit(request):
    '''
    提交裁剪过的图片
    '''
    if not request.is_ajax():
        return HttpResponseRedirect('/index/')
    else:
        data = request.POST['content'].split(',')[1]
        img = b64decode(data)
        #with open(os.path.join(settings.BASE_DIR, 'static/img/test.png'), 'wb') as f:
        #    f.write(img)
        path = default_storage.save('static/img/test.png', ContentFile(img))
        new_pic_path = hf.add_head_frame(path)
        return HttpResponse(json.dumps({'code': True, 'new_img_path': '/' + new_pic_path}))