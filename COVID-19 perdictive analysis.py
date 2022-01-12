#!/usr/bin/env python
# coding: utf-8

# # COVID-19 predictive analysis
# 
# > * Hang Gu S2124920/1
# 
# ----

# In[56]:


#crawl data
import time
import json
import requests

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)

# Capture real-time json data of Tencent epidemic
data = json.loads(requests.get(url=url).json()['data'])


# In[57]:


#View all keys of data data
print(data.keys())


# In[58]:


#View the information corresponding to the key value, namely the last update time, the total number of epidemics in China, the number of new additions in China, the display of new additions, the display of the increase switch and the area tree
#Take the last update time as an example, let's check it, the rest will not be displayed
data['lastUpdateTime']


# In[59]:


num = data['areaTree'][0]['children']


# In[60]:


# Parse the total number of confirmed cases in each province
#We define a new dictionary total_data to store the number of confirmed cases in each province
total_data = {}
for item in num:
    if item['name'] not in total_data:
        total_data.update({item['name']:0})
    for city_data in item['children']:
        total_data[item['name']] += int(city_data['total']['confirm'])    
print(total_data)


# In[100]:


import matplotlib.pyplot as plt 
import numpy as np
plt.rcParams['font.sans-serif'] = ['simhei']   # Used to display Chinese labels normally

names = total_data.keys()
numbers = total_data.values()
plt.figure(figsize=[10,4])

plt.bar(names,numbers)

plt.xlabel("Region", size=12)
plt.ylabel("Number", fontproperties='SimHei', rotation=90, size=12)
plt.title("Comparison of the number of confirmed cases in different provinces in China", size=16)
plt.xticks(list(names), rotation=90, size=12)
    
plt.show()


# In[62]:


#Know that Beijing is at 0, define the beijing variable
beijing=num[14]


# In[63]:


# Parse the total data of confirmed diagnoses in different areas of Beijing
beijing_children_total_data = {}
for item in beijing['children']:
     if item['name'] not in beijing_children_total_data:
         beijing_children_total_data.update({item['name']:0})
         beijing_children_total_data[item['name']] += int(item['total']['confirm'])
print(beijing_children_total_data)


# In[64]:


# Parse the total data of confirmed diagnoses in different areas of Beijing
bj_names = beijing_children_total_data.keys()
bj_numbers = beijing_children_total_data.values()


# In[65]:


# Drawing
plt.figure(figsize=[10,4])

plt.bar(bj_names,bj_numbers)

plt.xlabel("region", size=12)
plt.ylabel("Number", fontproperties='SimHei', rotation=90, size=12)
plt.title("Comparison of the number of confirmed cases in different areas of Beijing", size=16)
plt.xticks(list(bj_names), rotation=90, size=12)
    
plt.show()


# In[105]:


#Define the hebei variable and view its key-value pairs
hebei=num[31]
hebei.keys()


# In[106]:


#Check all prefecture-level cities in Hebei, you can see that Baoding is 0
hebei['children']


# In[107]:


#Query the data it represents, taking Baoding as an example
hebei['children'][0]


# In[108]:


#Check the number of confirmed cases in various prefecture-level cities in Hebei
hebei_children_total_data = {}
for item in hebei['children']:
     if item['name'] not in hebei_children_total_data:
         hebei_children_total_data.update({item['name']:0})
     hebei_children_total_data[item['name']] += int(item['total']['confirm'])
print(hebei_children_total_data)


# In[109]:


#Draw a comparison chart of the number of confirmed cases in various prefecture-level cities
hb_names = hebei_children_total_data.keys()
hb_numbers = hebei_children_total_data.values()
plt.figure(figsize=[10,4])

plt.bar(hb_names,hb_numbers)

plt.xlabel("region", size=12)
plt.ylabel("Number", fontproperties='SimHei', rotation=90, size=12)
plt.title("Comparison of the number of confirmed epidemic cases in mainland-level cities in Hebei Province", size=16)
plt.xticks(list(hb_names), rotation=90, size=12)
    
plt.show()


# In[144]:


# Parse the diagnosis data
total_data = {}
for item in num:
    if item['name'] not in total_data:
        total_data.update({item['name']:0})
    for city_data in item['children']:
        total_data[item['name']] +=int(city_data['total']['confirm'])    
print(total_data)


# Parse death data
total_dead_data = {}
for item in num:
    if item['name'] not in total_dead_data:
        total_dead_data.update({item['name']:0})
    for city_data in item['children']:
        total_dead_data[item['name']] +=int(city_data['total']['dead'])    
print(total_dead_data)

# Parse cure data
total_heal_data = {}
for item in num:
    if item['name'] not in total_heal_data:
        total_heal_data.update({item['name']:0})
    for city_data in item['children']:
        total_heal_data[item['name']] +=int(city_data['total']['heal'])    
print(total_heal_data)

# Parse the newly diagnosed data
total_new_data = {}
for item in num:
    if item['name'] not in total_new_data:
        total_new_data.update({item['name']:0})
    for city_data in item['children']:
        total_new_data[item['name']] +=int(city_data['today']['confirm']) # today    
print(total_new_data)


# In[146]:


