import my_tags as mt
import sqlite3


def fix_dataset(raw_freq:list, pmi_rank:list, tyring:list):
    t = ('Null', '0')
    t1 = ('(Null)', ' ')
    if len(raw_freq) < 20:
        while len(raw_freq) != 20:
            raw_freq.append(t)
    if len(pmi_rank) < 20:
        while len(pmi_rank) != 20:
            pmi_rank.append(t1)
    if len(tyring) < 20:
        while len(tyring) != 20:
            tyring.append("Null")


def push_data_scoreboard(table:str, raw_freq:list, pmi_rank:list, tyring:list):
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    data = []
    fix_dataset(raw_freq, pmi_rank, tyring)
    for i in range(1, 21):
        data.append(i)
        data.append(raw_freq[i - 1][0])
        data.append(int(raw_freq[i - 1][1]))
        pmi = pmi_rank[i - 1][0] + " " + pmi_rank[i - 1][1]
        data.append(pmi)
        data.append(tyring[i - 1])
        t = tuple(data)
        cursor.execute("INSERT INTO  " + table + "Scoreboard VALUES(?, ?, ?, ?, ?);", t)
        data.clear()
        db_connection.commit()
    db_connection.close()



def scoreboard(table:str):
    text = mt.get_column('title', table)
    text += mt.get_column('abstract', table)
    mt.strip_text(text)
    db_connection = sqlite3.connect('MWJ.db')
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + table + "Scoreboard;")
    db_connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS " + table + "Scoreboard(id INT PRIMARY KEY, RawFrequency TEXT, score INT, PmiRank TEXT, TyringRank TEXT);")
    db_connection.commit()
    raw_freq = mt.use_nltk(text)
    pmi_rank = mt.pmi_ranking(text)
    tyring = mt.t_score(text)
    push_data_scoreboard(table, raw_freq, pmi_rank, tyring)
    db_connection.close()


def refresh_scoreboards():
    scoreboard("AerospaceDefense")
    print("1")
    scoreboard("AdvancedCellular")
    print("2")
    #scoreboard("ArXiv")
    print("3")
    scoreboard("Broadband")
    print("4")
    scoreboard("EMI")
    print("5")
    scoreboard("Microelectronics")
    print("6")


#refresh_scoreboards()
#scoreboard("AdvancedCellular")
#scoreboard("Microelectronics")
scoreboard("ArXiv")
