import string
IOCENGLISH = 0.0686 #expected value for English text
EXPECTEDLIST = [0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074]
ALPH = list(string.ascii_uppercase)

def lettersToIndex(text):
    indexInAlph = []
    for letter in text:
        indexInAlph.append((ALPH).index(letter))
    return indexInAlph

def frequency(text):
    count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(ALPH)):
        for j in text:
            if ALPH[i] == j:
                count[i] = count[i] + 1
    return count

def splitTextFunction(text,coset,offset): #offset = start, coset = group len
    appendSplitText = ""
    for i in range(len(text)):
        if (i-offset)%(coset) == 0:
            appendSplitText += text[i]
    return appendSplitText

def calcIOC(text):
    sigma = 0
    count = frequency(text)
    for i in range(26):
        sigma = sigma + (count[i]*(count[i] - 1))
    ioc = sigma / (len(text) * (len(text)-1))
    return ioc

def calcKeyLen(iocList):
    smallestDiff = 999
    keyLen = 0
    iocDifferenceVals = []
    for i in range(len(iocList)):
        if IOCENGLISH - iocList[i] > 0:
            smallestDiff = IOCENGLISH - iocList[i]
            iocDifferenceVals.append(smallestDiff)
        else:
            smallestDiff = iocList[i] - IOCENGLISH
            iocDifferenceVals.append(smallestDiff)

    iocDifferenceValsCopy = []
    for diff in iocDifferenceVals:
        iocDifferenceValsCopy.append(diff)

    likeliestKeyLens = []
    while len(iocDifferenceValsCopy) != 0:
        #find min value in copy and append the index of this value in non copy to likeliestKeyLens. remove min value from copy.
        nextSmallestDiff = min(iocDifferenceValsCopy)
        nextKeyLen = [i for i,val in enumerate(iocDifferenceVals) if val==nextSmallestDiff] #list of the index(es) that have the next smallest value in iocdifferencevals
        for i in nextKeyLen:
            likeliestKeyLens.append(i + 1)
            iocDifferenceValsCopy.remove(nextSmallestDiff)
    return likeliestKeyLens


def rot1(numbers):
    numbers2 = []
    for val in numbers:
        numbers2.append((val - 1) % 26)
    return numbers2

def frequencyNums(nums):
    freqList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(26):
        freqList[i] = (nums).count(i)
    return freqList

def calcChiSquared(observedList,numsLen):
    
    chiSquaredVals = []
    for i in range(len(EXPECTEDLIST)):
        chiSquaredVals.append(((observedList[i] - (EXPECTEDLIST[i]*numsLen))**2)/(EXPECTEDLIST[i]*numsLen))
    chiSquared = sum(chiSquaredVals)
    return chiSquared

def calcKey(text,keyLen,index):
    caesar1 = (splitTextFunction(text,keyLen,index)) #for nth letter of key
    chiSquaredOptions = []
    indexCaesar = lettersToIndex(caesar1)
    chiSquaredOptions.append(calcChiSquared(frequencyNums(indexCaesar),len(indexCaesar)))
    for rotation in range(1,26):
        indexCaesar = rot1(indexCaesar)
        chiSquaredOptions.append(calcChiSquared(frequencyNums(indexCaesar),len(indexCaesar)))
    chiSquaredOptions2 = []
    for i in chiSquaredOptions:
        chiSquaredOptions2.append(i) #remove items only from chiSquaredOptions2

    expIndexList = []
    for i in range(len(chiSquaredOptions)):
        expIndex = chiSquaredOptions.index(min(chiSquaredOptions2))
        expIndexList.append(expIndex)
        chiSquaredOptions2.remove(min(chiSquaredOptions2))
    return expIndexList

def vigenere(message,key,option):
    indexListMessage = []
    indexListKey = []
    for letterM in message:
        indexListMessage.append((ALPH).index(letterM.upper()))
    for letterK in key:
        indexListKey.append((ALPH).index(letterK.upper()))
    iCipherTextList = []
    countM = 0
    countK = 0
    while len(indexListMessage) != len(iCipherTextList):
        if option == "ENCRYPTION":
            iCipherText = (indexListMessage[countM] + indexListKey[countK]) % 26
        elif option == "DECRYPTION":
            iCipherText = (indexListMessage[countM] - indexListKey[countK]) % 26
        iCipherTextList.append(iCipherText)
        countM += 1
        countK = (countK + 1) % len(key)
    cipherText = ""
    for i in iCipherTextList:
        cipherText += ALPH[i]
    return cipherText

