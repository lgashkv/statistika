#!/usr/bin/env python
# coding: utf-8

# In[61]:


import pandas as pd
horse = pd.read_csv('C:\\Users\\Ольга\\Downloads\\Downloads\\horse_data.csv')


# In[62]:


horse = pd.read_csv('C:\\Users\\Ольга\\Downloads\\Downloads\\horse_data.csv', header=None, na_values='?')
horse


# In[63]:


horse.columns=['surgery','Age','Hospital Number','rectal temperature','pulse','respiratory rate','temperature of extremities','peripheral pulse','mucous membranes','capillary refill time','pain','peristalsis','abdominal distension','nasogastric tube','nasogastric reflux','nasogastric reflux PH', 'rectal examination - feces','abdomen','packed cell volume','total protein','abdominocentesis appearance','abdomcentesis total protein','outcome','surgical lesion','first number is site of lesion','second number is type','third number is subtypefourth number is specific code','cp_data']


# In[64]:


horse


# In[65]:


df = horse[['surgery', 'Age','pain','peristalsis', 'abdominal distension','packed cell volume','total protein','outcome']]


# In[66]:


df


# In[67]:


df.describe()


# In[68]:


df.mode()


# In[69]:


# результаты:
#     1.Важной метрикой для столбца surgery считаю моду и mean. По ним видно, что большинство лошадей было прооперировано.
#     2.Для возраста также важна мода.Большинство лошадей имеют возраст 1 год. Показатель max указывает на выброс. Минимальный возраст 1 год, жеребят нет. 
#     3. pain- хотя это и субъективное суждение, но можно прослндить взаимосвязь между болью и сделанной операцией. Показатели 25%,50%,75% показывают что большинство лошадей испытывало от депрессии до периодической сильной боли. Мода указывает на самую частую оценку -прерывистую легкую боль.
#     4.Стандартное отклонение минимальное, значит можно расчитвать на среднее. Оно указывает, что значительное большинство лошадей не имело сильного тонуса кишечника.
#     5.Важный параметр. Небольшое std, мода и среднее указывают, что у лошадей или не было или было легкое вздутие живота. То есть ничего страшного с лошадьми не было.
#     6.Анализ крови. Норма от 30-50. 25%,50%,75%  - показывают, что анализы были в норме. Это видно и по среднему и по моде.
#     7.total protein. Видим явный выброс в значении макс. Но даже с учетом его, в целом белок нормальный, лошади не обезвожены.
#     8.интересует исход операций и как общая благоприятная картина была на самом деле благоприятной. Мода показывает, что большинство лошадей живы. Стандартное отклонение от среднего минимально


# In[70]:


# В выбранных числовых столбцах найти выбросы, выдвинуть гипотезы об их причинах и проинтерпретировать результаты. Принять и обосновать решение о дальнейшей работе с ними.\n",


# In[71]:


df9 = df.loc[df['Age'] > 2] 


# In[72]:


df9.describe()


# In[73]:


# Age встречается 24 раза. Это не может быть случайным единичным нажатием не той клавиши.все показатели разные, общего кроме возраста у лошадей нет. 
# замена 9 на Nan


# In[74]:


df['Age'].mask(df['Age'] == 9)


# In[75]:


df


# In[76]:


# total protein. возможно правильный показатель был в total protein не 89.000000, а 8,9. 
# При выборе этого значения, видим, что лошадь была усыплена, сама клиника незначительна, но packed cell volume выше нормы и белок тоже будет повышен.


# In[77]:


df.loc[df['total protein'] == 89.000000]


# In[78]:


# В описании сказано, что норма 6-7.5. в таблице есть 96 строк со значительно выше белком. 
# При этом лошади живы, packed cell volume в норме, многие не прооперированы. 
# Делаю вывод, что была ошибка в неправильной постановке точки. 


# In[79]:


# Подобных выбросов 82 строки.
#Можно сделать замену


# In[80]:


df.loc[df['total protein']>10,'true total protein']= df['total protein']/10
df.loc[df['total protein']<=10,'true total protein']= df['total protein']
df


# In[31]:


# Рассчитать количество выбросов для всех выбранных столбцов. Принять и обосновать решение о методе работы с пропусками по каждому столбцу, сформировать датафрейм, в котором пропуски будут отсутствовать.


# In[83]:


df.fillna(0)


# In[84]:


df.dropna()


# In[ ]:




