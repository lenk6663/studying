# Перечень тестов
## Блочные тесты

### Класс Player
* **Тест 1: Перемещение игрока вверх**
    * Начальное состояние: Игрок в позиции (x, y)
    * Входные данные: Вызов функции `move` с параметром `Direction.UP`
    * Ожидаемый результат: Позиция игрока станет (x, y - 1)
* **Тест 2: Перемещение игрока вправо**
    * Начальное состояние: Игрок в позиции (x, y)
    * Входные данные: Вызов функции `move` с параметром `Direction.RIGHT`
    * Ожидаемый результат: Позиция игрока станет (x + 1, y)
* **Тест 3: Перемещение игрока вниз**
    * Начальное состояние: Игрок в позиции (x, y)
    * Входные данные: Вызов функции `move` с параметром `Direction.DOWN`
    * Ожидаемый результат: Позиция игрока станет (x, y + 1)
* **Тест 4: Перемещение игрока влево**
    * Начальное состояние: Игрок в позиции (x, y)
    * Входные данные: Вызов функции `move` с параметром `Direction.LEFT`
    * Ожидаемый результат: Позиция игрока станет (x - 1, y)

### Класс Inventory
* **Тест 1: Добавление рыбы в инвентарь**
    * Начальное состояние: Инвентарь пуст
    * Входные данные: Вызов функции `add` с экземпляром класса `Fish`
    * Ожидаемый результат: В инвентаре появилась запись о рыбе
* **Тест 2: Удаление рыбы из инвентаря**
    * Начальное состояние: Инвентарь содержит одну рыбу
    * Входные данные: Вызов функции `del` с экземпляром класса `Fish`
    * Ожидаемый результат: Запись о рыбе в инвентаре удалена
* **Тест 3: Отображение содержимого инвентаря**
    * Начальное состояние: Инвентарь содержит список предметов
    * Входные данные: Вызов функции `display`
    * Ожидаемый результат: Список предметов из инвентаря отображается на экране

### Класс MiniGame
* **Тест 1: Перемещение курсора вверх**
    * Начальное состояние: Курсор в позиции (x, y)
    * Входные данные: Вызов функции `moveCursor` с параметром `Direction.UP`
    * Ожидаемый результат: Позиция курсора станет (x, y - 1)
* **Тест 2: Перемещение курсора вправо**
    * Начальное состояние: Курсор в позиции (x, y)
    * Входные данные: Вызов функции `moveCursor` с параметром `Direction.RIGHT`
    * Ожидаемый результат: Позиция курсора станет (x + 1, y)
* **Тест 3: Перемещение курсора вниз**
    * Начальное состояние: Курсор в позиции (x, y)
    * Входные данные: Вызов функции `moveCursor` с параметром `Direction.DOWN`
    * Ожидаемый результат: Позиция курсора станет (x, y + 1)
* **Тест 4: Перемещение курсора влево**
    * Начальное состояние: Курсор в позиции (x, y)
    * Входные данные: Вызов функции `moveCursor` с параметром `Direction.LEFT`
    * Ожидаемый результат: Позиция курсора станет (x - 1, y)

### Класс Fish
* **Тест 1: Отображение рыбы**
    * Начальное состояние: Рыба в позиции (x, y)
    * Входные данные: Вызов функции `draw`
    * Ожидаемый результат: На экране отображается изображение рыбы в позиции (x, y)

### Класс Shop
* **Тест 1: Отображение магазина**
    * Начальное состояние: Магазин закрыт
    * Входные данные: Вызов функции `display`
    * Ожидаемый результат: На экране отображается интерфейс магазина

### Класс Object
* **Тест 1: Увеличение количества объекта**
    * Начальное состояние: Объект с количеством 0
    * Входные данные: Вызов функции `increase_amount` с параметром 5
    * Ожидаемый результат: Количество объекта становится 5
* **Тест 2: Уменьшение количества объекта**
    * Начальное состояние: Объект с количеством 5
    * Входные данные: Вызов функции `reduce_amount` с параметром 3
    * Ожидаемый результат: Количество объекта становится 2

## План тестирования
#### Функциональная возможность 1: Пользователь может управлять персонажем на лодке

