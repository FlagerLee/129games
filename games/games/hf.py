'''
根据传入的图片，将头像框和图片进行合成
'''

import cv2

def add_head_frame(path: str):
    '''
    path是原始图片的路径
    '''
    #头像框路径
    head_frame_path = 'static/img/headframe.png'
    #读取图片
    origin_pic = cv2.imread(path)
    head_frame = cv2.imread(head_frame_path)

    #获取原图的信息
    rows, columns, channels = origin_pic.shape
    #resize头像框
    head_frame = cv2.resize(head_frame, (columns, rows))

    roi = origin_pic[0:rows, 0:columns]

    #头像框转化为灰度图
    hfgrey = cv2.cvtColor(head_frame, cv2.COLOR_BGR2GRAY)
    #从灰度图中提取头像框区域
    ret, mask = cv2.threshold(hfgrey, 250, 255, cv2.THRESH_BINARY)
    #取反，提取空白区域
    mask_inv = cv2.bitwise_not(mask)

    #将原图中应当放上头像框的部分裁掉
    pic_without_head_frame = cv2.bitwise_and(roi, roi, mask=mask)
    #提取出头像框的部分
    head_frame_part = cv2.bitwise_and(head_frame, head_frame, mask=mask_inv)

    #合成头像
    new_pic = cv2.add(pic_without_head_frame, head_frame_part)
    #储存图片
    new_filename = 'new_' + path.split('/')[-1]
    new_path = 'static/img/' + new_filename
    cv2.imwrite(new_path, new_pic)
    return new_path
