"""
authors: SunHui
data: 2021/02/16
"""
# import package from other source
import numpy as np
import pandas as pd
import re
import time
import sys
import os
from multiprocessing import Process

# define a Anteater class
class Anteater:
    """
    This class is used to create a source Anteater demo
    """
    # Some default parameters
    dataBase = './src/dataBase.txt'
    window = 12
    sim = 0.64




    def  __init__(self, testFile, similarFunc, k_mer, viewModel):
        self.testFile = testFile
        self.similarFunc = similarFunc
        self.k_mer = k_mer
        self.viewModel = viewModel  # Print running process
        #self.saveFile = saveFile

    def __del__(self):
        class_name = self.__class__.__name__
        print(str(class_name) + " destruction!")

    def run(self):
        """Anteater main function, is used to connect other function"""
        if self.viewModel:
            self.getParametersInfo()
        # step1: check source data format
        testFileFormat = self.sourceDataCheck()
        # step2: check similarFunc whether in [1,2,3,4,5]
        if self.similarFunc not in [1, 2, 3, 4, 5]:
            raise Exception('simFunc err')

        # step3: according file Selecting the Run Function
        if testFileFormat == '.txt':
            saveFile, saveFileSensitive, saveFileNoneSensitive = self.getFile()
            mySaveFile = saveFile + '.txt'
            mySaveFileSensitive = saveFileSensitive + '.txt'
            mySaveFileNoneSensitive = saveFileNoneSensitive + '.txt'
            if self.viewModel:
                print("RUNNING...")
                print("Data Base Path: ", self.dataBase)
                print("Test Data Path: ", self.testFile)
                print("Save Summary Data Path: ", mySaveFile)
                print("Save Sensitive Data Path: ", mySaveFileSensitive)
                print("Save None Sensitive Data Path: ", mySaveFileNoneSensitive)
            self.run_txtFile(mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive)
        if testFileFormat in ['.fa', '.fasta']:
            saveFile, saveFileSensitive, saveFileNoneSensitive = self.getFile()
            mySaveFile = saveFile + testFileFormat
            mySaveFileSensitive = saveFileSensitive + testFileFormat
            mySaveFileNoneSensitive = saveFileNoneSensitive + testFileFormat
            if self.viewModel:
                print("RUNNING...")
                print("Data Base Path: ", self.dataBase)
                print("Test Data Path: ", self.testFile)
                print("Save Summary Data Path: ", mySaveFile)
                print("Save Sensitive Data Path: ", mySaveFileSensitive)
                print("Save None Sensitive Data Path: ", mySaveFileNoneSensitive)
            self.run_fastAFile(mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive)
        if testFileFormat in ['.fq', '.fastq']:
            saveFile, saveFileSensitive, saveFileNoneSensitive = self.getFile()
            mySaveFile = saveFile + testFileFormat
            mySaveFileSensitive = saveFileSensitive + testFileFormat
            mySaveFileNoneSensitive = saveFileNoneSensitive + testFileFormat
            if self.viewModel:
                print("RUNNING...")
                print("Data Base Path: ", self.dataBase)
                print("Test Data Path: ", self.testFile)
                print("Save Summary Data Path: ", mySaveFile)
                print("Save Sensitive Data Path: ", mySaveFileSensitive)
                print("Save None Sensitive Data Path: ", mySaveFileNoneSensitive)
            self.run_fastQFile(mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive)

    def run_txtFile(self, mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive):
        """dealing with *.txt file"""
        writeFile = open(mySaveFile, 'w+')
        writeFileSens = open(mySaveFileSensitive, 'w+')
        writeFileNoneSens = open(mySaveFileNoneSensitive, 'w+')
        writeFile.write(self.testFile + "result" + '\n')
        loadTimeBegin = time.time()
        self.loadData(self.dataBase, self.k_mer)
        writeFile.write("load data time spend: " + str(time.time() - loadTimeBegin) + '\n')
        countSTR = 0
        countSNP = 0
        number = 0
        timeSum = 0
        with open(self.testFile) as mypath:
            # print("oooo")
            while True:
                # time1 = time.time()
                testSeq = mypath.readline().upper().replace('\n', '')
                # print(testSeq)
                if not testSeq:
                    break
                number = number + 1
                time_begin = time.time()
                if self.str_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                    countSTR = countSTR + 1
                    timeSum = timeSum + time.time() - time_begin
                    writeFileSens.write(testSeq + '\n')
                    writeFileNoneSens.write("*"*50 + '\n')
                    if self.viewModel:
                        print(str(number) + " str " + testSeq)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                    continue
                if self.snp_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                    countSNP = countSNP + 1
                    timeSum = timeSum + time.time() - time_begin
                    writeFileSens.write(testSeq + '\n')
                    writeFileNoneSens.write("*"*50 + '\n')
                    if self.viewModel:
                        print(str(number) + " snp " + testSeq)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                    continue
                timeSum = timeSum + time.time() - time_begin
                writeFileNoneSens.write(testSeq + '\n')
                writeFileSens.write("*"*50 + '\n')
                if self.viewModel:
                    print(str(number) + " none " + testSeq)
                    print("time spend: ", (time.time() - time_begin))
                    print()
        if self.viewModel:
            print("*"*70)
            print("THE RESULT:")
            print("str number is: " + str(countSTR))
            print("snp number is: " + str(countSNP))
            print("total number is：" + str(number))
            print("time spend is: " + str(timeSum))
            print("running over")
            print("*" * 70)
        writeFile.write("str number is: " + str(countSTR) + '\n')
        writeFile.write("snp number is: " + str(countSNP) + '\n')
        writeFile.write("total number is：" + str(number) + '\n')
        writeFile.write("time spend is: " + str(timeSum) + '\n')
        writeFile.close()
        writeFileNoneSens.close()
        writeFileSens.close()
        mypath.close()

    def run_fastAFile(self, mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive):
        """for *FASTA file """
        writeFile = open(mySaveFile, 'w+')
        writeFileSens = open(mySaveFileSensitive, 'w+')
        writeFileNoneSens = open(mySaveFileNoneSensitive, 'w+')
        writeFile.write(self.testFile + "result" + '\n')
        loadTimeBegin = time.time()
        self.loadData(self.dataBase, self.k_mer)
        writeFile.write("load data time spend: " + str(time.time() - loadTimeBegin) + '\n')
        countSTR = 0
        countSNP = 0
        number = 0
        timeSum = 0
        with open(self.testFile) as mypath:
            head =  mypath.readline()
            writeFileSens.write(head + '\n')
            writeFileNoneSens.write(head + '\n')
            if self.viewModel:
                print("[number, len(sourceLine), sourceLine]")
            while True:
                sourceLine = mypath.readline().replace("\n", "")
                line = sourceLine.upper().replace('\n', '')
                if not line:
                    break
                number = number + 1
                lineLen = len(line)
                if lineLen < 50:
                    writeFileNoneSens.write(sourceLine + '\n')
                    writeFileSens.write("*"*len(sourceLine) + '\n')
                    continue
                index = 0
                time_begin = time.time()
                flag = 0
                while index < lineLen:
                    testSeq = line[index: index+50]
                    index = index + 50
                    if self.str_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                        countSTR = countSTR + 1
                        flag = 1
                        break
                    if self.snp_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                        countSNP = countSNP + 1
                        flag = 1
                        break

                timeSum = timeSum + time.time() - time_begin
                if self.viewModel:
                    if flag == 1:
                        print(number, "sensitive ----> length: ", len(sourceLine), sourceLine)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                    else:
                        print(number, "none ----> length: ", len(sourceLine), sourceLine)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                if flag == 1:
                    writeFileSens.write(sourceLine + '\n')
                    writeFileNoneSens.write("*"*len(sourceLine) + '\n')
                else:
                    writeFileNoneSens.write(sourceLine + '\n')
                    writeFileSens.write("*"*len(sourceLine) + '\n')

        if self.viewModel:
            print("*"*70)
            print("THE RESULT:")
            print("str number is: " + str(countSTR))
            print("snp number is: " + str(countSNP))
            print("total number is：" + str(number))
            print("time spend is: " + str(timeSum))
            print("running over")
            print("*" * 70)
        writeFile.write("str number is: " + str(countSTR) + '\n')
        writeFile.write("snp number is: " + str(countSNP) + '\n')
        writeFile.write("total number is：" + str(number) + '\n')
        writeFile.write("time spend is: " + str(timeSum) + '\n')
        writeFileSens.close()
        writeFile.close()
        writeFileNoneSens.close()
        mypath.close()

    def run_fastQFile(self, mySaveFile, mySaveFileSensitive, mySaveFileNoneSensitive):
        """for *FASTA file """
        writeFile = open(mySaveFile, 'w+')
        writeFileSens = open(mySaveFileSensitive, 'w+')
        writeFileNoneSens = open(mySaveFileNoneSensitive, 'w+')
        writeFile.write(self.testFile + "result" + '\n')
        loadTimeBegin = time.time()
        self.loadData(self.dataBase, self.k_mer)
        writeFile.write("load data time spend: " + str(time.time() - loadTimeBegin) + '\n')
        countSTR = 0
        countSNP = 0
        number = 0
        timeSum = 0
        with open(self.testFile) as mypath:
            while True:
                line1 = mypath.readline().replace("\n","")
                sourceLine = mypath.readline().replace("\n","")
                line3 = mypath.readline().replace("\n", "")
                line4 = mypath.readline().replace("\n", "")
                if not sourceLine:
                    break
                number = number + 1
                line = sourceLine.upper().replace('\n', '')
                lineLen = len(line)
                if lineLen < 50:
                    writeFileNoneSens.write(line1 + '\n')
                    writeFileNoneSens.write(sourceLine + '\n')
                    writeFileNoneSens.write(line3 + '\n')
                    writeFileNoneSens.write(line4 + '\n')
                    writeFileSens.write("*" * len(line1) + '\n')
                    writeFileSens.write("*" * len(sourceLine) + '\n')
                    writeFileSens.write("*" * len(line3) + '\n')
                    writeFileSens.write("*" * len(line4) + '\n')
                    continue
                index = 0
                time_begin = time.time()
                flag = 0
                while index < lineLen:
                    testSeq = line[index: index + 50]
                    index = index + 50
                    if self.str_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                        countSTR = countSTR + 1
                        flag = 1
                        break
                    if self.snp_finder(self.sim, self.k_mer, self.similarFunc, testSeq):
                        countSNP = countSNP + 1
                        flag = 1
                        break

                timeSum = timeSum + time.time() - time_begin
                if self.viewModel:
                    if flag == 1:
                        print(number, "sensitive ----> length: ", len(sourceLine), sourceLine)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                    else:
                        print(number, "none ----> length: ", len(sourceLine), sourceLine)
                        print("time spend: ", (time.time() - time_begin))
                        print()
                if flag == 1:
                    writeFileSens.write(line1 + '\n')
                    writeFileSens.write(sourceLine + '\n')
                    writeFileSens.write(line3 + '\n')
                    writeFileSens.write(line4 + '\n')
                    writeFileNoneSens.write("*" * len(line1) + '\n')
                    writeFileNoneSens.write("*" * len(sourceLine) + '\n')
                    writeFileNoneSens.write("*" * len(line3) + '\n')
                    writeFileNoneSens.write("*" * len(line4) + '\n')
                else:
                    writeFileNoneSens.write(line1 + '\n')
                    writeFileNoneSens.write(sourceLine + '\n')
                    writeFileNoneSens.write(line3 + '\n')
                    writeFileNoneSens.write(line4 + '\n')
                    writeFileSens.write("*" * len(line1) + '\n')
                    writeFileSens.write("*" * len(sourceLine) + '\n')
                    writeFileSens.write("*" * len(line3) + '\n')
                    writeFileSens.write("*" * len(line4) + '\n')

            if self.viewModel:
                print("*" * 70)
                print("THE RESULT:")
                print("str number is: " + str(countSTR))
                print("snp number is: " + str(countSNP))
                print("total number is：" + str(number))
                print("time spend is: " + str(timeSum))
                print("running over")
                print("*" * 70)
            writeFile.write("str number is: " + str(countSTR) + '\n')
            writeFile.write("snp number is: " + str(countSNP) + '\n')
            writeFile.write("total number is：" + str(number) + '\n')
            writeFile.write("time spend is: " + str(timeSum) + '\n')
            writeFileSens.close()
            writeFile.close()
            writeFileNoneSens.close()
            mypath.close()

    def getParametersInfo(self):
        """this func is used to print parameters of Anteater algorithm"""
        print("*"*70)
        print("THE PARAMETERS: ")
        print("dataBase source: ", self.dataBase)
        print("testFile source: ", self.testFile)
        print("parameter of similarFunc: ", self.similarFunc)
        print("parameters of k_mer: ", self.k_mer)
        if self.similarFunc == 1:
            print("parameter of similarFunc: ", "Pearson correlation coefficient")
        if self.similarFunc == 2:
            print("parameter of similarFunc: ", "Spearman correlation coefficient")
        if self.similarFunc == 3:
            print("parameter of similarFunc: ", "Manhattan distance")
        if self.similarFunc == 4:
            print("parameter of similarFunc: ", "Edit distance algorithm")
        if self.similarFunc == 5:
            print("parameter of similarFunc: ", "Shift-hamming distance")
        print("*" * 70)

    def sourceDataCheck(self):
        """check testData file format"""
        if os.path.splitext(self.testFile)[1] not in [".fa", ".fq", ".txt", ".fasta", ".fastq"]:
            raise Exception('err! file format should be "*.fa", "*.fq", "*.txt"')
        return os.path.splitext(self.testFile)[1]

    def getDict(self, k_mer=4):
        """get encode dict, default parameter is 4 """
        if k_mer > 7:
            raise Exception('k_mer should <= 7')
        myDict = {}
        if k_mer == 1:
            for i in ['A', 'C', 'G', 'T']:
                myDict[i] = 0
        if k_mer == 2:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    myDict[i + j] = 0
        if k_mer == 3:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    for k in ['A', 'C', 'G', 'T']:
                        myDict[i + j + k] = 0
        if k_mer == 4:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    for k in ['A', 'C', 'G', 'T']:
                        for l in ['A', 'C', 'G', 'T']:
                            myDict[i + j + k + l] = 0
        if k_mer == 5:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    for k in ['A', 'C', 'G', 'T']:
                        for l in ['A', 'C', 'G', 'T']:
                            for m in ['A', 'C', 'G', 'T']:
                                myDict[i + j + k + l + m] = 0
        if k_mer == 6:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    for k in ['A', 'C', 'G', 'T']:
                        for l in ['A', 'C', 'G', 'T']:
                            for m in ['A', 'C', 'G', 'T']:
                                for n in ['A', 'C', 'G', 'T']:
                                    myDict[i + j + k + l + m + n] = 0
        if k_mer == 7:
            for i in ['A', 'C', 'G', 'T']:
                for j in ['A', 'C', 'G', 'T']:
                    for k in ['A', 'C', 'G', 'T']:
                        for l in ['A', 'C', 'G', 'T']:
                            for m in ['A', 'C', 'G', 'T']:
                                for n in ['A', 'C', 'G', 'T']:
                                    for o in ['A', 'C', 'G', 'T']:
                                        myDict[i + j + k + l + m + n + o] = 0
        return myDict

    def encodeString(self, k_mer, read):
        myTemplate = self.getDict(k_mer)
        for index in range(len(read) - k_mer):
            temp = str(read[index:index + k_mer])
            if temp in myTemplate:
                myTemplate[temp] = myTemplate[temp] + 1
        result = []
        for index in myTemplate:
            result.append(myTemplate[index])
        return result

    def pearson(self, k_mer, refSeq, readSeq):
        """Pearson correlation coefficient"""
        if type(refSeq) is str:
            encodeRefSeq = self.encodeString(k_mer, refSeq)
        else:
            encodeRefSeq = refSeq
        encodeReadSeq = self.encodeString(k_mer, readSeq)
        X1 = pd.Series(encodeRefSeq)
        Y1 = pd.Series(encodeReadSeq)
        #print((1+X1.corr(Y1, method="pearson"))/2)
        return  X1.corr(Y1, method="pearson")

    def spearman(self, k_mer, refSeq, readSeq):
        """Spearman correlation coefficient"""
        if type(refSeq) is str:
            encodeRefSeq = self.encodeString(k_mer, refSeq)
        else:
            encodeRefSeq = refSeq
        #encodeRefSeq = encodeString(k_mer, refSeq)
        encodeReadSeq = self.encodeString(k_mer, readSeq)
        X1 = pd.Series(encodeRefSeq)
        Y1 = pd.Series(encodeReadSeq)
        return X1.corr(Y1, method="spearman")

    def kendall(self, k_mer, refSeq, readSeq):
        """Kendall correlation coefficient"""
        if type(refSeq) is str:
            encodeRefSeq = self.encodeString(k_mer, refSeq)
        else:
            encodeRefSeq = refSeq
        encodeRefSeq = self.encodeString(k_mer, refSeq)
        encodeReadSeq = self.encodeString(k_mer, readSeq)
        X1 = pd.Series(encodeRefSeq)
        Y1 = pd.Series(encodeReadSeq)
        return (X1.corr(Y1, method="kendall"))  # 肯德尔相关性系数

    def edit_distance(self, word1, word2):
        """Edit distance algorithm"""
        len1 = len(word1)
        len2 = len(word2)
        dp = np.zeros((len1 + 1, len2 + 1))
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                delta = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        return (len(word1)-dp[len1][len2])/len(word1)

    def shift_hanming(self, readSeq, refSeq, numberOfE=3, threshold=0.64, readLength=50, grideSize=4):
        """Ptsa source code"""
        hanmingMask = np.zeros([2 * numberOfE + 1, readLength])
        reSultMatrix = np.zeros(readLength)
        count = 0
        for i in range(readLength):
            if (readSeq[i] == refSeq[i]):
                hanmingMask[numberOfE][i] = 1
                count = count + 1
        if (count >= threshold):
            return float(count / readLength)
        # building hanming matrix
        for i in range(numberOfE):
            count1 = 0
            count2 = 0
            for j in range(readLength):
                # insert redSed is a string which needed to match refSeq(左移)
                if (((i + j + 1) < readLength) and (readSeq[i + j + 1] == refSeq[j])):
                    hanmingMask[i][j] = 1
                    count1 = count1 + 1
                # delete (右移)
                if (((j + i + 1) < readLength) and (readSeq[j] == refSeq[j + i + 1])):
                    hanmingMask[i + numberOfE + 1][j + i + 1] = 1
                    count2 = count2 + 1
            if (count1 >= threshold):
                return float(count1 / readLength)
            if (count2 >= threshold):
                return float(count2 / readLength)
        # hanming matrix buiding over
        # build slid window for detecte sequential 1
        count = 0
        for i in range(readLength - grideSize + 1):
            slideWindow = hanmingMask[:, i:i + grideSize]
            for j in range(2 * numberOfE + 1):
                if (all(slideWindow[j] == [1, 1, 1, 1])):
                    reSultMatrix[i:i + grideSize] = slideWindow[j]
                elif (all(slideWindow[j] == [1, 1, 1, 0])):
                    reSultMatrix[i:i + grideSize] = slideWindow[j]
                elif (all(slideWindow[j] == [1, 1, 1, 0])):
                    reSultMatrix[i:i + grideSize] = slideWindow[j]
        for i in range(readLength):
            if (reSultMatrix[i] == 1):
                count = count + 1
        return float(count / readLength)

    def manhattan(self, k_mer, refSeq, readSeq):
        """Manhattan distance"""
        if type(refSeq) is str:
            encodeRefSeq = self.encodeString(k_mer, refSeq)
        else:
            encodeRefSeq = refSeq
        encodeRefSeq = self.encodeString(k_mer, refSeq)
        encodeReadSeq = self.encodeString(k_mer, readSeq)
        result = 0
        for index in range(len(encodeRefSeq)):
            result = result + abs(encodeRefSeq[index]-encodeReadSeq[index])
        return 1-result/len(encodeReadSeq)

    def countingGAC(self, line):
        """counting GCA"""
        return  float(line.count('A') / len(line)),\
                float(line.count('G') / len(line)), float(line.count('C') / len(line))

    def loadData(self, knowledgeDataPath, kmer):
        global knowledgeData
        myDict = self.getDict(kmer)
        knowledgeData = []
        number = 0
        with open(knowledgeDataPath) as file:
            while True:
                line = file.readline().upper().replace('\n', '')
                if not line:
                    break
                A, G, C = float(line.count('A') / len(line)), float(line.count('G') / len(line)), \
                          float(line.count('C') / len(line))
                knowledgeData.append([number, A, G, C, line, self.encodeString(kmer, line)])
                number = number + 1
        file.close()
        knowledgeData = pd.DataFrame(knowledgeData, columns=['Number', 'A', 'G', 'C', 'Read', 'Encoding']) \
            .sort_values(by=['A', 'G', 'C'], axis=0, ascending=[True, True, True])
        if self.viewModel:
            print("knowledge data shape is:")
            print(knowledgeData.shape)
            print("load knowledgeDataBase successfuly!")

    def queryPos(self, A, G, C):
        """get query data"""
        thresholdOfQueryBlock = 0.04  # 0.1, 0.05
        data = knowledgeData[
            (knowledgeData.A >= A - thresholdOfQueryBlock) & (knowledgeData.A <= A + thresholdOfQueryBlock) &
            (knowledgeData.C >= C - thresholdOfQueryBlock) & (knowledgeData.C <= C + thresholdOfQueryBlock) &
            (knowledgeData.G >= G - thresholdOfQueryBlock) & (knowledgeData.G <= G + thresholdOfQueryBlock)]
        return data

    def str_finder(self, sim, kmer, simFunc, readSeq):
        window_one = readSeq[self.window + 1:self.window * 2]
        window_two = readSeq[self.window * 2 + 1:self.window * 3]
        if simFunc == 1 and self.pearson(kmer, window_one, window_two) >= sim:
            return 1
        if simFunc == 2 and self.spearman(kmer, window_one, window_two) >= sim:
            return 1
        if simFunc == 3 and self.manhattan(kmer, window_one, window_two) >= sim:
            return 1
        if simFunc == 4 and self.edit_distance(window_one, window_two) >= sim:
            return 1
        if simFunc == 5 and self.shift_hanming(window_one, window_two, 3, sim, self.window - 1, 4) >= sim:
            return 1
        return 0

    def snp_finder(self, sim, kmer, simFunc, readSeq):
        # 第一步，根据碱基含量进行相似性查询
        A, G, C = self.countingGAC(readSeq)
        # 第二步： 得到相似性查询块
        data = self.queryPos(A, G, C)
        # 第三步： 进行相似性比对
        for index in range(len(data)):
            if simFunc == 1 and self.pearson(kmer, data.iloc[index][5], readSeq) >= sim:
                return 1
            if simFunc == 2 and self.spearman(kmer, data.iloc[index][5], readSeq) >= sim:
                return 1
            if simFunc == 3 and self.manhattan(kmer, data.iloc[index][5], readSeq) >= sim:
                return 1
            if simFunc == 4 and self.edit_distance(data.iloc[index][4], readSeq) >= sim:
                return 1
            if simFunc == 5 and self.shift_hanming(data.iloc[index][4], readSeq, 3, sim, 50 - 1, 4) >= sim:
                return 1
        return 0

    def getFile(self):
        PROJRCT_ROOT_DIR = os.getcwd()
        run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
        path = os.path.join(PROJRCT_ROOT_DIR, "result", run_id)
        os.makedirs(path, exist_ok=True)
        saveFile = path + "/Summary"
        saveFileSensitive = path + "/Sensitive"
        saveFileNoneSensitive = path + "/NoneSensitive"
        return saveFile, saveFileSensitive, saveFileNoneSensitive

def help():
    print("using::")
    print("anteater = Anteater(testFile=XXX, similarFunc=XXX, k_mer=XXX, viewModel=XXX)")
    print("testFile : support ---> [*.fa, *.fasta, *fq, *fastq, *.txt]")
    print("similarFunc: support ---> [1, 2, 3, 4, 5] ---> [person, spearman, manhattan, edit, shift-hanming]")
    print("k_mer: support ---> [1, 2, 3, 4, 5, 6, 7]")
    print("viewModel: support ---> [0, 1] ---> [False, True]")
