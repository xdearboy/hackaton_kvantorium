import random


class Pet:
    def __init__(self, pet_id: int, name: str, weight: float):
        self._pet_id = pet_id
        self._name = name
        self._age = 0
        self._weight = weight
        self._hunger = 50
        self._happiness = 70
        self._health = 80
        self._is_alive = True

    def feed(self, food_type: str):
        if not self._is_alive:
            return
        self._hunger = max(0, self._hunger - 10)

    def play(self, hours: int):
        if not self._is_alive:
            return
        self._happiness = min(100, self._happiness + (10 * hours))
        self._hunger = min(100, self._hunger + (5 * hours))

    def sleep(self, hours: int):
        if not self._is_alive:
            return
        self._health = min(100, self._health + (5 * hours))

    def tick(self):
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
    def feed(self, food_type: str):
        if not self._is_alive:
            return

        if food_type.lower() == "рыба":
            self._hunger = max(0, self._hunger - 20)
        else:
            super().feed(food_type)

    def tick(self):
        if not self._is_alive:
            return

        super().tick()

        if self._is_alive and self._happiness < 30:
            self._health = max(0, self._health - 10)
            if self._health <= 0:
                self._is_alive = False


class Dog(Pet):
    def __init__(self, pet_id: int, name: str, weight: float):
        super().__init__(pet_id, name, weight)
        self._days_without_walk = 0

    def feed(self, food_type: str):
        if not self._is_alive:
            return

        if food_type.lower() == "мясо":
            self._hunger = max(0, self._hunger - 25)
        else:
            super().feed(food_type)

    def play(self, hours: int):
        if not self._is_alive:
            return

        super().play(hours)

        if hours > 2:
            self._happiness = min(100, self._happiness + 20)
            self._days_without_walk = 0

    def tick(self):
        if not self._is_alive:
            return

        self._days_without_walk += 1

        if self._days_without_walk >= 3:
            self._health = max(0, self._health - 5)

        super().tick()

    def get_status(self) -> dict:
        status = super().get_status()
        status["days_without_walk"] = self._days_without_walk
        return status


class Parrot(Pet):
    def __init__(self, pet_id: int, name: str, weight: float):
        super().__init__(pet_id, name, weight)
        self._learned_words = []
        self._is_loud = False

    def feed(self, food_type: str):
        if not self._is_alive:
            return

        if food_type.lower() == "лакомство":
            self._hunger = max(0, self._hunger - 15)
            self._happiness = min(100, self._happiness + 15)
        else:
            super().feed(food_type)

    def play(self, hours: int):
        if not self._is_alive:
            return

        super().play(hours)

        if random.random() < 0.20:
            words_pool = ["Привет", "Кеша хороший", "Хочу кушать", "Пиастры!"]
            new_word = random.choice(words_pool)
            if new_word not in self._learned_words:
                self._learned_words.append(new_word)

    def tick(self):
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
        status = super().get_status()
        status["learned_words"] = self._learned_words.copy()
        status["is_loud"] = self._is_loud
        return status
