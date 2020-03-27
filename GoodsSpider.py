#coding=utf-8
"""
author : Srpihot
github : https://github.com/Srpihot/
update_time : 2020-03-27
version : GoodsSpider v1.0
"""

"""
淘宝登陆有时候不会跳出二维码页面，如果失败，请重新运行程序即可
"""
import re
import os
import sys
import time
import optparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def Welcome():
    os.system('cls')
    print("   ______                         __         ______            _        __                ")
    print(" .' ___  |                       |  ]      .' ____ \          (_)      |  ]               ")
    print("/ .'   \_|   .--.    .--.    .--.| |  .--. | (___ \_|_ .--.   __   .--.| | .---.  _ .--.  ")
    print("| |   ____ / .'`\ \/ .'`\ \/ /'`\' | ( (`\] _.____`.[ '/'`\ \[  |/ /'`\' |/ /__\\[ `/'`\] ")
    print("\ `.___]  || \__. || \__. || \__/  |  `'.'.| \____) || \__/ | | || \__/  || \__., | |     ")
    print(" `._____.'  '.__.'  '.__.'  '.__.;__][\__) )\______.'| ;.__/ [___]'.__.;__]'.__.'[___]    ")
    print("                                                    [__|                                  ")
    print("                  V1.0                                            By-Srpihot*             ")
    print("    My Site: https://Srpihot.Site                My Github: https://github.com/srpihot    ")

class Taobao_Commodity_Spider:

    def __init__(self, username, password,keywords,Spider_Speed,Save_Filename,get_page):
        """初始化参数"""
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        #设置无头模式
        options.add_argument('--headless')
        # 不加载图片,加快访问速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)
        # 初始化用户名
        self.username = username
        # 初始化密码
        self.password = password
        # 添加关键字
        self.keywords = keywords
        # 添加爬取速度
        self.Spider_Speed=Spider_Speed
        # 保存文件名称
        self.Save_Filename=Save_Filename
        # 爬取的页数
        self.get_page=get_page

    def run(self):
        """登陆接口"""
        self.browser.get(self.url)
        try:
            # 这里设置等待：等待输入框
            
            sina_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
            sina_login.click()
            
            
            weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > input:nth-child(1)')))
            weibo_user.send_keys(self.username)

            sina_password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > input:nth-child(1)')))
            sina_password.send_keys(self.password)

            submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
            submit.click()

            taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
            Welcome()
            # 登陆成功打印提示信息
            print("[+]登陆成功 您的淘宝账号用户名为：%s" % taobao_name.text)
            
        except Exception as e:
            Welcome()
            print('[-]',end='')
            print(e)
            self.browser.close()
            print("[-]登陆失败,请检查账号密码是否正确~")
            print("[/]可能是网络连接问题哦~重新加载一下~")


    def get_data(self):
        with open(self.Save_Filename+'.csv','w',encoding='utf-8') as f:
            f.write("ID,商品ID,商品标题,价格,图片URL,商品URL,商品短URL,销量,是否为天猫店,商店ID,商店名字,商店URL,商店地址,市场价格,促销价格,订单数量,总销售,库存\n")
        
        self.browser.get("https://www.taobao.com/")  
        id_num=0
        try:   
            #获取输入框焦点
            input_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
            
            #获取搜索butten焦点
            submit_element = self.wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[1]/button')))
            
            #输入关键字及搜索内容
            input_element.send_keys(self.keywords)
            
            #点击搜索
            submit_element.click()

            for page_i in range(1,int(self.get_page)+1):
                #获取本页源码
                html_add_js = self.browser.page_source
                
                #使用BS4进行分析:
                data_soup=BeautifulSoup(html_add_js,'lxml')

                #获取商品简略信息
                div_result=data_soup.select('.J_MouserOnverReq')
                
                for i in range(0,len(div_result)):
                    id_num+=1

                    #初始化数据
                    salePrice = 'None'
                    reservePrice = 'None'
                    orderCost = 'None'
                    totalSoldQuantity = 'None'
                    quantity = 'None'

                    #相关数据爬取
                    Picture_div_a = div_result[i].select('.J_MouseEneterLeave .pic-box-inner .pic a')
                    Picture_div_img = div_result[i].select('.J_MouseEneterLeave .pic-box-inner .pic a img') 
                    clickUrl =  Picture_div_a[0].attrs['data-href']
                    shortLinkUrl = Picture_div_a[0].attrs['href']
                    if 'https' not in clickUrl:
                        clickUrl =  'https:' + Picture_div_a[0].attrs['data-href']
                    picUrl = Picture_div_img[0].attrs['data-src']
                    Price = div_result[i].select('.J_MouseEneterLeave .row-1 .g_price-highlight strong')[0].string
                    sold_raw = div_result[i].select('.J_MouseEneterLeave .row-1 .deal-cnt')[0].string
                    sold = re.findall('\d+',sold_raw)[0]
                    title = div_result[i].select('.J_MouseEneterLeave .title a')[0].get_text().strip('\n').strip()
                    shop_id = div_result[i].select('.J_MouseEneterLeave .row-3 .shopname')[0].attrs['data-userid']
                    auctionId = div_result[i].select('.J_MouseEneterLeave .row-3 .shopname')[0].attrs['data-nid']
                    shop_link = div_result[i].select('.J_MouseEneterLeave .row-3 .shopname')[0].attrs['href']
                    shop_name = div_result[i].select('.J_MouseEneterLeave .row-3 .shop a .dsrs+span')[0].get_text()
                    shop_address = div_result[i].select('.J_MouseEneterLeave .row-3 .location')[0].get_text()
                    icon = div_result[i].select('.J_MouseEneterLeave .row-4 .icon')
                    tianmao_icon=0
                    if 'icon-service-tianmao' in str(icon):
                        tianmao_icon=1
                        tianmao_flag='是'

                        self.browser.get(clickUrl)
                        goods_html_add_js=self.browser.page_source

                        goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                        try:
                            salePrice = goods_data_soup.select('#J_StrPriceModBox .tm-price')[0].get_text()
                            reservePrice = goods_data_soup.select('#J_PromoPrice .tm-price')[0].get_text()
                            orderCost = goods_data_soup.select('.tm-ind-panel .tm-count')[0].get_text()
                            totalSoldQuantity = goods_data_soup.select('#J_ItemRates .tm-count')[0].get_text()
                            quantity_raw = goods_data_soup.select('#J_EmStock')[0].get_text()
                            quantity = re.findall('\d+',quantity_raw)[0]
                        except:
                            pass
                    else:
                        tianmao_icon=0
                        tianmao_flag='否'
                        
                        self.browser.get(clickUrl)
                        goods_html_add_js=self.browser.page_source

                        goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                        try:
                            salePrice = Price
                            reservePrice = Price
                            orderCost = sold
                            totalSoldQuantity = goods_data_soup.select('#J_SellCounter')[0].get_text()
                            quantity = goods_data_soup.select('#J_SpanStock')[0].get_text()
                        except:
                            pass
                    with open(self.Save_Filename+'.csv','a+',encoding='utf-8') as f:
                        f.write(str(id_num)+','+auctionId+','+title+','+Price+','+picUrl+','+clickUrl+','+shortLinkUrl+','+sold+','+tianmao_flag+','+shop_id+','+shop_name+','+shop_link+','+shop_address+','+salePrice+','+reservePrice+','+orderCost+','+totalSoldQuantity+','+quantity+'\n')

                    Welcome()
                    print('[+]成功爬取第{0}页第{1}条数据'.format(page_i,i+1))

                    if self.Spider_Speed == 'fast':
                        time.sleep(0)
                    if self.Spider_Speed == 'medium':
                        time.sleep(2)
                    if self.Spider_Speed == 'slow':
                        time.sleep(5)
                    
                    #print(id_num,auctionId,title,Price,picUrl,clickUrl,shortLinkUrl,sold,tianmao_flag,shop_id,shop_name,shop_link,shop_address,end='\n',sep='\t')
                    #print(id_num,clickUrl,salePrice,reservePrice,orderCost,totalSoldQuantity,quantity)
                    
                if int(page_i) == int(self.get_page):
                    Welcome()
                    print('[+]爬取结束')
                    exit(0)
                
                print(page_i)

                page_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Input')))
                page_element.send_keys(Keys.CONTROL, 'a')
                page_element.send_keys(str(page_i+1))
                turn_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Submit')))
                turn_element.click()


        except Exception as e:
            Welcome()
            print('[-]',end='')
            print(e)
            self.browser.close()
            print("[-]获取数据失败!")

