from packages import *



df = pd.read_csv('trans2.csv')

st_abb = pd.read_csv('US_StateAbb.csv')
st_abb['Postal Code'] = st_abb['Postal Code'].str.strip()
df['StateCode'] = df['Address'].str[-3:].str.strip()
df['State'] = pd.merge(left=df,right=st_abb, left_on='StateCode', right_on='Postal Code')['State']




df['text'] = df['StateCode'] + '<br>' + df['Payee']

data =  [ dict(
        type='choropleth',
        #colorscale = scl,
        autocolorscale = True,
        locations = df['StateCode'],
        z = df['Amount'],
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "USD")
        )
]


layout = dict(
        title = 'Location wise Expense Report',
        geo = dict(
            scope='usa',
            projection=dict( type="albers usa"),
            showlakes = True,
            showland = True,
            showsubunits = True,
            lakecolor = 'white',
            landcolor = "black")
             )

fig = go.Figure( data=data, layout=layout )
offline.plot(data,layout)
py.plotly.image.save_as(fig, filename='Expenses by Location.png')
