from typing import List, Dict, Optional
from datetime import datetime

from src.manage_pets import Pet

    """_summary_

    Returns:
        _type_: _description_
    """
class Owner:
    def __init__(self, owner_id: int, name: str, email: str):
        self._owner_id = owner_id
        self._name = name 
        self._email = email
        self._money: int = 100
        self._pets: List[Pet] = []
        self._inventory: Dict[str, int] = {}
        self._activity_log: List[str] = []
        self._log_activity("владелец создан")
        
    def _log_activity(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._activity_log.append(f"[{timestamp}] {message}")

    def adopt_pet(self, pet: Pet):
        if pet not in self._pets:
            self._pets.append(pet)
            self._log_activity(f"приютил питомца: {pet._name}")
    
    def get_pet(self, name: str) -> Optional[Pet]:
        for pet in self._pets:
            if pet._name.lower() == name.lower():
                return pet
        return None
    
    def feed_pet(self, pet_name: str, food: str):
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
        pet = self.get_pet(pet_name)
        if pet:
            if pet._is_alive:
                pet.play(hours)
                self._log_activity(f"поиграл с {pet_name} в течение {hours} ч.")
            else:
                self._log_activity(f"ошибка игры, {pet_name} уже мертв.")
        
    def put_pet_to_sleep(self, pet_name: str, hours: int):
        pet = self.get_pet(pet_name)
        if pet:
            if pet._is_alive:
                pet.sleep(hours)
                self._log_activity(f"отправил {pet_name} спать на {hours} ч.")
            else:
                self._log_activity(f"ошибка сна: {pet_name} уже мертв.")
        else:
            self._log_activity(f"ошибка сна: питомец {pet_name} не найден.")
    
    def buy_item(self, item_name: str, price: int):
        if self._money >= price:
            self._money -= price
            item_key = item_name.lower()
            self._inventory[item_key] = self._inventory.get(item_key, 0) + 1
            self._log_activity(f"купил '{item_name}' за {price} руб. осталось: {self._money} руб.")
        else:
            self._log_activity(f"не удалось купить '{item_name}': недостаточно денег (баланс: {self._money} руб.).")
    
    def tick(self):
        for pet in self._pets:
            if pet._is_alive:
                pet.tick()
                if not pet._is_alive:
                    self._log_activity(f"к сожалению, питомец {pet._name} умер.")
 
    def get_status(self) -> dict:
        return {
            "owner_id": self._owner_id,
            "name": self._name,
            "email": self._email,
            "money": self._money,
            "inventory": self._inventory,
            "pets": [pet.get_status() for pet in self._pets],
            "activity_log_length": len(self._activity_log)
        }
