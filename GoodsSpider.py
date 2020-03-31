#coding=utf-8
"""
author : Srpihot
<<<<<<< HEAD
github : https://github.com/Srpihot/GoodsSpider
update_time : 2020-03-31
version : GoodsSpider v1.2
=======
github : https://github.com/Srpihot/
update_time : 2020-03-30
version : GoodsSpider v1.1
>>>>>>> c73702ba57580c8e4e70b62aee1d58b9d017018d
"""

"""
淘宝登陆有时候不会跳出二维码页面，如果失败，请重新运行程序即可
"""
import re
import os
import sys
import random
import platform
import optparse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def Welcome():
    sys = platform.system()
    if sys == "Windows":
        os.system('cls')
    else:
        os.system('clear')
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

    def __init__(self, username, password,keywords,Spider_Speed,Save_Filename,get_page,Page_Once,site):
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
        # 爬取具体的页数
        self.Page_Once=Page_Once
        # 爬取具体网站分类
        self.site=site

    # 模拟人类的滑动轨迹
    def get_track(self,distance):      # distance为传入的总距离
        # 移动轨迹
        track=[]
        # 当前位移
        current=0
        # 减速阈值
        mid=distance*4/5
        # 计算间隔
        t=0.2
        # 初速度
        v=1

        while current<distance:
            if current<mid:
                # 加速度为2
                a=4
            else:
                # 加速度为-2
                a=-3
            v0=v
            # 当前速度
            v=v0+a*t
            # 移动距离
            move=v0*t+1/2*a*t*t
            # 当前位移
            current+=move
            # 加入轨迹
            track.append(round(move))
        return track
    
    #滑块解锁破解
    def move_to_gap(self,slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹

        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        sleep(0.5)
        ActionChains(self.browser).release().perform()


    def landing(self):
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
    
    #感谢yanjingke老哥提供的PR
    def swipe_down(self, second):
        # 大部分人被检测为机器人就是因为没有进一步模拟人工操作
        # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
        for i in range(int(second / 0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.browser.execute_script(js)
            if self.Spider_Speed == 'fast':
                sleep(0)
            if self.Spider_Speed == 'medium':
                sleep(0.3)
            if self.Spider_Speed == 'slow':
                sleep(0.5)
        js = "var q=document.body.scrollTop=10000"
        self.browser.execute_script(js)
        if self.Spider_Speed == 'fast':
            sleep(0)
        if self.Spider_Speed == 'medium':
            sleep(1)
        if self.Spider_Speed == 'slow':
            sleep(2)

    def get_taobao_goods_data(self):
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

                #获取本页url:
                url_old=self.browser.current_url

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
                        try:
                            # 模拟拽托
                            self.browser.switch_to.frame("sufei-dialog-content")
                            swipe_button=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))  # 等待滑动拖动控件出现
                            print('[/]爬取次数太多拉~遇到滑块解锁~')
                            print('[+]正在模拟人类的滑块解锁~')
                            self.move_to_gap(swipe_button,self.get_track(3600))
                            html_huakuang=self.browser.page_source
                            while '哎呀，出错了，点击' in html_huakuang:
                                print('[-]滑块破解失败~')
                                print('[+]重新模拟~')
                                sleep(0.5)
                                self.browser.switch_to.frame("sufei-dialog-content")
                                swipe_button=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))  # 等待滑动拖动控件出现
                                self.browser.find_element_by_css_selector('#nocaptcha > div > span > a').click()
                                self.move_to_gap(swipe_button,self.get_track(3600))
                            print('[+]模拟成功,开始爬取相关数据~')
                        except Exception as e:
                            print('[-]',e)
                        
                        self.browser.get(clickUrl)
                        can_swipe=random.randint(0,7)
                        if can_swipe%2==0:
                            self.swipe_down(1)

                        goods_html_add_js=self.browser.page_source
                        goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                        try:
                            salePrice = goods_data_soup.select('#J_StrPriceModBox .tm-price')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            reservePrice = goods_data_soup.select('#J_PromoPrice .tm-price')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            orderCost = goods_data_soup.select('.tm-ind-panel .tm-count')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            totalSoldQuantity = goods_data_soup.select('#J_ItemRates .tm-count')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            quantity_raw = goods_data_soup.select('#J_EmStock')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            quantity = re.findall('\d+',quantity_raw)[0]
                        except Exception as e:
                            print('[-]',e)
                    else:
                        tianmao_icon=0
                        tianmao_flag='否'

                        self.browser.get(clickUrl)
                        goods_html_add_js=self.browser.page_source
                        can_swipe=random.randint(0,7)
                        if can_swipe%2==0:
                            self.swipe_down(1)
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
                        sleep(0)
                    if self.Spider_Speed == 'medium':
                        sleep(2)
                    if self.Spider_Speed == 'slow':
                        sleep(5)
                    
                    #print(id_num,auctionId,title,Price,picUrl,clickUrl,shortLinkUrl,sold,tianmao_flag,shop_id,shop_name,shop_link,shop_address,end='\n',sep='\t')
                    #print(id_num,clickUrl,salePrice,reservePrice,orderCost,totalSoldQuantity,quantity)
                    
                if int(page_i) == int(self.get_page):
                    Welcome()
                    print('[+]爬取结束')
                    break
                else:
                    self.browser.get(url_old)
                    page_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Input')))
                    page_element.send_keys(Keys.CONTROL, 'a')
                    page_element.send_keys(str(page_i+1))
                    turn_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Submit')))
                    turn_element.click()


        except Exception as e:
            Welcome()
            print('[-]',e)
            self.browser.close()
            print("[-]获取数据失败!")
            exit(0)
    
    def get_taobao_goods_page_once(self):
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

            #跳转具体某一页
            page_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Input')))
            
            page_element.send_keys(Keys.CONTROL, 'a')
            
            page_element.send_keys(int(self.Page_Once))
            
            turn_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.J_Submit')))
            
            turn_element.click()

            
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
                    try:
                        # 模拟拽托
                        self.browser.switch_to.frame("sufei-dialog-content")
                        swipe_button=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))  # 等待滑动拖动控件出现
                        print('[/]爬取次数太多拉~遇到滑块解锁~')
                        print('[+]正在模拟人类的滑块解锁~')
                        self.move_to_gap(swipe_button,self.get_track(1200))
                        html_huakuang=self.browser.page_source
                        while '哎呀，出错了，点击' in html_huakuang:
                            print('[-]滑块破解失败~')
                            print('[+]重新模拟~')
                            sleep(0.5)
                            swipe_button=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))  # 等待滑动拖动控件出现
                            self.browser.find_element_by_css_selector('#nocaptcha > div > span > a').click()
                            self.move_to_gap(swipe_button,self.get_track(1200))
                        print('[+]模拟成功,开始爬取相关数据~')
                    except Exception as e:
                        print('[-]',e)
                    
                    self.browser.get(clickUrl)
                    can_swipe=random.randint(0,7)
                    if can_swipe%2==0:
                        self.swipe_down(1)

                    goods_html_add_js=self.browser.page_source
                    goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                    try:
                        salePrice = goods_data_soup.select('#J_StrPriceModBox .tm-price')[0].get_text()
                    except Exception as e:
                        print('[-]',e)
                    try:
                        reservePrice = goods_data_soup.select('#J_PromoPrice .tm-price')[0].get_text()
                    except Exception as e:
                        print('[-]',e)
                    try:
                        orderCost = goods_data_soup.select('.tm-ind-panel .tm-count')[0].get_text()
                    except Exception as e:
                        print('[-]',e)
                    try:
                        totalSoldQuantity = goods_data_soup.select('#J_ItemRates .tm-count')[0].get_text()
                    except Exception as e:
                        print('[-]',e)
                    try:
                        quantity_raw = goods_data_soup.select('#J_EmStock')[0].get_text()
                    except Exception as e:
                        print('[-]',e)
                    try:
                        quantity = re.findall('\d+',quantity_raw)[0]
                    except Exception as e:
                        print('[-]',e)
                else:
                    tianmao_icon=0
                    tianmao_flag='否'

                    self.browser.get(clickUrl)
                    goods_html_add_js=self.browser.page_source
                    can_swipe=random.randint(0,7)
                    if can_swipe%2==0:
                        self.swipe_down(1)
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
                print('[+]成功爬取第{0}页第{1}条数据'.format(self.Page_Once,i+1))

                if self.Spider_Speed == 'fast':
                    sleep(0)
                if self.Spider_Speed == 'medium':
                    sleep(2)
                if self.Spider_Speed == 'slow':
                    sleep(5)

            Welcome()
            print('[+]爬取结束')

        except Exception as e:
            Welcome()
            print('[-]',e)
            self.browser.close()
            print("[-]获取数据失败!")
            exit(0)    

    def get_jingdong_goods_data(self):
        with open(self.Save_Filename+'.csv','w',encoding='utf-8') as f:
            f.write("ID,商品ID,商品标题,价格,图片URL,商品URL,商品短URL,销量,商店ID,商店名字,商店URL,商店地址,市场价格,促销价格,订单数量,总销售,库存\n")
        
        self.browser.get("https://www.jd.com/")  
        id_num=0
        try:
            #获取输入框焦点
            input_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))
            
            #获取搜索butten焦点
            submit_element = self.wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[4]/div/div[2]/div/div[2]/button')))
            
            #输入关键字及搜索内容
            input_element.send_keys(self.keywords)
            
            #点击搜索
            submit_element.click()
            
            Welcome()
            print('[+]搜索成功~准备爬取~')

            for page_i in range(0,int(self.get_page)+2):
                
                #获取本页源码
                html_add_js = self.browser.page_source
                
                #使用BS4进行分析:
                data_soup=BeautifulSoup(html_add_js,'lxml')

                #获取商品简略信息
                div_result=data_soup.select('#J_goodsList li')
                
                url_new=self.browser.current_url

                if page_i > 1:
                    for i in range(0,len(div_result)):
                        id_num+=1

                        #初始化数据
                        salePrice = 'None'
                        reservePrice = 'None'
                        orderCost = 'None'
                        totalSoldQuantity = 'None'
                        quantity = 'None'

                        #相关数据爬取
                        try:
                            clickUrl =  div_result[i].select('.p-img a')[0].attrs['href']
                        except Exception as e:
                            print('[-]',e)
                        shortLinkUrl =clickUrl
                        if 'https' not in clickUrl:
                            clickUrl =  'https:' + clickUrl
                        try:
                            picUrl = div_result[i].select('.p-img img')[0].attrs['data-lazy-img']
                            if 'https' not in picUrl:
                                picUrl =  'https:' + picUrl
                        except Exception as e:
                            print('[-]',e)
                        try:
                            Price = div_result[i].select('.p-price i')[0].string
                        except Exception as e:
                            print('[-]',e)
                        try:
                            auctionId = div_result[i].attrs['data-sku']
                        except Exception as e:
                            print('[-]',e)
                        try:
                            sold = div_result[i].select('.p-commit a')[0].get_text()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            title = div_result[i].select('.p-name .promo-words')[0].get_text().strip('\n').strip()
                        except Exception as e:
                            print('[-]',e)
                        try:
                            shop_id = div_result[i].select('.p-shopnum')[0].attrs['data-verderid']
                        except:
                            try:
                                shop_id = div_result[i].select('.p-shopnum a')[0].attrs['href']
                                shop_id = re.findall('\d+',shop_id)[0]
                            except:
                                shop_id = '1000117165'
                        try:
                            shop_link = div_result[i].select('.p-shopnum a')[0].attrs['href']
                            if 'https' not in shop_link:
                                shop_link =  'https:' + shop_link
                        except:
                            shop_link = 'https://www.jd.com/allSort.aspx'
                        try:
                            shop_name = div_result[i].select('.hd-shopname')[0].get_text()
                        except:
                            shop_name = '京东自营'
                        
                        shop_address = '京东物流'
                        # print(picUrl,Price,clickUrl,auctionId,sold,title,shop_id,shop_name,shop_address)
                        
                        self.browser.get(clickUrl)
                        can_swipe=random.randint(0,7)
                        if can_swipe%2==0:
                            self.swipe_down(1)

                        goods_html_add_js=self.browser.page_source
                        goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                        try:
                            salePrice = goods_data_soup.select('#page_maprice')[0].get_text()
                            salePrice = re.findall('\d+',salePrice)[0]
                        except Exception as e:
                            print('[-]',e)
                        try:
                            reservePrice = goods_data_soup.select('#jd-price')[0].get_text()
                            reservePrice = re.findall('\d+',reservePrice)[0]
                        except Exception as e:
                            print('[-]',e)
                        try:
                            orderCost = sold
                        except Exception as e:
                            print('[-]',e)
                        try:
                            totalSoldQuantity = sold
                        except Exception as e:
                            print('[-]',e)
                        try:
                            quantity = goods_data_soup.select('#J_stock strong')[0].get_text()
                        except Exception as e:
                            print('[-]',e)

                        #print(id_num,clickUrl,salePrice,reservePrice,orderCost,totalSoldQuantity,quantity)

                        with open(self.Save_Filename+'.csv','a+',encoding='utf-8') as f:
                            f.write(str(id_num)+','+auctionId+','+title+','+Price+','+picUrl+','+clickUrl+','+shortLinkUrl+','+sold+','+shop_id+','+shop_name+','+shop_link+','+shop_address+','+salePrice+','+reservePrice+','+orderCost+','+totalSoldQuantity+','+quantity+'\n')

                        Welcome()
                        print('[+]成功爬取第{0}页第{1}条数据'.format(page_i-1,i+1))

                        if self.Spider_Speed == 'fast':
                            sleep(0)
                        if self.Spider_Speed == 'medium':
                            sleep(2)
                        if self.Spider_Speed == 'slow':
                            sleep(5)
            
                if int(page_i) == int(self.get_page+1):
                    Welcome()
                    print('[+]爬取结束')
                    break
                else:
                    if '&page' not in url_new:
                        url_base = url_new+'&page='
                        url_new=url_new+'&page=2'
                        self.browser.get(url_new)
                    else:
                        url_new=url_base+str(page_i*2)
                        self.browser.get(url_new)
                        # print(url_new)
            
    
        except Exception as e:
            Welcome()
            print('[-]',e)
            self.browser.close()
            print("[-]获取数据失败!")
            exit(0)

    def get_jingdong_goods_page_once(self):
        with open(self.Save_Filename+'.csv','w',encoding='utf-8') as f:
            f.write("ID,商品ID,商品标题,价格,图片URL,商品URL,商品短URL,销量,商店ID,商店名字,商店URL,商店地址,市场价格,促销价格,订单数量,总销售,库存\n")
        
        self.browser.get("https://www.jd.com/")  
        id_num=0
        try:
            #获取输入框焦点
            input_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))
            
            #获取搜索butten焦点
            submit_element = self.wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[4]/div/div[2]/div/div[2]/button')))
            
            #输入关键字及搜索内容
            input_element.send_keys(self.keywords)
            
            #点击搜索
            submit_element.click()
            
            Welcome()
            print('[+]搜索成功~准备爬取~')

            html_add_js = self.browser.page_source

            url_new=self.browser.current_url

            url_new=url_new+'&page='+str(self.Page_Once*2)
            
            self.browser.get(url_new)
            
            html_add_js = self.browser.page_source
            
            #使用BS4进行分析:
            data_soup=BeautifulSoup(html_add_js,'lxml')

            #获取商品简略信息
            div_result=data_soup.select('#J_goodsList li')

            for i in range(0,len(div_result)):
                id_num+=1

                #初始化数据
                salePrice = 'None'
                reservePrice = 'None'
                orderCost = 'None'
                totalSoldQuantity = 'None'
                quantity = 'None'

                #相关数据爬取
                try:
                    clickUrl =  div_result[i].select('.p-img a')[0].attrs['href']
                except Exception as e:
                    print('[-]',e)
                shortLinkUrl =clickUrl
                if 'https' not in clickUrl:
                    clickUrl =  'https:' + clickUrl
                try:
                    picUrl = div_result[i].select('.p-img img')[0].attrs['data-lazy-img']
                    if 'https' not in picUrl:
                        picUrl =  'https:' + picUrl
                except Exception as e:
                    print('[-]',e)
                try:
                    Price = div_result[i].select('.p-price i')[0].string
                except Exception as e:
                    print('[-]',e)
                try:
                    auctionId = div_result[i].attrs['data-sku']
                except Exception as e:
                    print('[-]',e)
                try:
                    sold = div_result[i].select('.p-commit a')[0].get_text()
                except Exception as e:
                    print('[-]',e)
                try:
                    title = div_result[i].select('.p-name .promo-words')[0].get_text().strip('\n').strip()
                except Exception as e:
                    print('[-]',e)
                try:
                    shop_id = div_result[i].select('.p-shopnum')[0].attrs['data-verderid']
                except:
                    try:
                        shop_id = div_result[i].select('.p-shopnum a')[0].attrs['href']
                        shop_id = re.findall('\d+',shop_id)[0]
                    except:
                        shop_id = '1000117165'
                try:
                    shop_link = div_result[i].select('.p-shopnum a')[0].attrs['href']
                    if 'https' not in shop_link:
                        shop_link =  'https:' + shop_link
                except:
                    shop_link = 'https://www.jd.com/allSort.aspx'
                try:
                    shop_name = div_result[i].select('.hd-shopname')[0].get_text()
                except:
                    shop_name = '京东自营'
                
                shop_address = '京东物流'
                # print(picUrl,Price,clickUrl,auctionId,sold,title,shop_id,shop_name,shop_address)
                
                self.browser.get(clickUrl)
                can_swipe=random.randint(0,7)
                if can_swipe%2==0:
                    self.swipe_down(1)

                goods_html_add_js=self.browser.page_source
                goods_data_soup=BeautifulSoup(goods_html_add_js,'lxml')
                try:
                    salePrice = goods_data_soup.select('#page_maprice')[0].get_text()
                    salePrice = re.findall('\d+',salePrice)[0]
                except Exception as e:
                    print('[-]',e)
                try:
                    reservePrice = goods_data_soup.select('#jd-price')[0].get_text()
                    reservePrice = re.findall('\d+',reservePrice)[0]
                except Exception as e:
                    print('[-]',e)
                try:
                    orderCost = sold
                except Exception as e:
                    print('[-]',e)
                try:
                    totalSoldQuantity = sold
                except Exception as e:
                    print('[-]',e)
                try:
                    quantity = goods_data_soup.select('#J_stock strong')[0].get_text()
                except Exception as e:
                    print('[-]',e)

                # #print(id_num,clickUrl,salePrice,reservePrice,orderCost,totalSoldQuantity,quantity)

                with open(self.Save_Filename+'.csv','a+',encoding='utf-8') as f:
                    f.write(str(id_num)+','+auctionId+','+title+','+Price+','+picUrl+','+clickUrl+','+shortLinkUrl+','+sold+','+shop_id+','+shop_name+','+shop_link+','+shop_address+','+salePrice+','+reservePrice+','+orderCost+','+totalSoldQuantity+','+quantity+'\n')

                Welcome()
                print('[+]成功爬取第{0}页第{1}条数据'.format(self.Page_Once,i+1))

                if self.Spider_Speed == 'fast':
                    sleep(0)
                if self.Spider_Speed == 'medium':
                    sleep(2)
                if self.Spider_Speed == 'slow':
                    sleep(5)

            Welcome()
            print('[+]爬取结束')
            
    
        except Exception as e:
            Welcome()
            print('[-]',e)
            self.browser.close()
            print("[-]获取数据失败!")
            exit(0)

