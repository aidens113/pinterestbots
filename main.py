import pyautogui
import time
import math
import random
import os
import sys
import requests
import wmi
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
from os.path import expanduser
import concurrent.futures
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
import concurrent.futures
from datetime import datetime
import time,string,zipfile,os
#import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

amountdelivered = 0
def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def randpresskeys(keys,driver):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','[',']','/','?',',','.']

    for key in keys:
        actions = ActionChains(driver)
        actions.send_keys(key)
        actions.perform()
        #time.sleep(random.uniform(0.05, 0.25))
        #myrand = random.randint(0,25)
        #if myrand >= 22 and str(key) not in "1234567890":
            #press_key(chars[random.randint(0,int(len(chars)-1))],driver)
            #time.sleep(random.uniform(0.1,0.8))
            #press_key(Keys.BACKSPACE,driver)
            #time.sleep(random.uniform(0.3,0.7))

def randkeys(element, keys, driver):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','[',']','/','?',',','.']
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))
        #myrand = random.randint(0,25)
        #if myrand >= 22 and str(key) not in "1234567890":
            #element.send_keys(chars[random.randint(0,int(len(chars)-1))])
            #time.sleep(random.uniform(0.1,0.5))
            #press_key(Keys.BACKSPACE,driver)
            
def drag_and_drop_file(drop_target, path, driver):
    JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
    """
   
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)



def create_proxyauth_extension(proxy_host, proxy_port,proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension

    return str -> plugin_path
    """
    if plugin_path is None:
        file='./chrome_proxy_helper'
        if not os.path.exists(file):
            os.mkdir(file)
        plugin_path = file+'/%s_%s@%s_%s.zip'%(proxy_username,proxy_password,proxy_host,proxy_port)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


        
def initdriver(proxy):
    print(proxy)
    chrome_options = webdriver.ChromeOptions()

    mobilerand = random.randint(0,10)
    useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  ,'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  ,'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36']
    devicemetricslist1 = [640,
                          480,
                          768]
    
    devicemetricslist2 = [1136,
                          800,
                          1024]

    if mobilerand >= 3:
        metric = random.randint(0,int(len(devicemetricslist1)-1))
        mobile_emulation = {
            "deviceMetrics": { "width": devicemetricslist1[metric], "height": devicemetricslist2[metric], "pixelRatio": 3.0 },
        
        "userAgent": useragents[random.randint(0,int(len(useragents)-1))]}
        #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    prefs = {"profile.managed_default_content_settings.images": 2,"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # chrome_options.add_argument('--user-data-dir=C:\\Users\\exoti\\AppData\\Local\\Google\\Chrome\\User Data\\')
    #chrome_options.add_extension('buster.zip')
    #chrome_options.add_argument(str('--profile-directory=Default'))
    #chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument(str('--proxy-server='+str(proxy)))
    #chrome_options.add_argument("--headless")
    #countries = ['IE','US','UK','CA']
    proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host=str(str(proxy.split(":")[0]).strip().replace("\n","").replace("\r","")),  #"51.161.115.64",
    proxy_port=str(str(proxy.split(":")[1]).strip().replace("\n","").replace("\r","")),#80,
    proxy_username="user",#+str(countries[therand])),#str(str(proxy.split(":")[2]).strip().replace("\n","").replace("\r","")),#"country-ca",
    proxy_password='passw',#str(str(proxy.split(":")[3]).strip().replace("\n","").replace("\r","")),
    scheme='http'
    )
    chrome_options.add_extension(proxyauth_plugin_path)
    
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    driver.set_page_load_timeout(90)
    driver.delete_all_cookies()
    #driver.set_window_position(-10000,0)
    return driver




def setreferer(request):
    del request.headers['Referer']
    #sources = ['https://google.com','https://instagram.com','https://facebook.com','https://yahoo.ca','https://bing.com','duckduckgo.com'] 
    
    request.headers['Referer'] = "https://google.com"


