import numpy as np
import itertools
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from graphviz import Digraph

#ввод матрицы
def conf_count():
    global snodes_count
    global tnodes_count
    global matrix_entry
    snodes_count = int(smatrix_size_entry.get())
    smatrix_size_entry.delete(0, END)
    tnodes_count = int(tmatrix_size_entry.get())
    tmatrix_size_entry.delete(0, END)
    label.grid_remove()
    l1=Label(text=f"Заполните матрицу {snodes_count}х{tnodes_count}:", font=('Helvetica', 16, 'bold'))
    l1.grid(row=0, column=0, columnspan=3, sticky=W, pady=10, padx=10)
    smatrix_size_entry.grid_remove()
    tmatrix_size_entry.grid_remove()
    first_page_btn.grid_remove()
    p=0
    matrix_entry = [0] * snodes_count * tnodes_count
    for i in range(snodes_count):
        for k in range(tnodes_count):
            matrix_entry[p] = Entry(root, width=10)
            matrix_entry[p].grid(row=i + 2, column=(k % tnodes_count)+1, sticky=W+E, padx=10)
            p=p+1
    for t in range(tnodes_count):
        Label(text=f"Y{t+1}").grid(row=1, column=t % tnodes_count +1, sticky=W+E, padx=10)
    for s in range(snodes_count):
        Label(text=f"X{s+1}").grid(row=s % snodes_count +2, column=0, sticky=E, padx=10)
    second_page_btn.grid(row=snodes_count+3, column=0, columnspan=2, sticky=W+E, pady=10, padx=10)
    third_page_btn.grid(row=snodes_count+3, column=tnodes_count-1, columnspan=2,  sticky=W+E, pady=10, padx=10)
    print(matrix_entry)

#рисование графа
def render_graph():
    global snodes_count     #это количество строк                        
    global tnodes_count     #это количество столбцов                        
    global matrix_entry
    global matrix
    matrix = [0] * snodes_count * tnodes_count 
    for i in range(len(matrix_entry)):
        matrix[i] = int(matrix_entry[i].get())
    print(matrix)  #вот он он
    i = 0
    s=0
    #рисовалка
    g = Digraph('G', filename='Рисунок графа')
    g.attr(rankdir='LR')
    g.attr('node', shape='circle')
    with g.subgraph(name='cluster_0') as c:
        c.attr(style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        for s in range(snodes_count):
            c.node(f"X{s+1}")
        c.attr(label='X')
    with g.subgraph(name='cluster_1') as c:
        c.attr(style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        for t in range(tnodes_count):
            c.node(f"Y{t+1}")
        c.attr(label='Y')
    for element in matrix:  #хватаем первый элемент из того списка
        if element == 1:                            
            g.edge(f"X{(i // tnodes_count)+1}", f"Y{(i % tnodes_count)+1}")     #если он 1, то ребро по такой формуле
        i += 1
    g.view()

#твой код
def main():
    global snodes_count     #это количество строк                        
    global tnodes_count     #это количество столбцов                        
    global matrix
    global resmatrix
    i=0
    j=0
    p=0
    element=0
    F = [0] * snodes_count # сделали пустой массив
    G = [0] * tnodes_count # сделали пустой массив
    for element in range(len(matrix)): # заполняем F и G Сложность n
        F[i] += matrix[element]
        G[j] += matrix[element]
        j+=1
        if (element+1) % tnodes_count == 0:
            i+=1
            j=0
    resmatrix = [0] * snodes_count * tnodes_count # создаем пустой массив в который будем добавлять элементы из matrix и сравнивать
    for p in range(len(matrix)):  #хватаем первый элемент из того списка
        resmatrix[p] = matrix[p] # забиваем первый элемент из matrix в resmatrix
        if resmatrix[p] == 1 and F[p // tnodes_count]>1 and G[p % tnodes_count]>1: # первым неравенством выбираем элемент, а вторым выбираем столбец
            resmatrix[p] -=1
            F[p // tnodes_count] -=1
            G[p % tnodes_count] -=1
    print(resmatrix)
    result()

def result():
    global snodes_count                     
    global tnodes_count                            
    global resmatrix
    i=0
    Label(text="Минимальное покрытие:", font=('Helvetica', 16, 'bold')).grid(row=snodes_count+4, column=0, columnspan=3, sticky=W, pady=2, padx=10)
    for element in resmatrix:  
        if element == 1:                            
            Label(text=f"(X{(i // tnodes_count)+1}, Y{(i % tnodes_count)+1})").grid(row=snodes_count+i+5,column=0, sticky=W+E, pady=2, padx=10)     #если он 1, то ребро по такой формуле
        i += 1





#объявление переменных и всего такого
root = Tk()
root.title('Поиск минимального покрытия графа')
nodes_count = 0
matrix = list()
matrix_entry = list()
label = Label(text="Введите количество строк и стобцов М:")
smatrix_size_entry = Entry(root, width=10)
tmatrix_size_entry = Entry(root, width=10)
first_page_btn = Button(text="Ввести", command=conf_count)
second_page_btn = Button(text="Отрисовать граф!",command=render_graph)
third_page_btn = Button(text="Найти наименьшее покрытие!", command=main)
label.grid(row=0, column=0, sticky=W, pady=10, padx=10)
smatrix_size_entry.grid(row=0, column=1, sticky=W+E, padx=10)
tmatrix_size_entry.grid(row=0, column=2, sticky=W+E, padx=10)
first_page_btn.grid(row=2, column=0, pady=10, padx=10)

#это просто шоб окошко было по центру или около того
root.update_idletasks()
s = root.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2 
w = w - width_root // 2
h = h - height_root // 2
root.geometry('+{}+{}'.format(w, h))
root.mainloop()
