import re
import requests

ji=1

def init():
    url_="https://leflacon.github.io"
    try:
        kv={'user_agent':'Mozilla/5.0'}
        requests.get(url_,headers=kv)
        return url_
    except:
        print("error(#ﾟДﾟ)")

def get_domain(url):
    url_xieyi=re.findall(r'.*(?=://)',url)[0]
    print('协议：'+url_xieyi)
    if len(re.findall(r'/',url))>2:
        if url_xieyi=='https':
            domain=re.findall(r'(?<=https://).*?(?=/)',url)[0]
        else:
            domain=re.findall(r'(?<=http://).*?(?=/)',url)[0]
    else:
        url=url+'/'
        if url_xieyi=='https':
            domain=re.findall(r'(?<=https://).*?(?=/)',url)[0]
        else:
            domain=re.findall(r'(?<=http://).*?(?=/)',url)[0]
    print('域名：'+domain)
    return domain

def small_spider(url):
    kv={'user_agent':'Mozilla/5.0'}
    r=requests.get(url,headers=kv)
    r.encoding=r.apparent_encoding
    pagetext=r.text
    page_urls=re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')',pagetext)
    return page_urls

def shaixuan(pagelinks):
    same_domain_url=[]
    for l in pagelinks:
        if re.findall(domain,l):
            same_domain_url.append(l)
    ans_url=[]
    for l in same_domain_url:
        if l not in ans_url:
            ans_url.append(l)
    return ans_url

class links:
     def __init__(self):
         self.vis=[]
         self.unvis=[]
     def get_vis(self):
         return self.vis
     def get_unvis(self):
         return self.unvis
     def add_vis(self,url):
         return self.vis.append(url)
     def add_unvis(self,url):
         return self.unvis.append(url)
     def delete_vis(self,url):
         return self.vis.remove(url)
     def pop_unvis(self):
         try:
             return self.unvis.pop()
         except:
             return None
     def insert_unvis(self,url):
         if url!="" and url not in self.vis and url not in self.unvis:
             return self.unvis.insert(0,url)
     def vis_num(self):
         return len(self.vis)
     def unvis_num(self):
         return len(self.unvis)
     def unvis_empty(self):
         return len(self.unvis)==0
        
class Spider():
    def __init__(self,url):
        self.links_=links()
        self.links_.insert_unvis(url)
    def crawl(self):
        for i in range(2,26):
            page_="https://leflacon.github.io/page/"+str(i)+"/"
            self.links_.add_unvis(page_)
            self.links_.add_vis(page_)
        while not self.links_.unvis_empty():
            global ji
            s1="爬到第"
            s2="个啦"
            print (s1,ji,s2)
            ji=ji+1
            cur_url=self.links_.pop_unvis()
            if cur_url is None or cur_url == '':
                continue
            cur_links=small_spider(cur_url)
            ok_links=shaixuan(cur_links)
            self.links_.add_vis(cur_url) 
            for link in ok_links:
                self.links_.insert_unvis(link)
        print("终于爬完啦(((o(*ﾟ▽ﾟ*)o)))！嘿咻！！")
        return self.links_.vis

def write_down(url_list):
    f=open('out.txt','w')
    for l in url_list:
        f.write(l)
        f.write('\n')
    f.close()
    
if __name__ == '__main__':
    url=init()
    domain=get_domain(url)
    spi=Spider(url)
    url_list=spi.crawl()
    write_down(url_list)