def register(driver):

    for _ in range(4):
        try:
            driver.get(urltovisit)
            break
        except Exception as EEEe:
            print("Error getting: "+str(EEEe))

    continuenow = False
    for k in range(60):
        try:
            driver.find_element_by_xpath("//*[text()[contains(.,'Sign up')]]").click()
            if k >= 5:
                driver.refresh()
                time.sleep(9)
                
            continuenow = True
            break
        except Exception as EEEe:
            print("Error: "+str(EEEe))
            time.sleep(1)

    if continuenow == True:
        domains = ['@outlook.com']
        file = open("usernames.txt","r")
        users = file.readlines()
        file.close()
        emailprefix = ""
        for _ in range(random.randint(1,2)):
            emailprefix = str(emailprefix + str(users[random.randint(0,int(len(users)-1))]))
        emailprefix = str(emailprefix+str(random.randint(9,9999)))

        email = str(emailprefix+domains[random.randint(0,int(len(domains)-1))]).replace(":","").replace("-","").replace("$","").replace(",","").replace("\n","").replace("\r","")

        chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','$','!','#','%','&']
        passw = ""
        for _ in range(random.randint(7,15)):
            passw = str(passw + chars[random.randint(0,int(len(chars)-1))]).replace(":","").replace("-","").replace("$","").replace(",","").replace("\n","").replace("\r","")
     
        time.sleep(2)
        randpresskeys(email,driver)
        time.sleep(5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        randpresskeys(passw,driver)
        time.sleep(0.5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        randpresskeys(str(random.randint(19,70)),driver)
        time.sleep(0.5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        press_key(Keys.SPACE,driver)
        time.sleep(0.5)
        press_key(Keys.SPACE,driver)
        time.sleep(0.5)
        time.sleep(10)
        for _ in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Your email is invalid.')]]").text
                return False
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Sign up')]]").text
                return False
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Next')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)



        for k in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Next')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                if k >= 10:
                    try:
                        driver.refresh()
                        time.sleep(9)
                    except:
                        time.sleep(0.01)
                time.sleep(1)


        time.sleep(5)

        for _ in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Male')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)

        time.sleep(5)
        
        for _ in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Next')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)

        time.sleep(5)
        
        
        for num in range(1,7):
            for _ in range(20):
                try:
                    driver.find_element_by_xpath(str("/html/body/div[2]/div/div/div/div[2]/div/div/div/div[3]/div/div[3]/div/div["+str(num)+"]")).click()
                    break                                         
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)
                try:
                    driver.find_element_by_xpath(str("/html/body/div[2]/div/div/div[3]/div/div[3]/div/div["+str(num)+"]")).click()
                    break                                                                     
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)
                try:
                    driver.find_element_by_xpath(str("/html/body/div[3]/div/div/div[3]/div/div[3]/div/div["+str(num)+"]")).click()
                    break                                                          
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)

        time.sleep(5)

        for _ in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Done')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)

        time.sleep(5)

        for _ in range(20):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Done')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
        time.sleep(25)
        file = open("myaccounts.txt","a")
        file.write(email+":"+passw+"\n")
        file.close()
        return True
    else:
        return False


def login(email,passw,driver):
    try:
        for _ in range(4):
            try:
                driver.get(urltovisit)
                break
            except Exception as EEee:
                print("Error: "+str(EEee))

        continuenow = False
        for k in range(60):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Log in')]]").click()
                continuenow = True
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                if k >= 5:
                    driver.refresh()
                    time.sleep(9)
                    
                time.sleep(1)
        if continuenow == True:
            randpresskeys(email,driver)
            time.sleep(5)
            press_key(Keys.TAB,driver)
            time.sleep(0.5)
            randpresskeys(passw,driver)
            time.sleep(0.5)
            press_key(Keys.TAB,driver)
            time.sleep(0.5)
            press_key(Keys.TAB,driver)
            time.sleep(0.5)
            press_key(Keys.SPACE,driver)
            time.sleep(0.5)
            press_key(Keys.SPACE,driver)
            time.sleep(30)
            onloginscreen = True
            for _ in range(10):
                try:
                    
                    driver.find_element_by_xpath("//*[text()[contains(.,'Log in')]]").text
                    
                    try:
                        driver.find_element_by_xpath("//*[text()[contains(.,'Welcome to Pinterest')]]").text
                    except:
                        print("No longer on login screen")
                        onloginscreen = False
                    if onloginscreen == False:  
                        return False
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)

                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'We protected your account')]]").text
                    return False
                except Exception as EEeeee:
                    print("Error: "+str(EEeeee))
                    


            return True
    except Exception as EEEE:
        print("Error logging in: "+str(EEEE))

