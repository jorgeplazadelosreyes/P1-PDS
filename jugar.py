import requests

length = 5
language = "/static/indonesian.txt"
base_url = 'https://pds-wordie.herokuapp.com'
file_url = f'{base_url}{language}'

r = requests.get(file_url)
requests.enconding = 'cp1252'
text = r.content.decode('cp1252', errors='ignore')
text_list = text.split('\n')

words = [w.strip().upper() for w in text_list]

fullWords = [x for x in words if len(x)==length]

def updateWords(word, wordList, state):
    rep = []
    #wordList.remove(word)
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

def main(abc):
    letters = letterScore(abc)
    tries = 0
    upAbc= abc
    while True:
        word = getWord(upAbc, letters)
        print("recomendado:",word)
        word = input("Ingrese: ")
        tries += 1
        state = input("respuesta: ")
        fin = input("listo?: ")
        print(state, tries)
        if fin == "s":
            return tries
        upAbc = updateWords(word, upAbc, state)
        print(upAbc)

main(fullWords)