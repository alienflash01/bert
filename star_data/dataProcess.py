#coding=utf-8
import random,os
import re

def getNewLines(filePath):
    """生成一个乱序的list，每个元素是 label+'\t'+内容的形式 """
    newLines = []
    with open(filePath, 'r', encoding="GB2312", errors='ignore') as f: 
        for line in f:
            if line.strip().split('\t')[1] == "TYPE":
                print("get type keyword: ", line)
            else:
                content, tag = line.strip().split("\t")
                newLine = "\t".join([tag, content])
                newLines.append(newLine)
        print("line num is ", len(newLines))
    random.shuffle(newLines)
    return newLines

def getDataSet(oriFilePath, trainFilePath, devFilePath):
    print("get data set")
    lines = getNewLines(oriFilePath)

    '''前9/10为训练集，后1/10为验证集'''
    trainLen = int(len(lines) - len(lines)/10)
    trainLines = lines[:trainLen]
    devLines = lines[trainLen:] 
    print(trainLen)

    with open(trainFilePath, 'w+', encoding="UTF-8") as newFile:        
        for line in trainLines:
            newFile.write(line +'\n')

    with open(devFilePath, 'w+', encoding="UTF-8") as newFile:        
        for line in devLines:
            newFile.write(line +'\n')

def getLabel(oriFilePath,labelFilePath):

    lines = getNewLines(oriFilePath)
    labels = set()

    with open(labelFilePath, 'w+',  encoding="UTF-8") as f:
        for line in lines:
            label = line.strip().split('\t')[0]
            if label not in labels:
                labels.add(label)
                f.write(label+'\n')

def get_labels(data_dir):
    """See base class."""
    labels = []
    with open(os.path.join(data_dir, "label.tsv")) as f:
        for line in f:
            labels.append(line.strip())
    return labels 

def main():
    getDataSet("./oriData/star_data/train.tsv", "./star_train.tsv","star_dev.tsv")
    getLabel("./oriData/star_data/train.tsv", "./label.tsv")
main()