def spamforums(driver):
    try:
        #GET LINKS
        for _ in range(4):
            try:
                for _ in range(4):
                    try:
                        driver.get("https://pinterest.com/homefeed")
                        break
                    except Exception as EEee:
                        print("Er: "+str(EEee))
                for _ in range(5):
                    press_key(Keys.PAGE_DOWN, driver)
                    time.sleep(0.2)
                    elements = driver.find_elements_by_tag_name('a')
                    thelinks = []
                    for element in elements:
                        if "/pin/" in str(element.get_attribute('href')):
                            thelinks.append(str(element.get_attribute('href')))

                newlist = []
                for link in thelinks:
                    if link not in newlist:
                        newlist.append(link)
    
                print(len(newlist))
                if len(newlist) >= 5:
                    #file = open("thelinks.txt","a")
                    #for link in newlist:
                    #    file.write(str(link+"\n"))
                    #file.close()
                    break
            
            except Exception as EEeee:
                print("ER: "+str(EEeee))
        #PROCESS LINKS
        for link in thelinks:
            for _ in range(4):
                try:
                    driver.get(link)
                    break
                except Exception as EEee:
                    print("ER: "+str(EEee))
            press_key(Keys.PAGE_DOWN, driver)
            time.sleep(1)
            #press_key(Keys.PAGE_DOWN, driver)
            #time.sleep(2)
            for _ in range(20):
                try:
                    elements = driver.find_elements_by_tag_name('textarea')
                    for element in elements:
                        try:
                            if "Add a comment" in str(element.get_attribute('placeholder')):
                                element.click()
                                time.sleep(15)
                                file = open("script2.txt","r")
                                script = file.read()
                                file.close()
                                randpresskeys(script,driver)
                                break
                        except Exception as EEeee:
                            print("Error clicking COMMENTBAR: "+str(EEeee))
                            press_key(Keys.PAGE_DOWN, driver)
                    time.sleep(1)
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)
            time.sleep(2)
            for _ in range(20):
                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'Done')]]").click()
                    time.sleep(15)
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)     
            
            
    except Exception as EEEE:
        print("Error with spamloop: "+str(EEEE))
    time.sleep(30)

def commenthype(driver): 
    try:
        file = open("pinstocomment.txt","r")
        postlinks = file.readlines()
        file.close()
        for postlink in postlinks:
            for _ in range(4):
                try:
                    driver.get(postlink)
                    break
                except Exception as EEee:
                    print("ER: "+str(EEee))
            press_key(Keys.PAGE_DOWN, driver)
            time.sleep(1)
            #press_key(Keys.PAGE_DOWN, driver)
            #time.sleep(2)
            for _ in range(20):
                try:
                    elements = driver.find_elements_by_tag_name('textarea')
                    for element in elements:
                        try:
                            if "Add a comment" in str(element.get_attribute('placeholder')):
                                element.click()
                                time.sleep(15)
                                file = open("hype.txt","r")
                                comments = file.readlines()
                                file.close()                            
                                randpresskeys(comments[random.randint(0,int(len(comments)-1))],driver)
                                break
                        except Exception as EEeee:
                            print("Error clicking COMMENTBAR: "+str(EEeee))
                            press_key(Keys.PAGE_DOWN, driver)
                    time.sleep(1)
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)
            time.sleep(2)
            for _ in range(20):
                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'Done')]]").click()
                    time.sleep(15)
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)     

            
                
    except Exception as EEEEE:
        print("Err: "+str(EEEEE))

