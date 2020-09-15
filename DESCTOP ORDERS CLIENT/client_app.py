from tkinter import *
import requests
from datetime import datetime
import tkinter.ttk as ttk
from tkinter.messagebox import *
import pickle
from ftplib import FTP_TLS
import random
import helpic_client_factory as helpic


l_selected = [] # selected items
last_time_change = ''
ent_order = 1
order = ''
lab_order_item = ''
folder_all = ''

# getting information from FTP-server and writing in file
def f_open_recieved():
    global last_time_change
    # trying to connect with FTP-server
    try:
        r = requests.get('http://{}/leftovers.txt'.format(helpic.directory_ftp))
        r.encoding = 'utf 8'

        s = r.text
        s = s.replace(',', '.')
        l = [i.split(';') for i in s.split('\n')]
    except:
        showinfo('Connection', 'You don\'t have internet conection\n\
        or REQUEST is WRONG\nThe information is OLD')

        # for DEMO version ONLY
        l = helpic.l_demo            # for DEMO version ONLY
        # return None  # for preventing parsing 'result from request'


    last_time_change = ''.join(l[-3])  # getting date/time 'text.txt'
    message = l[-2][0]  # getting MESSAGE 'text.txt'
    # l[-1] = ['']  !!! Be attantive!!!
    # creating file for keeping loaded information about items
    with open('client_app_input.pkl', 'wb') as f:
        pickle.dump(l[:-3], f)

    # Messege: put in lab_m and change forma
    if message != 'Message: \r':
        lab_m.configure(text=message, fg='red', relief=RAISED)
    if message == 'Message: \r':
        lab_m.configure(text='Information table in this place', fg='green', relief=FLAT)


def f_close(event):
    f_exit()

def f_exit():
    root.destroy()
# Menu File/About
def f_about():
    showinfo('ELETON REMOTE ORDER client',\
    """
                !!! Beta  Version !!!
     SELECTED:
     1. Двойной клик - изменение колличества
     2. "Красным" - остаток меньше заказа
     
     Загрузка остатков:
     1. При запуске приложения
     2. Кнопка SYNC
     
     Дата/время актуальности остатков: FILE
     
     Файл хранения заказов: 'client_app_order.txt'
     (внутри можно удалять)
     
     Все остальные файлы - служебные
     
     Отправка заказа: Кнопка SEND (так же происходит загрузка остатков)
     
     Верхнее  "чистое поле" - название предприятия
     
     Нижнее  "чистое поле" - для текстовых коментариев к заказу
     (отправляется вместе с заказом)
     
     Информационное табло - для рассылки общей информации
     
     Цены: отображаются РОЗНИТНЫЕ (без скидки)
     
     "чистое поле" над ITEMS - попытка сделать подбор в 
     папке ВСЯ ПРОДУКЦИЯ (не работает)
     
     Don't throw the slippers!!!
     Good luck!
               
     Konstiantyn Sh
     August_2019'
    """)

def f_del_selection(event):
    global l_selected
    item_sel = tree_sel.item(tree_sel.focus())

    item_text = item_sel['text']
    item_value = item_sel['values']

    i = [item_text, item_value[0], item_value[2],  item_value[1]]

    l_selected.remove(i) # removing chosen item from 'l_selected'

    f_del_selected() # Deleting all rows in the table  'tree_sel'
    f_creating_selected() # Creating new rows in the table  'tree_sel' using list = 'l_selected'

# Creating new rows in the table  'tree_sel' using list = 'l_selected'
def f_creating_selected():
    counter = 0
    for i in l_selected:
        tree_sel.tag_configure('Empty_store', background='lightblue', foreground='red')
        if f_tags(i[1], i[3]):
            tree_sel.insert('', counter, text=i[0], values=(i[1], i[3], i[2]), tags='Empty_store')  # 'i[3]' quantity in ORDER
        else:
            tree_sel.insert('', counter, text=i[0], values=(i[1], i[3], i[2]))  # 'i[3]' quantity in ORDER
        counter += 1
    lab_sum.config(text=f_get_sum()) # getting the SUM 'selected' items

# for RED text in 'sel_data'
def f_tags(i, ii):
    if i == '  ':
        num_store = 0
    else:
        num_store = int(i)
    if num_store < int(ii):
        tags = 'Empty_store'
        return tags

# Deliting rows in the table = 'tree_sel'
def f_del_selected():
    rows = tree_sel.get_children()
    for item in rows:
        tree_sel.delete(item)

# Deliting rows in the table = 'tree_sel'
# Button 'Clear all'
def f_clear_event(event):
    f_clear()

def f_clear():
    global l_selected
    l_selected = []
    f_del_selected()
    lab_sum.config(text='')  # deleting the SUM of previous 'selected' items


# Get curent date/time
def f_time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Get items in the table = 'tree_data' and changing text data/time
#on the button
def f_get_items_table():
    global last_time_change, folder_all

    # deleting rows before laoding data
    rows = tree_data.get_children()
    for item in rows:
        tree_data.delete(item)

    # creating new rows
    f_open_recieved()

    with open('client_app_input.pkl', 'rb') as f:
        l_recived = pickle.load(f)

    # group 'ВСЯ ПРОДУКЦИЯ'
    folder_all = tree_data.insert('', 0, text='ВСЯ ПРОДУКЦИЯ',  values=())
    counter = 0
    for i in sorted(l_recived, reverse=True):
        tree_data.insert(folder_all, counter, text=i[0], values=(i[1], i[2]))

    # groups with PLUS
    l_group = sorted((set([i[-1] for i in l_recived])))
    counter_folder = 1
    for i in l_group:
        folder = tree_data.insert('', counter_folder, text=str(i), values=())
        counter_folder += 1
        for data in l_recived:
            counter_row = 0
            if data[-1] == i:
                tree_data.insert(folder, counter_row, text=data[0], values=(data[1], data[2]))
                counter_row += 1

    lab_f.config(text='FILE = ' + last_time_change)  # date/time creating 'text.txt' on the MAIN server
    but_sync.config(text='SYNC = ' + f_time_now())      # date/time last syncronization with FTP-server
    print('Syncronization is finished')
# Table for ORDERS
def f_on_sel_tree(event):
    global l_selected

    item_sel = tree_data.item(tree_data.focus())
    item_text =  item_sel['text']
    item_value = item_sel['values']
    # becouse of ERROR during clicking on FOLDER
    try:
        i = [item_text, item_value[0], item_value[1], 1] # '1' default quantity for ORDER
    except IndexError:
        return None

    if f_avoid_duplicats(i):
       l_selected.append(i)

       f_del_selected()  # Deleting all rows in the table  'tree_sel'
       f_creating_selected()  # Creating new rows in the table  'tree_sel' using list = 'l_selected'

# parser for avoiding duplicats in Table for ORDERS
def f_avoid_duplicats(items):
    global l_selected
    for i in l_selected:
       if i[0] == items[0]:
           return False
    return True

def f_save_order(event):
    global ent_order, order, lab_order_item

    # to change quantity in 'l_selected'
    for i in l_selected:

        if i[0] == lab_order_item['text']:
            try:
               i[3] = int(ent_order.get())
               if type(i[3]) == int and i[3] != 0:
                   f_del_selected()  # Deleting all rows in the table  'tree_sel'
                   f_creating_selected()  # Creating new rows in the table  'tree_sel' using list = 'l_selected'
                   order.destroy()  # close window = ORDER
                   break
               else:
                   showinfo('WRONG number', 'Only \nNUMBERS \nare alowed(except ZERO)')
                   i[3] = 1
                   f_del_selected()  # Deleting all rows in the table  'tree_sel'
                   f_creating_selected()  # Creating new rows in the table  'tree_sel' using list = 'l_selected'
                   order.destroy()  # close window = ORDER
                   break
            except ValueError:
                showinfo('WRONG number', 'Only \nNUMBERS \nare alowed(except ZERO)')
                order.destroy()  # close window = ORDER
                break
# getting the SUM 'selected' items
def f_get_sum():
    #  l_selected    #   [i][2].replace(' ', '') # remuving 'gap' in numbers >=1000
    return round(sum(float(i[2].replace(' ', '')) * float(i[3]) for i in l_selected), 2)

