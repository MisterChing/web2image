#coding:utf-8
import os
import sys
from selenium import webdriver
import time
import signal

def phantomjs_generate_image(url, image_path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    phantomjs_path = os.path.dirname(curdir) + '/bin/phantomjs'
    dr = webdriver.PhantomJS(phantomjs_path)
    dr.set_window_size(1280, 800)
    try:
        dr.implicitly_wait(3)
        dr.set_page_load_timeout(10)
        dr.set_script_timeout(10)
        dr.get(url)
    except Exception as ex:
        print ex
        dr.close()
        dr.service.process.send_signal(signal.SIGTERM)
        dr.quit()
        return False
    js = """
var itv = setInterval(function(){
    var prevScrollHeight = document.body.scrollTop;
    window.scrollTo(0, document.body.scrollTop + 400);
    if(prevScrollHeight == document.body.scrollTop){
        clearInterval(itv);
        var ito = setTimeout(function(){
            document.title += 'scroll_complete';
            clearTimeout(ito);
        }, 1000)
    }
}, 100);
    """
    dr.execute_script(js)
    for i in xrange(30):
        if "scroll_complete" in dr.title:
            break
        time.sleep(1)
    dr.save_screenshot(image_path)
    dr.close()
    dr.service.process.send_signal(signal.SIGTERM)
    dr.quit()
    return True

def chrome_generate_image(url, image_path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.dirname(curdir) + '/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/google/chrome/google-chrome'
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('hide-scrollbars')
    options.add_argument('no-sandbox')
    options.add_argument('window-size=1280,800')
    dr = webdriver.Chrome(chromedriver_path, chrome_options=options)
    dr.get(url)
    js = """
var itv = setInterval(function(){
    var prevScrollHeight = document.body.scrollTop;
    window.scrollTo(0, document.body.scrollTop + 400);
    if(prevScrollHeight == document.body.scrollTop){
        clearInterval(itv);
        var ito = setTimeout(function(){
            document.title += 'scroll_complete';
            clearTimeout(ito);
        }, 1000)
    }
}, 100);
    """
    dr.execute_script(js)
    for i in xrange(30):
        if "scroll_complete" in dr.title:
            break
        time.sleep(10)
    dr.save_screenshot(image_path)
    #  dr.get_screenshot_as_file(image_path)
    dr.close()
    dr.service.process.send_signal(signal.SIGTERM)
    dr.quit()
    return True

