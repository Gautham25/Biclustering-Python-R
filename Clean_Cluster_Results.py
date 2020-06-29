import os
import numpy as np
import pandas as pd
import math
import json
from itertools import *

def userquesSimilarity(u,q,delta):
    usersMat = np.zeros([len(u), len(u)], dtype=float)
    quesMat = np.zeros([len(q), len(q)], dtype=float)

    for i in range(0, len(u)):
        for j in range(0, len(u)):
            p = set(u[i]) & set(u[j])
            usersMat[i][j] = math.sqrt(len(u[i]) - len(p))
            # print("Clusters = ", i + 1, " & ", j + 1)
            # print(len(p))

    # print("QUESTIONS")
    for i in range(0, len(q)):
        for j in range(0, len(q)):
            p = set(q[i]) & set(q[j])
            quesMat[i][j] = math.sqrt(len(q[i]) - len(p))

    userFileName = "../RCode/ClusterSimilarity/similarity_users_" + str(delta) + "_delta.txt"
    np.savetxt(userFileName, usersMat, fmt="%.5f", delimiter='\t')
    quesFileName = "../RCode/ClusterSimilarity/similarity_ques_" + str(delta) + "_delta.txt"
    np.savetxt(quesFileName, quesMat, fmt="%.5f", delimiter='\t')

def convertHeaderFormat(st):
    for m in [" ", "-", "(", ")", "&","#",","]:
        st = st.replace(m, ".")
    return st

def writeUsersQuesAns(users,questions,data,delta,cluster):
    # print(delta)
    fileName = open("../RCode/UQA/BCCCRanged/delta0_"+str(delta)+"c"+str(cluster)+".txt","w")
    # print(users)
    # print(questions)
    fileName.write("SubId")
    for k in questions:
        fileName.write("\t"+k)
    fileName.write("\n")
    for u in users:
        userData = data.loc[u]
        fileName.write(u)
        for q in questions:
            fileName.write("\t"+str(userData[q]))
        fileName.write("\n")

def writeBiVocResults(file,users,questions,cluster):
    fileName = open(file,"a+")
    fileName.write("cluster"+cluster+"_"+str(len(questions))+"_"+str(len(users))+"\tblack")
    for i in questions:
        fileName.write("\t"+i)
    for j in users:
        fileName.write("\t"+j)

def cleanResult(allFiles, scoreHeaders, cogHeaders, df):
    for j in allFiles:
        u = []
        q = []
        print(str(j))
        with open("../RCode/Results_Ranged/ResultsWithOutCogHeaders490/" + str(j)) as f:
            content = f.readlines()
        outputFilePath = "../RCode/ClusterResultsRanged/ResultsWithOutCogHeaders490/"
        content = [x.strip() for x in content]
        NoC = int((len(content) - 1) / 3)
        f1 = 1
        temp3 = []
        delta = (content[0].split("=", 1)[1]).strip()
        if not os.path.isdir(outputFilePath):
            os.mkdir(outputFilePath)
        fName = open(outputFilePath + "delta0_" + str(delta) + ".txt", "w")
        fName.write(content[0] + "\n")
        fName.write("Number of clusters = " + str(NoC) + "\n")
        c = 1
        fViz = "./BiVoCResults/VizTest"

        for i in range(1, len(content)):
            if (f1 == 1):
                # print(content[i])
                # print("Hello")
                t = (content[i]).split(",")
                users = "Number of users = " + t[0]
                questions = "Number of questions = " + t[1]
                cluster = "Cluster = " + str(c)
                c = c + 1
                fName.write(cluster + "\n")
                fName.write(users + "\n")
                fName.write(questions + "\n")
                temp3 = []
            elif (f1 == 2):
                temp = (content[i]).split(",")
                u.append(temp)
                temp3.append(temp)
            else:
                temp2 = (content[i]).split(",")
                q.append(temp2)
                d = {"users": temp, "questions": temp2}
                temp3.append(temp2)
                # print(temp3)
                # df = pd.DataFrame(data=d)
                if c-1 != 1:
                    with open(fViz+"d"+str(delta)+".txt","a+") as f:
                        f.write("\n")
                writeBiVocResults(fViz+"d"+str(delta)+".txt",temp,temp2,str(c-1))

                fMat = "../RCode/ClusterResultsMatForm/"
                if not os.path.isdir(fMat):
                    os.mkdir(fMat)
                fMat = open(fMat+"D0_"+str(delta)+"_cluster_"+str(c-1)+".csv","w")
                fName.write("Users")
                fMat.write("Users")

                for y in scoreHeaders:
                    fName.write("\t"+y)
                    fMat.write(","+ y )
                for y in cogHeaders:
                    fName.write("\t"+y)
                    fMat.write(","+y )
                for y in temp2:
                    fName.write("\t"+y)
                fName.write("\tQuestions\n")
                fMat.write("\n")
                # print(temp2)
                writeUsersQuesAns(temp, temp2, df, delta, c - 1)
                for z, y in zip_longest(temp, temp2):
                    if (str(z) == "None"):
                        z = ""
                    if (str(y) == "None"):
                        y = ""

                    if (z != ""):
                        scores = df.loc[str(z)]
                        # cogScores = df2.loc[str(z)]
                        fName.write(str(z))
                        # print(str(z))
                        fMat.write(str(z))
                        for l in scoreHeaders:
                            fName.write("\t"+str(scores[l]) )
                            fMat.write(","+str(scores[l]) )
                            # print(l+" "+str(scores[l]))
                        for l2 in cogHeaders:
                            fName.write("\t"+str(scores[l2]))
                            fMat.write(","+str(scores[l2]))
                        for m in temp2:
                            fName.write("\t"+str(scores[m]))
                        fName.write("\t"+str(y) + "\n")
                        fMat.write("\n")
                    else:
                        fName.write(str(z) + "\t" + str(y) + "\n")
                # fName.write(json.dumps(d))
                fName.write("\n \n")
                f1 = 0
            f1 = f1 + 1
        userquesSimilarity(u, q, delta)


if __name__ == "__main__":
    df = pd.read_csv("../Data/CleanData/BGCData490NewCog.csv")
    df2=pd.read_csv("../Code/CTest.csv")
    x = df["SubId"]
    df = df.set_index("SubId")
    df2 = df2.set_index("SubId")
    # print(df.columns.values)
    # del df['Q4.2-2(MMI)']
    # del df['Q4.3(MMI)']

    colNames = list(df.columns.values)

    for i in range(0,len(colNames)):
        colNames[i] = convertHeaderFormat(colNames[i])

    df.columns = df.columns[:0].tolist() + colNames


    with open("../Data/CleanData/ScoreHeaders.txt") as s:
        scoreHeaders = s.readlines()

    scoreHeaders = [x.strip() for x in scoreHeaders]

    with open("../Data/CleanData/CogHeaders2.txt") as s:
        cogHeaders = s.readlines()

    cogHeaders = [x.strip() for x in cogHeaders]
    cogHeaders.remove("MR_1")
    cogHeaders.remove("MR_2")

    for i in range(0,len(scoreHeaders)):
        scoreHeaders[i] = convertHeaderFormat(scoreHeaders[i])


    allUsers = []
    allFiles = os.listdir("../RCode/Results_Ranged/ResultsWithOutCogHeaders490/")
    cleanResult(allFiles, scoreHeaders, cogHeaders,df)
