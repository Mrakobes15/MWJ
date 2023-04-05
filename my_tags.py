from openpyxl import Workbook
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
import matplotlib.pyplot as plt
import openpyxl
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.collocations import *
import sqlite3
from pymystem3 import Mystem


def AddTags(data: list, company: list, radar_tags: list, table_name: str, column: list):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    count_row = 0
    for count_row in range(len(company)):
        if (column[count_row][1] is not None) or (column[count_row][1] == ''):
            add = str(column[count_row][1])
        else:
            add = ''
        for text in data:
            if text.find(company[count_row][1]) != -1:
                for r_tag in radar_tags:
                    if text.find(r_tag) != -1 and add.find(r_tag) == -1:
                        add += r_tag
                        add += ','
        if add != '':
            request = "UPDATE " + table_name + " SET tags = '" + add + "' WHERE id =" + str(company[count_row][0])
            cursor.execute(request)
        db_connection.commit()


def RefreshCompanyTags():
    dat = get_data("AerospaceAndDefence", 3, 4).split('\n')
    dat += get_data("microelectronics", 3, 4).split('\n')
    radar = get_column('Tags', 'RadarTags')
    radar.pop()
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, company FROM companies")
    cmp = cursor.fetchall()
    cursor.execute("SELECT id, tags FROM companies")
    column = cursor.fetchall()
    AddTags(dat, cmp, radar, "companies", column)


def RefreshMyTags(table_name: str):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, abstract FROM " + table_name)
    abstracts = cursor.fetchall()
    radar = get_column('Tags', 'RadarTags')
    radar.pop()
    cursor.execute("SELECT id, my_tags FROM " + table_name)
    MyTags = cursor.fetchall()
    count_row = 0
    for count_row in range(len(abstracts)):
        if (MyTags[count_row][1] is not None) or (MyTags[count_row][1] == ''):
            add = str(MyTags[count_row][1])
        else:
            add = ''
        add = ' '
        tmp = str(abstracts[count_row][1])
        for tags in radar:
            if tmp.find(tags) != -1 and add.find(tags):
                add += tags
                add += ','
        if add != '' and add is not None:
            request = "UPDATE " + table_name + " SET my_tags = '" + add + "' WHERE id =" + str(abstracts[count_row][0])
        cursor.execute(request)
        db_connection.commit()


def remove_commas(string):
    trans_table = {ord(','): None, ord(':'): None, ord('.'): None, ord('&'): None, ord('!'): None, ord('"'): None,
                   ord('?'): None, ord('\n'): None, ord('\t'): None, ord('@'): None,ord("'"): None}
    return string.translate(trans_table)


def get_column(column: str, table_name: str):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT " + column + " FROM " + table_name)
    radar_tags = cursor.fetchall()
    text = ''
    for tag in radar_tags:
        for tup in tag:
            text += tup
            text += ' '
    text = remove_commas(text)
    return text


def use_nltk(text: str):
    stoplist = stopwords.words('english')
    data = [word for word in text.split() if word not in stoplist]
    bigrams = list(nltk.bigrams(data))
    data = Counter([' '.join(i) for i in bigrams]).most_common(20)
    return data


def raw_frequency(text: str):
    N_best = 20
    bm = nltk.collocations.BigramAssocMeasures()
    stoplist = stopwords.words('english')
    data = [word for word in text.split() if word not in stoplist]
    f = BigramCollocationFinder.from_words(data)
    f.apply_freq_filter(2)
    raw_freq_ranking = [' '.join(i) for i in f.nbest(bm.raw_freq, N_best)]
    return raw_freq_ranking


def pmi_ranking(text: str):
    N_best = 20
    bm = nltk.collocations.BigramAssocMeasures()
    stoplist = stopwords.words('english')
    data = [word for word in text.split() if word not in stoplist]
    f = BigramCollocationFinder.from_words(data)
    f.apply_freq_filter(10)
    pmi_ranking = f.nbest(bm.pmi, N_best)
    return pmi_ranking


def t_score(text: str):
    N_best = 20
    bm = nltk.collocations.BigramAssocMeasures()
    stoplist = stopwords.words('english')
    data = [word for word in text.split() if word not in stoplist]
    f = BigramCollocationFinder.from_words(data)
    f.apply_freq_filter(2)
    tscore_ranking = [' '.join(i) for i in f.nbest(bm.student_t, N_best)]
    return tscore_ranking


def strip_text(text: str):
    # stoplist = stopwords.words('english')
    # data = [word for word in text.split() if word not in stoplist]
    m = Mystem()
    lemmas = m.lemmatize(text)
    result = ''.join(lemmas)
    return result


text = get_column('title', 'ArXiv')
# text = strip_text(text)
temp1 = use_nltk(text)
temp2 = raw_frequency(text)
temp3 = pmi_ranking(text)
temp4 = t_score(text)
"""print(temp1)
print(temp2)
print(temp3)
print(temp4)"""
