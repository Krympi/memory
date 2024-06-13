from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

app = QApplication([])

notes = {

}
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

#интерфейс
#параметры окна прил
n_w = QWidget()
n_w.setWindowTitle('Умные заметки')
n_w.resize(900, 600)

#виджеты окна
list_n = QListWidget()
list_n_l = QLabel('Список заметок')

button_n_c = QPushButton('Создать заметку')
button_n_d = QPushButton('Удалить заметку')
button_n_s = QPushButton('Сохранить заметку')

field_t = QLineEdit('')
field_t.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_t_add = QPushButton('Добавить к заметке')
button_t_del = QPushButton('Удалить от заметки')
button_t_search = QPushButton('Искать заметки по тегу')
list_ts = QListWidget()
list_ts_l = QLabel('Список тегов')

#расположение виджетов
layout_n = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_n_l)
col_2.addWidget(list_n)

row_1 = QHBoxLayout()
row_1.addWidget(button_n_c)
row_1.addWidget(button_n_d)

row_2 = QHBoxLayout()
row_2.addWidget(button_n_s)

col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_ts_l)
col_2.addWidget(list_ts)
col_2.addWidget(field_t)
row_3 = QHBoxLayout()
row_3.addWidget(button_t_add)
row_3.addWidget(button_t_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_t_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_n.addLayout(col_1, stretch = 2)
layout_n.addLayout(col_2, stretch = 1)
n_w.setLayout(layout_n)

def show_note():
    key = list_n.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])
    list_ts.clear()
    list_ts.addItems(notes[key]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(n_w, 'Добавить заметку', 'Название заметки')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги':[]}
        list_n.addItem(note_name)
        list_ts.addItems(notes[note_name]['теги'])
        print(notes)

def del_note():
    if list_n.selectedItems():
        key = list_n.selectedItems()[0].text()
        del notes[key]
        list_n.clear()
        list_ts.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')

def save_note():
    if list_n.selectedItems():
        key = list_n.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана')

def add_tag():
    if list_n.selectedItems():
        key = list_n.selectedItems()[0].text()
        tag = field_t.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_ts.addItem(tag)
            field_t.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана')

def del_tag():
    if list_ts.selectedItems():
        key = list_n.selectedItems()[0].text()
        tag = list_ts.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_ts.clear()
        list_ts.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для удаления не выбрана')

def search_tag():
    tag = field_t.text()
    if button_t_search.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button_t_search.setText('Cбросить поиск')
        list_n.clear()
        list_ts.clear()
        list_n.addItems(notes_filtered)
    elif button_t_search.text() == 'Сбросить поиск':
        field_t.clear()
        list_n.clear()
        list_ts.clear()
        layout_n.addItem(notes)
        button_t_search.setText('Искать заметки по тегу')
    else:
        pass

list_n.itemClicked.connect(show_note)
button_n_c.clicked.connect(add_note)
button_n_d.clicked.connect(del_note)
button_n_s.clicked.connect(save_note)
button_t_add.clicked.connect(add_tag)
button_t_del.clicked.connect(del_tag)
button_t_search.clicked.connect(search_tag)

n_w.show()
with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_n.addItems(notes)
app.exec_()