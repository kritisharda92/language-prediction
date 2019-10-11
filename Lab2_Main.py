import DataGeneration
from DecisionTree import DecisionTree
import sys


def main():

    # Sample command to run of terminal:
    #   python3 Lab2_Main.py predict test50

    # values can be 'train' or 'predict'
    entryPoint = sys.argv[1]

    # File used to train (train10, train20, train50 ) or test(test10, test20, test50)
    filename = sys.argv[2]

    dataGeneration = DataGeneration
    decisionTree = DecisionTree()

    # filename = 'train50'
    # predictFilename = 'test50'


    if entryPoint == 'train':
        data = dataGeneration.readFile(filename, 'train')
        features = dataGeneration.extractFeatures(data, 'train')
        tree = decisionTree.buildDecisionTree(features)
        print("Decision Tree Trained!")
        # print(tree)

    if entryPoint == 'predict':
        decisionTreeModel = 'decision_tree_model'
        predictData = dataGeneration.readFile(filename, 'predict')
        predictFeatures = dataGeneration.extractFeatures(predictData, 'predict')
        decisionTree.predictLanguage(predictFeatures, decisionTreeModel)

main()