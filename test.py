def round_robin_schedule(clubs):
    """Создает расписание матчей методом кругового турнира."""
    num_clubs = len(clubs)
    if num_clubs % 2 != 0:
        clubs.append(None)  # Добавляем "пустой" клуб, если количество нечетное

    num_days = num_clubs - 1
    half_size = num_clubs // 2

    schedule = []

    for day in range(num_days):
        daily_matches = []
        for i in range(half_size):
            club1 = clubs[i]
            club2 = clubs[num_clubs - i - 1]
            if club1 is not None and club2 is not None:
                daily_matches.append((club1, club2))
        schedule.append(daily_matches)

        # Поворот списка клубов
        clubs = [clubs[0]] + [clubs[-1]] + clubs[1:-1]

    return schedule

def print_schedule(schedule):
    """Печатает расписание матчей."""
    for day, matches in enumerate(schedule, start=1):
        print(f"День {day}:")
        for match in matches:
            print(f"  {match[0]} vs {match[1]}")
        print()

# Список клубов
clubs = [f"Клуб {i+1}" for i in range(20)]

# Генерация расписания матчей
schedule = round_robin_schedule(clubs)

# Печать расписания матчей
print_schedule(schedule)