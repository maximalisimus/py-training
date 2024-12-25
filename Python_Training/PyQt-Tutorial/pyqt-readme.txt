
pip install pyqt5 pyqt5-tools
or
pip install pyqt6 pyqt6-tools

------------------------------------------------------------------------

app.py

from PyQt6.QtWidgets import QApplication, QWidget

import sys # Только для доступа к аргументам командной строки

# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

# Создаём виджет Qt — окно.
window = QWidget()
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()


# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.

------------------------------------------------------------------------

python3 app.py

------------------------------------------------------------------------

Основные модули для Qt: QtWidgets, QtGui и QtCore.

Если не будете использовать аргументы командной строки для управления Qt, передайте пустой список:

app = QApplication([])

Затем создаём экземпляр QWidget, используя имя переменной window:

window = QWidget()
window.show()

В Qt все виджеты верхнего уровня — окна, 
то есть у них нет родительского элемента и 
они не вложены в другой виджет или макет.
В принципе, окно можно создать, используя любой виджет.

Виджеты без родительского элемента по умолчанию невидимы.

------------------------------------------------------------------------

QMainWindow пока не очень интересный. Добавим контент. 
Чтобы сделать настраиваемое окно, лучше создать подкласс QMainWindow, 
а затем настроить окно в блоке __init__. 
Так окно станет независимым в плане поведения. 

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

Изменение размеров окон и виджетов

В Qt размеры определяются с помощью объекта QSize. 
Он принимает параметры ширины и высоты. 
Например, так создаётся окно фиксированного размера 400 x 300 пикселей:

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

Кроме .setFixedSize() можно также вызвать 
.setMinimumSize() и .setMaximumSize(), 
чтобы установить минимальный и максимальный размеры соответственно.

------------------------------------------------------------------------

Слоты и игналы Qt

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Clicked!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

Получение данных

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

------------------------------------------------------------------------

Хранение данных

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_toggled)
        button.setChecked(self.button_is_checked)

        self.setCentralWidget(button)

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

        print(self.button_is_checked)

------------------------------------------------------------------------

Эта же схема применима к любым виджетам PyQt. Если в виджете нет сигнала, 
которым отправляется текущее состояние, 
нужно получить значение из виджета прямо в обработчике. 
Например, здесь мы проверяем состояние checked («Нажата») 
в нажатом обработчике:

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)

        self.setCentralWidget(self.button)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)

------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        # Также меняем заголовок окна.
        self.setWindowTitle("My Oneshot App")

------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

mouseMoveEvent - Мышь переместилась

mousePressEvent - Кнопка мыши нажата

mouseReleaseEvent - Кнопка мыши отпущена

mouseDoubleClickEvent - Обнаружен двойной клик

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

.button() - Конкретную кнопку, вызвавшую данное событие

.buttons() - Состояние всех кнопок мыши (флаги OR)

.position() - Относительную позицию виджета в виде целого QPoint .

	def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # здесь обрабатываем нажатие левой кнопки
            self.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            # здесь обрабатываем нажатие средней кнопки.
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            # здесь обрабатываем нажатие правой кнопки.
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT")

------------------------------------------------------------------------

Qt.NoButton - 0 (000) - Кнопка не нажата, 
						или событие не связано с нажатием кнопки

Qt.LeftButton - 1 (001) - Левая кнопка нажата

Qt.RightButton - 2 (010) - Правая кнопка нажата

Qt.MiddleButton - 4 (100) - Средняя кнопка 
							[обычно это колёсико мыши] нажата

------------------------------------------------------------------------

Контекстные меню

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(self.mapToGlobal(pos))

------------------------------------------------------------------------

Перенаправление наследования Python

def mousePressEvent(self, event):
    print("Mouse pressed!")
    super(self, MainWindow).contextMenuEvent(event)
    
Передача вверх по иерархии макета

class CustomButton(QPushButton)
        def mousePressEvent(self, e):
            e.accept()

class CustomButton(QPushButton)
        def event(self, e):
            e.ignore()

Виджеты

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


# Подкласс QMainWindow для настройки основного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()



QCheckbox - Чекбокс

QComboBox - Окно выпадающего списка

QDateEdit - Для редактирования даты и времени

QDateTimeEdit - Для редактирования даты и времени

QDial - Поворотный циферблат

QDoubleSpinbox - Спиннер для чисел с плавающей точкой

QFontComboBox - Список шрифтов

QLCDNumber - Довольно неприятный дисплей LCD

QLabel - Просто метка, не интерактивная

QLineEdit - Поле ввода со строкой

QProgressBar - Индикатор выполнения

QPushButton - Кнопка

QRadioButton - Переключаемый набор, в котором активен только один элемент

QSlider - Слайдер

QSpinBox - Спиннер для целых чисел

QTimeEdit - Поле редактирования времени

------------------------------------------------------------------------

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListBox, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

------------------------------------------------------------------------

widget = QLabel("Hello")

widget = QLabel("1")  # Создана метка с текстом 1.
widget.setText("2")   # Создана метка с текстом 2.



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.setCentralWidget(widget)
        
Qt.AlignmentFlag.AlignLeft
Выравнивает по левому краю

Qt.AlignmentFlag.AlignRight
Выравнивает по правому краю

