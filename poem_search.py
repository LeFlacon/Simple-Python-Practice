import os
import jieba
import json
import datetime
import random
from tkinter import *
import zhconv

project_path = os.getcwd()
file_path = project_path + "/chinesepoetry"
# file_path = project_path + "/test"
print("项目路径：", project_path)
print("数据集路径：", file_path)

'''
============
深度学习对对联
============
'''

global infile, outfile, zishi
try:
    with open("zknow.txt", "r", encoding='utf-8') as zishi_file:
        zishi = json.loads(zishi_file.read())
except IOError:
    zishi = {}


def couplet(s):
    x = []
    for i in range(len(s)):
        x.append(ran(s[i], random.random()))
    return "".join(x)


def ran(w, r):
    global zishi, writemode
    zikey = zishi.keys()
    if w != '' and w in zikey:
        zishikey = zishi[w].keys()
        max = ["", 0.0]
        for i in zishikey:
            if i != '$':
                if r < float(zishi[w][i]):
                    return i
                else:
                    r = r - float(zishi[w][i])
        return max[0]
    else:
        return "".join([ran(i, random.random()) for i in w])


def DuiDuiLian():
    try:
        # s = input("输入上联：")
        # s = jieba.lcut(s)
        # print("-----------------------------------")
        # print("上联：" + "".join(s))
        # print("下联：" + couplet(s))
        # print("-----------------------------------")
        # print("")
        text1.delete('1.0', END)
        s = e4.get()
        if s != "":
            s = jieba.lcut(s)
            text1.insert("insert", "=========================================\n")
            text1.insert("insert", "上联：")
            text1.insert("insert", "".join(s))
            text1.insert("insert", "\n")
            text1.insert("insert", "下联：")
            text1.insert("insert", ""+couplet(s))
            text1.insert("insert", "\n")
            text1.insert("insert", "=========================================\n")
        else:
            text1.insert("insert", "对诗输入为空\n")
    except Exception:
        print("对联系统出错")


'''
============
全局变量
============
'''

INDEX_SHUANGCI = {}
INDEX_WEIZHI = {}
# 根据古诗编号存古诗的题目/内容/作者，显示用
POET_MSG = []


'''
============
文件读写相关
============
'''


# 写json
def write_to_file(content, filename):
    file = open(filename, 'w', encoding='UTF-8')
    data = json.dumps(content, ensure_ascii=False, indent=4)
    file.write(data)
    file.close()


# 获取索引
def get_index(filename):
    file = open(project_path + '/' + filename, 'r', encoding='UTF-8')
    indexstr = file.read()
    index = json.JSONDecoder().decode(indexstr)
    return index


# 获取数据集数据
def get_poet(filename):
    file = open(file_path + '/' + filename, 'r', encoding='UTF-8')
    data = json.load(file)
    return data


'''
============
加载停用词
============
'''


def get_stop_words():
    print('加载停用词库...')
    stopwords = []
    with open(project_path + '/stopwords.txt', encoding='UTF-8') as openfile:
        lines = openfile.readlines()
        for line in lines:
            line = line.strip('\n')
            stopwords.append(line)
    return stopwords


STOPWORDS = get_stop_words()


def sort_list(dictt):
    sdict = {k: dictt[k] for k in sorted(dictt.keys())}
    return sdict


'''
============
建立索引
============
'''


