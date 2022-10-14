import requests
import bs4
import re

# Хедеры если надо, оставлю тут))
HEADERS = {
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Cookie': '_ym_uid=1665747734709981522; _ym_d=1665747734; _ym_isad=2',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
}

# Ключевые слова объединяются в регулярку и, в дальнейшем, ищутся
key_words = ['it-индустрия', 'джун', 'junior']
re_key_words = re.compile(r'|'.join(key_words), re.IGNORECASE)

base_url = 'https://habr.com'

# Сначала заходим на главную страницу
main_page = bs4.BeautifulSoup(requests.get('https://habr.com/ru/all', headers=HEADERS).text, features='html.parser')

# Формируем список ссылок
articles_links = [article.find(class_ = 'tm-article-snippet__title-link').attrs['href'] for article in main_page.find_all('article')]

# Заходим на каждую страничку статьи и вытаскиваем дату, хабы, название и текст
for article in articles_links:

    article_page = bs4.BeautifulSoup(requests.get(base_url + article, headers=HEADERS).text, features='html.parser')
    publisher = article_page.find(class_ = 'tm-user-info__username').text
    date = article_page.find('time').attrs['title']
    hubs = " ".join([ hub.find('span').text for hub in article_page.find_all(class_='tm-article-snippet__hubs-item-link')])
    article_text = ' '.join([par.text.strip() for par in article_page.find_all('p')])
    article_title = article_page.find(class_ = 'tm-article-snippet__title tm-article-snippet__title_h1').text

    article_preview = publisher + date + hubs + article_text + article_title

    # Проверяем соответствие по ключевым словам, если есть, печатаем.
    if re.search(re_key_words, article_preview):
        print(date, article_title, base_url + article, sep=' - ')