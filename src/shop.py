class Shop:
    """
    название | цена | описание
    рыба | 10 | корм для кошек
    мясо | 15 | корм для собак
    игрушка | 20 | развлечение
    лекарство | 30 | восстанавливает здоровье
    лакомство | 5 | вкусняшка
    """

    def __init__(self):
        self.items = [
            {"name": "рыба", "price": 10, "description": "корм для кошек"},
            {"name": "мясо", "price": 15, "description": "корм для собак"},
            {"name": "игрушка", "price": 20, "description": "развлечение"},
            {"name": "лекарство", "price": 30, "description": "восстанавливает здоровье"},
            {"name": "лакомство", "price": 5, "description": "вкусняшка"},
        ]

    def get_price(self, item_name: str) -> int:
        for item in self.items:
            if item["name"].lower() == item_name.lower():
                return item["price"]
        return None

    def show_items(self):
        print(f"{'название':<10} | {'цена':<5} | описание")
        print("-" * 45)
        for item in self.items:
            print(f"{item['name']:<10} | {item['price']:<5} | {item['description']}")
