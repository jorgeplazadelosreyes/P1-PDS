import requests
import time

base_url = 'https://pds-wordie.herokuapp.com'
player_key = 'RSFTSQY'

response = requests.get(f'{base_url}/api/games/')

def allGames():
    tries = 0
    count = 0
    games = response.json()['games']
    for game in games:
        ide = game["id"]
        if ide < 47:
            continue
        wordCount = game["words_count"]
        language = game["language"]
        wordLength = game["word_length"]
        file_url = f'{base_url}{language}'
        r = requests.get(file_url)
        requests.enconding = 'cp1252'
        text = r.content.decode('cp1252', errors='ignore')
        text_list = text.split('\n')

        words = [w.strip().upper() for w in text_list]

        fullWords = [x for x in words if len(x)==wordLength]
        dicts = {}
        for i in range(wordCount):
            dicts[i] = fullWords
        
        plus = main(dicts, game, wordCount)
        print(f"{count+1}. Intentos id {ide}: {plus}")
        
        tries += plus
        count += 1
    return tries
    

def sendWord(word, game):
    game = int(game["id"])
    data = {
        'game': game,
        'key': player_key,
        'word': word
    }
    r = requests.post(f'{base_url}/api/play/', data=data)
    return r.json()


def resetGame(game):
    game = int(game["id"])
    data = {
        'game': game,
        'key': player_key
    }
    r = requests.post(f'{base_url}/api/reset/', data=data)
    #print(r.json())

def main(dicts, game, wordCount):
    resetGame(game)
    letters = letterScore(dicts[0])
    tries = 0
    result = []
    wordsState = []
    while True:
        indx = pickWord(result, wordsState)
        word = getWord(dicts[indx], letters)
        #print(word)
        state = sendWord(word, game)
        tries += 1
        #print(state, tries)
        result = state["result"]
        wordsState = state["words_state"]
        fin = state["finished"]
        if fin == True:
            return tries
        for i in range(wordCount):
            dicts[i] = updateWords(word, dicts[i], result[i])

def getWord(words, letters):
    highestScore = 0
    highestWord = ""
    for word in words:
        history = []
        score = 0
        for let in word:
            if let not in history:
                score += letters[let]
                history.append(let)
        if score > highestScore:
            highestScore = score
            highestWord = word
    return highestWord
    
def updateWords(word, wordList, state):
    rep = []
    for i, num in enumerate(state):
        let = word[i]
        if num == "2":
            rep.append(let)
            wordList = [x for x in wordList if let in x]
            wordList = [x for x in wordList if x[i] == let]

    for i, num in enumerate(state):
        let = word[i]
        if num == "1":
            rep.append(let)
            wordList = [x for x in wordList if let in x]
            wordList = [x for x in wordList if x[i] != let]

    for i, num in enumerate(state):
        let = word[i]
        if num == "0":
            wordList = [x for x in wordList if x[i] != let]
            if let in rep:
                continue
            wordList = [x for x in wordList if let not in x]
    return wordList

def letterScore(words):
    letters = {}
    for word in words:
        for let in word:
            if let in letters:
                letters[let] += 1
            else:
                letters[let] = 1
    return letters

def pickWord(results, states):
    highest = 0
    index = 0
    count = 0
    for res in results:
        if states[count] == False:
            aux = 0
            for num in res:
                aux += int(num)
            if aux > highest:
                highest = aux
                index = count
        count += 1
    return index

start = time.time()
print("tries:", allGames())
end = time.time()
print("duracion:",(end-start)/60,"min")