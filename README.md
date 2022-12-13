# Yacut. Сервис коротких ссылок

## Описание проекта
Учебный проект на Flask и SQLAlchemy, сервис для создания коротких ссылок. 
Принимает от 
пользователя длинный URL адрес и предпочтительный анкор короткой ссылки (от 
1 до 16 символов) и выдает готовую короткую ссылку.Если предпочтительный 
анкор не указан, генерируется рандомные 6 символов по маске a-zA-Z0-9.

Так же, дополнительно сделан API.

POST-запрос на страницу http://127.0.0.1:5000/api/id/ , ключ custom_id 
- необязателен. Тело запроса - ниже
```
{
    "url": "<my_full_url>",
    "custom_id": "<my_short_url>"
}
```
И GET-запрос на страницу http://127.0.0.1:5000/api/id/<string:id>/ , где 
<string:id> - анкор короткой ссылки пользователя. Ответ - ниже
```
{
    "url": "<my_full_url>"
}
```

## Технологический стек
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [SQLALCHEMY](https://www.sqlalchemy.org/)
- [WTForms](https://wtforms.readthedocs.io/en/3.0.x/)


## Разворачивание проекта локально (Windows)
1. Скопировать себе гит (git clone)
2. Установить виртуальное окружение
3. Установить зависимости
```
pip install -r requirements.txt
```
5. Запускать сервер командой ```flask run```

## Автор
dvkonstantinov
telegram: https://t.me/Dvkonstantinov