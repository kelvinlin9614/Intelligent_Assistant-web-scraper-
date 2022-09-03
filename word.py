# Richard Pacheco
import json
import urllib.request


class InvalidWordError(Exception):
    pass


class word:
    def getDailyWord(date):
        url = 'http://api.wordnik.com:80/v4/words.json/wordOfTheDay?date=' + \
              date + '&api_key=d52b63b6880f17811310d0fbd3b0d3a8ef163a248f58dc831'
        response = urllib.request.urlopen(url)
        wordResponse = json.load(response)
        wordOTD = wordResponse['word']
        note = wordResponse['note']
        definition = wordResponse['definitions'][0]['text']
        altDefinition = wordResponse['definitions'][1]['text']
        return [wordOTD, definition, note, altDefinition]

    def getWord(word):
        try:
            url = str(f"https://api.wordnik.com/v4/word.json/{word}/definitions?limit=2" +
                      "&includeRelated=false&useCanonical=false&sourceDictionaries=webster"
                      + "&includeTags=false&api_key=d52b63b6880f17811310d0fbd3b0d3a8ef163a248f58dc831")
            response = urllib.request.urlopen(url)
            wordResponse = json.load(response)
            # check for an invalid word
            allDefinitions = wordResponse[0]['text'].split(";")
            definition = allDefinitions[0]
            if len(allDefinitions) > 1:
                altDef = allDefinitions[1]
            else:
                altDef = ""
            return [word, definition, altDef]
        except urllib.error.HTTPError:
            raise InvalidWordError
