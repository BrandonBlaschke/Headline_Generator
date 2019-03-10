import random

# Represents a word / string / char with frequency count
class Word:

    myChar = ""
    myCount = 1

    # Initialize object
    def __init__(self, txt):
        self.myChar = txt
        self.words = {}

    # Add the bi word to this
    def addBiWord(self, txt):
        if txt in self.words:
            self.words.get(txt).addOne()
        else:
            self.words[txt] = Word(txt)

    # Add the tri word to this
    def addTriWord(self, txt, txt2):
        self.words.get(txt).addBiWord(txt2)

    # Add one to the frequency count
    def addOne(self):
        self.myCount += 1

    # Recursive function to print words
    def printWords(self, aWord, level):

        if level == 1:
            print("\t" + aWord.myChar + " " + str(aWord.myCount))
        elif level == 2:
            print("\t\t" + aWord.myChar + " " + str(aWord.myCount))
            return

        for k, v in aWord.words.items():
            v.printWords(v, 2)

    # Print the word and frequency with also the other words it has
    def __str__(self):
        print(self.myChar + " " + str(self.myCount))
        for k, v in self.words.items():
            self.printWords(v, 1)
        return ""

# Add a word to the WordMap
def addToWordMap(text):
    if text in wordMap:
        wordMap.get(text).addOne()
    else:
        wordMap[text] = Word(text)

##### MAIN PROGRAM HERE #####

repeat = True
wordMap = {}

# Read n number of files here
while repeat:

    # Get file
    print("---------------------")

    fileName = input("Type in the file name to read ")
    print("READING: " + fileName)

    # Attempt to open file
    try:
        file = open(fileName, "r")
    except FileNotFoundError:
        print("Error Reading File")
        continue

    # Read the file every three words
    text = file.read().split()
    for i in range(0, len(text), 3):

        word1 = None
        word2 = None
        word3 = None

        # Place words in back end data structure
        if i < len(text):
            addToWordMap(text[i])
            word1 = text[i]
        if i + 1 < len(text):
            word2 = text[i+1]
            wordMap.get(word1).addBiWord(word2)
        if i + 2 < len(text):
            word3 = text[i+2]
            wordMap.get(word1).addTriWord(word2, word3)

    # Print dictionary for debugging
    # for k, v in wordMap.items():
    #     print(v)

    # Prompt to end loop
    con = input("Do you want to read another? y/n ")
    if con == "n":
        repeat = False

fileName = input("Name of output file (no \".txt\"): ")
sentences = input("Number of sentences: ")
newFile = open(fileName + ".txt", "w")

# Print the generated text
# randomWord = random.choice(list(wordMap.keys()))
secondWord = None
thirdWord = None

for i in range(int(sentences)): 

    currentWord = "Florida"

    # generate random sentences 
    for i in range(0, random.randint(4, 6)):

        print(currentWord + " ", end="")
        newFile.write(currentWord + " ")

        topProbability = 0
        topWord = ""
        bottom = wordMap.get(currentWord).myCount
        # Get second word
        for k, v in wordMap.get(currentWord).words.items():
            top = v.myCount
            tempProb = top / bottom
            # print("p(" + v.myChar + "|" + currentWord + ") = " + str(top) + " / " + str(bottom) + " = "+ str(tempProb))
            if tempProb > topProbability:
                topProbability = tempProb
                topWord = v.myChar
        #print("Top word is for biword is " + topWord)
        
        print(topWord + " ", end="")
        newFile.write(topWord + " ")
        if (topWord[-1] == '.'):
            break

        # Get third word
        bottom = wordMap.get(currentWord).words.get(topWord).myCount
        topProbability = 0
        oldTop = topWord
        for k, v in wordMap.get(currentWord).words.get(topWord).words.items():
            top = v.myCount
            tempProb = top / bottom + (random.randint(1,5) / 10)
            # print("p(" + v.myChar + "|" + currentWord + ", " + oldTop + ") = " +  str(top) + " / " + str(bottom) + " = " + str(tempProb))
            if tempProb > topProbability:
                topProbability = tempProb
                topWord = v.myChar

        print(topWord + " ", end="")
        newFile.write(topWord + " ")
        if (topWord[-1] == '.'):
            break

        # Select the next word
        currentWord = random.choice(list(wordMap.keys()))

    print()
    newFile.write("\n")
print("DONE")
newFile.close()
input()