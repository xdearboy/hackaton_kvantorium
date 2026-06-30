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
