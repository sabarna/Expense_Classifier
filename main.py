import pandas as pd
import re
import gQuery
import CategoryDictionary
import operator
import time
import matplotlib.pyplot as plt
from matplotlib import colors
from pylab import *

dict = {}
expenseType = []
cum_expense_list = []
validExpenseType = []
keywords = []
wordFreqDict = {}
finalDict = { 'Entertainment': 0 ,
              'Education':0,
              'Shopping':0,
              'Personal Care':0,
              'Health & Fitness':0,
              'Kids' :0,
              'Auto & Transport' :0,
              'ATM withdrawals' :0,
              'Money Transfers' :0,
              'Grocery' :0,
              'Dining' :0,
              'Tax'   :0,
              'Unclassified':0}
colorMap = {
            'Entertainment': 'red' ,
              'Education':'green',
              'Shopping':'lightcoral',
              'Personal Care':'pink',
              'Health & Fitness':'beige',
              'Kids' :'darkorange',
              'Auto & Transport' :'black',
              'ATM withdrawals' :'brown',
              'Money Transfers' :'moccasin',
              'Grocery' :'cadetblue',
              'Dining' :'deepskyblue',
              'Tax'   :'cyan',
              'Unclassified':'dimgray'

            }





validTags = ['NN','NNP','PRON','JJ','VBZ','RB','DET','PRT']
random_words = ['CHECKCARD']
stmt = pd.read_csv('/Users/sabarnachoudhuri/Desktop/stmt.csv')
stmt = stmt[stmt.Amount < 0]


numberOfTransactions  = stmt.Description.count()

def validateWord(word):
    if(word.isupper() and word.isdigit() != True and word not in random_words):
        return 1

def getValidtext(text):
    x = " "
    for word in text.split():
        if(validateWord(word)):
            x = x + ' ' + word
    return x

def removearticles(text):
  return re.sub('\s+(a|an|and|the)(\s+)', '\2', text)

def getMaxVoted(dict):
    return max(dict.items(), key=operator.itemgetter(1))[0]





def initDictFreq():
    dictfreq = { 'Entertainment': 0 ,
              'Education':0,
              'Shopping':0,
              'Personal Care':0,
              'Health & Fitness':0,
              'Kids' :0,
              'Auto & Transport' :0,
              'ATM withdrawals' :0,
              'Money Transfers' :0,
              'Grocery' :0,
              'Dining' :0,
              'Tax'   :0,
              'Unclassified':0}
    return dictfreq


for index, row in stmt.iterrows():
    dictfreq = initDictFreq()
    validText = getValidtext(removearticles(row.Description))

    scrapeList = set(gQuery.searchString(validText))
    unclassified = 1
    for scrapeWord in scrapeList:
        scrapeWord = removearticles(scrapeWord)
        for sw in scrapeWord.split(" "):
            for k, v in CategoryDictionary.CategoryDict.items():
                for value in v:
                    if(sw == value):
                        if(k == "Education"):
                            print("right here !!!")
                        dictfreq[k] += 1
                        unclassified = 0

    if unclassified == 1:
        finalDict['Unclassified']  += row.Amount

    ind  = getMaxVoted(dictfreq)
    finalDict[ind] += row.Amount

label =[]
color = []
expenditure = []

for key, value in finalDict.items():
    if(value != 0):
        label.append(key)
        color.append(colorMap[key])
        expenditure.append(value)

print(str(label) + "..." + str(expenditure))
'''pie(expenditure, labels = label)
title('Resultant Pie Chart', bbox={'facecolor':'0.8', 'pad':5})

plt.show()
''' 