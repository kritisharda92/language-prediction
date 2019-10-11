import math
import pickle

class TreeNode:

    value = ""
    # level = ""
    children = []

    def __init__(self, value, tree):
        """
        This is the constructor of the class TreeNode. This class is used in constructing the decison tree for
        prediction using the decision tree model
        :param value: Value of Node
        :param tree: Model of the decision tree
        """
        self.value = value
        # Make sure that the decision tree is in the form of a dictionary
        if(isinstance(tree,dict)):
            self.children = tree.keys()

class DecisionTree:

    def __init__(self):
        """
        This is the constructor for the Decision tree class. It defines all the necessary variables required by the
        decision tree like data, positive (en - English) and negitive (nl - Dutch) examples, total attributes it
        contains, class entropy and info gain of all attributes.
        """
        self.data = None
        self.decisionTree = {}
        self.enClass = 0
        self.nlClass = 0
        self.listAttributes = ["Contains-het", "Contains-de", "Contains-een", "Contains-en/aan", "Contains-ij", "wordLength14",
                              "Contains-a/an", "Contains-are/were", "Contains-and", "Contains-on/to", "Contains-the"]
        self.infoGain = []
        self.entropy = 0


    def buildDecisionTree(self, data):
        """
        Starts the procedure to build the decision tree and saves the decision tree model
        :param data: decision tree
        :return:
        """
        self.data = data
        self.decisionTree = self.buildTree(self.data, self.listAttributes)
        with open("decision_tree_model", "wb") as f:
                pickle.dump(self.decisionTree, f, pickle.HIGHEST_PROTOCOL)
        return self.decisionTree


    def buildTree(self, data, attributes):
        """
        This is a recursive function that builds a tree/subtree at each node by considering the information gain index
        and splitting the data by the attribute that has the highest information gain.
        :param data: the training data
        :param attributes: the features to be considered
        :return: decision tree
        """

        totalClasses = []
        data = data[:]
        assignedClass = self.assignClass()

        for record in data:
            totalClasses.append(record[-1])

        # if all attributes have been traversed or the algo runs out of data/records
        if len(attributes) < 1 or not data:
            return assignedClass

        countClass = totalClasses.count(totalClasses[0])

        # if all classes are same
        if countClass == len(totalClasses):
            return totalClasses[0]

        splitAttrIndex = self.getSplitAttr(data, attributes)
        decisionTree = {splitAttrIndex: {}}

        # Splitting the data using the attribute with the hightest info gain
        for attrVal in ['True', 'False']:
            subtreeAttributes = attributes[:]
            subtreeAttributes.pop(splitAttrIndex)
            # Get new data for children node
            subtreeData = self.getNewData(data, splitAttrIndex, attrVal)
            # generate subtree
            subtree = self.buildTree(subtreeData, subtreeAttributes)
            decisionTree[splitAttrIndex][attrVal] = subtree

        return decisionTree


    def assignClass(self):
        """
        Calculates the class to which maximum number of records belong
        :return: the class name 'en' or 'nl'
        """
        classes = {}
        classes['en'] = 0
        classes['nl'] = 0
        assignedClass = ""

        for record in self.data:
            if record[-1] == 'en':
                classes['en'] += 1
            elif record[-1] == 'nl':
                classes['nl'] += 1

        max = 0
        for key in classes.keys():
            # get max class
            if max < classes[key]:
                max = classes[key]
                assignedClass = key

        self.enClass = classes['en']
        self.nlClass = classes['nl']

        return assignedClass


    def getSplitAttr(self, data, attributes):
        """
        Calculated the info gain if each attribute and returns the index of attrubute that has the hightest info gain
        This is basically the splitting attribute
        :param data: Data records
        :param attributes: attributes present in data
        :return:
        """
        splitAttrIndex = 0
        lengthAttr = len(attributes)
        del self.infoGain[:]
        index = 0
        while index < lengthAttr:
            self.infoGain.append(self.getInfoGain(data, index))
            index += 1

        for gain in self.infoGain:
            if gain == max(self.infoGain):
                break
            splitAttrIndex += 1
        return splitAttrIndex


    def getClass(self, record, lang):
        """
        Calculates the class to which maximum number of records belong
        :return: the class name 'en' or 'nl'
        """
        counter = 0
        class1 = 'en'
        class2 = 'nl'
        if lang == class2:
            return lang
        for val in record:
            if counter > 5:
                if val == 'True':
                    return class1
            if counter < 6:
                if val == 'True':
                    return class2
            counter += 1
        return class1


    def getInfoGain(self, data, index):
        """
        Calculate the Info Gain
        :param data: Data
        :param index: Attribute index whose info gain needs to be calculated
        :return: info gain
        """
        # count for True Positive, True Negitive, False Positive and False Negitive
        TP = 0
        TN = 0
        FP = 0
        FN = 0

        for record in data:
            attrValue = record[index]
            clsValue = record[-1]

            if attrValue == 'True':
                if clsValue == 'en':
                    TP += 1
                else:
                    TN += 1
            elif attrValue == 'False':
                if clsValue == 'en':
                    FP += 1
                else:
                    FN += 1

        # calculate class entropy and entropy of each value of an attribute
        E_init = self.getEntropy(self.enClass, self.nlClass)
        E_attr = self.getAttrEntropy(TP, TN, FP, FN)

        infoGain = E_init - E_attr

        self.entropy = E_init
        return infoGain


    def getEntropy(self, pVal, nVal):
        """
        Calculates the entpropy given Postive class values and Negitive class values
        :param pVal: positive value
        :param nVal: negitive value
        :return:
        """
        totVal = pVal + nVal
        if pVal == 0 or nVal == 0:
            return 0

        pProb = pVal/totVal
        nProb = 1 - pProb
        entropy = - (pProb * math.log(pProb, 2) + nProb * math.log(nProb, 2))
        return entropy


    def getAttrEntropy(self, TP, TN, FP, FN):
        """
        Calculates the total entropy of an attribute
        :param TP: True Positive
        :param TN: True Negitive
        :param FP: False Positive
        :param FN: False Negitive
        :return: entropy
        """
        totVal = self.enClass + self.nlClass

        tProb = (TP + TN) / totVal
        tEntropy = self.getEntropy(TP, TN)

        fProb = (FP + FN) / totVal
        fEntropy = self.getEntropy(FP, FN)

        attrEntropy = tProb * tEntropy + fProb * fEntropy
        return attrEntropy


    def getNewData(self, data, splitIndex, attrVal):
        """
        Gets new data for the subtree after splitting the data using the attribute with best info gain
        :param data:
        :param splitIndex:
        :param attrVal:
        :return:
        """
        newData = []
        for record in data:
            if record[splitIndex] == attrVal:
                newRecord =[]
                lenRecord = len(record)

                for i in range(lenRecord):
                    # doesnt include the split attribute
                    if i == splitIndex:
                        continue
                    newRecord.append(record[i])
                newData.append(newRecord)
        return newData


    def predictLanguage(self, data, model):
        """
        Takes the decision tree model and the test data that needs to be classified and predicts the class for each
        record in the test data file
        :param data: test data to be classified
        :param model: decision tree model that is used for classification
        :return:
        """

        # The model is in the format .dat, needs to be converted back into a dictionary
        with open(model, "rb") as f:
            dtModel = dict(pickle.load(f))

        recNum = 1
        for record in data:
            subModel = dtModel
            # set default language to english
            language = 'en'
            # if submodel exits
            while (isinstance(subModel, dict)):
                subInd = next(iter(subModel))
                subModel = subModel[subInd]

                i = TreeNode(subInd, subModel).value
                val = record[i]
                keys = subModel.keys()

                if val in keys:
                    language = subModel[val]
                    subModel = subModel[val]
                    continue
                # if keys doesn't contain val
                language = ''
                break
            # Print the predicted classes
            if language != '':
                print('Class predicted for Record '+ str(recNum) + ': ' + self.getClass(record, language))
            recNum += 1