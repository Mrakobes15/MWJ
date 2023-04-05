import my_tags as mt
from pymystem3 import Mystem
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
import sqlite3


def canonize(text:str):
    text = mt.remove_commas(text)
    stop_words = stopwords.words('english')
    data = [word for word in text.split() if word not in stop_words]
    return data


def lemmatize(text:list):
    wnl = WordNetLemmatizer()
    result = ''
    for i in text:
        result += wnl.lemmatize(i)
        result += ' '
    return result


def normalization(table: str):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT id FROM " + table)
    ids = cursor.fetchall()
    count = 0
    for count in range(len(ids)):
        cursor.execute("SELECT abstract FROM " + table + " WHERE id = '" + str(count + 1) + "'")
        data = cursor.fetchone()
        text = data[0]
        text = canonize(text)
        text = lemmatize(text)
        request = "UPDATE " + table + " SET normalized = '" + text + "' WHERE id =" + str(count + 1)
        cursor.execute(request)
        db_connection.commit()
    db_connection.close()


tables = ["AdvancedCellular", "AerospaceDefense", "ArXiv", "Broadband", "EMI", "Microelectronics"]

normalization("Microelectronics")