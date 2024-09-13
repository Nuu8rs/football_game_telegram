import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer, Boolean, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from config import PositionCharacter, Gender, CONST_ENERGY, EPOCH_ZERO
from database.model_base import Base


class Character(Base):
    __tablename__ = 'characters'
    LEVEL_THRESHOLDS = [100, 300, 500, 900, 1500, 2500, 3900, 5500, 12000]
    
    id = Column(BigInteger, primary_key=True, index=True)
    
    characters_user_id = Column(BigInteger, ForeignKey('users.user_id'))  
    club_id = Column(BigInteger, ForeignKey('clubs.id'))
    
    exp   = Column(Integer, default=0, server_default="0", insert_default=0, nullable=False)
    money = Column(Integer, default=0, server_default="0", insert_default=0, nullable=False)
    
    name           = Column(String(255), index=True)
    technique      = Column(Integer, default=0)
    kicks          = Column(Integer, default=0)
    ball_selection = Column(Integer, default=0)
    speed          = Column(Integer, default=0)
    endurance      = Column(Integer, default=0)
    current_energy = Column(Integer, default=0)
    position       = Column(String(255))
    gender         = Column(String(255))
    
    character_in_training = Column(Boolean, default=False)
    education_reward_date = Column(DateTime, default=EPOCH_ZERO, server_default=text('\'1970-01-01 00:00:00\''))
    time_to_join_club     = Column(DateTime, default=EPOCH_ZERO, server_default=text('\'1970-01-01 00:00:00\''))
    
    created_at     = Column(DateTime, default=datetime.datetime.utcnow)
    is_bot         = Column(Boolean, default=False)
    
    owner = relationship("UserBot", back_populates="characters", lazy="selectin")
    club = relationship("Club", back_populates="characters", lazy="selectin")

    t_shirt_id = Column(BigInteger, ForeignKey('items.id'))
    shorts_id = Column(BigInteger, ForeignKey('items.id'))
    gaiters_id = Column(BigInteger, ForeignKey('items.id'))
    boots_id = Column(BigInteger, ForeignKey('items.id'))

    t_shirt = relationship("Item", foreign_keys=[t_shirt_id], lazy="selectin")
    shorts = relationship("Item", foreign_keys=[shorts_id], lazy="selectin")
    gaiters = relationship("Item", foreign_keys=[gaiters_id], lazy="selectin")
    boots = relationship("Item", foreign_keys=[boots_id], lazy="selectin")


    @property
    def koef_club_power(self) -> float:
        if not self.club:
            return 1.0
        return self.club.koef_energy

    @property
    def gender_enum(self):
        return Gender(self.gender) if self.gender else None

    @gender_enum.setter
    def gender_enum(self, value):
        if isinstance(value, Gender):
            self.gender = value.value

    @property
    def position_enum(self):
        return PositionCharacter(self.position) if self.position else None

    @position_enum.setter
    def position_enum(self, value):
        if isinstance(value, PositionCharacter):
            self.position = value.value

    @hybrid_property
    def level(self):
        for level, threshold in enumerate(self.LEVEL_THRESHOLDS, start=1):
            if self.exp < threshold:
                return level
        return len(self.LEVEL_THRESHOLDS)+1

    @hybrid_property
    def max_energy(self) -> int:
        return CONST_ENERGY
    
    @property
    def position_description(self):
        position_declensions = {
            PositionCharacter.MIDFIELDER: {
                Gender.MAN: "Півзахисник",
                Gender.WOMAN: "Півзахисниця"
            },
            PositionCharacter.DEFENDER: {
                Gender.MAN: "Захисник",
                Gender.WOMAN: "Захисниця"
            },
            PositionCharacter.GOALKEEPER: {
                Gender.MAN: "Воротар",
                Gender.WOMAN: "Воротарка"
            },
            PositionCharacter.ATTACKER: {
                Gender.MAN: "Нападник",
                Gender.WOMAN: "Нападниця"
            }
        }
        
        position_enum = self.position_enum
        gender_enum = self.gender_enum
        if position_enum and gender_enum:
            return position_declensions[position_enum][gender_enum]
        return None
    
    @property
    def item_stats(self):
        stats = {
            'technique': 0,
            'kicks': 0,
            'ball_selection': 0,
            'speed': 0,
            'endurance': 0,
        }
        
        items = [self.t_shirt, self.shorts, self.gaiters, self.boots]
        for item in items:
            if item:
                stats['technique'] += item.technique_item_stat
                stats['kicks'] += item.kicks_item_stat
                stats['ball_selection'] += item.ball_selection_item_stat
                stats['speed'] += item.speed_item_stat
                stats['endurance'] += item.endurance_item_stat


        return stats
    
    @property
    def effective_technique(self):
        return self.technique + self.item_stats['technique']

    @property
    def effective_kicks(self):
        return self.kicks + self.item_stats['kicks']

    @property
    def effective_ball_selection(self):
        return self.ball_selection + self.item_stats['ball_selection']

    @property
    def effective_speed(self):
        return self.speed + self.item_stats['speed']

    @property
    def effective_endurance(self):
        return self.endurance + self.item_stats['endurance']

    @property
    def full_power(self) -> int:
        total_stats = (
            self.effective_technique +
            self.effective_kicks +
            self.effective_ball_selection +
            self.effective_speed +
            self.effective_endurance
        )
        return total_stats * self.koef_club_power