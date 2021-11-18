#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
horse = pd.read_csv('C:\\Users\\Ольга\\Desktop\\Phyton\\horse_data.csv')


# In[2]:


horse = pd.read_csv('C:\\Users\\Ольга\\Desktop\\Phyton\\horse_data.csv', header=None, na_values='?')
horse


# In[3]:


horse.columns=['surgery','Age','Hospital Number','rectal temperature','pulse','respiratory rate','temperature of extremities','peripheral pulse','mucous membranes','capillary refill time','pain','peristalsis','abdominal distension','nasogastric tube','nasogastric reflux','nasogastric reflux PH', 'rectal examination - feces','abdomen','packed cell volume','total protein','abdominocentesis appearance','abdomcentesis total protein','outcome','surgical lesion','first number is site of lesion','second number is type','third number is subtypefourth number is specific code','cp_data']


# In[4]:


df = horse[['surgery', 'Age','rectal temperature','pulse','respiratory rate','temperature of extremities', 'pain', 'outcome']]


# In[5]:


df


# In[6]:


df.describe()


# In[7]:


df.mode()


# In[8]:


#сразу виден выброс в столбцах 'Age' по max Сначала заменяю его  


# In[9]:


dfage = df.loc[df['Age'] == 2]
dfage
#2 нет, сорее всего 9 и есть 2. меняю 9 на 2


# In[10]:


dfage9 = df.loc[df['Age'] > 2]
dfage9


# In[11]:


df.loc[df.Age > 2, 'Age'] = 2 
print(df)


# In[12]:


print(df['temperature of extremities'].unique())
print(df['pain'].unique())
print(df['outcome'].unique())
#выбросов нет


# In[13]:


#Теперь заново  рассчитываю базовые статистики


# In[14]:


df.describe()


# In[15]:


print("Статистические данные по группировке 'surgery'")
print("-----------------------------------")
print("Данные по столбцу rectal temperature")
print(df.groupby('surgery')['rectal temperature'].describe())
print("-----------------------------------")
print("Данные по столбцу pulse")
print(df.groupby('surgery')['pulse'].describe())
print("-----------------------------------")
print("Данные по столбцу respiratory rate")
print(df.groupby('surgery')['respiratory rate'].describe())


# In[16]:


#Pain категориальная величина, смотрим моду. Мне интересны показания для операции по интенсивности болей
print(df.groupby(['surgery']) ['pain'].value_counts())


# In[17]:


print(df.groupby(['surgery'])['temperature of extremities'].value_counts())


# In[18]:


# Итого главным показанием к операции повышенная частота пульса, высокая частота дыхания и  степень боли.
#Молодых лошадей с коликами почти нет.
#Почему то не прооперировано 19 лошадей, испытывающих сильные боли


# In[19]:


df[(df['surgery'] == 2) & (df['pain']>3)].describe()
#Просматриваю этих 19 лошадей, которые не прооперировали. Другие признаки тоже указывали на необходимость операции. Налицо недосмотрю


# In[20]:


#И интересен еще исход операций
print(df.groupby(['surgery'])['outcome'].value_counts())


# In[21]:


print(df.groupby(['surgery','outcome'])['outcome'].size() / len(df))


# In[22]:


#20% смертей лошадей в ходе операции. Поздняя диагностика? Тяжелый случай?


# In[23]:


df.groupby(['surgery','outcome'])['pain'].value_counts()


# In[24]:


#Одна из причин смертей лошади после операции - запущенность заболевания, характеризующаяся высокой степенью болей


# In[25]:


print("Данные по гибели животных'")
print("Прооперированные")
print(df[(df['surgery'] == 1) & (df['outcome'] > 1)].describe())
print("Непрооперированные")
print(df[(df['surgery'] == 2) & (df['outcome'] > 1)].describe())


# In[26]:


#Итого. Пульс свыше 80 критический для лошади и нужно оперировать до этих показаний. 
#Ждать когда лошадь достигнет степень боли 4-5 не стоит, высока вероятность смерти. 
#Ниже видно, что живые лошади не достигали порога пульса 80 (150 пульс- явный выброс) и конечности были теплыми


