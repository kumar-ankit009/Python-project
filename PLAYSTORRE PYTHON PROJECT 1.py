#!/usr/bin/env python
# coding: utf-8

# ##  PYTHON GOOGLE PLAY STORE PROJECT EDA ANALYSIS  ##

# In[1]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns 


# In[2]:


pd.read_csv('E:\playstore_analysis.csv')


# In[3]:


data = pd.read_csv('E:\playstore_analysis.csv')


# In[4]:


data.head()


# In[5]:


data.info()


# In[6]:


data.isnull().sum()


#  ## Task 1. Data clean up – Missing value treatment

#  ### a. Drop records where rating is missing since rating is our target/study variable

# In[8]:


data.dropna(how='any', subset=['Rating'], axis=0, inplace = True)


# In[9]:


data.Rating.isnull().sum()


#  ### b. Check the null values for the Android Ver column.
#     
# i. Are all 3 records having the same problem?
# 
# ii. Drop the 3rd record i.e. record for “Life Made WIFI …
# 
# iii. Replace remaining missing values with the mode

# In[10]:


## i. Are all 3 records having the same problem ?

data.loc[data['Android Ver'].isnull()]


# #### Yes, all 3 records are having same problem that is .. all are NaN

# In[11]:


## ii. Drop the 3rd record i.e. record for “Life Made WIFI …
    
data.drop([10472], inplace = True)


# In[12]:


data.loc[data['Android Ver'].isnull()]


# In[13]:


## iii.Replace remaining missing values with the mode

data['Android Ver'].fillna(data['Android Ver'].mode()[0], inplace=True)


#  #### c. Current ver – replace with most common value

# In[14]:


data['Current Ver'].fillna(data['Current Ver'].mode()[0], inplace=True)


# ## Task: 2. Data clean up – correcting the data types

#  #### a. Which all variables need to be brought to numeric types ?

# In[16]:


data.dtypes


# #### a . Reviews and installs needs to be changed to numeric ...

# #### b. Price variable – remove ' $ ' sign and convert to float

# In[17]:


price = []
for i in data['Price']:
    if i[0]=='$':
        price.append(i[1:])
    else:
        price.append(i)  


# In[18]:


data.drop(labels=data[data['Price']=='Everyone'].index, inplace = True)
data['Price']= price
data['Price']= data['Price'].astype('float')


#  #### c. Installs – remove ‘,’ and ‘+’ sign, convert to integer

# In[19]:


install = []
for j in data['Installs']:
    install.append(j.replace(',','').replace('+','').strip())

data['Installs']= install
data['Installs']= data['Installs'].astype('int')


# In[20]:


data.dtypes


# #### d . Convert all other identified columns to numeric

# In[21]:


data['Reviews']= data['Reviews'].astype('int')


# In[22]:


data.dtypes


# ## Task 3. Sanity checks – check for the following and handle accordingly

#  ### a. Avg. rating should be between 1 and 5, as only these values are allowed on the play store

#  #### i. Are there any such records? Drop if so

# In[23]:


data.loc[data.Rating < 1] & data.loc[data.Rating > 5]


#  #### There are no such records with rating less than 1 or greater than 5.

# ### b. Reviews should not be more than installs as only those who installed can review the app.
# 
# i. Are there any such records? Drop if so.
# 

# In[24]:


data.loc[data['Reviews'] > data['Installs']]


# #### Yes, there are 7 records where Review is greater than Installs.

# In[25]:


temp = data[data['Reviews']>data['Installs']].index
data.drop(labels=temp, inplace=True)


# In[27]:


data.loc[data['Reviews'] > data['Installs']]


# ###  Task 4. Identify and handle outliers

# #### a. Price column
# i. Make suitable plot to identify outliers in price

# In[28]:


plt.boxplot(data['Price'])
plt.show()


#  #### ii.Do you expect apps on the play store to cost $200? Check out these cases

# In[29]:


print('Yes we can expect apps on the play store to cost $200')
data.loc[data['Price'] > 200]


#  #### iii . Limit data to records with price < $30

# In[36]:


gt_30 = data[data['Price'] > 30].index
data.drop(labels=gt_30, inplace=True)


# In[37]:


count = data.loc[data['Price'] > 30].index
count.value_counts().sum()


# ####  iv After dropping the useless records, make the suitable plot again to identify outliers

# In[38]:


plt.boxplot(data['Price'])
plt.show()


# #### b. Reviews column

# #### i. Make suitable plot

# In[42]:


sns.distplot(data['Reviews'])
plt.show()


#  ### ii. Limit data to apps with < 1 Million reviews
# 

# In[43]:


gt_1m = data[data['Reviews'] > 1000000 ].index
data.drop(labels = gt_1m, inplace=True)
print(gt_1m.value_counts().sum(),'cols dropped')


# ### c. Installs
# i. What is the 95th percentile of the installs?

# In[44]:


percentile = data.Installs.quantile(0.95) #95th Percentile of Installs
print(percentile,"is 95th percentile of Installs")


# ### ii.Drop records having a value more than the 95th percentile

# In[46]:


for i in range(0,101,1):
    print(' the {} percentile of installs is {} '.format(i,np.percentile(data['Installs'],i)))


# In[48]:


temp1 = data[data["Installs"] > percentile].index
data.drop(labels = temp1, inplace = True)
print(temp1.value_counts().sum())#,'cols dropped')


