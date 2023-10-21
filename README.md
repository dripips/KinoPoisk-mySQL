# KinoPoisk mySQL
Этот скрипт предназначен для получения данных о фильмах из Kinopoisk API и их сохранения в базе данных MySQL.

## Использование

1. Установите все необходимые зависимости, выполнив:

```bash
pip install requests mysql-connector-python
```

2. Замените следующие значения в скрипте на свои собственные:

   - `host`: Адрес вашего MySQL-сервера
   - `user`: Имя пользователя MySQL
   - `password`: Пароль пользователя MySQL
   - `database`: Имя базы данных MySQL
   - `api_key`: Ваш API-ключ Kinopoisk
   - Диапазон `range` в цикле `for kinopoisk_id in range(490, 99999999)` можно изменить на нужный.

3. Запустите скрипт:

```bash
python app.py
```

Скрипт начнет получение данных о фильмах из Kinopoisk API и сохранение их в базе данных MySQL.

## Зависимости

- [requests](https://pypi.org/project/requests/): Для выполнения HTTP-запросов к Kinopoisk API.
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/): Для подключения к базе данных MySQL.

## Лицензия

Этот проект распространяется под [лицензией MIT](LICENSE).
