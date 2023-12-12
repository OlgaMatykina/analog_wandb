# wandb $->$ onedb (1db)
 Представляю вашему вниманию упрощенный аналог популярного инструмента для логирования экспериментов WandB. Веб-сервис написан с использованием библиотеки Flask и базы данных SQLite.  
 Запуск выполняется командой
 ```
  docker-compose up
 ```
В код эксперимента, который предстоит логировать, необходимо ввести username зарегистрированного пользователя, импортировать класс Run.
В папке experiments хранится пример эксперимента, для запуска нужно войти в запущенный ранее контейнер с помощью команды
```
docker exec -it analog_wandb-web-1 /bin/bash -c "/bin/bash"
```
и запустить код эксперимента
```
python -m experiments.main
```
Фрагмент работы сервиса представлен в следующем видео.

![onedb_edited2 (2)](https://github.com/OlgaMatykina/analog_wandb/assets/89583270/49c9a7b8-be0f-4ecc-8e41-3ef7da2c1aeb)