Qt.AlignmentFlag.AlignHCenter
Центрирует по горизонтали в доступном пространстве

Qt.AlignmentFlag.AlignJustify
Выравнивает текст в доступном пространстве



Qt.AlignmentFlag.AlignTop
Выравнивается по верху

Qt.AlignmentFlag.AlignBottom
Выравнивается по низу

Qt.AlignmentFlag.AlignVCenter
Центрирует вертикально в доступном пространстве

align_top_left = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop


Qt.AlignmentFlag.AlignCenter
Центрирует горизонтально и вертикально.

widget.setPixmap(QPixmap('otje.jpg'))

По умолчанию изображение масштабируется, 
сохраняя соотношение ширины и высоты. 
Если нужно растянуть и подогнать его по размерам окна, 
установите .setScaledContents(True) в QLabel:

widget.setScaledContents(True)

------------------------------------------------------------------------

QCheckBox

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Checked)

        # Включение трёх состояний: widget.setCheckState(Qt.PartiallyChecked)
        # Или: widget.setTriState(True)
        widget.stateChanged.connect(self.show_state)

        self.setCentralWidget(widget)


    def show_state(self, s):
        print(s == Qt.CheckState.Checked)
        print(s)


Qt.CheckState.Unchecked
Элемент не отмечен

Qt.CheckState.PartiallyChecked
Элемент отмечен частично

Qt.CheckState.Checked
Элемент отмечен




QComboBox

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        # Отправляет текущий индекс (позицию) выбранного элемента.
        widget.currentIndexChanged.connect( self.index_changed )

        # Есть альтернативный сигнал отправки текста.
        widget.textChanged.connect( self.text_changed )

        self.setCentralWidget(widget)


    def index_changed(self, i): # i — это int
        print(i)

    def text_changed(self, s): # s — это str
        print(s)

QComboBox.InsertPolicy.NoInsert
Не вставлять

QComboBox.InsertPolicy.InsertAtTop
Вставить как первый элемент

QComboBox.InsertPolicy.InsertAtCurrent
Заменить текущий выбранный элемент

QComboBox.InsertPolicy.InsertAtBottom
Вставить после последнего элемента

QComboBox.InsertPolicy.InsertAfterCurrent
Вставить после текущего элемента

QComboBox.InsertPolicy.InsertBeforeCurrent
Вставить перед текущим элементом

QComboBox.InsertPolicy.InsertAlphabetically
Вставить в алфавитном порядке



Чтобы использовать их, применяется флаг:

widget.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
Кроме того, можно ограничить количество 
элементов поля, например при помощи .setMaxCount:

widget.setMaxCount(10)




QListWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QListWidget()
        widget.addItems(["One", "Two", "Three"])

        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)


    def index_changed(self, i); # i — не индекс, а сам QList
        print(i.text())

    def text_changed(self, s): # s — это строка
        print(s)



QLineEdit


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QLineEdit()
        widget.setMaxLength(10)
        widget.setPlaceholderText("Enter your text")

        #widget.setReadOnly(True) # раскомментируйте, чтобы сделать доступным только для чтения

        widget.returnPressed.connect(self.return_pressed)
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)

        self.setCentralWidget(widget)


    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)





widget.setInputMask('000.000.000.000;_')




QSpinBox и QDoubleSpinBox



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QSpinBox()
        # Или: widget = QDoubleSpinBox()

        widget.setMinimum(-10)
        widget.setMaximum(3)
        # Или: widget.setRange(-10,3)

        widget.setPrefix("$")
        widget.setSuffix("c")
        widget.setSingleStep(3)  # Или, например, 0.5 в QDoubleSpinBox
        widget.valueChanged.connect(self.value_changed)
        widget.textChanged.connect(self.value_changed_str)

        self.setCentralWidget(widget)

    def value_changed(self, i):
        print(i)

    def value_changed_str(self, s):
        print(s)



QSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QSlider()

        widget.setMinimum(-10)
        widget.setMaximum(3)
        # Или: widget.setRange(-10,3)

        widget.setSingleStep(3)

        widget.valueChanged.connect(self.value_changed)
        widget.sliderMoved.connect(self.slider_position)
        widget.sliderPressed.connect(self.slider_pressed)
        widget.sliderReleased.connect(self.slider_released)

        self.setCentralWidget(widget)

    def value_changed(self, i):
        print(i)

    def slider_position(self, p):
        print("position", p)

    def slider_pressed(self):
        print("Pressed!")

    def slider_released(self):
        print("Released")




widget.QSlider(Qt.Orientiation.Vertical)


widget.QSlider(Qt.Orientiation.Horizontal)



QDial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QDial()
        widget.setRange(-10, 100)
        widget.setSingleStep(0.5)

        widget.valueChanged.connect(self.value_changed)
        widget.sliderMoved.connect(self.slider_position)
        widget.sliderPressed.connect(self.slider_pressed)
        widget.sliderReleased.connect(self.slider_released)

        self.setCentralWidget(widget)

    def value_changed(self, i):
        print(i)

    def slider_position(self, p):
        print("position", p)

    def slider_pressed(self):
        print("Pressed!")

    def slider_released(self):
        print("Released")


