def follow(driver):
    try:
        for _ in range(4):
            try:
                driver.get(followlink)
                break
            except Exception as Eee:
                print("Error: "+str(Eee))


        for k in range(10):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Follow')]]").click()
                break
            except Exception as EEe:
                if k  >= 16:
                    driver.refresh()
                print("Error: "+str(EEe))
                time.sleep(1)
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Log in')]]").text
                return False
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
        time.sleep(10)
                
    except Exception as EEee:
        print("Error: "+str(EEee))


#***********************************************
#   MESSAGING API FUNCTIONS BEGIN HERE
#***********************************************


def makegetrequest(url,headers,data=None,json=None):     
    #fakeip = str("1"+str(random.randint(10,99))+".1"+str(random.randint(10,99))+"."+str(random.randint(1,9))+"."+str(random.randint(10,99)))
    #print(fakeip)

    proxy  = {"http" : "http://proxyhere",
                  "https" : "http://proxyhere"}

    response = requests.get(str(url), headers=headers,proxies=proxy,data=data,json=json)
    return response


def makepostrequest(url,headers,data=None,json=None):     
    #fakeip = str("1"+str(random.randint(10,99))+".1"+str(random.randint(10,99))+"."+str(random.randint(1,9))+"."+str(random.randint(10,99)))
    #print(fakeip)

    proxy  = {"http" : "http://proxyhere",
                  "https" : "http://proxyhere"}

    response = requests.post(str(url), headers=headers,proxies=proxy,data=data,json=json)
    return response

def getuserID(username,thecookie,useragent,myID):
    url = str("https://www.pinterest.ca/resource/UserResource/get/?source_url=%2F&data=%7B%22options%22%3A%7B%22username%22%3A%22"+str(username)+"%22%2C%22field_set_key%22%3A%22profile%22%2C%22no_fetch_context_on_resource%22%3Afalse%7D%2C%22context%22%3A%7B%7D%7D&_="+str(myID))
    for _ in range(5):
        try:
            headers = {
            "host":"www.pinterest.ca",
            "user-agent": useragent ,
            'accept':'application/json, text/javascript, */*, q=0.01',
            'accept-language':'en-US,en;q=0.5',
            'accept-encoding':'gzip, deflate, br',
            'referer':'https://www.pinterest.ca/',
            'x-requested-with':'XMLHttpRequest',
            'x-app-version':'01cb108',
            'x-pinterest-appstate':'active',
            'x-pinterest-source-url':str('/'+str(username)+'/_saved/'),
            'x-pinterest-pws-handler':'www/[username]/_saved.js',
            'te':'trailers',
            'cookie':thecookie
            }
            response = makegetrequest(url,headers)
            #print(response.text)
            try:
                return str(str(response.text).split('"profile_cover":{"id":"')[1].split('"')[0])
            except:
                return str(str(response.text).split(',"id":"')[1].split('"')[0])
        except Exception as EEeee:
            print("ER: "+str(EEeee))

def sendDM(username,thecookie,useragent,myuserid):
    global amountdelivered
    for _ in range(5):
        try:
            ID = getuserID(username,thecookie,useragent,myuserid)
            print(ID)
            url = "https://www.pinterest.ca/resource/ConversationsResource/create/"
            headers = {
            "user-agent": useragent ,
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'accept':'application/json, text/javascript, */*, q=0.01',
            'accept-language':'en-US,en;q=0.5',
            'accept-encoding':'gzip, deflate, br',
            'referer':'https://www.pinterest.ca/',
            'x-requested-with':	'XMLHttpRequest',
            'x-app-version':'01cb108',
            'content-type': 'application/x-www-form-urlencoded',
            'x-csrftoken':str(thecookie.split("csrftoken=")[1].split(";")[0]),
            'x-pinterest-appstate':'active',
            'x-pinterest-source-url':'/livigstonbarry/_saved/',
            'x-pinterest-pws-handler':'www/[username]/_saved.js',
            'content-length':'264',
            'origin':'https://www.pinterest.ca',
            'te':'trailers',
            'cookie':thecookie
            }
            data = str("source_url=%2Flivigstonbarry%2F_saved%2F&data=%7B%22options%22%3A%7B%22user_ids%22%3A%5B%22"+str(ID)+"%22%5D%2C%22emails%22%3A%5B%5D%2C%22text%22%3A%22This is crazy! @Giftedgiveaway is giving away free Iphones from sponsors. You should check it out!%22%2C%22pin%22%3A%221112178070449011536%22%2C%22no_fetch_context_on_resource%22%3Afalse%7D%2C%22context%22%3A%7B%7D%7D")
            response = makepostrequest(url,headers,data)
            print(response.text)
            amountdelivered += 1
            return
        except Exception as EEeee:
            print("ER: "+str(EEeee))

