import json
import os

from src.manage_owner import Owner
from src.shop import Shop


class Report:
    def __init__(self, pets):
        self.pets = pets

    def generate(self) -> str:
        if not self.pets:
            return "у владельца пока нет питомцев."

        lines = ["=== репорт об состоянии питомцев ==="]
        for pet in self.pets:
            status = pet.get_status()
            name = status["name"]
            alive = status["is_alive"]

            if not alive:
                lines.append(f"- {name}: МЁРТВ")
                continue

            health = status["health"]
            hunger = status["hunger"]
            happiness = status["happiness"]

            if health < 30:
                state = "критическое (требует сна/лечения)"
            elif hunger > 70:
                state = "голодает (требует еды)"
            elif happiness < 30:
                state = "грустит (требуют игр)"
            else:
                state = "стабильное"

            lines.append(
                f"- {name}: состояние: {state} | здоровье: {health} | голод: {hunger} | счастье: {happiness}"
            )
        return "\n".join(lines)


class Game:
    def __init__(self, day_counter: int, is_running: bool):
        self._owner = Owner(owner_id=1, name="Игрок", email="player@game.com")
        self._shop = Shop()
        self._day_counter = day_counter
        self._is_running = is_running

    def start_day(self):
        if not self._is_running:
            return
        self._day_counter += 1
        self._owner.tick()

    def show_status(self) -> str:
        status = self._owner.get_status()
        output = [
            f"=== день {self._day_counter} ===",
            f"игрок: {status['name']} | баланс: {status['money']} руб.",
            f"инвентарь: {status['inventory']}",
            "питомцы:",
        ]
        for pet in status["pets"]:
            alive_str = "Жив" if pet["is_alive"] else "Мёртв"
            output.append(
                f"  - {pet['name']} [{alive_str}] -> Здоровье: {pet['health']}, Голод: {pet['hunger']}, Счастье: {pet['happiness']}"
            )
        return "\n".join(output)

    def save_game(self, filename: str):
        data = {
            "day_counter": self._day_counter,
            "is_running": self._is_running,
            "owner": self._owner.get_status(),
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_game(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден.")

        with open(filename, encoding="utf-8") as f:
            data = json.load(f)

        self._day_counter = data["day_counter"]
        self._is_running = data["is_running"]

        owner_data = data["owner"]
        self._owner = Owner(
            owner_id=owner_data["owner_id"],
            name=owner_data["name"],
            email=owner_data["email"],
        )
        self._owner._money = owner_data["money"]
        self._owner._inventory = owner_data["inventory"]

        from src.manage_pets import Cat, Dog, Parrot

        for pet_data in owner_data["pets"]:
            pet_type = pet_data.get("type", "Cat")
            if pet_type == "Dog":
                pet = Dog(pet_id=pet_data["id"], name=pet_data["name"], weight=5.0)
                pet._days_without_walk = pet_data.get("days_without_walk", 0)
            elif pet_type == "Parrot":
                pet = Parrot(pet_id=pet_data["id"], name=pet_data["name"], weight=0.3)
            else:
                pet = Cat(pet_id=pet_data["id"], name=pet_data["name"], weight=4.0)

            pet._hunger = pet_data["hunger"]
            pet._happiness = pet_data["happiness"]
            pet._health = pet_data["health"]
            pet._is_alive = pet_data["is_alive"]
            self._owner.adopt_pet(pet)

    def get_report(self) -> str:
        report_generator = Report(self._owner._pets)
        return report_generator.generate()