def f_win_order(event):
    global ent_order, order, lab_order_item   # order - window, 'I don't find better solution, only by GLOBAL'
    #new_order = IntVar()

    # for 'text' in 'ent_order'
    item_sel = tree_sel.item(tree_sel.focus())

    item_text =  item_sel['text']

    # window ORDER
    order = Toplevel(root, bg='lightblue',bd=5, relief=SUNKEN)
    order.title('ORDER')
    order.geometry('400x150')
    lab_order_title = Label(order, text='ORDER', width=7, pady=5, bd=5, fg='black', bg='lightblue', font='arial 12',\
                            relief=FLAT)
    lab_order_item = Label(order, text=item_text, width=40, pady=5, padx=5, bd=5, fg='black',\
                           font='arial 10', relief=FLAT)
    ent_order = Entry(order, width=4, bd=5, font='arial 12', fg='black', relief=SUNKEN)
    but_order = Button(order,text='SAVE', width=10, pady=5, bd=5, fg='black', bg='lightgreen', font='arial 12',\
                            relief=RAISED)
    ent_order.insert(1, item_sel['values'][1])  # put in 'sell' quantity from tree_sel

    lab_order_title.grid(row=1, column=0, columnspan=2)
    lab_order_item.grid(row=2, column=0, columnspan=2)
    ent_order.grid(row=2, column=3)
    but_order.grid(row=3, column=0, columnspan=2)

    but_order.bind('<Button-1>', f_save_order)

# sending order
def f_send():
    global l_selected
    if askyesno('Sending ORDER', 'Do yo really want to \nSEND your ORDER?'):
        f_sending_order() # sending file to FTP
        print('Your ORDER:')

        for i in l_selected:
            print ('{}: {} item x {}'.format( i[0], i[3], i[2]))
        print(f_get_sum())
        print('Castomer: {}'.format(ent_cast.get()))
        print('Messege: {}'.format(txt_article.get(1.0, END)))

        #creating .txt ORDER file
        with open('client_app_order.txt', 'r',encoding='utf-8') as f:
            data = f.read()

        for i in l_selected:
           data += '{}: {} item x {}\n'.format( i[0], i[3], i[2])
        data += 'Sum: {}  Time: {}\nCastomer :{}\nMessege: {}\n{}\n'.format(f_get_sum(),f_time_now(), ent_cast.get(), txt_article.get(1.0, END),15 * '- -')
        with open('client_app_order.txt', 'w', encoding='utf-8') as f:
            f.write(data)

        f_clear()  # clear sel_treeand  sum after pushing 'SEND'

# connection and sending ORDER to FTP
def f_sending_order():
    global l_selected
    l = l_selected + [ent_cast.get(),txt_article.get(1.0, END), f_time_now()]

    with open('client_app_order.pkl', 'wb') as f:
        pickle.dump(l, f)
    print('start sending......')
    try:
      ftps = FTP_TLS(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)

      ftps.cwd('/www/{}'.format(helpic.directory_ftp))
    except:
        showinfo('Connection', 'You don\'t have internet conection\n\
                                       or login/pasword were changed')
        return None

    sufix = random.randint(1, 1000000)
    file_name = 'order{}.pkl'.format(sufix)

    ftps.storbinary('STOR ' + file_name, open('client_app_order.pkl', 'rb'))  # загрузка файла НА сервер
    print('finish sending')
    ftps.quit()

    f_get_items_table()  # getting information from FTP-server and writing in file

# searching in folder = ALL PRODACTION
def f_search(event):

    for i in tree_data.get_children(item=folder_all):
        if tree_data.item(i)['text'].lower().startswith(ent_search.get()):

            try:
               tree_data.selection_set(i)  # set slider position
               tree_data.see(i)            # blue color (item's  string)
            except IndexError:
                pass
            break

root = Tk()
root.title('ELETON  REMOTE ORDER')
root.geometry('800x800')

m = Menu()
root.config(menu=m)
fm = Menu(m, fg='green', font='arial 10')

m.add_cascade(label='File', menu=fm)
fm.add_command(label='About', command=f_about)
fm.add_command(label='Exit', command=f_exit)



fra_top = LabelFrame(root, text='ITEMS', width=500, height=200, bd=5, padx=5, pady=5, bg='lightblue')
fra_bottom = LabelFrame(root, text='SELECTED', width=500, height=200, bd=5, padx=5, pady=5, bg='lightgreen')