# In[27]:


df[df['outcome'] == 1].describe()


# In[28]:


#Выбросы через межквартльный размах


# In[29]:


q1 = df['rectal temperature'].quantile(0.25)
q3 = df['rectal temperature'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - (1.5 * iqr) 
upper_bound = q3 + (1.5 * iqr)
remove_outliers_rectemp = df[df['rectal temperature'].between(lower_bound, upper_bound, inclusive=True)]
remove_outliers_rectemp


# In[30]:


q1 = df['pulse'].quantile(0.25)
q3 = df['pulse'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - (1.5 * iqr) 
upper_bound = q3 + (1.5 * iqr)
remove_outliers_pulse = df[df['pulse'].between(lower_bound, upper_bound, inclusive=True)]
remove_outliers_pulse 


# In[31]:


q1 = df['respiratory rate'].quantile(0.25)
q3 = df['respiratory rate'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - (1.5 * iqr) 
upper_bound = q3 + (1.5 * iqr)
remove_outliers_respirrate = df[df['pulse'].between(lower_bound, upper_bound, inclusive=True)]
remove_outliers_respirrate 


# In[32]:


print("Значение медианы по столбцу respiratory rate стало",remove_outliers_respirrate['respiratory rate'].median(),"было",df['respiratory rate'].median())
print("Значение медианы по столбцу pulse стало",remove_outliers_pulse['pulse'].median(),"было",df['pulse'].median())
print("Значение медианы по столбцу rectal temperature стало",remove_outliers_rectemp['rectal temperature'].median(),"было",df['rectal temperature'].median())


# In[33]:


df.info()


# In[34]:


df.dropna(thresh=7).info()


# In[35]:


#Все категорильные величины меняю на моду


# In[54]:


print(df.groupby(['surgery','outcome'])['temperature of extremities'].value_counts())
df1 = df
df1['temperature of extremities'].fillna(df['temperature of extremities'].mode()[0], inplace=True)
print(df1.groupby(['surgery','outcome'])['temperature of extremities'].value_counts())


# In[55]:


print(df.groupby(['surgery','outcome'])['pain'].value_counts())
df1 = df
df1['pain'].fillna(df['pain'].mode()[0], inplace=True)
print(df1.groupby(['surgery','outcome'])['pain'].value_counts())


# In[56]:


print(df.groupby(['surgery','pulse'])['outcome'].value_counts())
df1 = df
df1['outcome'].fillna(df['outcome'].mode()[0], inplace=True)
print(df1.groupby(['surgery','pulse'])['outcome'].value_counts())


# In[57]:


#Медианой меняю respiratory rate и пульс. Потому что среднее с десятыми долями у ЧД и пульса не может быть


# In[58]:


print(df.groupby(['surgery','outcome'])['pulse'].median())
df1 = df
df1['pulse'].fillna(df.groupby(['surgery','outcome'])['pulse'].transform('median'), inplace=True)


# In[59]:


print(df.groupby(['surgery','outcome'])['respiratory rate'].median())
df1 = df
df1['respiratory rate'].fillna(df.groupby(['surgery','outcome'])['respiratory rate'].transform('median'), inplace=True)


# In[71]:


print(df.groupby(['surgery','outcome'])['rectal temperature'].mean())
df1 = df
df1['rectal temperature'].fillna(df.groupby(['surgery','outcome'])['rectal temperature'].transform('mean'), inplace=True)


# In[72]:


print(df['rectal temperature'].describe())
print('-----------------------------------')
print(df1['rectal temperature'].describe())


# In[76]:


print(df.groupby(['pain','pulse'])['surgery'].median())
df1 = df
df1['surgery'].fillna(df.groupby(['pain','pulse'])['surgery'].transform('median'), inplace=True)


# In[77]:


df.info()


# In[ ]:


#почему surgery по-прежнему показывает пропуск???


# In[ ]:




