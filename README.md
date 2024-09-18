## Стек
FastAPI, SQLAlchemy, PostgreSQL

## Запуск проекта
1. В терминале ввести команду `docker-compose up -d --build`
2. Перейти по адресу http://localhost:8000/docs
3. Использовать ручку API `/auth/register` на странице http://localhost:8000/docs
4. Использовать ручку `/auth/login` на странице http://localhost:8000/docs
5. После этого можно использовать остальные ручки на странице http://localhost:8000/docs

## Что было сделано
- Регистрация
- Вход в систему
- Писать статьи
- Просмотр списка статей
- Детальный просмотр статьи и её прочтение (одно и то же)
- Удаление своей статьи объявления
- Написание комментариев к статье
- Реализован функционал администратора
    - Удаление комментариев в любой статье
    - Назначение пользователя администратором
- Серверная пагинация
- Фильтрация статей
- Сортировка статей
- Авторизация с помощью JWT-токена
- Жалоба на статью
- Отзыв на статью
- Просмотр администратором жалоб на статьи
- Бан/разбан пользователя администратором
- Сборка проекта в докер-образ
- Настройка логгера(терминал)

Описание API находится в файле `openapi.yml`.
Все зависимости находятся в файле `requirements.txt`.