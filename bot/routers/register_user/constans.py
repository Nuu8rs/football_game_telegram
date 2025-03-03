from aiogram.types import FSInputFile


START_REGISTER_PHOTO = FSInputFile("src/register_user/pre_register.jpg") 
CREATER_CHARACTER_PHOTO = FSInputFile("src/register_user/create_character.jpg") 
SEND_NAME_CHARACTER_PHOTO = FSInputFile("src/register_user/send_name.jpg")
SELECT_POSITION_PHOTO = FSInputFile("src/register_user/select_position.jpg") 
TERRITORY_ACADEMY_PHOTO = FSInputFile("src/register_user/territory_academy.jpg") 
JOIN_TO_CLUB_PHOTO = FSInputFile("src/register_user/join_to_club.jpg") 
FIRST_TRAINING_PHOTO = FSInputFile("src/register_user/first_training.jpg") 
FORGOT_TRAINING_PHOTO = FSInputFile("src/register_user/forgot_training.jpg")
SELECT_GENDER_PHOTO = FSInputFile("src/register_user/choise_gender.jpg")

TIME_SLEEP_REGISTER_MESSAGE = 7 
TIME_FORGOT_MESSAGE = 60*4
COUNT_FORGOT_MESSAGE = 3