def enterKey():
    key = input("ENTER KEY: ")
    while key.isalpha() == False:
        print("ENTER ONLY LETTERS.")
        key = input("ENTER KEY: ")
    return key

def getKeyLengths(text, maxKeyLen):
    iocList = []
    splitText = []

    for coset in range(1,int(maxKeyLen)+1):
        for offset in range(coset):
            appendSplitText = splitTextFunction(text,coset,offset)
            if len(appendSplitText) > 1:
                splitText.append(appendSplitText)

        calculatedIOCS = []
        for i in splitText:
            calculatedIOCS.append(calcIOC(i))
        iocList.append(sum(calculatedIOCS)/len(calculatedIOCS))
        splitText = []
        
    likeliestKeyLens = calcKeyLen(iocList)
    return likeliestKeyLens
    
def getKeys(keyLen, text):
    expIndexListAll = []
    for i in range(keyLen): #expIndexList is the 26 letter values from most to least likely of the ith letter of the key (0=1st letter)
        expIndexList = calcKey(text,keyLen,i)
        expIndexListAll.append(expIndexList)
    return expIndexListAll

def unknownKey(text):
    while True:
        try:
            maxKeyLen = input("ENTER MAX KEY LEN: ")
            if int(maxKeyLen) >= len(text) or int(maxKeyLen) <= 0:
                raise Exception
            break
        except:
            print("MAX KEY LEN MUST BE AN INTEGER WHICH IS LESS THAN THE LENGTH OF THE MESSAGE AND GREATER THAN 0")
            print("LENGTH OF MESSAGE:",len(text))
            
    likeliestKeyLens = getKeyLengths(text, maxKeyLen)
    #choose key length to use
    print("MOST LIKELY KEY LENS IN ORDER (MOST LIKELY TO LEAST LIKELY):",likeliestKeyLens)
    expKeyLen = likeliestKeyLens[0]
    print("EXPECTED KEY LENGTH:",expKeyLen)
    while True:
        try:
            keyLen = int(input("ENTER KEY LEN: ")) #chosen key length
            if int(keyLen) > int(maxKeyLen):
                raise Exception
            else:
                break
        except:
            print("ENTER ONLY INTEGERS.")

    expIndexListAll = getKeys(keyLen, text)
    keyIndex = []
    key = []
    print("MOST LIKELY LETTERS FOR KEY:")
    for likeliness in range(len(ALPH)):
        for posKey in range(keyLen):
            keyIndex.append(expIndexListAll[posKey][likeliness])
        for i in keyIndex:
            key.append(ALPH[i])
        print(key)
        keyIndex = []
        key = []
    keyInp = input("ENTER 1 TO USE MOST LIKELY KEY. IF NOT, ENTER KEY: ")
    while keyInp != "1" and keyInp.isalpha() == False:
        print("ENTER TEXT OR '1' ONLY.")
        keyInp = input("ENTER 1 TO USE MOST LIKELY KEY. IF NOT, ENTER KEY: ")
    if keyInp == "1":
        keyInp = ""
        for posKey in range(len(expIndexListAll)):
            keyInp += ALPH[expIndexListAll[posKey][0]]
    return keyInp

def main():
    #input option
    option = input("ENTER 'ENCRYPTION' OR 'DECRYPTION': ").upper()
    while option != "ENCRYPTION" and option != "DECRYPTION":
        print("PLEASE SELECT A VALID OPTION.")
        option = input("ENTER 'ENCRYPTION' OR 'DECRYPTION': ").upper()
    
    #input text
    text = input("ENTER TEXT: ").upper()
    while text.isalpha() == False:
        print("ENTER ONLY LETTERS.")
        text = input("ENTER TEXT: ")

    keyKnown = ""
    if option == "DECRYPTION":
        keyKnown = input("IS THE KEY KNOWN? ENTER 'Y' OR 'N': ").upper()
        while keyKnown != "Y" and keyKnown != "N":
            print("ENTER EITHER 'Y' OR 'N'")
            keyKnown = input("IS THE KEY KNOWN? ENTER 'Y' OR 'N': ").upper()

    if option == "ENCRYPTION" or keyKnown == "Y": #encrypting or decrypting with a known key
        key = enterKey()
    else: #decrypting with an unknown key
        key = unknownKey(text)

    print(vigenere(text,key,option))

main()