#Fonts for tree_tables
style = ttk.Style()
style.configure('Treeview', font='arial 12')
style.configure('Treeview.Heading', font='arial 12')

# table for LIST with nomenklatura
tree_data = ttk.Treeview(fra_top)

tree_data['columns'] = ('quantity', 'price')
tree_data.column('quantity', width=150, anchor='n')
tree_data.column('price', width=150)
tree_data.heading('quantity', text='К-во')
tree_data.heading('price', text='Цена')

# table for SELECTED with nomenklatura
tree_sel = ttk.Treeview(fra_bottom)
tree_sel['columns'] = ('quantity', 'order', 'price')
tree_sel.column('quantity', width=100, anchor='n')
tree_sel.column('order', width=100, anchor='n')
tree_sel.column('price', width=100)
tree_sel.heading('quantity', text='К-во')
tree_sel.heading('order', text='Заказ')
tree_sel.heading('price', text='Цена')


scr_tree_data=Scrollbar(fra_top, command=tree_data.yview)
tree_data.config(yscrollcommand=scr_tree_data.set)

tree_data.grid(row=1, column=0, padx=5, pady=5)
scr_tree_data.grid(row=1, column=1, sticky='ns')

scr_tree_sel=Scrollbar(fra_bottom, command=tree_sel.yview)
tree_sel.config(yscrollcommand=scr_tree_sel.set)

tree_sel.grid(row=1, column=0, padx=5, pady=5)
scr_tree_sel.grid(row=1, column=1, padx=5, pady=5, sticky='ns')

lab_m = Label(root, width=80, height=2,text='Information table in this place', font='arial 12', fg='green', bd=5, relief=FLAT)
ent_cast = Entry(root, width=25, font='arial 16', fg='green', bd=5, relief=SUNKEN)
ent_search = Entry(root,width=15, font='arial 12', fg='green', bd=5, relief=SUNKEN )
txt_article = Text(root, width=80, height=3, font='arial 12', fg='green', bd=5, relief=SUNKEN, wrap=WORD)
but_clear = Button(root, text='Clear ALL', relief=RAISED, bd=5, fg='blue', font='arial 12', activebackground='red')
lab_f = Label(root, width=25, font='arial 10', fg='green', bd=5, relief=FLAT)
but_sync = Button(root, height=1, width=25, font='arial 12',bg='lightblue', activebackground='lightgreen', fg='green',\
                bd=5, relief=RAISED, command=f_get_items_table)
lab_sum = Label(root, width=15, font='arial 12',bg='lightgreen', fg='black', bd=5, relief=SUNKEN)
but_send = Button(root, text='SEND', width=25, height=1, font='arial 10',bg='lightblue', activebackground='lightgreen',\
                  fg='green', bd=5, relief=RAISED, command=f_send)

lab_m.grid(row=1, columnspan=3, column=0, padx=1, pady=2)
but_sync.grid(row=2, column=0, padx=1, pady=2, sticky='w')
lab_f.grid(row=2, column=1, padx=1, pady=2)
ent_cast.grid(row=2, column=2, padx=1, pady=2, sticky='w')

ent_search.grid(row=3, column=0, padx=1, pady=2, sticky='w')
fra_top.grid(row=4, column=0, columnspan=3, padx=1, pady=2, sticky='we')
fra_bottom.grid(row=5, column=0, columnspan=3, padx=1, pady=2, sticky='we')
lab_sum.grid(row=6, column=0, padx=1, pady=2)
but_clear.grid(row=6, column=1, padx=1, pady=2, sticky='w')
but_send.grid(row=6, column=2, padx=1, pady=2, sticky='w')
txt_article.grid(row=7, column=0, columnspan=3, padx=1, pady=2)




f_get_items_table()  # Fill items for start  TABLE

root.bind('<Control-z>', f_close)
ent_search.bind('<Key>', f_search)
ent_search.bind('<Return>', f_search)
but_clear.bind('<Button-1>', f_clear_event)
tree_data.bind('<Double-Button-1>', f_on_sel_tree)
tree_sel.bind('<Double-Button-1>', f_win_order)
tree_sel.bind('<Delete>', f_del_selection)

root.mainloop()

