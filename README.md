## Проектная работа 4, 5го и 7го спринта

## Переменные которые надо указать в .env предоставлены в .env.simple для развертывания ASYNC_API:

### Микросервис поддерживает контракт из AuthService

### Для просмотра документации http://localhost/api/openapi#/

### При обращении к ендпоинтам сервиса требуется валидный jwt access token который можно получить при регистрации и последующем логине в AuthService

![image](https://user-images.githubusercontent.com/62523428/154866443-19e5c1e3-3b71-44dc-84fc-a2f02bb6cef7.png)

![image](https://user-images.githubusercontent.com/62523428/154866476-f39f9ca1-b8d8-4063-a9ec-a0f845366aa0.png)




Запускаем контейнеры:

docker-compose up -d


Для запуска тестового контейнера:

docker-compose -f docker-compose.tests.yaml up -d

Для просмотра логов контейнреа использовать:

docker logs -f <имя_контейнера>


Ссылка на ETL: https://github.com/bisuMei/ETL
