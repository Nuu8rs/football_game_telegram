from dataclasses import dataclass

from database.models.character import Character
from enum import Enum

class RoleDuel(Enum):
    GOALKEEPER = "goalkeeper"
    FORWARD = "forward"

class PositionAngle:
    UP = "up"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class DuelUser:
    user_1: Character
    user_2: Character
    
    points_user_1: int = 0
    points_user_2: int = 0
    
    role_user_1: RoleDuel
    role_user_2: RoleDuel
    
    position_angle_user_1: PositionAngle | None = None
    position_angle_user_2: PositionAngle | None = None
    
    
    @property
    def all_users_duel(self) -> list[Character]:
        return [self.user_1, self.user_2]
    
    
    def change_roles_character(self) -> None:
        self.role_user_1,self.role_user_2 = self.role_user_2,self.role_user_1
    
    def anulate_angle_users(self) -> None:
        self.position_angle_user_1, self.position_angle_user_2 = None, None 
    
    def get_user_by_role(self, role: RoleDuel) -> Character:
        return self.user_1 if self.role_user_1 == role else self.user_2
    
    def add_points_to_role(self, role: RoleDuel, points: int):
        if self.role_user_1 == role:
            self.points_user_1 =+ points
        else:
            self.points_user_2 =+ points