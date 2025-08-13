from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def check_data():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌Заполнить сначала",
                              callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


start_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/start")]
],
    resize_keyboard=True,
    one_time_keyboard=True)


edit_option_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Изменить название', callback_data = 'edit_name')],
    [InlineKeyboardButton(text = 'Изменить описание', callback_data = 'edit_desc')],
    [InlineKeyboardButton(text = 'Выйти в главное меню', callback_data = 'exit_to_menu')]
])



start_option_button = InlineKeyboardMarkup(inline_keyboard =[
    [InlineKeyboardButton(text = 'Открыть список задач📋', callback_data = 'open_tasks')],
    [InlineKeyboardButton(text = 'Создать новую задачу🆕', callback_data = 'create_new_task')],
    [InlineKeyboardButton(text = 'Удалить задачу🗑', callback_data = 'delete_task')],
    [InlineKeyboardButton(text = 'Изменить статус выполения задачи✏️', callback_data = 'is_task_done')],
    [InlineKeyboardButton(text = 'Редактировать задачу📝', callback_data = 'edit_task')],
    [InlineKeyboardButton(text = 'Закончить работу бота🚪', callback_data = 'finish')]
])



bot_finish_working = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Да✅', callback_data = 'stay')], [InlineKeyboardButton(text = 'Нет❌', callback_data = 'leave')]
])



go_to_option = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Вернуться к меню выбора опции', callback_data = 'exit_to_option')],
])

go_to_main = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Вернуться в главное меню', callback_data = 'exit_to_menu')],
])

holy_hand_grenade = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Вернуться в главное меню', callback_data = 'exit_to_menu')],
    [InlineKeyboardButton(text = 'Удалить все задачи', callback_data = 'holy_hand_grenade')]
])

admin_panel = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Посмотреть список пользователей', callback_data = 'view_all_users')],
])