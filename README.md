##### Установка среды разработки в ANACONDA

1) открыть conda prompt
2) Выполнить команду (environment.yml находится в корне проекта)
~~~
conda env create -f environment.yml
~~~
3) Для входа в среду conda activate qt5


##### Редактирование UI файла

Виполнить
~~~
qt5-tools designer
~~~

После выбрать файл в папке assets

##### Билд UI файла

Находясь в дирректории проекта выполнить
~~~

python -m PyQt5.uic.pyuic -x ./assets/MainWindow.ui -o ./UI/MainWindow.py

~~~

##### Билд приложения

Вызывать в каталоге где надо сохрвнить файл !!!!!!!!!! А НЕ В КАТАЛОГЕ ПРОЕКТА

~~~

pyinstaller --onefile --noconsole --icon=PATH PATH_TO_MAIN

~~~

Для простоты добавлена дирректоия build в корень проека

