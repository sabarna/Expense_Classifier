from packages import *



df = pd.read_csv('trans2.csv')


def getDayName(row):
    return calendar.day_name[row['Day_of_Week_Int']]

def getMonthName(row):
    return calendar.month_name[row['Month_Int']]

def createExpensesDataFrame(df):
    expend = df[df['Amount'] < 0]
    expend['Amount'] = abs(expend['Amount']) #assignment warning
    expend['Posted Date'] = pd.to_datetime(expend['Posted Date'])
    expend['Day_of_Week_Int'] = expend['Posted Date'].dt.dayofweek
    expend['Month_Int'] =  expend['Posted Date'].dt.month
    expend['Year'] = expend['Posted Date'].dt.year
    expend['Day of Week'] = expend.apply(getDayName, axis = 1)
    expend['Month'] = expend.apply(getMonthName, axis = 1)
    expend = expend.drop('Day_of_Week_Int', 1)
    expend = expend.drop('Month_Int', 1)
    return expend


def groupByDow(df):
    grpd_by_dow = df.groupby('Day of Week')['Amount'].sum()
    grpd_by_dow = grpd_by_dow.reset_index()
    data = [go.Bar (x = grpd_by_dow['Day of Week'], y = grpd_by_dow['Amount'])]
    layout = go.Layout(title='Group by Day of week', width=800, height=640)
    fig = go.Figure(data = data,layout = layout)
    py.plotly.image.save_as(fig, filename='Expenses by DOW.png')



def groupByMonth(df):
    grpd_by_mnth = df.groupby('Month')['Amount'].sum()
    grpd_by_mnth = grpd_by_mnth.reset_index()
    data = [go.Bar (x = grpd_by_mnth['Month'], y = grpd_by_mnth['Amount'])]
    layout = go.Layout(title='Group by Month', width=800, height=640)
    fig = go.Figure(data = data,layout = layout)
    py.plotly.image.save_as(fig, filename='Expenses by Month.png')


def groupByDate(df):
    grpd_by_date = df.groupby('Posted Date')['Amount'].sum()
    grpd_by_date = grpd_by_date.reset_index()
    data = [go.Scatter(x = grpd_by_date['Posted Date'], y = grpd_by_date['Amount'])]
    layout = go.Layout(title='Group by Date', width=800, height=640)
    fig = go.Figure(data = data,layout = layout)
    py.plotly.image.save_as(fig, filename='Expenses by Date.png')






expend = createExpensesDataFrame(df)
groupByDow(expend)
groupByMonth(expend)
groupByDate(expend)







