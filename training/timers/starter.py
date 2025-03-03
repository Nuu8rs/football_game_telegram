import random
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from training.utils.sender_message import RegisterInTrainingSender
from training.utils.sender_notification import NotificationSender
from training.core.manager_training import TrainingManager
from training.constans import TIME_TRAINING, TIME_REGISTER_TRAINING

from services.training_service import TrainingService

class StartTraining:
    _time_from_presell = TIME_REGISTER_TRAINING
    START_TAIMERS = [
        "14:00"
    ]
    # START_TAIMERS = [
    #     "13:00",
    #     "14:00",
    #     "15:00",
    #     "16:00"
    # ]    

    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.sender_message: RegisterInTrainingSender = None
        self.notification_sender: NotificationSender = None

    @property
    def time_training(self) -> datetime:
        time_str = random.choice(self.START_TAIMERS)
        hour, minute = map(int, time_str.split(":"))
        current_time = datetime.now()
        
        return current_time.replace(
            hour=hour, 
            minute=minute, 
            second=0
        )
    async def _register_timer_training(self, time_training: datetime):
        last_training_timer = await TrainingService.get_last_training_timer()
        if not last_training_timer:
            await TrainingService.register_training_timer(
                time_start = time_training
            )
            return
        if self.time_training.date() != last_training_timer.time_start.date():
            await TrainingService.register_training_timer(
                time_start = time_training 
            )
            
            
    async def start_training(self):
        
        time_traning = self.time_training
        await self._register_timer_training(time_traning)      
          
        self.sender_message = RegisterInTrainingSender(
            end_time = time_traning
        )
        self.notification_sender = NotificationSender(
            start_time = time_traning
        )
        await self._start_shedulers(time_traning)
        
    async def _start_shedulers(self, time_traning: datetime):
        
        await self._start_send_notification()
        
        await self._start_preregiste_message(time_traning = time_traning)
        await self._start_traning(time_traning = time_traning)
        await self._end_training(time_traning = time_traning)
        self.scheduler.start()

    async def _start_send_notification(self):
        await self.notification_sender.send_notification()
 
    async def _start_preregiste_message(self, time_traning: datetime):
        pre_timer = time_traning - self._time_from_presell
        self.scheduler.add_job(
            func=self.sender_message.start_send_message,  
            trigger=DateTrigger(
                pre_timer
            ),
            misfire_grace_time=10
        )
        
    async def _start_traning(self, time_traning: datetime):
        self.scheduler.add_job(
            func=TrainingManager.start_training,  
            trigger=DateTrigger(time_traning),
            misfire_grace_time=10
        )
        
    async def _end_training(self, time_traning: datetime):
        _end_time = time_traning + TIME_TRAINING
        
        self.scheduler.add_job(
            func=TrainingManager.end_all_trainings,
            trigger=DateTrigger(_end_time),
            misfire_grace_time=10
        )

class SchedulerEveryDayStartTraining:
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start_scheduler(self):
        await StartTraining().start_training()
        # self.scheduler.add_job(
        #     func=StartTraining().start_training,
        #     trigger=CronTrigger(hour=12, minute=0),
        #     misfire_grace_time=10
        # )
        
        # self.scheduler.start()