import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import hashlib

def extract_news(url):
    try:
        s = 0
        # Отправляем GET-запрос к указанному URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим все статьи на странице новостного агенства
        articles = soup.find_all('article')
        # Открываем файл для записи лога
        with open('news_log.txt', 'a') as log_file:
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            log_file.write(f"Время запуска поиска: {current_time}\n\n")
            # Проходим по всем статьям на странице
            for article in articles:
                headline = article.find('h3').text.strip()
                announcement = article.find('p').text.strip()
                authors = article.find('span').text.strip()
                # Создаем уникальный хэш для каждой статьи
                article_hash = hashlib.sha256((headline + announcement + authors).encode('utf-8')).hexdigest()
                if article_hash not in previous_articles:
                    previous_articles.add(article_hash)
                    # Проверяем наличие ключевых слов в заголовке и аннотации
                    if any(keyword in headline for keyword in keywords) or any(keyword in announcement for keyword in keywords):
                        # Пропускаем начальные анонсы статей и записываем в лог только статьи с авторами
                        if authors: 
                            log_file.write(f"Заголовок: {headline}\n")
                            log_file.write(f"Аннотация: {announcement}\n")
                            log_file.write(f"Авторы: {authors}\n")
                            log_file.write("="*100 + "\n")
                            s = s+1
            if  s == 0:   
                log_file.write(f"Новых новостей пока нет\n\n")   
            
    except Exception as e:
        print(f"Ошибка поиска: {e}")
# Определяем список ключевых слов для поиска         
keywords = ["Democrat", "Republic", "Trump", "Biden", "election", "President"]
# URL новостного агенства
url = 'https://www.nytimes.com/section/politics'
# Создаем множество для хранения уже обработанных статей
previous_articles = set()   
# Запуск поиска новостей каждые 30 минут в течение 4 часов
for _ in range(8):
    extract_news(url)
    time.sleep(1800)  # Пауза 30 минут (1800 секунд)