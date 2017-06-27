from packages import *

df= pd.read_csv('test_sh.csv')
df['Amount'] = df['Amount']
print(type(df['Amount']))
#df['Amount'] = df['Amount'].astype(float)
df['Payee'] = df['Payee']
print(list(df.columns.values))
#df = df[df['Amount'] <0]

#df = df.head(20)

#dict = dict(zip(df['Payee'],df['Amount']))



def initCatVote():
    CategoryVote = { 'Entertainment':0,'Education': 0,'Shopping':0,'Personal Care':0,'Health & Fitness':0,'Kids':0,'Auto & Transport' :0,
                 'ATM withdrawals':0, 'Money Transfers' :0, 'Grocery' :0,'Dining' :0,'Tax':0,'OnlineTransaction':0,'Miscellaneous':0 }
    return CategoryVote


def createTrnsDict(df):
    temp_dict_tmp = dict(zip(df['Payee'],df['Amount']))
    #temp_dict_tmp = dict(zip(df['Description'],df['Amount']))
    temp_dict = removeOutliers(temp_dict_tmp)
    return temp_dict


def removeOutliers(tmp_dict):
    l = []
    for k, v in  tmp_dict.items():
        l.append(v)
    tmp_dict_mean = np.mean(l)
    tmp_dict_sd = np.std(l)
    print("~~~MEAN~~~"+ str(tmp_dict_mean))
    print("~~~SD~~~"+ str(tmp_dict_sd))
    tmp_dict_ret = {k: v for k, v in tmp_dict.items() if abs((v-tmp_dict_mean)/tmp_dict_sd) < 3 }
    return tmp_dict_ret




def validateWord(word):
    if(word.isupper() and word.isdigit() != True):
        return 1

def getValidtext(text):
    x = " "
    for word in text.split():
        if(validateWord(word)):
            x = x + ' ' + word
    return x


def prelimSearch(trns, CategoryVote):
    trns_list = trns.split()
  #  print(trns_list)
    for t in trns_list:
        for category, list in CategoryDict.items():
            if t.lower() in list:
                CategoryVote[category] += 1
                return 1
            if '.com' in t.lower():
                CategoryVote['OnlineTransaction'] += 1
                return 1
            elif 'www' in t.lower():
                CategoryVote['OnlineTransaction'] += 1
                return 1
            else :
                continue
    return 0;


def parseResuts(results):
    crumbList = []
    for result in results:
        if 'pagemap' in result.keys():
            if 'breadcrumb' in result['pagemap']:
                for l in result['pagemap']['breadcrumb']:
                    if 'title' in l.keys():
                       # print(l['title'])
                        crumbList.append(l['title'])
    returnList = set(crumbList)
    return returnList



def secondarySearch(trns, CategoryVote):
    results = google_search(trns, my_api_key, my_cse_id, num=10)
    if results == "Not found":
        searchTerms = []
    else:
        searchTerms = parseResuts(results)
    for t in searchTerms:
        for t_split in t.split():
            for category, list in CategoryDict.items():
                if t_split.lower() in list:
                    CategoryVote[category] += 1
                    return 1
                else :
                    continue
    return 0;



def idCategory(transaction, CategoryVote):
    prelimfound = prelimSearch(transaction,CategoryVote)
    if prelimfound == 1:
        return 1
    else:
        secfound = secondarySearch(transaction, CategoryVote)
        if secfound == 1:
            return 1
        else :
            return 0



def idCategoryList(df):
    trns_dict = createTrnsDict(df)
    df_plt = pd.DataFrame(columns= ['Transaction','Category','Amount'])
    i = 0
    for transaction,value in trns_dict.items():
        CategoryVote = initCatVote()
        transaction = getValidtext(transaction)
      #  print(transaction)
        idbool = idCategory(transaction, CategoryVote)
        if idbool == 0:
            CategoryVote['Miscellaneous'] += 1
        trns_category = max(CategoryVote.items(), key=operator.itemgetter(1))[0]
       # print("*****" + trns_category+ "*****")
        df_plt.loc[i] = [transaction, trns_category, abs(value)]
        i += 1
    return df_plt


def plotpie(df_trns):
    TotalAmnt = df_trns['Amount'].sum()
    grpd_by_cat = df_trns.groupby('Category')['Amount'].sum()
    grpd_by_cat = grpd_by_cat.reset_index()
    grpd_by_cat['Perc'] = grpd_by_cat['Amount']/TotalAmnt
    fig = {
    'data': [{'labels': grpd_by_cat['Category'],
              'values': grpd_by_cat['Perc'],
              'type': 'pie'}],
    'layout': {'title': 'Expense Classification Report'}
     }
    py.plotly.image.save_as(fig, filename='Expenses Classification.png')


df_1 = idCategoryList(df)

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df_1.to_excel(writer, sheet_name='Sheet1')
writer.save()


print(df_1)
plotpie(df_1)