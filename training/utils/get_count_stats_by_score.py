from training.constans import STAT_RANGES


def calculate_stat(score: int) -> int:
    for score_range, bonus in STAT_RANGES.items():
        if score in score_range:
            return bonus
    return 0