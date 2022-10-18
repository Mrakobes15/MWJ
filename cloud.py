from openpyxl import Workbook
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
import matplotlib.pyplot as plt
import openpyxl
import re



def create_cloud(wc):
    plt.figure(figsize=(40, 30))
    plt.imshow(wc)
    plt.axis('off')


def get_data():
    wb = openpyxl.load_workbook("tables\AerospaceAndDefence.xlsx")
    ws = wb.active
    text = ''
    for i in range(1, ws.max_row):
        for col in ws.iter_cols(3, 4):
            if col[i].value is not None:
                text += ' '
                text += col[i].value

    return text


STOPWORDS_EN = get_stop_words("english")
data = get_data()
data = re.sub(r'==.*?==+', '', data)
wordcloud = WordCloud(width=2000,
                      height=1500,
                      max_words=100,
                      random_state=1,
                      background_color='black',
                      margin=20,
                      colormap='Pastel1',
                      collocations=False,
                      stopwords=STOPWORDS_EN).generate(data)
#create_cloud(WordCloud)
wordcloud.to_file('wc.png')
