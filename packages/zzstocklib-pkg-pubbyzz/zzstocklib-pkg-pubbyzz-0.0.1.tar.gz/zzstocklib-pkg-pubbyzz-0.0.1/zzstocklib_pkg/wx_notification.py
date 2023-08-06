from urllib import request,parse
import time,datetime
import json
import zzlogger

logger = zzlogger.logger

def send_wxnotification(message):
    """发送公众号提醒"""               #文档字符串用三引号括起，Python使用它们来生成有关程序中函数的文档。
    miao_code="tLmPyT4"
    text = message

    page = request.urlopen("http://miaotixing.com/trigger?" + parse.urlencode({"id":miao_code, "text":text, "type":"json"}))
    result = page.read()
    jsonObj = json.loads(result)

    if(jsonObj["code"] == 0):
        logger.debug("send " + message + " to WeChat success!")
    else:
        logger.error("failed, err code:" + str(jsonObj["code"]) + ", desc:" + jsonObj["msg"])


