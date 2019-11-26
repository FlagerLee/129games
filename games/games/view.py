from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
import cv2

def index(request):
    print(request.is_ajax())
    if request.is_ajax():
        '''
        判断是否为ajax请求。
        网站中的ajax请求有上传图片和下载图片。
        '''
        #data:接收到的图片文件
        data=dict(request.FILES)['content'][0]
        #img_content是图片文件的内容，可直接被opencv操作，类型为bytes
        img_content = data.read()
        pass
    else:
        '''
        非ajax请求，加载网页
        '''
        return render(request, 'index.html', {})