from django.http import HttpResponseRedirect
from django.shortcuts import render
import json

def index(request):
    print(request.is_ajax())
    if request.is_ajax():
        '''
        判断是否为ajax请求。
        网站中的ajax请求有上传图片和下载图片。
        '''
        data = request.body.decode('utf-8')
        data = json.loads(data)
        print(data)
        pass
    else:
        '''
        非ajax请求，加载网页
        '''
        return render(request, 'index.html', {})