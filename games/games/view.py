# -*- coding: utf-8 -*-
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
import random
sgm = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','o','r','s','t','u','v','w','x','y','z']
def random_string():
    s = ''
    for i in range(32):
        s += sgm[random.randint(0,25)]
    return s
def index(request):
    print(request.is_ajax())
    if request.session.get('id', '') == '':
        request.session['id'] = random_string()
    if request.is_ajax():
        '''
        判断是否为ajax请求。
        网站中的ajax请求有上传图片和下载图片。
        '''
        #data:接收到的图片文件
        data=dict(request.FILES)['content'][0]
        #将问津进行存储，并返回原图预览
        default_storage.delete('static/img/test' + request.session['id'] + '.png')
        path = default_storage.save('static/img/test' + request.session['id'] + '.png', ContentFile(data.read()))
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
    if request.session.get('id', '') == '':
        request.session['id'] = random_string()
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
        default_storage.delete('static/img/test' + request.session['id'] + '.png')
        path = default_storage.save('static/img/test' + request.session['id'] + '.png', ContentFile(img))
        new_pic_path = hf.add_head_frame(path)
        return HttpResponse(json.dumps({'code': True, 'new_img_path': '/' + new_pic_path}))