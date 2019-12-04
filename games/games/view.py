from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import FileResponse
from django.http import Http404
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
    if request.is_ajax():
        '''
        判断是否为ajax请求。
        网站中的ajax请求有上传图片和下载图片。
        '''
        #data:接收到的图片文件
        code = request.POST['code']
        data=dict(request.FILES)['content'][0]
        #防止模拟前端发送恶意code
        try:
            code = int(code)
        except Exception:
            return HttpResponseRedirect(request, 'index.html', {})
        #将问津进行存储，并返回原图预览
        path = 'static/img/' + str(code) + '.png'
        with open(path, 'wb') as png:
            png.write(data.read())
        #返回原图预览
        return HttpResponse(json.dumps({'code': True, 'img_path': '/' + path}))
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
        code = request.POST['code']
        data = request.POST['content'].split(',')[1]
        img = b64decode(data)
        #防止恶意code
        try:
            code = int(code)
        except Exception:
            return HttpResponseRedirect(request, 'index.html', {})
        path = 'static/img/cropped_' + str(code) + '.png'
        with open(path, 'wb') as png:
            png.write(img)
        new_pic_path = hf.add_head_frame(path)
        return HttpResponse(json.dumps({'code': True, 'new_img_path': '/' + new_pic_path}))

def download(request, code):
    '''
    下载请求
    '''
    path = settings.BASE_DIR + '/static/img/new_cropped_' + str(code) + '.png'
    if os.path.exists(path):
        content = open(path, 'rb')
        filename = 'new_image.png'
        response = FileResponse(content)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return response
    else:
        return Http404


def deletepic(code):
    '''
    删除编码为code的图片
    '''
    baseurl = settings.BASE_DIR + '/static/img/'
    if os.path.exists(baseurl + str(code) + '.png'):
        os.remove(baseurl + str(code) + '.png')
    if os.path.exists(baseurl + 'cropped_' + str(code) + '.png'):
        os.remove(baseurl + 'cropped_' + str(code) + '.png')
    if os.path.exists(baseurl + 'new_cropped_' + str(code) + '.png'):
        os.remove(baseurl + 'new_cropped_' + str(code) + '.png')

def close(request):
    '''
    关闭窗口
    '''
    if not request.is_ajax():
        return HttpResponseRedirect('/index/')
    else:
        code = request.POST['code']
        deletepic(code)
        return HttpResponse(json.dumps({}))