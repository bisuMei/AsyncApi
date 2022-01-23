Проектная работа 4 и 5го спринта

Переменные которые надо указать в .env для развертывания ASYNC_API:

PROJECT_NAME=movies

REDIS_HOST=a_redis

REDIS_PORT=6379

ELASTIC_HOST=a_elasticsearch

ELASTIC_PORT=9200

ELASTIC_INDEX={"movies": "movies", "persons": "persons", "genres": "genres"}

SERVICE_HOST=a_main-app

SERVICE_PORT=8000

Для запуска проекта использовать докер компоуз:

docker-compose up -d

Для запуска тестового окружения в директории tests/functional/.env прописать:

PROJECT_NAME=movies

REDIS_HOST=a_redis

REDIS_PORT=6379

ELASTIC_HOST=a_elasticsearch

ELASTIC_PORT=9200

ELASTIC_INDEX={"movies": "test_movies", "persons": "test_persons", "genres": "test_genres"}

SERVICE_HOST=a_main-app-test

SERVICE_PORT=8080

Далее стартуем команду:

docker-compose -f docker-compose.tests.yaml up -d

Для просмотра логов контейнреа использовать:

docker logs -f <имя_контейнера>


Ссылка на ETL: https://github.com/bisuMei/ETL
