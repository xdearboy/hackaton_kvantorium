import json
from src.manage_owner import Owner
from src.shop import Shop
from src.manage_pets import Cat, Dog, Parrot
from src.report import Report


class Game:
  """
  Основной класс игры "Виртуальный питомец".

  Свойства:
      _owner (Owner) - владелец питомцев
      _shop (Shop) - магазин товаров
      _day_counter (int) - счётчик дней (начинается с 1)
      _is_running (bool) - статус работы игры

  Методы:
      start_day() -> None - начать новый день (вызывает tick для владельца)
      show_status() -> None - вывести статус игры в консоль
      get_report() -> str - получить отчёт о состоянии питомцев
      save_game(filename) -> None - сохранить игру в JSON-файл
      load_game(filename) -> None - загрузить игру из JSON-файла
  """

  def __init__(self, owner: Owner, shop: Shop):
    """
    Инициализация игры.

    Аргументы:
        owner (Owner): владелец питомцев
        shop (Shop): магазин товаров
    """
    self._owner = owner
    self._shop = shop
    self._day_counter: int = 1
    self._is_running: bool = True

  def start_day(self) -> None:
    """
    Начать новый день. Вызывает tick() для владельца и увеличивает счётчик дней.
    """
    if not self._is_running:
      return
    self._owner.tick()
    self._day_counter += 1

  def show_status(self) -> None:
    """
    Выводит текущий статус игры (день, имя игрока, баланс).
    """
    status = self._owner.get_status()
    print(f'день: {self._day_counter}')
    print(f'игрок: {status["name"]} | баланс: {status["money"]} руб')

  def get_report(self) -> str:
    """
    Генерирует отчёт о состоянии всех питомцев.

    Возвращает:
        str: текстовый отчёт
    """
    report_generator = Report(self._owner._pets)
    return report_generator.generate()

  def save_game(self, filename: str) -> None:
    """
    Сохраняет текущее состояние игры в JSON-файл.

    Аргументы:
        filename (str): имя файла для сохранения
    """
    owner_status = self._owner.get_status()

    pets_data = []
    for pet in self._owner._pets:
      pet_status = pet.get_status()
      pet_status['type'] = pet.__class__.__name__
      pet_status['weight'] = getattr(pet, '_weight', 1.0)
      pets_data.append(pet_status)

    data = {
      'day_counter': self._day_counter,
      'is_running': self._is_running,
      'owner': {
        'owner_id': owner_status['owner_id'],
        'name': owner_status['name'],
        'email': owner_status['email'],
        'money': owner_status['money'],
        'inventory': owner_status['inventory'],
        'activity_log': self._owner._activity_log,
      },
      'pets': pets_data,
    }
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  def load_game(self, filename: str) -> None:
    """
    Загружает состояние игры из JSON-файла.

    Аргументы:
        filename (str): имя файла для загрузки
    """
    with open(filename, 'r', encoding='utf-8') as f:
      data = json.load(f)

    self._day_counter = data['day_counter']
    self._is_running = data['is_running']

    owner_data = data['owner']
    self._owner = Owner(owner_data['owner_id'], owner_data['name'], owner_data['email'])
    self._owner._money = owner_data['money']
    self._owner._inventory = owner_data['inventory']
    self._owner._activity_log = owner_data['activity_log']

    classes = {'Cat': Cat, 'Dog': Dog, 'Parrot': Parrot}
    for p in data['pets']:
      pet_class = classes.get(p['type'])
      if pet_class:
        pet = pet_class(p['id'], p['name'], p['weight'])
        pet._hunger = p['hunger']
        pet._happiness = p['happiness']
        pet._health = p['health']
        pet._is_alive = p['is_alive']
        if p['type'] == 'Dog':
          pet._days_without_walk = p.get('days_without_walk', 0)
        elif p['type'] == 'Parrot':
          pet._learned_words = p.get('learned_words', [])
          pet._is_loud = p.get('is_loud', False)
        self._owner.adopt_pet(pet)
