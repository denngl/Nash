#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


#print("Введите количество строк:")
#a = int(input())


# In[3]:


#matrix = np.random.randint(-10,10,size=(a,a))
matrix = [[4,2,2], 
          [2,5,0], 
          [0,2,5]]
print(matrix)


# In[4]:


def prep_matr(i,A):
    matrix = np.ones((i+2,i+3))
    #matrix[1:i+2, 1] *= -1 #столбец свободных членов
    matrix[i+1,1:i+2] *= -1 #коэффициенты целевой функции
    #matrix[1:i+1, 2:i+2] = A*(-1) #заполняем матрицей
    matrix[1:i+1, 2:i+2] = A #заполняем матрицей
    matrix[1:i+2, 0] = range(i+1,2*(i+1)) #свободные переменные индексы
    matrix[i+1,1] = 0 #коэффициент при целевой
    matrix[i+1,0] = -5 #аналог f
    matrix[0] *= 0
    matrix[0, 2:i+2] = range(1,i+1)
        
    
    print(matrix)
    return matrix


# In[5]:


def simplex_find(i,A):
    a = abs(A[i+1, 2:i+2])
    b = (np.where(a == np.amax(a))[0]) #массив индексов макс элементов
    lead_column = b[0]+2 #+2 потому что перед ним два служебных столбца, индекс лид столбца
    print("Ведущий столбец " , A[0, lead_column]) 
    # c = A[1:i+1, lead_column].copy()#+1 потому что сдвинуто на 2, но 1 прибавили на прошлом шаге, лид столбец
    c = np.zeros(i)
    print(c)
    print(A)
    for n in range (0,i):
       if((A[n+1, 1] > 0) and (A[n+1, lead_column] < 0)):
            c[n] = float("inf")
       else: 
            c[n] = A[n+1, 1] / A[n+1, lead_column]
    
    print(c) #печатаем  отношение свободных членов к лид столбцу
    
    d = (np.where(c == np.amin(c))[0]) #массив индексов мин элементов
    if(abs(c[d[0]]) == np.inf):
        raise Exception("Фигня тут")
    lead_line = d[0]+1 #+1 потому что нумерация свободных переменных с 1, индекс лид строки
    print("Ведущая строка " , A[lead_line, 0] )
    print(A)
    
    return lead_column, lead_line


# In[6]:


def simplex_change(i, A):
    lead_elems = simplex_find(i, A)
    lc = lead_elems[0]
    ll = lead_elems[1]
    ln = A[ll, lc]
    print(lead_elems)
    
    temp = A[ll, 0]
    A[ll, 0] = A[0, lc] # переменную при ведущем столбце ставим в первую строку \\\\\ меняем строчки местами
    A[0, lc] = temp # переменную при ведущем столбце меняем на переменную, которая была в ведущей строке
    
    for n in range(1,i+2):
            if (n == ll):
                continue # не трогаем вспомогательный коэффициент для строки с ведущим элементом
            else:
                A[n, i+2] =  (-1)*A[n, lc]
                
    print("Вспомогательные кэфы, ведущие местами\n", A)
                
    for n in range(1,i+2): #записываем новую строку
            if (n == lc):
                A[ll, n] = 1/ln
            else:
                A[ll, n] /=  ln
               
    print("Новую строку\n", A)
    
    for n in range(1,i+2): #внешний цикл по строкам
            if (n == ll):
                continue # не трогаем новую строку
            else:
                for m in range(1, i+2):
                    if(m == lc):
                        A[n,m] = A[ll,m]*A[n, i+2]#+0 так как в преыдущей таблице не было такой строки
                    else:
                        A[n,m] = A[ll,m]*A[n, i+2]+A[n,m]
    print(A)
    
    return


# In[7]:


def simplex_check(i, A):
    for n in range(2, i+2):
        if(A[i+1, n] < 0):
            return 0
    return 1
        


# In[8]:


def nash_equilibrium(A):
    a = (np.shape(A))[0]
    B = prep_matr(a, A)
    while (not simplex_check(a,B)):
        simplex_change(a,B)
    
    price = 1/np.sum(B[1:a+1,1])
    print("Оптимальная второго", price*B[1:a+1,1])
    print("Оптимальная первого", price*B[a+1,2:a+2])
    print(price)
    
    x = np.arange(1, a+1)
    y = price*B[1:a+1,1]
    fig, ax = plt.subplots()

    ax.bar(x, y)

    #ax.set_facecolor('seashell')
    #fig.set_facecolor('floralwhite')
    fig.set_figwidth(2)    #  ширина Figure
    #fig.set_figheight(3)    #  высота Figure

    plt.show()
    
    x = np.arange(1, a+1)
    y = price*B[a+1,2:a+2]
    fig, ax = plt.subplots()

    ax.bar(x, y)

    #ax.set_facecolor('seashell')
   # fig.set_facecolor('floralwhite')
    fig.set_figwidth(2)    #  ширина Figure
   # fig.set_figheight(3)    #  высота Figure

    plt.show()

    return


# In[9]:


nash_equilibrium(matrix)


# In[ ]:




