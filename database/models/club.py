from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from config import LEAGUES
from database.model_base import Base




class Club(Base):
    __tablename__ = 'clubs'
    
    id             = Column(BigInteger, primary_key=True, index=True)
    name_club      = Column(String(100), nullable=False)
    owner_id       = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    link_to_chat   = Column(String(255), nullable=True)
    league         = Column(String(254), nullable=False, default=LEAGUES[0])
    is_fake_club   = Column(Boolean, default=False)
    
    energy_applied = Column(Integer, default=0, server_default='0')
    
    owner          = relationship("UserBot", back_populates="clubs", lazy="selectin")
    characters     = relationship("Character", back_populates="club", lazy="selectin")

    @hybrid_property
    def total_power(self) -> int:
        return sum(character.full_power for character in self.characters)

    @hybrid_property
    def koef_energy(self) -> float:
        if self.energy_applied >= 500:
            return 1.3
        elif self.energy_applied >= 400:
            return 1.25
        elif self.energy_applied >= 300:
            return 1.2
        elif self.energy_applied >= 200:
            return 1.15
        elif self.energy_applied >= 100:
            return 1.1
        else:
            return 1.0