def thedmloop(accs,cookie):
    file = open("useragents.txt","r")
    useragents = file.readlines()
    file.close()
    useragent = str(useragents[random.randint(0,int(len(useragents)-1))]).strip().replace("\n","").replace("\r","")
    
    for acc in accs:
        print(str(acc))
        sendDM(acc.strip().replace("\n","").replace("\r",""),cookie,useragent,"1635300375869")
                                                                               

        
def updatethread():
    global amountdelivered
    while True:
        print("PINTEREST REQUESTS DM BOT V.1")
        print(str("Traffic Delivered: "+str(amountdelivered)))
        time.sleep(1)
        os.system('cls')


def getcookies(driver):
    for _ in range(5):
        try:
            cookiestr = ""
            for cookie in driver.get_cookies():
                cookiestr = str(cookiestr+str(str(cookie['name'])+"="+str(cookie['value'])+";").replace("\n","").replace("\r",""))
            file = open("cookies.txt","a")
            file.write(str(cookiestr+"\n"))
            file.close()
            return
        except Exception as EEEEE:
            print("Big error getting cookies: "+str(EEEEE))
        


#***********************************************
#   MESSAGING API FUNCTIONS END HERE
#***********************************************


def olddm(driver,user):
    try:
        for _ in range(4):
            try:
                driver.get(postlink)
                break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)



        breakl = False
        for _ in range(20):
            try:
                elements = driver.find_elements_by_tag_name('button')
                for element in elements:
                    if "Messages" in str(element.get_attribute('aria-label')):
                        element.click()
                        breakl = True
                        break
                if breakl == True:
                    break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        
        breakl = False
        for _ in range(20):
            try:
                elements = driver.find_elements_by_tag_name('input')
                for element in elements:
                    if "Search by name or email" in str(element.get_attribute('placeholder')):
                        element.click()
                        breakl = True
                        break
                if breakl == True:
                    break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        time.sleep(6)

        randpresskeys(user.strip().replace("\n","").replace("\r",""),driver)
        press_key(Keys.ENTER,driver)
        time.sleep(5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        press_key(Keys.SPACE,driver)


        file = open("dm.txt","r")
        themsg = file.read()
        file.close()

        for _ in range(20):
            try:
                driver.find_element_by_id('messageDraft').send_keys(themsg)
                break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        for _ in range(20):
            try:
                elements = driver.find_elements_by_tag_name('button')
                for element in elements:
                    if "Send message to conversation" in str(element.get_attribute('aria-label')):
                        element.click()
                        break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)
        time.sleep(5) 
    except Exception as EEEEE:
        print("ERror: "+str(EEEEE))


def sendpost(driver,user):
    try:
        for _ in range(4):
            try:
                driver.get(postlink)
                break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        time.sleep(5)

        breakl = False
        for _ in range(20):
            try:
                elements = driver.find_elements_by_tag_name('button')
                for element in elements:
                    if "Send" in str(element.get_attribute('aria-label')):
                        element.click()
                        breakl = True
                        break
                if breakl == True:
                    break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)


        breakl = False
        for _ in range(20):
            try:
                elements = driver.find_elements_by_tag_name('input')
                for element in elements:
                    if "Search for a name or email" in str(element.get_attribute('aria-label')):
                        element.send_keys(user.strip())
                        breakl = True
                        break
                if breakl == True:
                    break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        time.sleep(1)
        press_key(Keys.ENTER,driver)
        time.sleep(20)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        press_key(Keys.TAB,driver)
        time.sleep(0.5)
        press_key(Keys.SPACE,driver)
        time.sleep(3)
                
        for _ in range(10):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Send')]]").click()
                break
            except Exception as EEe:
                print("Error: "+str(EEe))

        for _ in range(5):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'strange activity on your account')]]").text
                return False
                break
            except Exception as EEee:
                print("Er: "+str(EEee))

            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Log in')]]").text
                return False
                break
            except Exception as EEee:
                print("Er: "+str(EEee))
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'hit a block (message requests) we have in')]]").text
                return False
                break
            except Exception as EEee:
                print("Er: "+str(EEee))
                time.sleep(1)
                
        time.sleep(10)
    except Exception as EEeee:
        print("Error: "+str(EEeee))



