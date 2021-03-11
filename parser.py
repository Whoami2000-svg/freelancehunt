import requests
from bs4 import BeautifulSoup
import telebot 
import time 
def numsearch(s):
    flag = False
    for i in '0123456789':
        if i in s:
            flag = True
            break
    return flag

last_orders = []
categories = ['python/22.html', 'php/1.html', 'veb-programmirovanie/99.html', 'html-css-verstka/124.html', 'parsing-dannyih/169.html', 'prikladnoe-programmirovanie/103.html', 'razrabotka-botov/180.html']
    

bot = telebot.TeleBot('1689331285:AAGOQeZ_UjZ6zZXEqHZj9RfxI0PzUVcilbI')
@bot.message_handler(commands=["start"])
def start(message):
    while True:   
        for categorie in categories:            
            req = 'https://freelancehunt.com/projects/skill/' + categorie
            response = requests.get(req).text
            soup = BeautifulSoup(response, 'lxml')
            trs = soup.find('table', class_='table table-normal project-list').find_all('tr')
            trs = soup.find_all('tr')
            for i in range(0, 3):
                tr = trs[i]
                title = tr.find('a')
                cost = tr.find('td').find('span')
                title = title.text
                cost = cost.text               
                link = tr.find('a')
                link = link.get('href')
                title = str(title)
                cost = str(cost)
                link = str(link)

                response = requests.get(link).text
                soup = BeautifulSoup(response, 'lxml')
                description = soup.find('div', id="project-description").find_all('p')
                description_now = str()
                for p in description:
                    description_now += p.text + "\n"
                if cost == '':
                    cost = "не указана"
                else:
                    cost = cost[2:-2]
                now = [title, cost, description_now, link ]
                if not now[0] in last_orders:

                    last_orders.append(now[0])
                    if not numsearch(now[1]):
                        now[1] = 'не указана'
                    elif 'реми' in now[1]:
                        now[1] = 'премиум проект'

                    message_text = str('Название: ' + now[0]  + '\n\nОписание: ' + now[2] + '\n\nЦена: ' + now[1] + '\n\nПодробнее по ссылке: ' +  now[3])
                    bot.send_message(message.chat.id, message_text)
        time.sleep(300) 
        if len(categories) > 30:
            categories.pop(len(categories)-1)         
            categories.pop(len(categories)-1) 
            categories.pop(len(categories)-1) 


if __name__ == '__main__':
    bot.infinity_polling()