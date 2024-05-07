import re
import requests
import json
import sys
import time
import hashlib

def get_public_ip():
    try:
        response = requests.get('http://ip-api.com/json/?fields=status,query')
        if response.status_code == 200:
            json_obj=json.loads(response.text)
            public_ip = json_obj["query"]
            return public_ip
        else:
            print("Failed to retrieve public IP: HTTP status code", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
        return None

def generate_url(category, ts=None):
    url = 'http://d06.cdntest.top'                     # 测试域名
    subpath = '/'                                         # 包含子域名  
    sign_key = 'key'                               # url签名字段
    salt = 'wE65Xz'               # 鉴权盐
    now = int(time.mktime(time.strptime(ts, "%Y%m%d%H%M%S")) if ts else time.time())                # 如果输入了时间，用输入ts，否则用当前ts   
    if '11'==category or category=='1':
        #1 URL 方式；将鉴权密钥放置在URL 
        #http://waf.antscdn.com/?User-Agent=1644478226_cbb91dbffa3f12933e7019896170c16e
        print("MODE 1")
        ts = now
        if '11'==category :
            data = '%s_%s_%s' % (ts, salt,get_public_ip())
        else :
            data = '%s_%s' % (ts, salt)
        data=data.encode("utf-8")
        sign = hashlib.md5(data).hexdigest()
        request_url = '%s%s?%s=%s_%s' %(url, subpath, sign_key, ts, sign)
        print(request_url)
        r=requests.get(url=url);
        print(r.text)
    elif '12'==category or category=='2':
        #2 HTTP HEADER 方式； sign_key 放在headers_in 中,可以为user-agent/ auth/sign/等自定义HTTP 请求头key-value
        #{'User-Agent': '1644478197_bbae3d26eb0dea4592a979a9cfe33d0d Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'}
        ts = now
        if '12' == category:
            data = '%s_%s_%s' % (ts, salt, get_public_ip())
        else:
            data = '%s_%s' % (ts, salt)
        data=data.encode("utf-8")
        sign = hashlib.md5(data).hexdigest()
        request_head_key_value = '%s_%s' %(ts, sign)      
        headers={
            sign_key:request_head_key_value+"_Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"            
        }        
        print(headers);
        print(f"curl -H \"{sign_key}:{request_head_key_value}_Mozilla/5.0\" {url}")
        r=requests.get(url=url,headers=headers);
        print(r.text)
    elif '13'==category or  category=='3':
        url="http://cdntest.com/v2/public/index.php/index/index/login?/xRh7yxZKod2XBvvOIqiFoTMfzhYtlugaQATUoQnaXueu5y5fKZlrf1gpA74/8RuZWiujmN3YU8dUHjHUpE8FZEsz4HlNESupfyHQSnS8qwTxiGNBUMa2MCsmQtMgrGZZN6YJxwfVSsep/gsNMVZI+cUHWsuMuxHM/ubBOZR+tEKmaN+APzlG1dTAmbHeQE1aDfsbETSRaVsfb114nEwbQ2f5/ELSRGYQurxggl25ymNlXOj3/SiaYbsw2BxfSQVUUMJnqDh72Ir3TjwjTrThagwE+MpOOOikC3d2zlAVbU=";

        if '13' == category:
            data = '%s_%s_%s' % (ts, salt, get_public_ip())
        else:
            data = '%s_%s' % (ts, salt)
        sign = hashlib.md5(data).hexdigest()
        t_value = '%s_%s' % (ts, sign)
        data ="sign_key="+t_value
        r=requests.post(url=url,headers={},data=data)
        print(r.status_code)
        print(r.text)   




if __name__ == '__main__':
    print("current public ip:"+get_public_ip())
    #run: python ants_api_sign.py 1
    if len(sys.argv) == 1:
        generate_url('12')
        #print('usage: python ants_api_sign.py 2 ')
    else:             
        args = sys.argv[1:]
        generate_url(*args)