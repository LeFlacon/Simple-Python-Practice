from numpy import *

def loaddata_set(fileName):
    data=[]
    f=open(fileName)
    ff=f.readlines()
    del ff[0]
    for line in ff:
        s=line.strip().split(',')
        if('clear' in s[5]):
            s[5]=(float)(0.1)
        elif ('green' in s[5]):
            s[5]=(float)(0.2)
        elif ('black' in s[5]):
            s[5]=(float)(0.3)
        elif ('white' in s[5]):
            s[5]=(float)(0.4)
        elif ('blue' in s[5]):
            s[5]=(float)(0.5)
        elif ('blood' in s[5]):
            s[5]=(float)(0.6)
        del s[6]
        del s[0]
        ll=list(map(float,s))
        data.append(ll)
    return data

#欧几里得距离
def distance_e(vecA, vecB):
    return sqrt(sum(power(vecA-vecB,2)))

#取k个随机质心
def rand_center(data_set,k):
    n=shape(data_set)[1]
    centerr=mat(zeros((k,n)))#每个质心n个坐标值
    for j in range(n):
        minj=min(data_set[:,j])
        maxj=max(data_set[:,j])
        cha=float(maxj-minj)
        centerr[:,j]=minj+cha*random.rand(k,1)
    return centerr

#kmeans算法
def kmeans(data_set,k,distMeans=distance_e,createCent=rand_center):
    m=shape(data_set)[0]
    ans_classify=mat(zeros((m,2)))
    #第一列存所属的质心，第二列存到质心的距离
    centerr=createCent(data_set,k)
    flag=True#是否已收敛
    while flag:
        flag=False;
        for i in range(m):#把每一个数据点划分到离它最近的质心
            minn=inf;
            cur=-1;
            for j in range(k):
                juli=distMeans(centerr[j,:],data_set[i,:])
                if juli<minn:
                    minn=juli;cur=j#如果第i个数据点到第j个中心点更近，则将i归属为j
            if ans_classify[i,0]!=cur:flag=True;#如果分配发生变化，则需要继续迭代
            ans_classify[i,:]=cur,minn**2#将第i个数据点的情况存入字典
        print(centerr)
        for cc in range(k):#重新计算中心点
            ptsInClust=data_set[nonzero(ans_classify[:,0].A==cc)[0]]#去第一列等于cent的所有列
            centerr[cc,:]=mean(ptsInClust,axis=0)#算出这些数据的中心点
    return centerr,ans_classify

data_mat=mat(loaddata_set('Halloween.csv'))
getcenter,get_classify=kmeans(data_mat,3)
print(getcenter)
print(get_classify)
