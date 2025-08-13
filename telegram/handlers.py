from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender

import keyboards.all_kb as kb

from kazakov_list import To_Do

class Form_new_task(StatesGroup):
    task_id = State()
    title = State()
    desc = State()
    done = State()
    
class Form_delete_task(StatesGroup):
    task_id = State()
    
class Form_change_bool(StatesGroup):
    task_id = State()

class Form_edit_task(StatesGroup):
    task_id = State()
    is_title = State()
    is_desc = State()
    title_text = State()
    desc_text = State()
    
class Bot_Finish_work(StatesGroup):
    finish_work = State()

td = To_Do()
td.connect()

router = Router()



@router.message(Command('commands'))
async def open_commands(message: Message, state: FSMContext, bot: Bot) -> None:
    negr = message.from_user.id
    td.add_user(negr)
    await state.clear()
    await message.answer('Список команд:',
                         reply_markup = kb.start_option_button)

@router.callback_query(F.data == 'open_tasks')
async def open_tasks(callback: CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    try:
        output = td.log_To_Screen()
        await bot.send_message(callback.message.chat.id, output)
    except TypeError:
        await bot.send_message(callback.message.chat.id, output)
    await bot.send_message(callback.message.chat.id, 'Список команд:',
                           reply_markup = kb.start_option_button)

@router.callback_query(F.data == 'create_new_task')
async def start_create_new_task(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Введите название новой задачи:',
                               reply_markup = kb.go_to_main)
    await state.set_state(Form_new_task.title)

@router.message(F.text, Form_new_task.title)
async def start_create_new_desc(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(title = message.text, user_id = message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await message.answer('Введите описание новой задачи:',
                             reply_markup = kb.go_to_main) 
    await state.set_state(Form_new_task.desc)
  
  
@router.message(F.text, Form_new_task.desc)
async def finish_create_new_task(message: Message, state: FSMContext) -> None:
    await state.update_data(desc = message.text, user_id = message.from_user.id)
    await state.set_state(Form_new_task.task_id)
    await state.update_data(task_id = td.return_arr_len(), user_id = message.from_user.id)
    await state.set_state(Form_new_task.done) 
    await state.update_data(done = False, user_id = message.from_user.id)
    data = await state.get_data()
    await message.answer(f'{td.create_New_Task(data, message.from_user.id)}')
    await message.answer(f'{td.log_To_Screen()}')
    await state.clear()
    await message.answer('Список команд:',
                           reply_markup = kb.start_option_button)

    

@router.callback_query(F.data == 'delete_task')
async def start_delete_task(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Для удаления задачи введите её номер')
        await bot.send_message(callback.message.chat.id, f'{td.log_To_Screen()}',
                               reply_markup = kb.holy_hand_grenade)
    await state.set_state(Form_delete_task.task_id)
    
@router.message(F.text, Form_delete_task.task_id)
async def finish_delete_task(message: Message, state: FSMContext) -> None:
    await state.update_data(task_id = message.text, user_id = message.from_user.id)
    await state.set_state(Form_delete_task.task_id)
    data = await state.get_data()
    oshibka = td.delete_Task(data)
    if oshibka["Error"]:
        await message.answer(oshibka.get('text'))
        return 
    await message.answer(oshibka.get('text')) 
    await message.answer(f'{td.log_To_Screen()}')
    await state.clear()
    await message.answer('Список команд:',
                           reply_markup = kb.start_option_button)
    
    
@router.callback_query(F.data == 'is_task_done')
async def start_change_bool(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Введите номер задачи, состояние которой хотите изменить')
        await bot.send_message(callback.message.chat.id, f'{td.log_To_Screen()}',
                               reply_markup = kb.go_to_main)
    await state.set_state(Form_change_bool.task_id)
    
@router.message(F.text, Form_change_bool.task_id)
async def finish_change_bool(message: Message, state: FSMContext) -> None:
    await state.update_data(task_id = message.text, user_id = message.from_user.id)
    await state.set_state(Form_change_bool.task_id)
    data = await state.get_data()
    invalid = td.change_Bool(data)
    if invalid["Error"]:
        await message.answer(invalid.get('text'))
        return
    await message.answer(invalid.get('text'))
    await message.answer(f'{td.log_To_Screen()}')
    await state.clear()
    await message.answer('Список команд:',
                           reply_markup = kb.start_option_button)



@router.callback_query(F.data == 'edit_task')
async def start_edit_task(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    await state.clear()
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Введите номер задачи, которую хотите отредактировать')
        await bot.send_message(callback.message.chat.id, f'{td.log_To_Screen()}',
                               reply_markup = kb.go_to_main)
    await state.set_state(Form_edit_task.task_id)

@router.message(F.text, Form_edit_task.task_id)
async def edit_task_options(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(task_id = message.text, user_id = message.from_user.id)
    await state.set_state(Form_edit_task.task_id)
    data = await state.get_data()
    invalid = td.is_tasks(data['task_id'])
    if invalid["Error"]:
        await message.answer(invalid.get('text'))
        return
    await message.answer(invalid.get('text'))
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await bot.send_message(message.from_user.id, "Выберите нужную опцию",
                             reply_markup = kb.edit_option_button)
    
@router.callback_query(F.data == 'edit_name')
async def edit_task_button(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "Напишите новое название:",
                               reply_markup = kb.go_to_option)
    await state.set_state(Form_edit_task.title_text)    
        
@router.message(F.text, Form_edit_task.title_text)
async def edit_task_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(title_text = message.text, user_id = message.from_user.id)
    data = await state.get_data()
    output = td.edit_Task(int(data['task_id']), title = message.text)['text']
    await bot.send_message(message.from_user.id, output)
    await state.clear()
    await message.answer('Список команд:',
                           reply_markup = kb.start_option_button)
    
@router.callback_query(F.data == 'edit_desc')
async def edit_task_button(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "Напишите новую задачу:",
                               reply_markup = kb.go_to_option)
    await state.set_state(Form_edit_task.desc_text)
    
@router.message(F.text, Form_edit_task.desc_text)
async def edit_task_desc(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(desc_text = message.text, user_id = message.from_user.id)
    data = await state.get_data()
    output = td.edit_Task(int(data['task_id']), desc = message.text)['text']
    await bot.send_message(message.from_user.id, output)
    await state.clear()
    await message.answer('Список команд:',
                           reply_markup = kb.start_option_button)
  
       
@router.callback_query(F.data == 'exit_to_option')
async def edit_task_button(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "Выберите нужную опцию",
                                reply_markup = kb.edit_option_button)
    await state.clear()

@router.callback_query(F.data == 'exit_to_menu')
async def edit_task_button(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Список команд:',
                           reply_markup = kb.start_option_button)
    await state.clear()

    
@router.callback_query(F.data == 'finish')
async def work_finish(callback: CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, 'Вы точно хотите закончить работу с ботом?',
                             reply_markup = kb.bot_finish_working)

@router.callback_query(F.data == 'leave')
async def leave(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "Возврат в главное меню")
    await state.clear()
    await bot.send_message(callback.message.chat.id, 'Список команд:',
                           reply_markup = kb.start_option_button)
    
@router.callback_query(F.data == 'stay')
async def stay(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "Прекращение работы бота")
    await state.clear()
    

@router.callback_query(F.data == 'holy_hand_grenade')
async def delete_all(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=str(callback.message.message_id), reply_markup=None)
    td.holy_hand_grenade()
    async with ChatActionSender.typing(bot = bot, chat_id = callback.message.chat.id):
        await bot.send_message(callback.message.chat.id, "HOLY HAND GRENADE")
        await bot.send_message(callback.message.chat.id, f'{td.log_To_Screen()}',
                               reply_markup = kb.start_option_button)
    await state.clear()
    