def csv2xlsx(filename):
    try:
        import pandas as pd
        import openpyxl
    except:
        os.system('pip3 install pandas')
        os.system('pip3 install openpyxl')
    csv = pd.read_csv(filename+'.csv', encoding='utf-8' , error_bad_lines=False)
    csv.to_excel(filename+'.xlsx', sheet_name='data')
    os.remove(filename +'.csv')

if __name__ == "__main__":
    Welcome()
    parse=optparse.OptionParser(usage='"usage:%prog [options] arg1"',version="%prog 1.0")
    parse.add_option('-u','--username',dest='username',type='str',metavar='用户名',help='请输入微博用户名')
    parse.add_option('-p','--password',dest='password',type='str',metavar='密码',help='请输入微博密码')
    parse.add_option('-k','--keyword',dest='keyword',type='str',metavar='商品名称',help='请输入希望爬取的商品名')
    parse.add_option('-g','--getpage',dest='get_page',type='int',metavar='爬取页数',default=3,help='请输入希望爬取的页数 注意:页数越多爬取时间越长')
    parse.add_option('-s','--Speed',dest='Spider_Speed',type='str',metavar='爬取速度',default='medium',help='fast 快 | medium 中等 | slow 慢')
    parse.add_option('-o',dest='Save_Filename',type='str',metavar='保存文件名称',default='Goods',help='请输入文件名称')
    parse.add_option('--site',dest='site',type='str',metavar='站点名称',default='taobao',help='请输入想要爬取的站点 | taobao 淘宝 | jingdong 京东')
    parse.add_option('-q','--quantity',dest='quantity',type='int',metavar='爬取的商品数量',default=0,help='请输入想要爬取的商品数量 PS：暂时不可用')
    parse.add_option('--page',dest='Page_Once',type='int',metavar='具体某一页',help='请输入想要爬取的具体一页')
    parse.add_option('--attr',dest='attr_file',type='str',metavar='生成文件格式',default='csv',help='请输入生成的文件格式 | csv/xlsx')
    Spider_args,args = parse.parse_args()

    if Spider_args.username is None or Spider_args.password is None or Spider_args.keyword is None :
        if Spider_args.site == 'taobao':
            Welcome()
            print('[-]您的输入有误,请使用命令 --help 或者 -h 获得帮助。')
            exit(0)
        else:
            pass

    spider = Taobao_Commodity_Spider(Spider_args.username,Spider_args.password,Spider_args.keyword,Spider_args.Spider_Speed,Spider_args.Save_Filename,Spider_args.get_page,Spider_args.Page_Once,Spider_args.site)
    if Spider_args.site == 'taobao':
        spider.landing()
    if Spider_args.Page_Once is not None:
        if Spider_args.site == 'taobao':
            spider.get_taobao_goods_page_once()
        if Spider_args.site == 'jingdong':
            spider.get_jingdong_goods_page_once()
    else:
        if Spider_args.site == 'taobao':
            if Spider_args.quantity != 0:
                Spider_args.get_page = int(Spider_args.quantity / 48)
                if Spider_args.quantity % 48 != 0:
                    Spider_args.get_page += 1
            spider.get_taobao_goods_data()

        if Spider_args.site == 'jingdong':
            if Spider_args.quantity != 0:
                Spider_args.get_page = int(Spider_args.quantity / 30)
                if Spider_args.quantity % 30 != 0:
                    Spider_args.get_page += 1
            spider.get_jingdong_goods_data()   
    
    if Spider_args.attr_file == 'xlsx':
        csv2xlsx(Spider_args.Save_Filename)
