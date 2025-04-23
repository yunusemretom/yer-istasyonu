"""
Created by Yunus Emre TOM

"""
from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import messagebox
import time

son_link = ""
original_window =""
browser = ""

def website_start():
    global original_window
    global browser

    browser = webdriver.Firefox()
    browser.get('https://web.whatsapp.com/')

    messagebox.showinfo("Uyarı", "Başlmaya hazır olunca basın")

    original_window = browser.current_window_handle

def konum(link):
    if link != None:
        browser.switch_to.new_window('tab')
        browser.get(link)
        time.sleep(3)
        url = browser.current_url

        # Başlangıç ve bitiş işaretlerini belirle
        start_marker = "/@"
        end_marker = ",17z"

        # İlgili bölgeyi bul
        start_index = url.find(start_marker)
        end_index = url.find(end_marker, start_index)

        # Bölgeyi al
        konum_verisi = url[start_index + len(start_marker):end_index]

        browser.close()
        browser.switch_to.window(original_window)

        return konum_verisi
    else:
        return None
    
def link_bul():
    global son_link

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    linkler = soup.find_all('a')
    linkler_list = []

    for i in linkler:
        
        i = i.get("href")
        try:
            if i[0:24] == "https://maps.google.com/" or i[0:24] == "https://maps.app.goo.gl/":
                linkler_list.append(i)

        except:
            pass
    
    linkler_uzunluk = len(linkler_list)
    try:
        link = linkler_list[linkler_uzunluk-1]
    
        if link != son_link:
            #print(link)
            son_link = link
            return konum(link)
    except:
        return None

def browser_close():
    browser.quit()
"""
Created by Yunus Emre TOM

"""
from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import messagebox
import time

son_link = ""
original_window =""
browser = ""

def website_start():
    global original_window
    global browser

    browser = webdriver.Firefox()
    browser.get('https://web.whatsapp.com/')

    messagebox.showinfo("Uyarı", "Başlmaya hazır olunca basın")

    original_window = browser.current_window_handle

def konum(link):
    if link != None:
        browser.switch_to.new_window('tab')
        browser.get(link)
        time.sleep(3)
        url = browser.current_url

        # Başlangıç ve bitiş işaretlerini belirle
        start_marker = "/@"
        end_marker = ",17z"

        # İlgili bölgeyi bul
        start_index = url.find(start_marker)
        end_index = url.find(end_marker, start_index)

        # Bölgeyi al
        konum_verisi = url[start_index + len(start_marker):end_index]

        browser.close()
        browser.switch_to.window(original_window)

        return konum_verisi
    else:
        return None
    
def link_bul():
    global son_link

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    linkler = soup.find_all('a')
    linkler_list = []

    for i in linkler:
        
        i = i.get("href")
        try:
            if i[0:24] == "https://maps.google.com/" or i[0:24] == "https://maps.app.goo.gl/":
                linkler_list.append(i)

        except:
            pass
    
    linkler_uzunluk = len(linkler_list)
    try:
        link = linkler_list[linkler_uzunluk-1]
    
        if link != son_link:
            #print(link)
            son_link = link
            return konum(link)
    except:
        return None

def browser_close():
    browser.quit()