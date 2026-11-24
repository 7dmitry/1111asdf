import os
import telebot
from telebot import TeleBot, types
from bs4 import BeautifulSoup
import requests
from PIL import Image
import time
import random
import sqlite3
import traceback
import bs4
from zipfile import ZipFile
from datetime import datetime, timedelta
import json

FILE_NAME = 'stat.json'
def load_data():
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        return json.load(f)
data = load_data()
def save_data(data):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def toggle_value(index):
    data = load_data()
    values = data['values']
    if index < 0 or index >= len(values):
        raise IndexError('Неверный индекс')
    # переключение 0 ↔ 1
    values[index] = 1 if values[index] == 0 else 0
    save_data(data)
    return values

time_new = datetime.now().strftime('%H:%M:%S') + " - "
print(time_new, '---///Запуск бота///---')

token = os.getenv("BOT_TOKEN2")
bot = telebot.TeleBot(token)

con = sqlite3.connect('modtitle.db')
cur = con.cursor()
# ➭
icon = '🌾'
icon_ivent = '☑️'
icon2 = '🌱'
icon2_ivent = '🍀'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
           'Upgrade-Insecure-Requests': '1'}

def check():
    time_new = datetime.now().strftime('%H:%M:%S') + " - "
    title_db = cur.execute("SELECT title_1,title_2,title_3,title_4,title_5,title_6,title_7 FROM TITLE") 
    title_db = cur.fetchone()
    print(time_new, 'БД подключена')
    
    random_check = random.randint(1, 5000)
    all_title = []
    url_title_pc = ['https://ru-minecraft.ru/mody-minecraft/',
                    'https://ru-minecraft.ru/mody-minecraft/shaders/',
                    'https://ru-minecraft.ru/karty-dlja-minecraft/']
    
    url_title_pe = ['https://mcpehub.org/mods/',
                    'https://mcpehub.org/shaders/',
                    'https://mcpehub.org/textures/',
                    'https://mcpehub.org/maps/']
    time_new = datetime.now().strftime('%H:%M:%S') + " - "
    print(time_new, 'Загрузка названий ПК...')
    for URL in url_title_pc:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser") 
        random_time()
        title = soup.find("h2", class_="news__title").find('a').getText() 
        all_title.append(title)
        time_new = datetime.now().strftime('%H:%M:%S') + " - "
        print(time_new, URL)
        
        
    print(time_new, 'Загрузка названий ПЕ...', )    
    for URL in url_title_pe:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser") 
        random_time()
        title = soup.find("h2", class_="black medium").getText()
        all_title.append(title)
        time_new = datetime.now().strftime('%H:%M:%S') + " - "
        print(time_new, URL)
    time_new = datetime.now().strftime('%H:%M:%S') + " - "  
       
    if title_db[0] != all_title[0]:
        pc('https://ru-minecraft.ru/mody-minecraft/')
        print(time_new, '✅ https://ru-minecraft.ru/mody-minecraft/')
    if title_db[1] != all_title[1]:
        pc('https://ru-minecraft.ru/mody-minecraft/shaders/')
        print(time_new, '✅ https://ru-minecraft.ru/mody-minecraft/shaders/')
    if title_db[2] != all_title[2]:
        pc('https://ru-minecraft.ru/karty-dlja-minecraft/')
        print(time_new, '✅ https://ru-minecraft.ru/karty-dlja-minecraft/')
    if title_db[3] != all_title[3]:
        pe('https://mcpehub.org/mods/')
        print(time_new, '✅ https://mcpehub.org/mods/')
    if title_db[4] != all_title[4]:
        pe('https://mcpehub.org/shaders/')
        print(time_new, '✅ https://mcpehub.org/shaders/')
    if title_db[5] != all_title[5]:
        pe('https://mcpehub.org/textures/')
        print(time_new, '✅ https://mcpehub.org/textures/')
    if title_db[6] != all_title[6]:
        pe('https://mcpehub.org/maps/') 
        print(time_new, '✅ https://mcpehub.org/maps/') 
         
    cur.execute("UPDATE TITLE SET (title_1,title_2,title_3,title_4,title_5,title_6,title_7) = (?,?,?,?,?,?,?)",all_title) 
    con.commit()
    time_new = datetime.now().strftime('%H:%M:%S') + "- "
    print(time_new, 'БД обновлена') 
    print(time_new, '🚩 Публикация завершена') 
    random_time2()
    check()
    
    
