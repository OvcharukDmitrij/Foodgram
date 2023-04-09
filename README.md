# Foodgram!
### Cоциальная сеть со вкусными рецептами!

Приложение позволяет публиковать свои рецепты,
смотреть рецепты других пользователей,
подписываться на других авторов, добавлять рецепты в избранное и в
список покупок, а также распечатывать список ингредиентов из понравившихся рецептов.

### Технологии

Для разработки проекта применялись следующие технологии:

#### *Python*
#### *Django*
#### *PostgreSQL*
#### *API DRF*
#### *Docker*
#### *GitHub*
#### и сотни страниц с информацией в интернете)))

### Приложение доступно по адресу [http://62.84.125.113]

### Запуск проекта:
1. Клонируйте проект:
```
git clone https://github.com/OvcharukDmitrij/foodgram-project-react
```
2. Скопируйте файлы с локального компьютера на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
3. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
4. Загрузите образы Backend и Frontend на DockerHub:
```
docker push <username>/<imagename>:<tag>: 
```
5. Соберите контейнер, выполните миграции, создайте суперюзера и соберите статику:
```
sudo docker-compose up -d --build
sudo docker-compose migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
6. Скопируйте данные с перечнем ингредиентов:
```
sudo docker-compose exec backend python manage.py load_data
```

