#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs-python.ru/standart-library/modul-threading-python/klass-thread-modulja-threading/

Атрибуты и методы объекта Thread.

Thread.start() запускает экземпляр Thread,
Thread.run() представляет активность потока,
Thread.join() ждет, пока поток не завершится,
Thread.name имя потока,
Thread.getName() старый API getter для атрибута name,
Thread.setName() старый API setter для атрибута name,
Thread.ident идентификатор потока,
Thread.native_id интегральный идентификатор потока,
Thread.is_alive() сообщает, является ли поток живим,
Thread.daemon сообщает, является ли поток демоническим,
Thread.isDaemon() старый API для атрибута daemon,
Thread.setDaemon() старый API для атрибута daemon,
Пример выполнения функции в 5-ти потоках.

th = threading.Thread(group=None, target=None, 
                     name=None, args=(), 
                     kwargs={}, *, daemon=None)

group=None - зарезервировано для будущего расширения при реализации класса ThreadGroup.
target=None - вызываемый объект (функция), который будет вызываться методом Thread.run(). По умолчанию None и означает, что ничего не вызывается.
name=None - имя потока. По умолчанию уникальное имя создается в форме "Thread-N", где N - небольшое десятичное число или с версии Python 3.10 Thread-N (target), где target - это target.__ name__, если конечно указан аргумент target.
args=() - кортеж аргументов для вызываемого объекта target. По умолчанию ()
kwargs={} - словарь ключевых аргументов для вызываемого объекта target. По умолчанию {}.
daemon=None - если аргумент daemon не None, то он явно устанавливает, является ли поток демоническим. Если daemon=None (по умолчанию), то демоническое свойство наследуется от текущего потока.

Класс Thread модуля threading запускает какое либо действие, которое будет выполняется в отдельном потоке управления.

Есть два способа запустить какое либо действие:

Передать вызываемый объект (функцию) в конструктор.
Переопределить метод Thread.run() в подклассе.
Внимание! Никакие другие методы не должны переопределяться в подклассе (кроме конструктора). Другими словами, можно переопределять только методы __init__() и Thread.run() этого класса.

Как только объект потока создан, его деятельность должна быть запущена путем вызова метода потока Thread.start(). Это вызывает метод Thread.run() в отдельном потоке управления.

Как только активность потока запущена, он считается "живым". Поток перестает быть активным, когда его метод Thread.run() завершается либо обычно, либо при возникновении необработанного исключения. Метод Thread.is_alive() проверяет, жив ли поток.

Другие потоки могут вызывать метод Thread.join(), который блокирует вызывающий поток до тех пор, пока не завершится поток, чей метод .join() вызван. Например, если для всех порожденных программой потоков вызвать этот метод, то дальнейшее выполнение программы будет заблокировано до тех пор пока все потоки не завершатся.

У потока есть имя. Имя может быть передано конструктору (аргумент name) и прочитано или изменено через атрибут Thread.name.

Если метод Thread.run() вызывает исключение, то для его обработки вызывается threading.excepthook(). По умолчанию threading.excepthook() молча игнорирует исключение SystemExit.

Поток можно пометить как "демонический поток". Значение этого флага заключается в том, что когда программа Python завершается, работающими остаются только потоки демона. Начальное значение наследуется от создающего потока. Флаг можно установить с помощью свойства Thread.daemon или аргумента конструктора daemon.

Примечание. Потоки демона внезапно останавливаются при завершении работы. Их ресурсы (такие как открытые файлы, транзакции базы данных и т. д.) могут быть освобождены неправильно. Если необходимо, чтобы потоки корректно останавливались, то делайте их недемоническими и используйте подходящий механизм сигнализации, такой как объект threading.Event().

Существует объект основного потока программы. Основной поток соответствует начальному потоку управления в программе Python. Это не поток демона.

Существует вероятность того, что будут созданы "объекты фиктивного потока". Это объекты потоков, соответствующие "чужеродным потокам", которые представляют собой потоки управления, запускаемые вне модуля потоковой передачи, например непосредственно из кода языка C. Объекты фиктивного потока имеют ограниченную функциональность. Они всегда считаются живыми и демоническими и не могут быть объединены методом Thread.join(). Они никогда не удаляются, так как невозможно обнаружить завершение чужих потоков.

Изменено в версии 3.10: если аргумент name опущен, то используется имя функции target.