def random_time():
    rnumber = random.uniform(0.1, 10.9)
    time_new = datetime.now().strftime('%H:%M:%S') + "- "
    print(f"{time_new}⏳Ожидание: {rnumber:.2f} секунд")
    time.sleep(rnumber)  

def random_time2():
    rnumber = random.uniform(66000.1, 72000.9)
    time_new = datetime.now().strftime('%H:%M:%S') + "- "
    print(f"{time_new}⏳Ожидание следующей проверки: {rnumber:.2f} секунд")
    time.sleep(rnumber)  
    
def pe(URL):
    try:
        time_new = datetime.now().strftime('%H:%M:%S') + "- "
        print(time_new, '☑️Парсинг страницы:', URL)
        random_time()
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser") 
        title = soup.find("h2", class_="black medium").getText() 
        post_about = (soup.find("p", class_="black regular").getText()).replace('....', '')
        URLPOST = soup.find("article", class_="col-xs-12 col-sm-4 col-md-6").find('a').get('href')
        random_time()
        page2 = requests.get(URLPOST, headers=headers)
        soup2 = BeautifulSoup(page2.content, "html.parser")
        img_tag = soup2.find("div", class_="fullstory-content regular black").find('img')
        img = 	'https://mcpehub.org'  + (img_tag.get('src') if img_tag else None)
        try:
            versions = soup2.find("div", class_="block-list medium green").find_all('p')
            version_post = [p.getText() for p in versions]
        except:
            version_post = ['0']
        time_new = datetime.now().strftime('%H:%M:%S') + "- "
        print(time_new, '🎯Успешный парсинг страницы:', URL)
        version_teg_post = []
        for version in version_post:
            v = '#м' + (version[:4]).replace('.', '')
            if (v in version_teg_post) == False:
                version_teg_post.append(v)  
        version_post = ', '.join(version_post)
        version_teg_post = ', '.join(version_teg_post)
        
        if URL == 'https://mcpehub.org/mods/':
            if data['values'][3] == 0:
                post_device = f'📱Устройство телефон(мод)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{post_about}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}' 
            if data['values'][3] == 1:
                post_device = f'{icon2}мод для майнкрафт пе'
                channel_url = '@minemob1'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по модам{icon2_ivent}](https://t.me/minemob1)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title}\n\n{post_about}\n\n Теги: {version_teg_post}\n{post_channel}'
            toggle_value(3)    
        if URL == 'https://mcpehub.org/shaders/':
            if data['values'][4] == 0:
                post_device = f'📱Устройство телефон(шейдер)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{post_about}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}'
            if data['values'][4] == 1:
                post_device = f'{icon2}шейдер для майнкрафт пе'
                channel_url = '@shaders1'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по шейдерам{icon2_ivent}](https://t.me/shaders1)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title}\n{post_about}\n\n Теги: {version_teg_post}\n{post_channel}'
            toggle_value(4)    
               
            
        if URL == 'https://mcpehub.org/textures/':  
            if data['values'][5] == 0:
                post_device = f'📱Устройство телефон(текстурпак)' 
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{post_about}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}'
            if data['values'][5] == 1:
                post_device = f'{icon2}текстурпак для майнкрафт пе'
                channel_url = '@shaders1'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по шейдерам{icon2_ivent}](https://t.me/shaders1)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title}\n{post_about}\n\n Теги: {version_teg_post}\n{post_channel}'
            toggle_value(5)
        if URL == 'https://mcpehub.org/maps/':
            if data['values'][6] == 0:
                post_device = f'📱Устройство телефон(карта)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{post_about}\n \n{post_device}\n \n{post_channel}'
            if data['values'][6] == 1:
                post_device = f'{icon2}карта для майнкрафт пе'
                channel_url = '@minemob2'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по картам{icon2_ivent}](https://t.me/minemob2)'
                post_text = f'{post_device}\n{icon2}{title}\n{post_about}\n \n{post_channel}'
            toggle_value(6)    
        print(time_new, f'Канал {channel_url}, {post_device}')
        markup = types.InlineKeyboardMarkup()
        btn_downl = types.InlineKeyboardButton(text="✔️Подробнее", url = URLPOST)
        markup.add(btn_downl)
        bot.send_photo(channel_url, (img), (post_text), reply_markup = markup,parse_mode='Markdown') 
        allfilesname = soup2.find('div', class_='item-content').find_all('span', class_='black medium') 
        allfilesurl_new = soup2.find("div", class_="item-content").find_all('a', class_="flex middle center green-bg medium white")
        allfilesurl = [a.get('href') for a in soup2.find("div", class_="item-content").find_all('a', class_="flex middle center green-bg medium white")]
        allfilesname = [span.getText() for span in allfilesname]
        filterwords =['(', ')', 'Скачать']
        i = 0
        while (len(allfilesname) > i):
            for char in filterwords:
                allfilesname[i] = allfilesname[i].replace(char, '')
            i += 1
        for urlinlist in allfilesurl:
            urlinlist = urlinlist.replace("dlfile", "getfile")
            
        i = 0           
        while (len(allfilesurl) > i):
            response = requests.get(url=allfilesurl[i], headers=headers)
            with open(f"{allfilesname[i]}", 'wb') as file:
                    file.write(response.content)
            bot.send_document(channel_url, open(f"{allfilesname[i]}", 'rb'))
            time.sleep(20)
            os.remove(f"{allfilesname[i]}") 
            i += 1
                   
    except Exception as e:
        time_new = datetime.now().strftime('%H:%M:%S') + "- "
        print(time_new, '❗️Ошибка при парсинге страницы❗️:', URL)
        print(traceback.format_exc())
        print(time_new, '⬆️🔴Ошибка при парсинге страницы🔴⬆️:', URL)
        
        

def pc(URL):
    try:
        time_new = datetime.now().strftime('%H:%M:%S') + " - "
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")  
          
        img_post = soup.find("div" , style="text-align:center;").find('img').get("src")
        
        version_near = soup.find('h2', class_='news__title').get_text()
        version_post = []
        version_teg_post = []
        version_split = version_near.split()
        
        i = 0
       
        for version_new in version_split:
            if version_new[0] == '[':
                
                version_post.append(version_new[1:-1])
                version_teg = version_post[i][:-1].replace(".", "")
                version_teg = ('#м' + version_teg) 
                
                num = 0
                if i == 0:
                    version_teg_post.append(version_teg)
                for return_teg in version_teg_post:
                    if return_teg == version_teg: 
                        num += 1       
                if num == 0:
                    version_teg_post.append(version_teg)               
                i += 1        
        
        title_post = soup.find("div", style="text-align:justify;").getText()  
        url_post = soup.find('h2', class_='news__title').find('a').get('href')
        
        version_post = (', '.join(version_post))
        version_teg_post = (', '.join(version_teg_post))
        
        if URL == 'https://ru-minecraft.ru/mody-minecraft/':
            if data['values'][0] == 0:
                post_device = f'💻Устройство ПК(мод)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{title_post}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}'
            if data['values'][0] == 1:
                post_device = f'{icon2}мод для майнкрафт пк'
                channel_url = '@minemob1'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по модам{icon2_ivent}](https://t.me/minemob1)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title_post}\n \nТеги: {version_teg_post}\n{post_channel}'
            toggle_value(0)    
        if URL == 'https://ru-minecraft.ru/mody-minecraft/shaders/':
            if data['values'][1] == 0:
                post_device = f'💻Устройство ПК(шейдер)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{title_post}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}'         
            if data['values'][1] == 1:
                post_device = f'{icon2}шейдеры для майнкрафт пк'
                channel_url = '@shaders1'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'[{icon2_ivent}Канал по шейдерам{icon2_ivent}](https://t.me/shaders1)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title_post}\n \nТеги: {version_teg_post}\n{post_channel}'
            toggle_value(1)         
        if URL == 'https://ru-minecraft.ru/karty-dlja-minecraft/':
            if data['values'][2] == 0:
                post_device = f'💻Устройство ПК(карта)'
                channel_url = '@Iminemods'
                post_channel = f'[{icon_ivent}Канал по модам/шейдерам/картам{icon_ivent}](https://t.me/Iminemods)'
                post_text = f'{icon}{title_post}\n \n{post_device}\nВерсия: {version_post}\n \n{post_channel}'
            if data['values'][2] == 1:
                post_device = f'{icon2}карта для майнкрафт пк'
                channel_url = '@minemob2'
                post_version = f'{icon2}Версия: {version_post}'
                post_channel = f'{icon2_ivent}[Канал по картам](https://t.me/minemob2)'
                post_text = f'{post_device}\n{post_version}\n{icon2}{title_post}\n \nТеги: {version_teg_post}\n{post_channel}'
            toggle_value(2)    
        print(time_new, f'Канал {channel_url}, {post_device}')
        markup = types.InlineKeyboardMarkup()
        btn_downl = types.InlineKeyboardButton(text="✔️Подробнее", url = url_post)
        markup.add(btn_downl)
        bot.send_photo(channel_url, (img_post), (post_text), reply_markup = markup,parse_mode='Markdown')   
        
        
    except Exception as e:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    check()
