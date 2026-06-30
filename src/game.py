from src.manage_owner import Owner


class VirtualPetError(Exception):
    pass


class PetNotFoundError(VirtualPetError):
    pass


class NotEnoughMoneyError(VirtualPetError):
    pass


class PetDiedError(VirtualPetError):
    pass


class InvalidActionError(VirtualPetError):
    pass


class Shop:
    def __init__(self):
        self.items = [
            {"name": "рыба", "price": 10, "description": "корм для кошек"},
            {"name": "мясо", "price": 15, "description": "корм для собак"},
            {"name": "игрушка", "price": 20, "description": "развлечение"},
            {
                "name": "лекарство",
                "price": 30,
                "description": "восстанавливает здоровье",
            },
            {"name": "лакомство", "price": 5, "description": "вкусняшка"},
        ]

    def show_items(self):
        print(f"{'название':<10} | {'цена':<5} | описание")
        print("-" * 45)
        for item in self.items:
            print(f"{item['name']:<10} | {item['price']:<5} | {item['description']}")

    def buy(self, item_name: str, owner: Owner):
        target_item = None
        for item in self.items:
            if item["name"].lower() == item_name.lower():
                target_item = item
                break

        if not target_item:
            raise InvalidActionError(f"товар '{item_name}' отсутствует в магазине.")

        if owner._money < target_item["price"]:
            raise NotEnoughMoneyError(
                f"недостаточно денег для покупки '{item_name}'. нужно: {target_item['price']}, доступно: {owner._money}."
            )

        owner._money -= target_item["price"]
        item_key = target_item["name"].lower()
        owner._inventory[item_key] = owner._inventory.get(item_key, 0) + 1
        owner._log_activity(f"купил '{target_item['name']}' за {target_item['price']} руб.")
