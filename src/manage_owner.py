from datetime import datetime

from src.manage_pets import Pet
from src.shop import Shop


class Owner:
    """
    Клад владельца питомцев.

    Свойства:
        _owner_id (int) - уникальный идентификатор владельца
        _name (str) - имя владельца
        _email (str) - электронная почта
        _money (int) - денежные средства (начальный баланс: 100 руб)
        _pets (list[Pet]) - список питомцев
        _inventory (dict[str, int]) - инвентарь (словарь: название_товара -> количество)
        _activity_log (list[str]) - лог действий

    Методы:
        _log_activity(message) - запись действия в лог
        adopt_pet(pet) - взять питомца
        get_pet(name) - найти питомца по имени
        feed_pet(pet_name, food) - покормить питомца (тратит еду из инвентаря)
        play_with_pet(pet_name, hours) - поиграть с питомцем
        put_pet_to_sleep(pet_name, hours) - уложить питомца спать
        buy_item(shop, item_name) - купить товар в магазине
        tick() - имитация дня для всех питомцев
        get_status() - полный статус владельца
    """

    def __init__(self, owner_id: int, name: str, email: str):
        """
        Инициализация владельца.

        Аргументы:
            owner_id (int): уникальный идентификатор владельца
            name (str): имя владельца
            email (str): электронная почта
        """
        self._owner_id = owner_id
        self._name = name
        self._email = email
        self._money: int = 100
        self._pets: list[Pet] = []
        self._inventory: dict[str, int] = {}
        self._activity_log: list[str] = []
        self._log_activity("владелец создан")

    def _log_activity(self, message: str):
        """
        Записывает действие в лог активности.

        Аргументы:
            message (str): описание действия
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._activity_log.append(f"[{timestamp}] {message}")

    def adopt_pet(self, pet: Pet):
        """
        Взять питомца.

        Аргументы:
            pet (Pet): питомец для добавления в список
        """
        if pet not in self._pets:
            self._pets.append(pet)
            self._log_activity(f"приютил питомца: {pet._name}")

    def get_pet(self, name: str) -> Pet | None:
        """
        Найти питомца по имени (без учёта регистра).

        Аргументы:
            name (str): имя питомца

        Возвращает:
            Pet | None: найденный питомец или None
        """
        for pet in self._pets:
            if pet._name.lower() == name.lower():
                return pet
        return None

    def feed_pet(self, pet_name: str, food: str):
        """
        Покормить питомца (тратит еду из инвентаря).

        Аргументы:
            pet_name (str): имя питомца
            food (str): тип еды (должен быть в инвентаре)
        """
        pet = self.get_pet(pet_name)
        if not pet:
            self._log_activity(f"ошибка кормления: питомец {pet_name} не найден")
            return

        if not pet._is_alive:
            self._log_activity(f"ошибка кормления: {pet_name} уже мертв")
            return

        food_key = food.lower()
        if self._inventory.get(food_key, 0) > 0:
            self._inventory[food_key] -= 1
            pet.feed(food)
            self._log_activity(f"покормил птицу: {pet_name} едой '{food}'.")
            if self._inventory[food_key] == 0:
                del self._inventory[food_key]
        else:
            self._log_activity(f"ошибка кормления: с собой нет '{food}'.")

    def play_with_pet(self, pet_name: str, hours: int):
        """
        Поиграть с питомцем.

        Аргументы:
            pet_name (str): имя питомца
            hours (int): количество часов игры
        """
        pet = self.get_pet(pet_name)
        if pet:
            if pet._is_alive:
                pet.play(hours)
                self._log_activity(f"поиграл с {pet_name} в течение {hours} ч.")
            else:
                self._log_activity(f"ошибка игры, {pet_name} уже мертв.")

    def put_pet_to_sleep(self, pet_name: str, hours: int):
        """
        Уложить питомца спать.

        Аргументы:
            pet_name (str): имя питомца
            hours (int): количество часов сна
        """
        pet = self.get_pet(pet_name)
        if pet:
            if pet._is_alive:
                pet.sleep(hours)
                self._log_activity(f"отправил {pet_name} спать на {hours} ч.")
            else:
                self._log_activity(f"ошибка сна: {pet_name} уже мертв.")
        else:
            self._log_activity(f"ошибка сна: питомец {pet_name} не найден.")

    def buy_item(self, shop: "Shop", item_name: str):
        """
        Купить товар в магазине.

        Аргументы:
            shop (Shop): магазин
            item_name (str): название товара
        """
        price = shop.get_price(item_name)

        if price is None:
            self._log_activity(f"товар '{item_name}' не найден в магазине.")
            return

        if self._money >= price:
            self._money -= price
            item_key = item_name.lower()
            self._inventory[item_key] = self._inventory.get(item_key, 0) + 1
            self._log_activity(f"купил '{item_name}' за {price} руб. осталось: {self._money} руб.")
        else:
            self._log_activity(
                f"не удалось купить '{item_name}': недостаточно денег (баланс: {self._money} руб.)."
            )

    def tick(self):
        """
        Имитация одного дня для всех питомцев.

        Если питомец умирает во время тика, записывает об этом в лог.
        """
        for pet in self._pets:
            if pet._is_alive:
                pet.tick()
                if not pet._is_alive:
                    self._log_activity(f"к сожалению, питомец {pet._name} умер.")

    def get_status(self) -> dict:
        """
        Возвращает полный статус владельца.

        Возвращает:
            dict: owner_id, name, email, money, inventory, pets, activity_log_length
        """
        return {
            "owner_id": self._owner_id,
            "name": self._name,
            "email": self._email,
            "money": self._money,
            "inventory": self._inventory,
            "pets": [pet.get_status() for pet in self._pets],
            "activity_log_length": len(self._activity_log),
        }
