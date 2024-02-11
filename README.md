# Телефонный справочник
## Техническое задание
**Реализовать телефонный справочник со следующими возможностями:**
1. Вывод постранично записей из справочника на экран
2. Добавление новой записи в справочник
3. Возможность редактирования записей в справочнике
4. Поиск записей по одной или нескольким характеристикам
   
**Требования к программе:**
1. Реализация интерфейса через консоль (без веб- или графического интерфейса)
2. Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист
3. В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый)
   
**Плюсом будет:**
1. Аннотирование функций и переменных
2. Документирование функций
3. Подробно описанный функционал программы
4. Размещение готовой программы и примера файла с данными на github

## Описание реализации
Данная программа представляет собой консольное приложение телефонного справочника. 

Реализован функционал вывода, добавления и редактирования записей, а также поиска записей по одной или нескольким характеристикам (полям).

Справочная информация хранится в файле формата JSON, который должен находиться в директории программы.

**Зависимости**

Для запуска необходима установка модуля Prettytable:

    pip install prettytable
