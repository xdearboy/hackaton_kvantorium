import random


class Pet:
    """
    Базовый класс питомца.

    Свойства:
        _pet_id (int) - уникальный идентификатор питомца
        _name (str) - имя питомца
        _age (int) - возраст питомца (в тиках)
        _weight (float) - вес питомца в кг
        _hunger (int) - уровень голода (0-100, 0 = сыт, 100 = голоден)
        _happiness (int) - уровень счастья (0-100)
        _health (int) - уровень здоровья (0-100)
        _is_alive (bool) - статус жизни питомца

    Методы:
        __init__(pet_id, name, weight) -> None
        feed(food_type) -> None - покормить питомца (снижает голод на 10)
        play(hours) -> None - поиграть с питомцем (повышает счастье, tăng голод)
        sleep(hours) -> None - уложить питомца спать (повышает здоровье)
        tick() -> None - имитация одного дня (голод растёт, счастье падает, проверка смерти)
        get_status() -> dict - возвращает словарь со всеми характеристиками питомца
    """

    def __init__(self, pet_id: int, name: str, weight: float):
        """
        Инициализация питомца.

        Аргументы:
            pet_id (int): уникальный идентификатор питомца
            name (str): имя питомца
            weight (float): вес питомца в кг
        """
        self._pet_id = pet_id
        self._name = name
        self._age = 0
        self._weight = weight
        self._hunger = 50
        self._happiness = 70
        self._health = 80
        self._is_alive = True

    def feed(self, food_type: str):
        """
        Покормить питомца.

        Аргументы:
            food_type (str): тип еды (по умолчанию снижает голод на 10)
        """
        if not self._is_alive:
            return
        self._hunger = max(0, self._hunger - 10)

    def play(self, hours: int):
        """
        Поиграть с питомцем.

        Аргументы:
            hours (int): количество часов игры
        """
        if not self._is_alive:
            return
        self._happiness = min(100, self._happiness + (10 * hours))
        self._hunger = min(100, self._hunger + (5 * hours))

    def sleep(self, hours: int):
        """
        Уложить питомца спать.

        Аргументы:
            hours (int): количество часов сна
        """
        if not self._is_alive:
            return
        self._health = min(100, self._health + (5 * hours))

    def tick(self):
        """
        Имитация одного дня жизни питомца.

        Каждый тик:
        - Голод увеличивается на 1-3
        - Счастье уменьшается на 0-2
        - Если голод > 90: здоровье падает на 2-5
        - Если счастье < 10: здоровье падает на 1-3
        - Если здоровье <= 0 или голод >= 100: питомец умирает
        """
        if not self._is_alive:
            return

        self._hunger += random.randint(1, 3)
        self._happiness -= random.randint(0, 2)
        self._happiness = max(0, self._happiness)

        if self._hunger > 90:
            self._health -= random.randint(2, 5)

        if self._happiness < 10:
            self._health -= random.randint(1, 3)

        self._health = max(0, min(100, self._health))

        if self._health <= 0 or self._hunger >= 100:
            self._is_alive = False
            self._health = 0

    def get_status(self) -> dict:
        """
        Возвращает статус питомца.

        Возвращает:
            dict: словарь со всеми характеристиками питомца
        """
        return {
            "id": self._pet_id,
            "name": self._name,
            "hunger": self._hunger,
            "happiness": self._happiness,
            "health": self._health,
            "is_alive": self._is_alive,
        }

    def __str__(self) -> str:
        status = "Жив(а)" if self._is_alive else "Мёртв(а)"
        return f"питомец: {self._name} [{status}]. голод питомца: {self._hunger}, счастье: {self._happiness}, здоровье: {self._health}"


class Cat(Pet):
    """
    Класс кошки.

    Наследует Pet. Особенности:
        - Рыба снижает голод на 20 (вместо 10)
        - Если счастье < 30, здоровье падает на 10 за тик

    Методы:
        feed(food_type) - кормление (рыба даёт бонус)
        tick() - особая логика тика для кошки
    """

    def feed(self, food_type: str):
        """
        Покормить кошку.

        Аргументы:
            food_type (str): тип еды. Рыба снижает голод на 20, остальное на 10.
        """
        if not self._is_alive:
            return

        if food_type.lower() == "рыба":
            self._hunger = max(0, self._hunger - 20)
        else:
            super().feed(food_type)

    def tick(self):
        """
        Имитация дня для кошки.

        После стандартного тика:
        - Если счастье < 30: здоровье падает на 10
        - Если здоровье <= 0: кошка умирает
        """
        if not self._is_alive:
            return

        super().tick()

        if self._is_alive and self._happiness < 30:
            self._health = max(0, self._health - 10)
            if self._health <= 0:
                self._is_alive = False


