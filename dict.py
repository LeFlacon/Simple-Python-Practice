import requests
import re

def get():
    word=input("(・ω・)ノ请输入需要翻译的英文单词：\n")
    url="http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index"
    gotit=requests.get(url).content.decode('utf-8')
    return gotit
def find():
    l1=re.findall("详细释义.+<p class=\"collapse-content\">",get(),re.S)
    l2=re.findall("                \w+",str(l1))
    print("翻译结果如下：\n")
    for i in l2:
        i=i.strip()
        print(i)
while (1):
    find()
