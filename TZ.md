# Техническое задание (примерное)
## Игра "Виртуальный питомец"

> **Примечание:** ТЗ восстановлено по исходному коду, так как организаторы хакатона не захотели предоставлять оригинальное ТЗ. Здесь представлено приблизительное описание того, что было в задании.

### Описание
Разработать текстовую консольную игру на Python с использованием ООП (наследование, инкапсуляция, полиморфизм).

**Требования:**
- Минимум два уровня наследования

---

### Магазин

Товары:
| Название | Цена | Описание |
|---|---|---|
| рыба | 10 | корм для кошек |
| мясо | 15 | корм для собак |
| игрушка | 20 | развлечение |
| лекарство | 30 | восстанавливает здоровье |
| лакомство | 5 | вкусняшка |

---

### Классы и методы

**Pet** (базовый класс):
- `__init__`(pet_id, name, weight) -> None
- feed(food_type) -> str
- play(hours) -> str
- sleep(hours) -> str
- tick() -> None
- get_status() -> dict

**Cat(Pet)**:
- feed(food_type) -> str
- tick() -> None

**Dog(Pet)**:
- `__init__`(pet_id, name, weight) -> None
- feed(food_type) -> str
- play(hours) -> str
- tick() -> None
- get_status() -> dict

**Parrot(Pet)**:
- `__init__`(pet_id, name, weight) -> None
- feed(food_type) -> str
- play(hours) -> str
- tick() -> None
- get_status() -> dict

**Owner**:
- `__init__`(owner_id, name, email) -> None
- _log_activity(message) -> None
- adopt_pet(pet) -> None
- get_pet(name) -> Pet
- feed_pet(pet_name, food) -> str
- play_with_pet(pet_name, hours) -> str
- put_pet_to_sleep(pet_name, hours) -> str
- buy_item(shop, item_name) -> str
- tick() -> None
- get_status() -> dict

**Shop**:
- `__init__`() -> None
- get_price(item_name) -> int
- show_items() -> None

**Game**:
- `__init__`(owner, shop) -> None
- start_day() -> None
- show_status() -> None
- get_report() -> str
- save_game(filename) -> None
- load_game(filename) -> None

**Report**:
- `__init__`(pets) -> None
- generate() -> str

---

### Критерии оценки (Приложение №1)

Максимум 50 баллов:

| Критерий | Баллы |
|---|---|
| Соответствие заданию | 0–10 |
| Сложность решения | 0–10 |
| Гибкость решения | 0–10 |
| Оригинальность решения | 0–10 |
| Верстка кода | 0–10 |
| **Итого** | **50** |