def dmloop(driver,myusername):
    try:
        usernames = collectusernames(driver,myusername,2)
        
        cookiestr = ""
        for cookie in driver.get_cookies():
            cookiestr = str(cookiestr+str(str(cookie['name'])+"="+str(cookie['value'])+";"))            
        
        thedmloop(usernames,cookiestr)
        #file = open("useragents.txt","r")
        #useragents = file.readlines()
        #file.close()
        #useragent = str(useragents[random.randint(0,int(len(useragents)-1))]).strip().replace("\n","").replace("\r","")
        #sendDM("Giftedgiveaway",cookiestr,useragent,"1635300375869")
                                                                                   

    except Exception as EEEE:
        print("Error: "+str(EEEE))
    


def collectusernames(driver,myusername,usernamestoget):
    #GET LINKS
    usernames = []
    while True:
        for _ in range(4):
            try:
                for _ in range(4):
                    try:
                        driver.get("https://pinterest.com/homefeed")
                        break
                    except Exception as EEee:
                        print("Er: "+str(EEee))
                for _ in range(3):
                    press_key(Keys.PAGE_DOWN, driver)
                    time.sleep(0.2)
                    elements = driver.find_elements_by_tag_name('a')
                    thelinks = []
                    for element in elements:
                        if "/pin/" in str(element.get_attribute('href')):
                            thelinks.append(str(element.get_attribute('href')))

                newlist = []
                for link in thelinks:
                    if link not in newlist:
                        newlist.append(link)
    
                print(len(newlist))
                if len(newlist) >= 5:
                    file = open("thelinks.txt","a")
                    for link in newlist:
                        file.write(str(link+"\n"))
                    file.close()
                    break
            
            except Exception as EEeee:
                print("ER: "+str(EEeee))

        for _ in range(3):
            for link in thelinks:
                for _ in range(4):
                    try:
                        driver.get(link)
                        break
                    except Exception as EEee:
                        print("ER: "+str(EEee))


                press_key(Keys.PAGE_DOWN, driver)
                time.sleep(0.2)


                thelink = "None"
                breakl = False
                for _ in range(20):
                    try:
                        elements = driver.find_elements_by_tag_name('a')
                        for element in elements:
                            if "Wk9 xQ4 CCY czT eEj kVc uCz" in str(element.get_attribute('class')) and myusername.strip() not in str(element.get_attribute('href')).split("/")[3] and "pin" not in str(element.get_attribute('href')).split("/")[3] and len(str(element.get_attribute('href')).split("/")[3]) >= 3:
                                thelink = str(element.get_attribute('href'))
                                breakl = True
                                break
                    except Exception as EEee:
                        print("Error: "+str(EEee))
                        time.sleep(1)
                if breakl == True:
                    break
                    
            if thelink != "None":
                for _ in range(4):
                    try:
                        driver.get(thelink)
                        break
                    except Exception as EEeee:
                        print("Err: "+str(EEeee))
            
            breakl = False
            for k in range(10):
                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'followers')]]").click()
                    breakl = True
                    break
                except Exception as EEe:
                    if k  >= 16:
                        driver.refresh()
                    print("Error: "+str(EEe))
                    time.sleep(3)
            if breakl == True:
                break
        
        for _ in range(10):
            try:
                elements = driver.find_elements_by_tag_name('a')
                for element in elements:
                    if len(usernames) >= usernamestoget:
                        return usernames
                    if "Wk9 xQ4 CCY czT eEj kVc FTD L4E DI9 BG7" in str(element.get_attribute('class')) and myusername.strip() not in str(element.get_attribute('href')).split("/")[3] and "pin" not in str(element.get_attribute('href')).split("/")[3] and len(str(element.get_attribute('href')).split("/")[3]) >= 3:
                        username = str(str(element.get_attribute('href')).split("/")[3])
                        if username not in str(usernames):
                            usernames.append(username)
                break
            except Exception as EEee:
                print("Err: "+str(EEee))
                time.sleep(1)        

