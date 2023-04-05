import requests
from bs4 import BeautifulSoup as Bs
import datetime
from openpyxl import Workbook
from os import path, mkdir
import cloud
import sqlite3


#"CREATE TABLE IF NOT EXISTS ArXiv(id INT PRIMARY KEY, title TEXT, abstract TEXT, MyTagsTEXT, authors TEXT);"


def get_page(page_utl: str):
    request = requests.get(page_utl)
    page = Bs(request.content, 'html.parser')
    return page


def CheckTags(tags: list, data: str):
    add = ''
    for tag in tags:
        if data.find(tag) != -1:
            add += tag
            add += ','

    return add


def check_doubles(table_name: str, column: str, data: str, searchwords: str):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT " + column + " FROM " + table_name + " WHERE searchwords = '" + searchwords + "'")
    column = cursor.fetchall()
    for tag in column:
        for tup in tag:
            if tup == data:
                return True
    return False


def push_arxiv_db(title: str, abstract: str, tags: str, authors: str, searchwords: str, links: str):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ArXiv(id INT PRIMARY KEY, title TEXT, abstract TEXT, MyTags TEXT, authors TEXT, searchwords TEXT, link TEXT);")
    if check_doubles('ArXiv', 'title', title, searchwords) == False:
        data1 = []
        cursor.execute("SELECT id FROM ArXiv")
        id = cursor.fetchall()
        if len(id) == 0:
            data1.append(1)
        else:
            data1.append(int(id[-1][0]) + 1)
        data1.append(title)
        data1.append(abstract)
        data1.append(tags)
        data1.append(authors)
        data1.append(searchwords)
        data1.append(links)
        t = tuple(data1)
        cursor.execute("INSERT INTO ArXiv VALUES(?, ?, ?, ?, ?, ?, ?);", t)
        data1.clear()
        db_connection.commit()
    db_connection.close()

def arxiv_parser(link: str, searchwords: str):
    page_num = 0
    page = get_page(page_utl=link + str(page_num))
    while page:
        page = get_page(page_utl=link + str(page_num))
        radar_tags = cloud.get_column('Tags', 'RadarTags')
        radar_tags.pop()
        articles_list = page.select('.arxiv-result')
        if len(articles_list) == 0:
            break
        for article in articles_list:
            try:
                title = article.find('p', class_='title is-5 mathjax').get_text()
                title = " ".join(title.split())
                authors = [author.text for author in article.select('.authors > a')]
                authors = ", ".join(authors)
                abstract = article.find('span', class_='abstract-full has-text-grey-dark mathjax').get_text()
                abstract = abstract[: -7]
                abstract = " ".join(abstract.split())
                tags = CheckTags(radar_tags, abstract)
                links = article.find('p', class_='list-title is-inline-block').find('a').get('href')
            except AttributeError:
                title = 'Нет данных'
                authors = 'Нет данных'
                abstract = 'Нет данных'
            push_arxiv_db(title, abstract, tags, authors, searchwords, links)
        page_num += 200
    else:
        print("No more pages")





#arxivParser("https://arxiv.org/search/?searchtype=all&query=radar&abstracts=show&size=200&order=-announced_date_first&start=", "radar")
#arxivParser("https://arxiv.org/search/?query=mmWave&searchtype=all&abstracts=show&order=-announced_date_first&size=200&start=", "mmWave")
