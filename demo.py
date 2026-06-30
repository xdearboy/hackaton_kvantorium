from src.manage_owner import Owner
from src.shop import Shop
from src.manage_pets import Cat, Dog, Parrot
from src.report import Report
from src.game import Game


print('--- запуск демо игры...---')
owner = Owner(1, 'Арсений', 'lovelisa228@mail.ru')
shop = Shop()

cat = Cat(101, 'Василиса', 3.5)
dog = Dog(102, 'Шарик', 12.0)
parrot = Parrot(103, 'Кеша', 0.2)

owner.adopt_pet(cat)
owner.adopt_pet(dog)
owner.adopt_pet(parrot)

game = Game(owner, shop)

print('\n--- товары в наличие ---')
game._shop.show_items()

print('\n--- покупки в магазине ---')
game._owner.buy_item(game._shop, 'рыба')
game._owner.buy_item(game._shop, 'мясо')
game._owner.buy_item(game._shop, 'лакомство')

print('\n--- уход за питомцами ---')
print(cat)
print('вы покормили кошку рыбой!')
game._owner.feed_pet('Василиса', 'рыба')
print(cat)

print()
print(dog)
game._owner.play_with_pet('Шарик', 3)
print('вы поиграли с собакой')
game._owner.feed_pet('Шарик', 'мясо')
print('вы покормили собаку')
print(dog)

print('\n--- пропускаем время (3 тика) ---')
game.start_day()
game.start_day()
game.start_day()

print(game.get_report())

print('\n--- проверка сохранения игры ---')
game.save_game('savefile.json')
print('игра сохранена в savefile.json')

print('\n--- проверка загрузки игры ---')
new_game = Game(None, shop)
new_game.load_game('savefile.json')
print('игра загружена из файла')
new_game.show_status()
print(new_game.get_report())
