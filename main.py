# -*- coding: utf-8 -*-

import qrcode
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol
import math
import hashlib
import trans
import sys
import getopt

#每个二维码保存的数据
K = 2000

def split_data(data):
    """拆分数据，分段生成二维码

    Args:
        data (string): 需要拆分的数据

    Returns:
        list: 拆分后的字符串列表
    """
    dataList = []
    # print(len(data))
    size = math.ceil(len(data)/K)
    for i in range(0, size):
        start = i *K
        end = (i+1)*K if len(data)  > (i+1)*K else len(data)
        dataList.append(data[start:end])
    
    return dataList

def check_valid(data1, data2):
    """检查加密后再解密的数据是否与原数据一致

    Args:
        data1 (string): 未加密的数据
        data2 (string): 从二维码读取，并解密后的数据

    Returns:
        bool: 数据一致,返回true
    """
    return  hashlib.md5(data1) == hashlib.md5(data2)
    
        

def generate_qrcode(data):
    """生成二维码

    Args:
        data (string): 需要生成二维码的字符串

    Returns:
        Image: 二维码图片
    """
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
    
def create_qrcode_image(datas, path):
    """创建图片

    Args:
        datas (List): 需要创建二维码的字符串列表
        path (str): 生成图片的路径
    """
    width, height = int(8.27 * 300), int(11.7 * 300)
    image = Image.new('RGB',(width, height), "white")
    
    x, y = 0 ,0
    for data in datas:
        qrcode = generate_qrcode(data)
        qr_height, qr_width = qrcode.size
        if x + qr_width < width:
            image.paste (qrcode, (x, y))
        else:
            y += last_qr_height
            x = 0
            image.paste (qrcode, (x, y))
        x += qr_width
        # image.show()
        last_qr_height = qr_height

    image.save(path)    
    
    
# 读取二维码内容
def read_qrcode(path, secrets_path):
    """读取二维码

    Args:
        path (string): 包含二维码的图片路径
    """
    im = Image.open(path)
    decoded = decode(Image.open(path), symbols=[ZBarSymbol.QRCODE])
    qr_dic = {}
    
    # 获取二维码的左上角坐标
    for qr_data in decoded:
        x = qr_data[2][0]
        y = qr_data[2][1]
        qr_dic[(x,y)] = qr_data[0]
    datas = [] 
    # print(sorted(qr_dic.keys()))
    
    #按顺序解析二维码内容并拼接
    for qr in sorted(qr_dic.keys()):
        datas.append(bytes.decode(qr_dic[qr]))
    file_str = "".join(datas)
    str = trans.decrypt_message(file_str)
    with open(secrets_path, "w") as f:
        f.write(str)
        

def main(argv):
    qrcode_path = ''
    data_path = ''
    mode = ''
    message = """
使用方式:
密钥转换为图片 main.py -m <encrypt> -d <datafile> -p <pic>
图片转换为秘钥 main.py -m <decrypt> -p <pic> -d <datafile>
"""
    try:
        opts, args = getopt.getopt(argv,"h:m:d:p:", ["help","mode=","data=", "pic="])
    except getopt.GetoptError:
        print(message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(message)
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-d", "--data"):
            data_path = arg
        elif opt in ("-p", "--pic"):
            qrcode_path = arg
    
    if mode in ("en" , "encrypt"):
        secrets = ""
        with open(data_path, 'r') as f:
            secrets = f.read()
        
        #加密字符串
        encypt_secrets =  trans.encrypt_message(secrets)
        #生成二维码
        create_qrcode_image(split_data(encypt_secrets), qrcode_path)
    elif mode in ("de", "decrypt"):
        #读取二维码，写入文件
        read_qrcode(qrcode_path, data_path)
        
                
            
if __name__ == '__main__':
    main(sys.argv[1:])
    main(["-m", "de", "-p", "a.jpg", "-d", "key.convert"])
    
    # qrcode_path = '/Users/michael/Develop/key2paper/qrcode.png'

    # key=""
    # with open("/Users/michael/Develop/key2paper/keys",'r' ) as f:
    #     key=f.read()
    # encode_key = key_encrypt.encrypt_message(key)
    # datas = split_data(encode_key)
    # create_qrcode_image(datas, qrcode_path)
    # pic_path = "/Users/michael/Develop/key2paper/q.jpg"
    # read_qrcode(pic_path)