if __name__ == "__main__":

    Welcome()
    parse=optparse.OptionParser(usage='"usage:%prog [options] arg1"',version="%prog 1.0")
    parse.add_option('-u','--username',dest='username',type='str',metavar='用户名',help='请输入微博用户名')
    parse.add_option('-p','--password',dest='password',type='str',metavar='密码',help='请输入微博密码')
    parse.add_option('-k','--keyword',dest='keyword',type='str',metavar='商品名称',help='请输入希望爬取的商品名')
    parse.add_option('-g','--getpage',dest='get_page',type='int',metavar='爬取页数',default=3,help='请输入希望爬取的页数 注意:页数越多爬取时间越长')
    parse.add_option('-s','--Speed',dest='Spider_Speed',type='str',metavar='爬取速度',default='medium',help='fast 快 | medium 中等 | slow 慢')
    parse.add_option('-o',dest='Save_Filename',type='str',metavar='保存文件名称',default='Goods',help='请输入文件名称')
    Spider_args,args = parse.parse_args()

    if Spider_args.username is None or Spider_args.password is None or Spider_args.keyword is None:
        Welcome()
        print('[-]您的输入有误,请使用命令 --help 或者 -h 获得帮助。')
        exit(0)

    spider = Taobao_Commodity_Spider(Spider_args.username,Spider_args.password,Spider_args.keyword,Spider_args.Spider_Speed,Spider_args.Save_Filename,Spider_args.get_page)
    spider.run()
    spider.get_data()

