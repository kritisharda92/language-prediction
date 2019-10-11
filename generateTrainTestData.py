
def readFile(filename):
    file = open(filename, 'r')
    data = file.read()
    data = data.strip().split(" ")
    return data


def writeFile(data):
    file = open('test20', 'w')
    count = 0
    str = ''
    for word in data:

        if(count == 0):
            # Change according to train/ test
            # str = 'nl|'+ word
            str = word
        else:
            str = str + ' ' + word
        count = count + 1

        # Change Count Here
        if count == 20:
            file.write(str+'\n')
            count = 0
            str = ''
    file.close()


def main():
    testFile = 'testFile'
    trainFile = 'trainFile'

    data = readFile(testFile)
    writeFile(data)


main()