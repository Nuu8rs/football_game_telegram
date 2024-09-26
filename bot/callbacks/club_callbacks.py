from aiogram.filters.callback_data import CallbackData

class SelectClubToJoin(CallbackData, prefix="select_club"):
    club_id: int
    
class JoinToClub(CallbackData, prefix = "join_to_club"):
    club_id: int
    
class LeaveThisClub(CallbackData, prefix = "leave_club"):
    club_id: int
    
class TransferOwner(CallbackData, prefix="transfer_owner"):
    user_id_new_owner: int
    
class DeleteClub(CallbackData, prefix="delete_club"):
    club_id: int