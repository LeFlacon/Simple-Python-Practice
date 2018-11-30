import six
import sys

class HuffNode(object):
    def get_times(self):
        raise NotImplementedError(
            "抽象类没有定义获取次数的函数")
    def isleaf(self):
        raise NotImplementedError(
            "抽象类没有定义判断是否为叶节点的函数")

class LeafNode(HuffNode):
    def __init__(self,c=0,times=0,):
        super(LeafNode, self).__init__()
        self.c=c
        self.times=times
    def isleaf(self):
        return True
    def get_times(self):
        return self.times
    def get_c(self):
        return self.c

class OtherNode(HuffNode):
    def __init__(self,lchild=None,rchild=None):
        super(OtherNode,self).__init__()
        self.times=lchild.get_times()+rchild.get_times()
        self.lchild=lchild
        self.rchild=rchild
    def isleaf(self):
        return False
    def get_times(self):
        return self.times
    def get_lchild(self):
        return self.lchild
    def get_rchild(self):
        return self.rchild

class HuffTree(object):
    def __init__(self,flag,c=0,times=0,left_tree=None,right_tree=None):
        super(HuffTree, self).__init__()
        if flag==0:
            self.root=LeafNode(c,times)
        else:
            self.root=OtherNode(left_tree.get_root(), right_tree.get_root())
    def get_root(self):
        return self.root
    def get_times(self):
        return self.root.get_times()
    def encode(self,root,code,char_times):
        if root.isleaf():
            char_times[root.get_c()]=code
            # print(("it = %c  and  times = %d  code = %s")%(chr(root.get_c()),root.get_times(),code))
            return None
        else:
            self.encode(root.get_lchild(),code+'0',char_times)
            self.encode(root.get_rchild(),code+'1',char_times)

def build(list_HuffTree):
    while len(list_HuffTree)>1:
        list_HuffTree.sort(key=lambda x: x.get_times()) 
        n1=list_HuffTree[0]
        n2=list_HuffTree[1]
        list_HuffTree=list_HuffTree[2:]
        new_HuffTree=HuffTree(1,0,0,n1,n2)
        list_HuffTree.append(new_HuffTree)
    return list_HuffTree[0]

def yasuo(in_file_name,out_file_name):
    f=open(in_file_name,'rb')
    data=f.read()
    size=f.tell()
    char_times={}
    for x in range(size):
        tmp=data[x]
        if tmp in char_times.keys():
            char_times[tmp]=char_times[tmp]+1
        else:
            char_times[tmp]=1
    # for tmp in char_times.keys():
        # print(tmp,' : ',char_times[tmp])
    list_HuffTree = []
    for x in char_times.keys():
        leaf_=HuffTree(0,x,char_times[x],None,None)
        list_HuffTree.append(leaf_)
    leaf_num=len(char_times.keys())
    a4=leaf_num&255
    leaf_num=leaf_num>>8
    a3=leaf_num&255
    leaf_num=leaf_num>>8
    a2=leaf_num&255
    leaf_num=leaf_num>>8
    a1=leaf_num&255
    output=open(out_file_name,'wb')
    output.write(six.int2byte(a1))
    output.write(six.int2byte(a2))
    output.write(six.int2byte(a3))
    output.write(six.int2byte(a4))
    for x in char_times.keys():
        output.write(six.int2byte(x))
        tmpp=char_times[x]
        a4=tmpp&255
        tmpp=tmpp>>8
        a3=tmpp&255
        tmpp=tmpp>>8
        a2=tmpp&255
        tmpp=tmpp>>8
        a1=tmpp&255
        output.write(six.int2byte(a1))
        output.write(six.int2byte(a2))
        output.write(six.int2byte(a3))
        output.write(six.int2byte(a4))

    HTree=build(list_HuffTree)
    HTree.encode(HTree.get_root(),'',char_times)
    
    code=''
    for i in range(size):
        key=data[i]
        code=code+char_times[key]
        ans=0
        while len(code)>8:
            for x in range(8):
                ans=ans<<1
                if code[x]=='1':
                    ans=ans|1
            code=code[8:]
            output.write(six.int2byte(ans))
            ans=0

    output.write(six.int2byte(len(code)))
    ans=0
    for i in range(len(code)):
        ans=ans<<1
        if code[i]=='1':
            ans=ans|1
    for i in range(8-len(code)):
        ans=ans<<1
    output.write(six.int2byte(ans))
    output.close()

def jieyasuo(in_file_name, out_file_name):
    f=open(in_file_name,'rb')
    data=f.read()
    size=f.tell()
    a1=data[0]
    a2=data[1]
    a3=data[2]
    a4=data[3]    
    j=0
    j=j|a1
    j=j<<8
    j=j|a2
    j=j<<8
    j=j|a3
    j=j<<8
    j=j|a4

    leaf_num=j
    char_times={}
    for i in range(leaf_num):
        c=data[4+i*5+0]
        a1=data[4+i*5+1]
        a2=data[4+i*5+2]
        a3=data[4+i*5+3]
        a4=data[4+i*5+4]
        j=0
        j=j|a1
        j=j<<8
        j=j|a2
        j=j<<8
        j=j|a3
        j=j<<8
        j=j|a4
        # print(c,j)
        char_times[c]=j
    list_HuffTree=[]
    for x in char_times.keys():
        tmp=HuffTree(0,x,char_times[x],None,None)
        list_HuffTree.append(tmp)
    HTree=build(list_HuffTree)
    HTree.encode(HTree.get_root(),'',char_times)

    output=open(out_file_name,'wb')
    code=''
    currnode=HTree.get_root()
    for x in range(leaf_num*5+4,size):
        c=data[x]
        for i in range(8):
            if c&128:
                code=code+'1'
            else:
                code=code+'0'
            c=c<<1
        while len(code)>24:
            if currnode.isleaf():
                tmp_byte=six.int2byte(currnode.get_c())
                output.write(tmp_byte)
                currnode=HTree.get_root()
            if code[0]=='1':
                currnode=currnode.get_rchild()
            else:
                currnode=currnode.get_lchild()
            code=code[1:]
    sub_code=code[-16:-8]
    last_leaf_num=0
    for i in range(8):
        last_leaf_num=last_leaf_num<<1
        if sub_code[i]=='1':
            last_leaf_num=last_leaf_num|1
    code=code[:-16]+code[-8:-8+last_leaf_num]
    while len(code)>0:
        if currnode.isleaf():
            tmp_byte=six.int2byte(currnode.get_c())
            output.write(tmp_byte)
            currnode=HTree.get_root()
        if code[0]=='1':
            currnode=currnode.get_rchild()
        else:
            currnode=currnode.get_lchild()
        code=code[1:]
    if currnode.isleaf():
        tmp_byte=six.int2byte(currnode.get_c())
        output.write(tmp_byte)
        currnode=HTree.get_root()
    output.close()

if __name__ == '__main__':
    print("0.压缩 1.解压缩\n")
    FLAG=input("请输入操作：")
    INPUTFILE=input("请输入需要操作的文件名：")
    OUTPUTFILE=input("请输入保存结果的文件名：")
    if FLAG=='0':
        print("压缩文件")
        yasuo(INPUTFILE,OUTPUTFILE)
    else:
        print("解压缩文件")
        jieyasuo(INPUTFILE,OUTPUTFILE)
