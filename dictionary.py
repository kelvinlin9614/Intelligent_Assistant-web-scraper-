# Richard Pacheco
from word import word, InvalidWordError
from datetime import datetime, timedelta


def getWordOTD():
    now = datetime.now()
    today = datetime.strftime(now, "%Y-%m-%d")
    return word.getDailyWord(today)


def getLastWordOTD():
    now = datetime.now()
    yesterday = now - timedelta(1)
    yesterday = datetime.strftime(yesterday, "%Y-%m-%d")
    return word.getDailyWord(yesterday)


def definition(myWord):
    try:
        defin = word.getWord(myWord)
        return defin
    except InvalidWordError:
        return [myWord, "Invalid word.", ""]


# class Dictionary:
#     pass
