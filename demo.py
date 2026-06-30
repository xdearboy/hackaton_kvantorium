from src.manage_owner import Owner
from src.shop import Shop
from src.manage_pets import Cat, Dog, Parrot
from src.report import Report


print("--- запуск демо игры...---")
owner = Owner(1, "Арсений", "lovelisa228@mail.ru")
shop = Shop()

cat = Cat(101, "Василиса", 3.5)
dog = Dog(102, "Шарик", 12.0)
parrot = Parrot(103, "Кеша", 0.2)

owner.adopt_pet(cat)
owner.adopt_pet(dog)
owner.adopt_pet(parrot)

print("\n--- товары в наличие ---")
shop.show_items()

print("\n--- покупки в магазине ---")
owner.buy_item(shop, "рыба")
owner.buy_item(shop, "мясо")
owner.buy_item(shop, "лакомство")

print("\n--- уход за питомцами ---")
print(cat)
owner.feed_pet("Василиса", "рыба")
print(cat)

print()
print(dog)
owner.play_with_pet("Шарик", 3)
owner.feed_pet("Шарик", "мясо")
print(dog)

print("\n--- пропускаем время (3 тика) ---")
owner.tick()
owner.tick()
owner.tick()

print("\n--- отчет о состоянии питомцев ---")
report = Report(owner._pets)
print(report.generate())