def senddmwithcookies(threadnum):
    threadnum += 1
    global urltovisit
    file = open("myaccounts.txt","r")
    accs = file.readlines()
    file.close()
    thei = 0
    loggedin = False
    while True:
        try:
            driver = initdriver("proxyhere")    
                    
            acc = accs[int(thei * threadnum)]
            thei += 1
            email = acc.split(":")[0].strip().replace("\n","").replace("\r","")
            passw = acc.split(":")[1].strip().replace("\n","").replace("\r","")
            if login(email,passw,driver) == True:  
                usernames = collectusernames(driver,email.split("@")[0],100)
                print(usernames)
                loggedin = True
            try:
                driver.close()
                driver.quit()
            except:
                print("Er closing driver")
            if loggedin == True:
                break
                
        except Exception as EEee:
            print("Error: "+str(EEee))
            try:
                driver.close()
                driver.quit()
            except:
                print("Er closing driver")

    while True:
        try:
            #register(driver)
            file = open("cookies.txt","r")
            thecookies = file.read()
            file.close()
            cookies = thecookies.split("END")
            thei = 1
            myii = 0
            accstomessage = 2
            while True:
                cookiestr = cookies[int(thei * threadnum)]
                file = open("useragents.txt","r")
                useragents = file.readlines()
                file.close()
                useragent = str(useragents[random.randint(0,int(len(useragents)-1))]).strip().replace("\n","").replace("\r","")
                
                try:
                    for _ in range(accstomessage):
                        myii += 1
                        usernametosend = usernames[myii]
                        sendDM(usernametosend,cookiestr,useragent,"1635300375869")
                except Exception as EEeee:
                    print("ERR: "+str(EEeee)) 
                thei += 1
                    
        except Exception as EEEEE:
            print("Big error: "+str(EEEEE))
    

def makepin(driver,fileindex):
    try:

        file = open("posts/poststructure.txt","r")
        thedata = file.readlines()
        file.close()

        mydata = thedata[fileindex].split(";")
        thetitle = mydata[0]
        description = mydata[1]
        thelink = mydata[2]
        imgpath = str(str(os.getcwd())+"\\posts\\"+str(fileindex)+".jpg")

        driver.refresh()
        time.sleep(1)
        
        for _ in range(4):
            try:
                driver.get(str(str(driver.current_url)+"pin-builder/"))
                break
            except Exception as EEeee:
                print("ER: "+str(EEeee))

        breakl = False
        for thei in range(10):
            try:
                elements = driver.find_elements_by_tag_name('textarea')
                for element in elements:
                    if "Add your title" in str(element.get_attribute('placeholder')):
                        randkeys(element,thetitle,driver)
                        breakl = True
                        break
                if thei >= 5:
                    driver.refresh()
                    time.sleep(10)
                if breakl == True:
                    break
                time.sleep(1)
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)

        for _ in range(5):
            try:
                randkeys(driver.find_element_by_class_name("DraftEditor-editorContainer"),description,driver)
                break
            except Exception as EEee:
                print("Er: "+str(EEee))
                time.sleep(1)

        breakl = False
        for _ in range(10):
            try:
                elements = driver.find_elements_by_tag_name('textarea')
                for element in elements:
                    if "Add a destination link" in str(element.get_attribute('placeholder')):
                        randkeys(element,thelink,driver)
                        breakl = True
                        break
                if breakl == True:
                    break
                time.sleep(1)
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)


        
                        
        driver.find_element_by_xpath("//input[@type='file']").send_keys(str(imgpath))
                        
            

        time.sleep(10)
     
    except Exception as EEEEE:
        print("ER: "+str(EEEEE))