def create_index():
    path = file_path
    filenames = os.listdir(path)
    shuangci_index = {}
    weizhi_index = {}
    msg_poet = []
    ji = 0
    for filename in filenames:
        # print(filename)
        name = os.path.split(filename)[1].split(".")
        if name[0] == 'authors':
            continue
        else:
            poet_json = get_poet(filename)
            for poet in poet_json:
                author = poet['author']
                paragragh = poet['paragraphs']
                title = poet['title']
                # 储存古诗词信息
                poet_dict = {}
                poet_dict['title'] = title
                poet_dict['author'] = author
                poet_dict['paragragh'] = paragragh
                msg_poet.append(poet_dict)
                # 建立双词索引
                hang = len(paragragh)
                paragraphs = ''
                for j in range(hang):
                    paragraphs = paragraphs + paragragh[j]
                results = list(jieba.cut_for_search(paragraphs))
                # 去除停用词
                final = []
                for word in results:
                    if word not in STOPWORDS:
                        final.append(word)
                results = final
                for word in results:
                    if len(word) <= 1:
                        continue
                    if word[0] not in shuangci_index:
                        poet_list = []
                        poet_list.append(ji)
                        shuangci_index[word[0]] = {}
                        shuangci_index[word[0]][word] = poet_list
                    else:
                        if word not in shuangci_index[word[0]]:
                            poet_list = []
                            poet_list.append(ji)
                            shuangci_index[word[0]][word] = poet_list
                        else:
                            shuangci_index[word[0]][word].append(ji)

                # 建立位置索引
                for i in range(len(paragraphs)):
                    if paragraphs[i] not in STOPWORDS:
                        if paragraphs[i] not in weizhi_index:
                            weizhi_list = []
                            weizhi_list.append(i)
                            weizhi_index[paragraphs[i]] = {}
                            weizhi_index[paragraphs[i]][ji] = weizhi_list
                        else:
                            if ji not in weizhi_index[paragraphs[i]]:
                                weizhi_list = []
                                weizhi_list.append(i)
                                weizhi_index[paragraphs[i]][ji] = weizhi_list
                            else:
                                weizhi_index[paragraphs[i]][ji].append(i)

                ji += 1

    shuangci_index = sort_list(shuangci_index)
    write_to_file(shuangci_index, project_path + '/shuangci.json')
    weizhi_index = sort_list(weizhi_index)
    write_to_file(weizhi_index, project_path + '/weizhi.json')
    write_to_file(msg_poet, project_path + '/poet_msg.json')


'''
============
搜索
============
'''


# 通过古诗号输出古诗信息
def ShowPoet(num):
    if num > 0 and num < len(POET_MSG):
        # print("=========================================")
        # print("古诗名：", end="")
        # print(POET_MSG[num]["title"])
        # print("作者：", end="")
        # print(POET_MSG[num]["author"])
        # print("内容：", end="")
        # print(POET_MSG[num]["paragragh"])
        # print("=========================================")
        text1.insert("insert", "=========================================\n")
        text1.insert("insert", "古诗名：")
        text1.insert("insert", POET_MSG[num]["title"])
        text1.insert("insert", "\n")
        text1.insert("insert", "作者：")
        text1.insert("insert", POET_MSG[num]["author"])
        text1.insert("insert", "\n")
        text1.insert("insert", "内容：")
        text1.insert("insert", POET_MSG[num]["paragragh"])
        text1.insert("insert", "\n")
        text1.insert("insert", "=========================================\n")
        return 1
    else:
        return 0


def JiaoList(list1, list2):
    res = []
    for item in list1:
        if item in list2:
            res.append(item)
    return res


def SubList(list1, list2):
    res = []
    for item in list1:
        if item not in list2:
            res.append(item)
    return res


def CheckList(list1, list2):
    res = []
    for item1 in list1:
        for item2 in list2:
            if item2 == item1 + 1:
                res.append(item2)
    return res


def SearchWord(word):
    if (len(word) == 0):
        return
    print(word)
    if (len(word) > 1):
        if word[0] in INDEX_SHUANGCI:
            if word in INDEX_SHUANGCI[word[0]]:
                return INDEX_SHUANGCI[word[0]][word]
    if word[0] not in INDEX_WEIZHI:
        return []
    # poeta存储包含每个字的文档集
    poeta = INDEX_WEIZHI[word[0]].keys()
    for i in range(1, len(word)):
        zi = word[i]
        if zi not in INDEX_WEIZHI:
            return []
        poetb = INDEX_WEIZHI[zi].keys()
        poeta = JiaoList(poeta, poetb)
    if len(poeta) == 0:
        return []
    res = []
    # weizhia存储包含当前短语的可能的位置集
    for poetid in poeta:
        weizhia = INDEX_WEIZHI[word[0]][poetid]
        for i in range(1, len(word)):
            weizhib = INDEX_WEIZHI[word[i]][poetid]
            weizhia = CheckList(weizhia, weizhib)
        if len(weizhia) != 0:
            res.append(poetid)
    # if len(res) == 0:
    # print("没有找到关于\"" + word + "\"的信息")
    return res