class Dog(Pet):
    """
    Класс собаки.

    Наследует Pet. Особенности:
        - Мясо снижает голод на 25 (вместо 10)
        - Игра > 2 часов даёт бонус +20 к счастью и сбрасывает счётчик прогулок
        - Каждый тик увеличивает _days_without_walk
        - Если без прогулки >= 3 дня: здоровье падает на 5

    Свойства:
        _days_without_walk (int) - дни без прогулки

    Методы:
        feed(food_type) - кормление (мясо даёт бонус)
        play(hours) - игра (бонус за длительную игру)
        tick() - особая логика тика для собаки
        get_status() - статус с учётом прогулок
    """

    def __init__(self, pet_id: int, name: str, weight: float):
        """
        Инициализация собаки.

        Аргументы:
            pet_id (int): уникальный идентификатор
            name (str): имя собаки
            weight (float): вес в кг
        """
        super().__init__(pet_id, name, weight)
        self._days_without_walk = 0

    def feed(self, food_type: str):
        """
        Покормить собаку.

        Аргументы:
            food_type (str): тип еды. Мясо снижает голод на 25, остальное на 10.
        """
        if not self._is_alive:
            return

        if food_type.lower() == "мясо":
            self._hunger = max(0, self._hunger - 25)
        else:
            super().feed(food_type)

    def play(self, hours: int):
        """
        Поиграть с собакой.

        Аргументы:
            hours (int): количество часов игры. Если > 2: бонус +20 к счастью,
            сброс счётчика прогулок.
        """
        if not self._is_alive:
            return

        super().play(hours)

        if hours > 2:
            self._happiness = min(100, self._happiness + 20)
            self._days_without_walk = 0

    def tick(self):
        """
        Имитация дня для собаки.

        Каждый тик:
        - Увеличивает _days_without_walk на 1
        - Если без прогулки >= 3 дня: здоровье падает на 5
        """
        if not self._is_alive:
            return

        self._days_without_walk += 1

        if self._days_without_walk >= 3:
            self._health = max(0, self._health - 5)

        super().tick()

    def get_status(self) -> dict:
        """
        Возвращает статус собаки.

        Возвращает:
            dict: стандартный статус + days_without_walk
        """
        status = super().get_status()
        status["days_without_walk"] = self._days_without_walk
        return status


class Parrot(Pet):
    """
    Класс попугая.

    Наследует Pet. Особенности:
        - Лакомство снижает голод на 15 и повышает счастье на 15
        - Игра с 20% шансом добавляет новое слово в _learned_words
        - Если счастье < 20: здоровье падает на 3, попугай становится громким
        - Если здоровье <= 0: попугай умирает

    Свойства:
        _learned_words (list[str]) - список выученных слов
        _is_loud (bool) - громкий ли попугай (когда грустит)

    Методы:
        feed(food_type) - кормление (лакомство даёт бонус)
        play(hours) - игра (шанс выучить слово)
        tick() - особая логика тика для попугая
        get_status() - статус с учётом слов и громкости
    """

    def __init__(self, pet_id: int, name: str, weight: float):
        """
        Инициализация попугая.

        Аргументы:
            pet_id (int): уникальный идентификатор
            name (str): имя попугая
            weight (float): вес в кг
        """
        super().__init__(pet_id, name, weight)
        self._learned_words = []
        self._is_loud = False

    def feed(self, food_type: str):
        """
        Покормить попугая.

        Аргументы:
            food_type (str): тип еды. Лакомство снижает голод на 15 и повышает счастье на 15.
        """
        if not self._is_alive:
            return

        if food_type.lower() == "лакомство":
            self._hunger = max(0, self._hunger - 15)
            self._happiness = min(100, self._happiness + 15)
        else:
            super().feed(food_type)

    def play(self, hours: int):
        """
        Поиграть с попугаем.

        Аргументы:
            hours (int): количество часов игры. 20% шанс выучить новое слово.
        """
        if not self._is_alive:
            return

        super().play(hours)

        if random.random() < 0.20:
            words_pool = ["Привет", "Кеша хороший", "Хочу кушать", "Пиастры!"]
            new_word = random.choice(words_pool)
            if new_word not in self._learned_words:
                self._learned_words.append(new_word)

    def tick(self):
        """
        Имитация дня для попугая.

        После стандартного тика:
        - Если счастье < 20: здоровье падает на 3, попугай становится громким
        - Если здоровье <= 0: попугай умирает
        - Иначе: попугай тихий
        """
        if not self._is_alive:
            return

        super().tick()

        if self._is_alive and self._happiness < 20:
            self._health = max(0, self._health - 3)
            self._is_loud = True

            if self._health <= 0:
                self._is_alive = False
                self._health = 0
        else:
            self._is_loud = False

    def get_status(self) -> dict:
        """
        Возвращает статус попугая.

        Возвращает:
            dict: стандартный статус + learned_words + is_loud
        """
        status = super().get_status()
        status["learned_words"] = self._learned_words.copy()
        status["is_loud"] = self._is_loud
        return status
