#!/usr/bin/env python
# coding: utf-8

# # COVID-19 predictive analysis
# 
# > * Hang Gu S2124920/1
# 
# ----

# # Foreword
# The world's COVID-19 in 2021 is still very serious. This project mainly analyzes the epidemic situation in China. We will analyze expectations through different analysis methods, and visually display the epidemic through different charts. In this way, we can obtain more scientific results. And based on this result, we can predict the expected trend and take precautionary measures in advance.

# # Analysis steps
# ## import library

# In[3]:


import time
import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.ensemble import RandomForestClassifier #for the model
from sklearn.tree import export_graphviz #plot tree
from sklearn.metrics import roc_curve, auc #for model evaluation
from sklearn.metrics import classification_report #for model evaluation
from sklearn.metrics import confusion_matrix #for model evaluation
from sklearn.model_selection import train_test_split #for data splitting
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# ## Get data source
# For this project, I use Python crawler technology to obtain real-time epidemic data from Tencent's website, so as to ensure that the data is updated in time.

# In[4]:


def catch_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    #Return data dictionary
    data = json.loads(reponse['data'])
    return data
data = catch_data()
data.keys()
lastUpdateTime = data['lastUpdateTime']
chinaTotal = data['chinaTotal']
chinaAdd = data['chinaAdd']
print(chinaTotal)
print("......")
print(chinaAdd)


# ## The pie chart of the national total is drawn

# 1.Pie chart of the epidemic today

# In[5]:


from pyecharts.charts import Pie
import pyecharts.options as opts
(
    Pie(init_opts=opts.InitOpts(width='720px',height='320px'))#默认900，600
    .add(series_name='', data_pair=[list(z) for z in zip(chinaTotal.keys(), chinaTotal.values())])#饼图
 
).render_notebook()


# 2.Pie chart of yesterday's data:

# In[6]:


from pyecharts.charts import Pie
import pyecharts.options as opts
(
    Pie(init_opts=opts.InitOpts(width='720px',height='320px'))#默认900，600
    .add(series_name='', data_pair=[list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())])#饼图

).render_notebook()


# # Map the data of all parts of the country

# ## 1.Obtaining Data Details

# In[18]:


import time
import json
import requests
from datetime import datetime
import pandas as pd
import numpy as np
def catch_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    #Return data dictionary
    data = json.loads(reponse['data'])
    return data
data = catch_data()
data.keys()
lastUpdateTime = data['lastUpdateTime']
# Data details, data structure is more complex, step by step to print out to see, first understand the data structure
areaTree = data['areaTree']
# Chinese domestic data
china_data = areaTree[0]['children']
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']
    province_list = china_data[a]['children']
    for b in range(len(province_list)):
        city = province_list[b]['name']
        total = province_list[b]['total']
        today = province_list[b]['today']
        china_dict = {}
        china_dict['province'] = province
        china_dict['city'] = city
        china_dict['total'] = total
        china_dict['today'] = today
        china_list.append(china_dict)

china_data = pd.DataFrame(china_list)
china_data.head()


# ## 2. Data processing
# 
# Note: Since the data this time is different from the previous ones, I will only filter the data I need to use.

# In[8]:


# 定义数据处理函数
def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm
def dead(x):
    dead = eval(str(x))['dead']
    return dead
def heal(x):
    heal =  eval(str(x))['heal']
    return heal
# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data = china_data[["province","city","confirm","dead","heal"]]
china_data.head()


# ## 3. Extract the data we need

# In[9]:


area_data = china_data.groupby("province")["confirm"].sum().reset_index()
area_data.columns = ["province","confirm"]
print(area_data )


# ## 4.Mapping the epidemic

# In[13]:


from pyecharts.charts import Map
import pyecharts.options as opts
from pyecharts.globals import ChartType

(
    Map()
    .add("",[list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",is_map_symbol_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="Map of the total number of confirmed cases of COVID-19 in China in 2021"),visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                pieces = [
                    
                        {"min": 5000 , "label": '>5000',"color": "#893448"}, #不指定 max，表示 max 为无限大
                        {"min": 1000, "max": 4999, "label": '1000-4999',"color" : "#ff585e" },
                        {"min": 500, "max": 999, "label": '500-1000',"color": "#fb8146"},
                        {"min": 101, "max": 499, "label": '101-499',"color": "#ffA500"},
                        {"min": 10, "max": 100, "label": '10-100',"color": "#ffb248"},
                        {"min": 0, "max": 9, "label": '0-9',"color" : "#fff2d1" }]))

).render_notebook()


# In[ ]:




