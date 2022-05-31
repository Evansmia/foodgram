# Foodgram - продуктовый помощник

## Доступен по адресу: **http://84.201.155.233/**
### Администратор: почта - reviewer@reviewer.ru, пароль - 12345
### Тестовый пользователь 1: Ivan1@yandex.ru/testuser1 и Тестовый пользователь 2: viki35@yandex.ru/testuser2 

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Описание проекта
Онлайн-сервис Foodgram («Продуктовый помощник») создан для начинающих кулинаров и опытных гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать в формате .txt сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект разворачивается в Docker контейнерах: backend-приложение API, PostgreSQL-база данных, nginx-сервер и frontend-контейнер.

## Системные требования
- Python 3.7+
- Docker
- Works on Linux, Windows, macOS

## Запуск проекта на виртуальном сервере
Клонируйте репозиторий и перейдите в него в командной строке.
Создайте и активируйте виртуальное окружение:
```
git clone https://github.com/Evansmia/foodgram-project-react.git
```
Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```bash
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

````
Скопируйте файлы `docker-compose.yml`, `nginx.conf` и `.env` из папки `/infra/` на Ваш виртуальный сервер:
```bash
scp <название файла> <username>@<server_ip>:/home/<username>/

```
Далее зайдите на виртуальный сервер и подготовьте его к работе с проектом:
 
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
sudo apt install docker-compose

```
Теперь можно развернуть проект с помощью Docker используя контейнеризацию:

```bash
sudo docker-compose up -d --build

```
Осталось выполнить миграции, подключить статику, создать профиль админастратора:

```bash
sudo docker exec -it <name или id контейнера backend> python manage.py migrate
sudo docker exec -it <name или id контейнера backend> python manage.py collectstatic
sudo docker exec -it <name или id контейнера backend> python manage.py createsuperuser

```
И в конце подгрузить список ингредиентов:

```bash
sudo docker exec -it <name или id контейнера backend> python manage.py loadjson --path "recipes/data/ingredients.json"

```