def repin(driver,thelink):
    try:
        for _ in range(4):
            try:
                driver.get(thelink)
                break
            except Exception as EEee:
                print("ER: "+str(EEee))

        time.sleep(5) 

        for k in range(10):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Save')]]").click()
                breakl = True
                break
            except Exception as EEe:
                try:
                    driver.execute_script('document.getElementsByClassName("MIw zI7 iyn Hsu")[0].remove()')
                except:
                    print("ER")
                if k  >= 16:
                    driver.refresh()
                print("Error: "+str(EEe))
                time.sleep(3)

        time.sleep(10)
        if breakl == True:
            return
    except Exception as EEEEE:
        print("ERR: "+str(EEEEE))


def randomrepin(driver,pins):
    global postlink
    pinsdone = 0
    while True:
        try:
            try:
                for _ in range(4):
                    try:
                        driver.get("https://pinterest.com/homefeed")
                        break
                    except Exception as EEee:
                        print("Er: "+str(EEee))
                for _ in range(3):
                    press_key(Keys.PAGE_DOWN, driver)
                    time.sleep(0.2)
                    elements = driver.find_elements_by_tag_name('a')
                    thelinks = []
                    for element in elements:
                        if "/pin/" in str(element.get_attribute('href')):
                            thelinks.append(str(element.get_attribute('href')))

                newlist = []
                for link in thelinks:
                    if link not in newlist:
                        newlist.append(link)
            
            except Exception as EEeee:
                print("ER: "+str(EEeee))

            for link in thelinks:
                pinsdone += 1
                repin(driver,link)
                if pinsdone >= pins:
                    repin(driver,postlink)
                    return
            
        except Exception as EEEEE:
            print("ERR: "+str(EEEEE))
    
def spam(proxy,threadnum):
    threadnum += 1
    global urltovisit
    while True:
        try:
            #register(driver)
            file = open("myaccounts.txt","r")
            accs = file.readlines()
            file.close()
            thei = 1
            while True:
                try:
                    driver = initdriver(proxy)    
                    
                    acc = accs[int(thei * threadnum)]
                    thei += 1
                    email = acc.split(":")[0].strip().replace("\n","").replace("\r","")
                    passw = acc.split(":")[1].strip().replace("\n","").replace("\r","")
                    if login(email,passw,driver) == True:
                        print("Success account")
                    
                        #commenthype(driver)
                        #follow(driver)
                        #spamforums(driver)
                        randomrepin(driver,5)
                        #if dmloop(driver,email.split("@")[0]) == False:
                        #    try:
                        #        driver.close()
                        #        driver.quit()
                        #    except:
                        #        print("Error closing driver")
                        #    break
                        #try:
                        #    driver.get("https://pinterest.com")
                        #except:
                        #    print("ER")
                        #getcookies(driver)
                        time.sleep(2)
                    else:
                        print("Failed account")
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        print("Error closing driver")
                except Exception as EEeee:
                    print("Error, breaking loop: "+str(EEeee))
                    break
            
            #time.sleep(random.uniform(7.000, 18.000))        
        except Exception as EEE:
            print("Error: "+str(EEE))
            try:
                driver.close()
                driver.quit()
            except:
                print("Error closing driver")
def startthreads(threadnum):
    
    threads = []
    file = open("proxies.txt","r")
    proxies = file.readlines()
    file.close()
    #target=spam, args=("megaproxy.rotating.proxyrack.net:222",i,)
    #target=senddmwithcookies,args=[i]
    for i in range(threadnum):
        Thread = threading.Thread(target=spam, args=(postlink,i,))    
        threads.append(Thread)
    for thread in threads:
        thread.start()
        time.sleep(random.uniform(0.9, 2.0))
    for thread in threads:
        thread.join()

    
print("""
WELCOME TO PINTEREST FORUM COMMENTS V.1
POST TO PINTEREST.COM WITH LINKS
-
""")
urltovisit = "https://pinterest.com"
followlink = ""
postlink = ""
threadstodo = int(input("Threads: "))
startthreads(threadstodo)

#driver = initdriver(")
#time.sleep(60)
#spamforums(driver)