#------------------------------------------------------------------------------
#Step 2: Draw a histogram
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt 
import numpy as np

plt.figure(figsize=[10,6])
plt.rcParams['font.sans-serif'] = ['SimHei'] #Used to display Chinese labels normally
plt.rcParams['axes.unicode_minus'] = False #Used to display the negative sign normally

#-----------------------------1.Plot diagnosis data-----------------------------------
p1 = plt.subplot(221)

# retrieve data
names = total_data.keys()
nums = total_data.values()
print(names)
print(nums)
print(total_data)
plt.bar(names, nums, width=0.3, color='green')

# set title
plt.ylabel("Number of confirmed cases", rotation=90)
plt.xticks(list(names), rotation=-60, size=8)
# 显示数字
for a, b in zip(list(names), list(nums)):
    plt.text(a, b, b, ha='center', va='bottom', size=6)
plt.sca(p1)

#-----------------------------2.Plot newly diagnosed data-----------------------------------
p2 = plt.subplot(222)
names = total_new_data.keys()
nums = total_new_data.values()
print(names)
print(nums)
plt.bar(names, nums, width=0.3, color='yellow')
plt.ylabel("Newly diagnosed number", rotation=90)
plt.xticks(list(names), rotation=-60, size=8)
# 显示数字
for a, b in zip(list(names), list(nums)):
    plt.text(a, b, b, ha='center', va='bottom', size=6)
plt.sca(p2)

#-----------------------------3.Plot death data-----------------------------------
p3 = plt.subplot(223)
names = total_dead_data.keys()
nums = total_dead_data.values()
print(names)
print(nums)
plt.bar(names, nums, width=0.3, color='blue')
plt.xlabel("region")
plt.ylabel("Number of deaths", rotation=90)
plt.xticks(list(names), rotation=-60, size=8)
for a, b in zip(list(names), list(nums)):
    plt.text(a, b, b, ha='center', va='bottom', size=6)
plt.sca(p3)

#-----------------------------4.Plot healing data-----------------------------------
p4 = plt.subplot(224)
names = total_heal_data.keys()
nums = total_heal_data.values()
print(names)
print(nums)
plt.bar(names, nums, width=0.3, color='red')
plt.xlabel("region")
plt.ylabel("Number of people cured", rotation=90)
plt.xticks(list(names), rotation=-60, size=8)
for a, b in zip(list(names), list(nums)):
    plt.text(a, b, b, ha='center', va='bottom', size=6)
plt.sca(p4)
plt.show()


# In[147]:


#------------------------------------------------------------------------------
# Step 3:Save data to CSV file
#------------------------------------------------------------------------------
names = list(total_data.keys()) # province names
num1 = list(total_data.values()) # Diagnosis data
num2 = list(total_suspect_data.values()) # Suspected data (all 0)
num3 = list(total_dead_data.values()) # death data
num4 = list(total_heal_data.values()) # heal data
num5 = list(total_new_data.values()) # New confirmed cases
print(names)
print(num1)
print(num2)
print(num3)
print(num4)
print(num5)

# Get the name of the current date (2022-01-12-gz.csv)
n = time.strftime("%Y-%m-%d") + "-gz-4db.csv"
fw = open(n, 'w', encoding='utf-8')
fw.write('province,type,data\n')
i = 0
while i<len(names):
    fw.write(names[i]+',confirm,'+str(num1[i])+'\n')
    fw.write(names[i]+',dead,'+str(num3[i])+'\n')
    fw.write(names[i]+',heal,'+str(num4[i])+'\n')
    fw.write(names[i]+',new_confirm,'+str(num5[i])+'\n')
    i = i + 1
else:
    print("Over write file!")
    fw.close()


# In[149]:


#------------------------------------------------------------------------------
# Step 4: Call Seaborn to draw a histogram
#------------------------------------------------------------------------------
import time
import matplotlib
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 
# read data
n = time.strftime("%Y-%m-%d") + "-gz-4db.csv"
data = pd.read_csv(n)

# setup window
fig, ax = plt.subplots(1,1)
print(data['province'])

# Set the drawing style and font
sns.set_style("whitegrid",{'font.sans-serif':['simhei','Arial']})

# draw histogram
g = sns.barplot(x="province", y="data", hue="type", data=data, ax=ax,
             palette=sns.color_palette("hls", 8))

# Set the title of the Axes
ax.set_title('Latest epidemic situation')

# Set the axis text direction
ax.set_xticklabels(ax.get_xticklabels(), rotation=-60)

# Set the font size of the axis scale
ax.tick_params(axis='x',labelsize=8)
ax.tick_params(axis='y',labelsize=8)

plt.show()


# In[158]:


# -*- coding:utf-8 -*-
# Python implements normal distribution
# Plot the normal distribution probability density function
import numpy as np
import matplotlib.pyplot as plt
import math

u = 0  # mean μ
u01 = -2
sig = math.sqrt(0.2)  # standard deviation delta

x = np.linspace(u - 3 * sig, u + 3 * sig, 50)
y_sig = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig)
print(x)
print("=" * 20)
print(y_sig)
plt.plot(x, y_sig, "r-", linewidth=2)
plt.grid(True)
plt.show()


# In[ ]:




