#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import pandas as pd
import requests 
from bs4 import BeautifulSoup as bs
import numpy as np


# In[3]:


# the url 
url = "https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&search_type=all&isCpeNameSearch=false&hyperlink_types=CISA+Known+Exploited+Vulnerabilities"
html = requests.get(url).content
soup = bs(html)


# In[6]:


# a function to parse NaNs

def item_extract(item_cont, item_key):
    parse = item_cont.select(item_key)
    if parse == []:
        return np.nan
    else: 
        return parse[0].text


# In[8]:


# the list of keys

vuln_key = "strong > a"
summary_key= "td > p"
published_key = "tr > td:nth-child(2) >span"
cvss_key = "td > span > a"

glossary = []
vuln_lst = []
summary_lst = []
published_lst = []
cvss_lst = []

for x in range(0,43):
    url = f"https://nvd.nist.gov/vuln/search/results?isCpeNameSearch=false&results_type=overview&hyperlink_types=CISA+Known+Exploited+Vulnerabilities&form_type=Basic&search_type=all&startIndex={x*20}"
    html = requests.get(url).content
    soup = bs(html)
    print(url)


    container = soup.select("tbody > tr")

    for i in container:
    
        #vuln
        vuln = item_extract(i, vuln_key)
        vuln_lst.append(vuln)
    
        #summary
        summary = item_extract(i, summary_key)
        summary_lst.append(summary)
    
        #published
        published = item_extract(i, published_key)
        published_lst.append(published)
    
        #CVSS
        cvss = item_extract(i, cvss_key)
        cvss_lst.append(cvss)
    
#print(vuln_lst)
#print(summary_lst)
#print(published_lst)
#print(cvss_lst)

pd.DataFrame({"vuln" : vuln_lst,
                    "summary":summary_lst,
                    "published": published_lst,
                    "cvss": cvss_lst})
         


# In[10]:


#renaming columns and saving the df as a new "df_col"
df_col = df.rename(columns = {"vuln": "Vulnerabilities","published": "Vuln published","cvss": "Score"})
df_col


# In[11]:


# new column from score
df_col["Year"] = df_col.Vulnerabilities.str.split("-",expand = True)[1]
df_col


# In[22]:


# splitting the columnn
df_col["Score"] = df_col.Score.str.split(" ",expand = True)[0]
df_col


# In[31]:


# sorting by columns
df_col.groupby(["Score","Year"]).mean()


# In[114]:


# creating 4 cat for the Score now called "Severity" column
df_col["Severity"] = pd.qcut(df_col.Score, q = 4, labels=["low", "medium", "high", "critical"])
df_col


# In[59]:


# Dtype were objects
df_col.Score = df_col.Score.astype(float)
df_col.Year = df_col.Year.astype(float)


# In[60]:


df_col.info()


# In[68]:


# a corrleation between Year and Score
import seaborn as sns
df_col.corr()
sns.heatmap(df_col.corr())


# In[88]:


#df_col.groupby("Year").Severity.value_counts()
plut = pd.DataFrame(df_col.groupby("Year").size()).reset_index().sort_values("Year")
import seaborn as sns
plut.columns = ["Year", "Severity"]
sns.barplot(data=plut,x="Year", y = "Severity")


# In[94]:


# plotting by Year and Severity
df_col.groupby(["Year","Severity"]).size().unstack().critical.plot()


# In[95]:


sns.heatmap(df_col.corr(), annot =True)

