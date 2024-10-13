from pvp_duels.types import DuelUser


class DuelManager:
    active_duels: dict[str,'DuelUser'] = {}

    @classmethod
    def add_pool_duel(cls, duel_id:str, duel_obj: 'DuelUser'):
        cls.active_duels[duel_id] = duel_obj
        
    @classmethod
    def delete_pool_duel(cls, duel_id: str):
        cls.active_duels.__delitem__(duel_id)
        
    @classmethod
    def get_duel_by_id(cls, duel_id: str) -> DuelUser:
        return cls.active_duels.get(duel_id, False)
