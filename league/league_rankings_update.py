from loader import bot

from services.league_service import LeagueFightService

class UpdateLeagueRaiting:
    bot = bot
    
    
    async def start_update_rait_club(self):
        all_fights_in_league = await LeagueFightService.get_league_fights_current_month()
        