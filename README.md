Инструкция по установке и запуску
1. Клонирование репозитория
Откройте терминал и выполните команду:
git clone https://github.com/Sealal07/hospital_flask_phy51_1.git
cd hospital_flask_phy51_1/hospital

2. Настройка виртуального окружения
Рекомендуется использовать виртуальное окружение для изоляции зависимостей проекта:

# Создание окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (macOS/Linux)
source venv/bin/activate

3. Установка зависимостей
Установите все необходимые библиотеки из файла requirements.txt:

pip install -r requirements.txt


4. Инициализация базы данных
Проект использует Flask-Migrate и SQLAlchemy. Перед первым запуском необходимо создать базу данных (по умолчанию sqlite):

flask db init
flask db migrate -m "Initial migration"
flask db upgrade



5. Запуск приложения
Запустите сервер разработки:

python run.py
После запуска приложение будет доступно по адресу: http://127.0.0.1:5000/

