import json
from peewee import *
import os
from sys import exit

"""Скрипт для подключения к БД
    Блок с настройками
    1) Json в .env существует и валидный?
        [да]:
        1.1) Попытка загрузить данные
        [нет]:
        1.1) Попросить пользователя ввести валидные данные
        1.2) Создать/Переписать JSON
    Блок с подключением
    2) Попытка подключения
    3) Подключение НЕ успешно?
        [да]: ошибка в данных для подключения?
            [да]: Вызвать блок с настройками и выдать ошибку
            [нет]: Вызвать ошибку и завершить выполнение программы
    4) Вернуть python класс для подключения к бд

    Ожидаемая форма json:
        database: string
        user: string
        password: string
        host: string (стандарт localhost)
        port: int (4 числа)
"""

# параметры
ENV = ".env"
DB_JSON = ".env/db_parameters.json"

"""Ф-ии для работы с настройками"""
def is_env_exist():
    if os.path.isdir(ENV):
        return True
    else:
        return False

def is_json_exist():
    if os.path.isfile(DB_JSON):
        return True
    else:
        return False

def is_parameters_valid(parameters: dict) -> tuple[bool, str]:
    if parameters.get("database") == None or parameters.get("user") == None or parameters.get("password") == None or parameters.get("host") == None or parameters.get("port") == None:
        return (False, "Данные не должны быть пустые")
    if type(parameters["database"]) != str:
        return (False, f"database должно быть str! Получено: {type(parameters["database"])}")
    if type(parameters["host"]) != str:
        return (False, f"host должно быть str! Получено: {type(parameters["host"])}")
    if type(parameters["password"]) != str:
        return (False, f"password должно быть str! Получено: {type(parameters["password"])}")
    if type(parameters["port"]) != int:
        return (False, f"port должно быть int! Получено: {type(parameters["port"])}")
    if type(parameters["user"]) != str:
        return (False, f"user должно быть str! Получено: {type(parameters["user"])}")
    if len(str(parameters["port"])) != 4:
        return (False, "port должен быть 4 символа в длину!")
    # если ни одной ошибки, то...
    return (True, "")
    
def load_options() -> dict:
    """загрузка настроек"""
    try:
        with open(DB_JSON, "r", encoding="utf-8") as file:
            parameters = json.load(file)
            parameters["port"] = int(parameters["port"]) # превращаем порт в число
            return parameters
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка: синтаксиса в JSON: {e}")
    except ValueError:
        raise ValueError("Ошибка: 'port' должен быть числом")

def setting_parameters() -> dict:
    print("Настройка подключения к базе...")
    parameters = {}
    def input_parameters():
        parameters["host"] = input("host: ")
        parameters["port"] = int(input("port: "))
        parameters["database"] = input("database: ")
        parameters["user"] = input("user: ")
        parameters["password"] = input("password: ")
        validation = is_parameters_valid(parameters)
        if not validation[0]:
            print("Данные введены не правильно!")
            print(validation[1])
            input("Для повторного ввода нажмите Enter...")
            # Рекурсия
            input_parameters()
    input_parameters()
    print("Сохранение параметров...")
    with open(DB_JSON, "w", encoding="utf-8") as file:
        json.dump(parameters, file)
    print("Параметры сохранены!")
    return parameters
"""конец блока настроек"""
def db_connect() -> PostgresqlDatabase:
    parameters = {}
    """Блок настроек"""
    if not is_env_exist():
        """Если папка env не существует, то создать"""
        os.mkdir(".env");
    if not is_json_exist():
        parameters = setting_parameters()
    else: # если файл есть
        try: # Пробуем прочесть
            if is_parameters_valid(load_options())[0]:
                parameters = load_options()
            else:
                parameters = setting_parameters()
        except Exception as e: # на случай ошибки при чтении файла!
            """Загрузить настройки и продолжить уже с ними"""
            print(f"Ошибка при чтении файла: {e}")
            parameters = setting_parameters()
    """Теперь создать подключение"""
    db = None
    def try_connect(db, parameters):
        try:
            db = PostgresqlDatabase(
                database=parameters.get("database"),
                user=parameters.get("user"),
                password=parameters.get("password"),
                host=parameters.get("host"),
                port=parameters.get("port"),
                autorollback=True
                )
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            if input("Поменять настройки? [y/n]").lower() == "y":
                parameters = setting_parameters()
                try_connect(db, parameters)
            else:
                print("Завершение работы...")
                exit(0)
    try_connect(db, parameters)
    if db is not None:
        return db

if __name__ == "__main__":
    db = db_connect()