import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer, Boolean, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from config import PositionCharacter, Gender, LEAGUES, CONST_ENERGY, EPOCH_ZERO
import math


Base = declarative_base()

class UserBot(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)  
    user_name = Column(String(255), index=True)  
    user_full_name = Column(String(255)) 
    user_time_register = Column(DateTime, default=datetime.datetime.utcnow)
    
    characters = relationship("Character", back_populates="owner", lazy="selectin")
    clubs = relationship("Club", back_populates="owner", lazy="selectin")

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(BigInteger, primary_key=True, index=True)
    characters_user_id = Column(BigInteger, ForeignKey('users.user_id'))  
    club_id = Column(BigInteger, ForeignKey('clubs.id'))
    
    exp   = Column(Integer, default=0, server_default="0")
    money = Column(Integer, default=0, server_default="0")
    
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

    # time_character_training = Column(DateTime, nullable=True)
    # training_characteristic = Column(String(255), nullable=True)
    
    
    created_at     = Column(DateTime, default=datetime.datetime.utcnow)
    is_bot         = Column(Boolean, default=False)
    owner = relationship("UserBot", back_populates="characters", lazy="selectin")
    club = relationship("Club", back_populates="characters", lazy="selectin")

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
        if self.exp < 10:
            return 1
        a = 5
        b = 5
        c = -2 * self.exp
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return 1 
        level = (-b + math.sqrt(discriminant)) // (2 * a)
        return int(level)

    @hybrid_property
    def max_energy(self) -> int:
        return CONST_ENERGY

    @hybrid_property
    def full_power(self) -> int:
        return (self.technique + self.kicks + self.ball_selection + self.speed + self.endurance) * self.koef_club_power
    
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

class Club(Base):
    __tablename__ = 'clubs'
    
    id             = Column(BigInteger, primary_key=True, index=True)
    name_club      = Column(String(100), nullable=False)
    owner_id       = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    link_to_chat   = Column(String(255), nullable=True)
    league         = Column(String(255), nullable=False, default=LEAGUES[0])
    is_fake_club   = Column(Boolean, default=False)
    
    energy_applied = Column(Float, default=0, server_default='0', nullable=False)
    
    owner          = relationship("UserBot", back_populates="clubs", lazy="selectin")
    characters     = relationship("Character", back_populates="club", lazy="selectin")

    @hybrid_property
    def total_power(self) -> int:
        return sum(character.full_power for character in self.characters)

    @hybrid_property
    def koef_energy(self) -> float:
        if self.energy_applied > 500:
            return 1.3
        elif self.energy_applied > 400:
            return 1.25
        elif self.energy_applied > 300:
            return 1.2
        elif self.energy_applied > 200:
            return 1.15
        elif self.energy_applied > 100:
            return 1.1
        else:
            return 1.0
    
class LeagueFight(Base):
    __tablename__ = "league_fight"
    
    id               = Column(BigInteger, primary_key=True, index=True)
    match_id         = Column(String(255), nullable=False)
    group_id         = Column(String(255), nullable=False)
    time_to_start    = Column(DateTime)
  
    first_club_id    = Column(BigInteger, ForeignKey('clubs.id'), nullable=False)
    second_club_id   = Column(BigInteger, ForeignKey('clubs.id'), nullable=False)
    
    first_club       = relationship("Club", foreign_keys=[first_club_id], lazy="selectin")
    second_club      = relationship("Club", foreign_keys=[second_club_id], lazy="selectin")
    
    goal_first_club  = Column(Integer, default=0)
    goal_second_club = Column(Integer, default=0)
    
    @hybrid_property
    def total_points_first_club(self) -> int:
        if self.goal_first_club == self.goal_second_club:
            return 1
        elif self.goal_first_club > self.goal_second_club:
            return 3
        else:
            return 0
    
    @hybrid_property
    def total_points_second_club(self) -> int:
        if self.goal_first_club == self.goal_second_club:
            return 1
        elif self.goal_first_club < self.goal_second_club:
            return 3
        else:
            return 0