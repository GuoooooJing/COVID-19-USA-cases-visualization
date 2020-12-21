from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
import state_code
from state_code import SAMPLE
import collections
import plotly.graph_objects as go
import plotly.express as px


files = os.listdir('./us_dataset/')
files.sort()
output_df = []
entire = pd.DataFrame(columns=['code','state','total_confirmed', 'death', 'recovered','testing_rate', 'hosp_rate', 'mortality_rate', 'date', 'testing_2'])
number = 1
for i in files:
    #print(i)
    total = {}
    raw_df = pd.read_csv('./us_dataset/'+i).fillna(0)

    country = 'Country_Region'
    state = 'Province_State'
    check = raw_df[country] == 'US'
    df = raw_df[check]

    for _, row in df.iterrows():
        us_state = row[state]
        if us_state not in state_code.CODE:
            #print(us_state)
            continue
        #print(row[state],i)
        if us_state in total:
            #print(total[temp])
            total[us_state][0] += row['Confirmed']
            total[us_state][1] += row['Deaths']
            total[us_state][2] += row['Recovered']
            total[us_state][3] += row['Testing_Rate'].astype(float)
            total[us_state][3] += row['Hospitalization_Rate']
            total[us_state][3] += row['Mortality_Rate']
        else:
            total[us_state] = [row['Confirmed'],row['Deaths'], row['Recovered'], row['Testing_Rate'], row['Hospitalization_Rate'], row['Mortality_Rate']]
            
    usa_df = pd.DataFrame(columns=['code','state','total_confirmed', 'death', 'recovered','testing_rate', 'hosp_rate', 'mortality_rate', 'date'])


    for j in total:
        a_row = [state_code.CODE[j], j] + total[j] + [i[:10],total[j][3]**(0.5)]
        leng = len(entire)
        #usa_df.loc[leng] = a_row
        entire.loc[leng] = a_row
        #row_df = pd.DataFrame([a_row])
        # usa_df = usa_df.append(a_row, ignore_index=True)
    number += 1
    #print(usa_df)
    output_df.append(usa_df.fillna(0))



entire["total_confirmed"] = pd.to_numeric(entire.total_confirmed, errors='coerce')
entire["death"]= pd.to_numeric(entire.death, errors='coerce')
# mortality_rate w/ Greys
# testing_rate w/ Greens and color bar
# hosp_rate w/ Peach
#print(entire.dtypes)

### Hospitalization Rate
COLOR = px.colors.sequential.Peach
COLUMN = 'hosp_rate'
fig = px.choropleth(entire,  locations='code', scope='usa', color=COLUMN, title='COVID-19 US Data Visualization with Hospitalization Rate data', 
color_continuous_scale = COLOR, locationmode="USA-states", hover_name=COLUMN, animation_frame='date')

### Mortality  Rate
# COLOR = px.colors.sequential.Greys
# COLUMN = 'mortality_rate'
# fig = px.choropleth(entire,  locations='code', scope='usa', color=COLUMN, title='COVID-19 US Data Visualization with Mortality Rate data', 
# color_continuous_scale = COLOR, locationmode="USA-states", hover_name=COLUMN, animation_frame='date')

### Testing Rate
# COLOR = px.colors.sequential.Greens
# COLUMN = 'testing_rate'
# fig = px.choropleth(entire,  locations='code', scope='usa', color='testing_2', title='COVID-19 US Data Visualization with Testing Cases data (per 100000 people)', 
# color_continuous_scale = COLOR, locationmode="USA-states", hover_name=COLUMN, animation_frame='date')
# fig.layout.coloraxis['colorbar'] = dict(
#         title = {'text':COLUMN},
#         tickvals=[0, 28, 56, 84, 112, 141],
#         ticktext=["0" ,"800", "3100", "7000", "12500", "20000"])
# fig.layout.coloraxis['cmax'] = 141
# fig.layout.coloraxis['cmin'] = 0


fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.write_html('./demo/'+COLUMN+'.html')
fig.show()
print("finished")