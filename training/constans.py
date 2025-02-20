from datetime import timedelta
from .types import Stage

TIME_TRAINING = timedelta(minutes=30)
TIME_REGISTER_TRAINING = timedelta(minutes=30)

MAX_LIMIT_JOIN_CHARACTERS = 50

DIRECTIONS = ["↖️", "⬆️", "↗️", "⬅️", "➡️", "↙️", "⬇️", "↘️"]

QTE_STAGES = [Stage.STAGE_4, Stage.STAGE_6]

COUNT_QTE_STAGES = 5
MAX_SCORE_QTE = 35
BASE_SCORE_QTE = MAX_SCORE_QTE / COUNT_QTE_STAGES

PENALTY_STEP = 0.3  # Шаг штрафа в секундах
PENALTY_VALUE = 2  # Штраф за каждую задержку
MIN_SCORE = 2  # Минимальный балл


STAT_RANGES = {
    range(70, 101): 3,
    range(40, 70): 2,
    range(20, 40): 1,
    range(0, 20): 0
}