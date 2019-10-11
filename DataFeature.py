
def readFile(filename, fileType):
    """
    Read the file and generate the data for decision tree
    :param filename: input file
    :param fileType: file type
    :return:
    """
    file = open(filename, 'r')
    data = file.read()
    data = data.strip().split("\n")

    dataList = []

    if fileType == 'train':
        for line in data:
            newRecord = []
            [language, line] = line.strip().split("|")
            newRecord.append(language)
            words = line.split(" ")
            words = [word.lower() for word in words]
            newRecord.append(words)
            dataList.append(newRecord)

    if fileType == 'predict':
        for line in data:
            words = line.strip().split(" ")
            dataList.append(words)

    return dataList


def extractFeatures(data, fileType):
    """
    Sets the Features for english and dutch language for each record
    :param data:
    :param fileType:
    :return:
    """
    featureList = []

    for record in data:
        exampleRecord = []

        if fileType == 'train':
            wordList = record[1]
            exampleRecord = setFeatues(wordList)
            exampleRecord.append(record[0])

        elif fileType == 'predict':
            exampleRecord = setFeatues(record[0])
        featureList.append(exampleRecord)

    return featureList


def setFeatues(wordList):
    """
    Extracts features for English and dutch language from the given input record
    :param wordList:
    :return:
    """
    exampleRecord = []

    # Dutch Features
    exampleRecord.append(str(('het' in wordList) == True))
    exampleRecord.append(str(('de' in wordList) == True))
    exampleRecord.append(str(('een' in wordList) == True))
    exampleRecord.append(str(('en' in wordList) == True or ('aan' in wordList) == True))
    exampleRecord.append(str(wordContains_ij(wordList)))
    exampleRecord.append(str(wordLength14(wordList)))

    # English Features
    exampleRecord.append(str(('a' in wordList) == True or ('an' in wordList) == True))
    exampleRecord.append(str(('are' in wordList) == True or ('were' in wordList) == True))
    exampleRecord.append(str(('and' in wordList) == True))
    exampleRecord.append(str(('on' in wordList) == True or ('to' in wordList) == True))
    exampleRecord.append(str(('the' in wordList) == True))

    return exampleRecord


def wordContains_ij(wordList):
    count = 0
    for word in wordList:
        if 'ij' in word.lower():
            count = count + 1
    if count >= 2:
        return True
    else:
        return False


def wordLength14(wordList):
    count = 0
    for word in wordList:
        if len(word)>13:
            count = count + 1
    if count >= 3:
        return True
    else:
        return False
