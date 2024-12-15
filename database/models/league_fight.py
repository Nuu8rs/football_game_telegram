from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped

from database.model_base import Base
from database.models.club import Club

class LeagueFight(Base):
    __tablename__ = "league_fight"
    
    id               = Column(BigInteger, primary_key=True, index=True)
    match_id         = Column(String(255), nullable=False, unique=True)
    group_id         = Column(String(255), nullable=False)
    time_to_start    = Column(DateTime)
  
    first_club_id    = Column(BigInteger, ForeignKey('clubs.id'), nullable=False)
    second_club_id   = Column(BigInteger, ForeignKey('clubs.id'), nullable=False)
    
    first_club:Mapped["Club"]   = relationship("Club", foreign_keys=[first_club_id], lazy="selectin")
    second_club:Mapped["Club"]  = relationship("Club", foreign_keys=[second_club_id], lazy="selectin")
    
    goal_first_club  = Column(Integer, default=0)
    goal_second_club = Column(Integer, default=0)
    
    is_beast_league: bool = Column(Boolean, nullable=False, server_default = "0")
    is_top_20_club: bool = Column(Boolean, nullable=False, server_default = "0")
    
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