#  ## Data analysis to answer business questions

# ### Task 5. What is the distribution of ratings like? (use Seaborn) More skewed towards higher/lower values?

#  ### a. How do you explain this?

# In[49]:


sns.distplot(data['Rating'])
plt.show()
print('The skewness of this distribution is',data['Rating'].skew())
print('The Median of this distribution {} is greater than mean {} of this distribution'.format(data.Rating.median(),data.Rating.mean()))


#  ### b. What is the implication of this on your analysis?

# In[50]:


data['Rating'].mode()


# #### Since mode>= median > mean, the distribution of Rating is Negatively Skewed.Therefore distribution of Rating is more Skewed towards lower values.
# 
# 

# ### 6. What are the top Content Rating values?
# a. Are there any values with very few records?

# In[51]:


data['Content Rating'].value_counts()


# #### Adults only 18+ and Unrated are values with very few records so we drop them

# In[52]:


#Replacing unwanted values with NaN
cr = []
for k in data['Content Rating']:
    cr.append(k.replace('Adults only 18+','NaN').replace('Unrated','NaN'))

data['Content Rating']=cr


# In[53]:


# Droping the NaN values.
temp2 = data[data["Content Rating"] == 'NaN'].index
data.drop(labels=temp2, inplace=True)
print('droped cols',temp2)


# In[54]:


data['Content Rating'].value_counts() # Just  Check


# ## Task 7. Effect of size on rating

# #### a. Make a joinplot to understand the effect of size on rating

# In[56]:


sns.jointplot(y ='Size', x ='Rating', data = data, kind ='hex')
plt.show()


# #### c. How do you explain the pattern?
# 
# Generally on increasing Rating, Size of App also increases. But this is not always true ie. for higher Rating, their is constant Size. Thus we can conclude that their is positive correlation between Size and Rating.
# 
# 

# ## Task 8. Effect of price on rating

# ### a. Make a jointplot (with regression line)
# 

# In[57]:


sns.jointplot(x='Price', y='Rating', data=data, kind='reg')
plt.show()


# #### b. What pattern do you see?
# Generally on increasing the Price, Rating remains almost constant greater than 4.

# #### c. How do you explain the pattern?
# Since on increasing the Price, Rating remains almost constant greater than 4. Thus it can be concluded that their is very weak Positive correlation between Rating and Price.

# In[58]:


data.corr()


# ### d. Replot the data, this time with only records with price > 0
# 

# In[59]:


ps1=data.loc[data.Price>0]
sns.jointplot(x='Price', y='Rating', data=ps1, kind='reg')
plt.show()


# #### e. Does the pattern change?
# Yes, On limiting the record with Price > 0, the overall pattern changed a slight ie their is very weakly Negative Correlation between Price and Rating.

# In[60]:


data.corr()


# ### f. What is your overall inference on the effect of price on the rating

# #### Generally increasing the Prices, doesn't have signifcant effect on Higher Rating. For Higher Price, Rating is High and almost constant ie greater than 4

# ## Task 9. Look at all the numeric interactions together

# #### a. Make a pairplort with the colulmns - 'Reviews', 'Size', 'Rating', 'Price

# In[61]:


sns.pairplot(data, vars=['Reviews', 'Size', 'Rating', 'Price'], kind='reg')
plt.show()


# ## Task 10. Rating vs. content rating

# ### a. Make a bar plot displaying the rating for each content rating

# In[66]:


data.groupby(['Content Rating'])['Rating'].count().plot.bar(color="darkblue")
plt.show()


# ### b. Which metric would you use? Mean? Median? Some other quantile?

# #### We must use Median in this case as we are having Outliers in Rating. Because in case of Outliers , median is the best measure of central tendency.

# In[67]:


plt.boxplot(data['Rating'])
plt.show()


# ### c. Choose the right metric and plot

# In[68]:


data.groupby(['Content Rating'])['Rating'].median().plot.barh(color="darkblue")
plt.show()


# ## Task 11. Content rating vs. size vs. rating – 3 variables at a time

# #### a. Create 5 buckets (20% records in each) based on Size

# In[70]:


bins=[0, 20000, 40000, 60000, 80000, 100000]
data['Bucket Size'] = pd.cut(data['Size'], bins, labels=['0-20k','20k-40k','40k-60k','60k-80k','80k-100k'])
pd.pivot_table(data, values='Rating', index='Bucket Size', columns='Content Rating')


# #### b. By Content Rating vs. Size buckets, get the rating (20th percentile) for each combination

# In[72]:


temp3=pd.pivot_table(data, values='Rating', index='Bucket Size', columns='Content Rating', aggfunc=lambda x:np.quantile(x,0.2))
temp3


# ### c . Make a heatmap of this

# #### i. Annotated
# 

# In[73]:


f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(temp3, annot=True, linewidths=.5, fmt='.1f',ax=ax)
plt.show()


# #### ii.Greens color map

# In[74]:


f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(temp3, annot=True, linewidths=.5, cmap='Greens',fmt='.1f',ax=ax)
plt.show()


# #### d. What’s your inference? Are lighter apps preferred in all categories? Heavier? Some?

# #### Based on analysis, its not true that lighter apps are preferred in all categories. Because apps with size 40k-60k and 80k-100k have got the highest rating in all cateegories. So, in general we can conclude that heavier apps are preferred in all categories.

# In[ ]:




