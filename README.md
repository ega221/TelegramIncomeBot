# TelegramIncomeBot

## Сборка
1. Клонируйте репозиторий
2. Установите зависимости: pip install -r requirements.txt
3. Задайте в файле окружения .env собственный токен telegram
4. Запустите приложение: make local-start-app
5. Инициализируйте миграции: make init-alembic
6. Обновите миграции: make local-migration-up
7. Запустите приложение: python ./run_bot.py

## Какие команды выполняет бот?
1. /start: начать диалог
2. /make_income: создать источник дохода
3. /make_expense: создать источник расхода
4. /cancel: отменить текущую команду
