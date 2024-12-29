from pydantic import BaseModel
from dataclasses import dataclass, field
import random
import time

@dataclass
class ITEM:
    name: str
    chance: int
    min: int = 1
    max: int = 100
    step_count: int = 1
    count_item: int = field(init=False)
    description: str = ""

    def __post_init__(self):
        self.count_item = self.get_count()

    def get_count(self):
        return random.randrange(start=self.min, stop=self.max, step=self.step_count)

    
class Box(BaseModel):
    items: list[ITEM]
    weighted_items: list[ITEM] = []
    min_items: int = 100

    def normalize_chances(self):
        total_chance = sum(item.chance for item in self.items)
        for item in self.items:
            item.chance = (item.chance / total_chance) * 100

    @property
    def all_chance_items(self) -> list[int]:
        return [item.chance for item in self.items]

    def _add_items(self):
        if len(self.weighted_items) < self.min_items:
            while len(self.weighted_items) < self.min_items:
                random_item = random.choices(self.items, weights=self.all_chance_items, k=1)[0]
                new_item = ITEM(
                    name=random_item.name,
                    chance=random_item.chance,
                    min=random_item.min,
                    max=random_item.max,
                    step_count=random_item.step_count,
                    description = random_item.description
                )
                new_item.count_item = new_item.get_count()
                self.weighted_items.append(new_item)
    
    @property
    def items_in_box(self) -> list[ITEM]:
        if not self.weighted_items:
            self.normalize_chances()
            self._add_items()
        return self.weighted_items
    
    @property
    def winner_items(self) -> list[ITEM]:
        return random.choices(self.items_in_box, k=10)       
    
    
class OpenBox:
    length_of_line: int = 25
    target_index: int = 5
    pointer_index: int = 0 

    def __init__(self, items: list[ITEM]):
        self.items = items
        self.pointer_index: int = 0
        self.is_active: bool = True

    def generate_scroll_line(self) -> str:
        return " | ".join(
            f"{item.name[:3].ljust(3)} x{str(item.count_item).rjust(3)}"
            for item in self.items
        )

    @property
    def winner_item(self) -> ITEM:
        return self.items[self.target_index]

    def generate_text_line(self) -> str:
        scroll_line = self.generate_scroll_line()
        return f"{scroll_line} | {scroll_line}"

    def get_next_frame(self):
        if not self.is_active:
            return

        scroll_line = self.generate_text_line()
        visible_window = self.length_of_line - 4

        # Длина массива для привязки позиции в тексте к списку
        total_items = len(self.items)

        while self.is_active:
            start_index = self.pointer_index
            end_index = start_index + visible_window
            visible_text = scroll_line[start_index:end_index]
            visible_line = f"| {visible_text.ljust(visible_window)} |"
            center_position = visible_window // 2

            # Рассчитываем текущую позицию в списке по указателю
            current_index_in_list = (self.pointer_index // (self.length_of_line // total_items)) % total_items

            # Проверяем, совпадает ли текущая позиция с `target_index`
            if current_index_in_list == self.target_index:
                # Победный текст в текущем положении
                winner_text = f"{self.winner_item.name[:3].ljust(3)} x{str(self.winner_item.count_item).rjust(3)}"

                winner_start = visible_text.find(winner_text)
                if winner_start != -1:
                    winner_center_position = winner_start + len(winner_text) // 2
                    if abs(winner_center_position - center_position) <= 1:
                        self.is_active = False

            pointer_line = " " * center_position + "🔼"

            yield f"{visible_line}\n{pointer_line}"
            if self.is_active:
                self.pointer_index = (self.pointer_index + 1) % len(scroll_line)
if __name__ == "__main__":
    try:
        box_money = Box(items=[ITEM(name="💸", chance=50, min=1, max=3)])
        
        open_box_money = OpenBox(box_money.winner_items)

        frame_generator_money = open_box_money.get_next_frame()
        num = 0
        while True:
            try:
                frame = next(frame_generator_money)
                if frame and num % 3 == 0:
                    print(f"\r{frame}", end="")
                time.sleep(0.2)
                num += 1
            except StopIteration:
                break  # Генератор завершился, выходим из цикла
        print(open_box_money.winner_item.count_item)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
