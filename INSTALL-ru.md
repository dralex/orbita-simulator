# Руководство по установке на Linux

Для работы симулятора вам нужен Python (версии 3.x).

1. Прежде всего обновим все системные пакеты и установим python3.

```
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3
$ sudo apt install python3-pip
```

2. Установите Google Protocol Buffers (https://protobuf.dev) версии 3.

```
$ sudo apt install protobuf-compiler
```

3. Установите все необходимые библиотеки из файла `requirements.txt` с помощью `pip`:

```
$ pip3 install -r requirements.txt
```

4. Выберите интересующую вас модель и запустите в ее директории исполнение Makefile-а:

```
$ cd models/earth
$ make unix
```

Makefile собирает необходимые для работы симулятора кодировщики XML и необходимые обработчики протоколов.

5. Попробуйте запустить тестовый аппарат из директории `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

6. Чтобы узнать аргументы для запуска в командной строке выполните скрипт `simulation.py` без параметров.

7. Для запуска серверной версии Орбиты подкорректируйте файл `orbit_server.cfg` и запустите сервер как демона.

8. Для локализаций сообщений симулятора (на русский язык), необходимо установить пакет `gettext` и запустить команду `make messages` в директории соответствующей модели. 


# Руководство по установке на MacOS


1. Прежде всего установим менеджер пакетов brew (https://brew.sh/index_ru).

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Установим python3 .

```
$ brew install python3
```

3. Установите Google Protocol Buffers (https://protobuf.dev) версии 3.

```
$ brew install protobuf
```

4. Установите все необходимые библиотеки из файла `requirements.txt` с помощью `pip`:

```
$ pip3 install -r requirements.txt
```

5. Выберите интересующую вас модель и запустите в ее директории исполнение Makefile-а:

```
$ cd models/earth
$ make unix
```

Makefile собирает необходимые для работы симулятора кодировщики XML и необходимые обработчики протоколов.

6. Попробуйте запустить тестовый аппарат из директории `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

7. Чтобы узнать аргументы для запуска в командной строке выполните скрипт `simulation.py` без параметров.

8. Для запуска серверной версии Орбиты подкорректируйте файл `orbit_server.cfg` и запустите сервер как демона.

9. Для локализаций сообщений симулятора (на русский язык), необходимо установить пакет `gettext` и запустить команду `make messages` в директории соответствующей модели. 



# Руководство по установке на Windows


1. Прежде всего установим python3 (https://www.python.org/downloads/windows).

2. Установим инструмент make (все команды будем выполнять в окне PowerShell).
```
$ Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
$ choco install make
```

3. Установите Google Protocol Buffers (https://protobuf.dev) версии 3.

3.1 Устанавливаем архив win64/win32 из официального репозитория (https://github.com/protocolbuffers/protobuf/releases).

3.2 Разархивируйте архив в удобное для вас место.

3.3 Скопируйте путь до файла protoc.exe, который будет находиться в архиве.

3.4 Добавьте путь до файла в параметры среды (в поле PATH)



4. Установите все необходимые библиотеки из файла `requirements.txt` с помощью `pip`:

```
$ pip3 install -r requirements.txt
```

5. Выберите интересующую вас модель и запустите в ее директории исполнение Makefile-а:

5.1 Если вы запускаете симулятор впервые:
```
$ cd models/earth
$ make win
```
5.2 Если вы запускаете симулятор повторно и внесли какие-то изменения:
```
$ cd models/earth
$ make clean_win
$ make win
```

Makefile собирает необходимые для работы симулятора кодировщики XML и необходимые обработчики протоколов.

6. Попробуйте запустить тестовый аппарат из директории `probes`:

```
$ python3 simulation.py probes/test1.xml --debug-log=debug.log --mission-log=telemetry.log --image=.
```

7. Чтобы узнать аргументы для запуска в командной строке выполните скрипт `simulation.py` без параметров.

8. Для запуска серверной версии Орбиты подкорректируйте файл `orbit_server.cfg` и запустите сервер как демона.

9. Для локализаций сообщений симулятора (на русский язык), необходимо установить пакет `gettext` и запустить команду `make messages` в директории соответствующей модели. 
