from .create_bots import BOTS 

from .constans import LIMIT_CLUBS_IN_GROUP

class DestributeMatches:

    def __init__(self, scores_clubs: dict[int, int]) -> None:    
        self.scores_clubs = scores_clubs


    def destribute_group_clubs(self):
        clubs_ids = list(self.scores_clubs.keys())

        return [
            clubs_ids[i:i + LIMIT_CLUBS_IN_GROUP] 
            for i in range(0, len(clubs_ids), LIMIT_CLUBS_IN_GROUP)
        ]
    
    async def validate_groups(
        self,
        groups: list[list[int]]
    ):
        for group in groups:
            if len(group) == LIMIT_CLUBS_IN_GROUP:
                continue
            
            bots = BOTS(
                average_club_strength = 1000,
                name_league = "DEFAULT_LEAGUE"
            )
            clubs = await bots.create_bot_clubs(
                len_bots_club = LIMIT_CLUBS_IN_GROUP - len(group) 
            )
            group.extend([club.id for club in clubs])
            
        return groups
        
    async def get_groups(self) -> list[list[int]]:
        destribute_group_clubs = self.destribute_group_clubs()
        destribute_group_clubs = await self.validate_groups(destribute_group_clubs)
        return destribute_group_clubs