* Тест 1: Перемещение персонажа вверх
* Начальное состояние: Персонаж в позиции (x, y)
* Входные данные: Нажатие клавиши "W"
* Ожидаемый результат: Позиция персонажа станет (x, y - 1)
* Тест 2: Перемещение персонажа вправо
* Начальное состояние: Персонаж в позиции (x, y)
* Входные данные: Нажатие клавиши "D"
* Ожидаемый результат: Позиция персонажа станет (x + 1, y)
* Тест 3: Перемещение персонажа вниз
* Начальное состояние: Персонаж в позиции (x, y)
* Входные данные: Нажатие клавиши "S"
* Ожидаемый результат: Позиция персонажа станет (x, y + 1)
* Тест 4: Перемещение персонажа влево
* Начальное состояние: Персонаж в позиции (x, y)
* Входные данные: Нажатие клавиши "A"
* Ожидаемый результат: Позиция персонажа станет (x - 1, y)

#### Функциональная возможность 2: Пользователь может играть в миниигру ловли рыбы

* Тест 1: Запуск миниигры
* Начальное состояние: Персонаж находится вблизи рыбного места
* Входные данные: Нажатие клавиши "E"
* Ожидаемый результат: Открывается интерфейс миниигры
* Тест 2: Перемещение курсора вверх
* Начальное состояние: Курсор в позиции (x, y)
* Входные данные: Движение мыши вверх
* Ожидаемый результат: Позиция курсора станет (x, y - 1)
* Тест 3: Перемещение курсора вправо
* Начальное состояние: Курсор в позиции (x, y)
* Входные данные: Движение мыши вправо
* Ожидаемый результат: Позиция курсора станет (x + 1, y)
* Тест 4: Перемещение курсора вниз
* Начальное состояние: Курсор в позиции (x, y)
* Входные данные: Движение мыши вниз
* Ожидаемый результат: Позиция курсора станет (x, y + 1)
* Тест 5: Перемещение курсора влево
* Начальное состояние: Курсор в позиции (x, y)
* Входные данные: Движение мыши влево
* Ожидаемый результат: Позиция курсора станет (x - 1, y)

#### Функциональная возможность 3: Пользователь может продавать рыбу в магазине и на островах

* Тест 1: Открытие магазина
* Начальное состояние: Персонаж находится вблизи магазина
* Входные данные: Нажатие клавиши "E"
* Ожидаемый результат: Открывается интерфейс магазина
* Тест 2: Выбор опции продажи рыбы
* Начальное состояние: Интерфейс магазина открыт
* Входные данные: Выбор опции "Продать рыбу"
* Ожидаемый результат: Открывается меню продажи рыбы
* Тест 3: Продажа рыбы
* Начальное состояние: Меню продажи рыбы открыто
* Входные данные: Выбор рыбы и нажатие кнопки "Продать"
* Ожидаемый результат: Рыба продаётся, и на счет игрока зачисляются деньги

#### Функциональная возможность 4: Пользователь может покупать улучшения в магазине

* Тест 1: Выбор опции улучшения
* Начальное состояние: Интерфейс магазина открыт
* Входные данные: Выбор опции "Улучшения"
* Ожидаемый результат: Открывается меню улучшений
* Тест 2: Улучшение лодки
* Начальное состояние: Меню улучшений открыто
* Входные данные: Выбор улучшения "Улучшение лодки"
* Ожидаемый результат: Лодка улучшается, и её скорость увеличивается
* Тест 3: Улучшение удочки
* Начальное состояние: Меню улучшений открыто
* Входные данные: Выбор улучшения "Улучшение удочки"
* Ожидаемый результат: Удочка улучшается, и скорость перемещения крючка увеличивается

#### Функциональная возможность 5: Пользователь может купить наживку или прикорм в магазине

* Тест 1: Выбор опции покупки наживки
* Начальное состояние: Интерфейс магазина открыт
* Входные данные: Выбор опции "Купить наживку"
* Ожидаемый результат: Открывается меню покупки наживки
* Тест 2: Покупка наживки
* Начальное состояние: Меню покупки наживки открыто
* Входные данные: Выбор наживки и нажатие кнопки "Купить"
* Ожидаемый результат: Наживка покупается, и в инвентаре игрока появляется запись об этом
* Тест 3: Покупка прикорма
* Начальное состояние: Меню покупки прикорма открыто
* Входные данные: Выбор прикорма и нажатие кнопки "Купить"
* Ожидаемый результат: Прикорм покупается, и в инвентаре игрока появляется запись об этом

#### Функциональная возможность 6: Пользователь может открыть инвентарь при помощи кнопки E

* Тест 1: Открытие инвентаря
* Начальное состояние: Игра запущена
* Входные данные: Нажатие клавиши "E"
* Ожидаемый результат: Открывается интерфейс инвентаря