# 多个搜索词满足任一：或
def SearchOr():
    text_or = e1.get()
    if (text_or == ""):
        print("输入为空！")
        return
    # print("查询系统载入中...")
    # print("请输入可能包含的内容:（用空格分隔，#则跳过）")
    # text_or = input()
    text_or = zhconv.convert(text_or, 'zh-tw')
    search_list = list(text_or.split(" "))
    print("您输入的词语集合为:", end="")
    print(search_list)
    res = []
    for word in search_list:
        poetlist = SearchWord(word)
        res = res + poetlist
    res = set(res)
    if len(res) == 0:
        print("没有找到关于\"" + text_or + "\"的信息")
    # for poetid in res:
    #     ShowPoet(int(poetid))
    return res


# 多个搜索词需同时满足：与
def SearchAnd():
    text_and = e2.get()
    if (text_and == ""):
        print("输入为空！")
        return
    text_and = zhconv.convert(text_and, 'zh-tw')
    search_list = list(text_and.split(" "))
    print("您输入的词语集合为:", end="")
    print(search_list)
    res = []
    for word in search_list:
        poetlist = SearchWord(word)
        if len(res) != 0:
            res = JiaoList(res, poetlist)
        else:
            res = poetlist
    res = set(res)
    if len(res) == 0:
        print("没有找到关于\"" + text_and + "\"的信息")
    # for poetid in res:
    #     ShowPoet(int(poetid))
    return res


# 多个搜索词需不满足：非
def SearchNot():
    text_not = e3.get()
    if (text_not == ""):
        print("输入为空！")
        return
    text_not = zhconv.convert(text_not, 'zh-tw')
    search_list = list(text_not.split(" "))
    print("您输入的词语集合为:", end="")
    print(search_list)
    res = []
    for word in search_list:
        poetlist = SearchWord(word)
        if len(res) != 0:
            res = JiaoList(res, poetlist)
        else:
            res = poetlist
    res = set(res)
    # for poetid in res:
    #     ShowPoet(int(poetid))
    return res


def MainSearch():
    text1.delete('1.0', END)
    if e1.get() == "" and e2.get() == "":
        print("请输入需要检索的内容")
    res = []
    if str(e1.get()) != "":
        tmp = list(SearchOr())
        if len(tmp) == 0:
            text1.insert("insert", "无搜索结果")
            return
        else:
            res = res + tmp
    if str(e2.get()) != "":
        tmp = list(SearchAnd())
        if len(tmp) == 0:
            text1.insert("insert", "无搜索结果")
            return
        else:
            res = res + tmp
    if str(e3.get()) != "":
        tmp = SearchNot()
        res = SubList(res, tmp)
    res = list(set(res))
    if len(res) == 0:
        text1.insert("insert", "无搜索结果")
        return
    else:
        for poetid in res:
            ShowPoet(int(poetid))


'''
============
START
============
'''

# print("建立索引...")
# print("建立索引开始时间：", datetime.datetime.now())
# create_index()
# print("建立索引结束时间：", datetime.datetime.now())

print("打开索引...")
print("打开索引开始时间：", datetime.datetime.now())
INDEX_SHUANGCI = get_index("shuangci.json")
INDEX_WEIZHI = get_index("weizhi.json")
POET_MSG = get_index("poet_msg.json")
print("打开索引结束时间：", datetime.datetime.now())

all_title_num = len(POET_MSG)
print("共有" + str(all_title_num) + "首古诗词...")

root = Tk()
root.title("1711447古诗词检索系统")
root.geometry("400x600")
lab = Label(root, text='欢迎使用古诗词检索系统！', bg='grey', font=('Arial', 14), width=30, height=2)
lab.pack()

label1 = Label(root, text='请输入"或"搜索内容')
label1.pack()
v1 = StringVar()
e1 = Entry(root, textvariable=v1, validate='focusout')
e1.pack()

label1 = Label(root, text='请输入"与"搜索内容')
label1.pack()
v2 = StringVar()
e2 = Entry(root, textvariable=v2, validate='focusout')
e2.pack()

label1 = Label(root, text='请输入"非"搜索内容')
label1.pack()
v3 = StringVar()
e3 = Entry(root, textvariable=v3, validate='focusout')
e3.pack()

b1 = Button(root, text="搜索", command=MainSearch)
b1.pack()

label4 = Label(root, text='请输入想要对的诗句')
label4.pack()
v4 = StringVar()
e4 = Entry(root, textvariable=v4, validate='focusout')
e4.pack()

b2 = Button(root, text="对诗", command=DuiDuiLian)
b2.pack()

text1 = Text(root)
text1.pack()

root.mainloop()
