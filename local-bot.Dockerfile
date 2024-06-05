# Укажите необходимую версию python
FROM python:3.12-slim

ENV APP_DIR /opt/app

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR $APP_DIR

# Скопируйте в контейнер файлы, которые редко меняются
COPY requirements.txt requirements.txt

# Установите зависимости
RUN  apt-get update \
     && apt-get -y install libpq-dev gcc \
     && groupadd -r web \
     && useradd -d $APP_DIR -r -g web web \
     && chown web:web -R $APP_DIR \
     && apt-get install -y netcat-traditional \
     && apt-get install -y build-essential \
     && apt-get install -y acl \
     && pip install --upgrade pip

RUN pip install -r requirements.txt

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . $APP_DIR

# Выдаем пользователю права на испольняемый файл, чтобы он смог его запустить.
RUN setfacl -R -m u:web:rwx $APP_DIR/run_bot.py

USER web

ENTRYPOINT ["python", "./run_bot.py", ".env"]