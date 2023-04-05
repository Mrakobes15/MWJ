import mwj
import ArXiv


def show_interface():
    print("Welcome aboard, username! Choose your move: ")
    print("1. Parse or refresh MWJ Aerospace&Defense channel")
    print("2. Parse or refresh MWJ Semiconductor/RFIC/MMIC channel")
    print("3. Parse or refresh 6G/Advanced Cellular channel")
    print("4. Parse or refresh Broadband channel")
    print("5. Parse or refresh EMC/EMI channel")
    print("6. Parse new ArXiv.com query")
    print("0. Exit")


def parse_arxiv():
    print("Paste query: ")
    query = input()
    link = "https://arxiv.org/search/?query=" + query + "&searchtype=all&abstracts=show&order=-announced_date_first&size=200&start=0"
    ArXiv.arxiv_parser(link, query)


def deal_key(key: int):
    match key:
        case '1':
            mwj.mwj_parser("https://www.microwavejournal.com/articles/topic/3372?page=", "AerospaceDefense")
        case '2':
            mwj.mwj_parser("https://www.microwavejournal.com/articles/topic/3572?page=", "Microelectronics")
        case '3':
            mwj.mwj_parser("http://www.microwavejournal.com/articles/topic/3886?page=", "AdvancedCellular")
        case '4':
            mwj.mwj_parser("https://www.microwavejournal.com/articles/topic/3797?page=", "Broadband")
        case '5':
            mwj.mwj_parser("https://www.microwavejournal.com/articles/topic/3794?page=", "EMI")
        case '6':
            parse_arxiv()


show_interface()
key = input()
deal_key(key)