# SOCIAL NETWORK
### Описание
Добро пожаловать! Приложение **SOCIAL NETWORK** создано для того чтобы создавать пользователей, создавать посты, лайкать посты и анализировать происходящее)
### Установка
- Нужно клонировать репозиторий командой:
```bash
git clone https://github.com/PavelKhanOff/social-network
```
- [Установите Докер](https://docs.docker.com/engine/install/)
- Из корневой директории локально разверните у себя контейнер командами:
```bash
docker build -t social-network .
docker run 
```
#### Первоначальная настройка Django:
```bash
- docker-compose exec web python manage.py migrate --noinput
- docker-compose exec web python manage.py collectstatic --no-input
```
#### Создание суперпользователя:
```bash
- docker-compose exec web python manage.py createsuperuser
```

### Алгоритм регистрации пользователей:
Нужно отправить POST запрос на адрес /api/users/, указать username, password и email)
#### Автор:
Автор Павел Хан. Задание было выполнено в тестового задания.


docker build -t yamdb .
docker run -it -p 8000:8000 yamdb
