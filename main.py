from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import keyboard
import asyncio
import db_api
import random
import time
import threading
import telebot
import sender

token = '6465991193:AAEVIZhCn4YZ20h_O9_no6bamHbk6ixi8zI'
bot_for_send = telebot.TeleBot(token=token)
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
sender.set_bot(dp)
sender.init_handlers()
# CHANNEL_ID_POSTBACK = -1001849822929
CHANNEL_ID_POSTBACK_FD = -1001949431375
CHANNEL_ID_POSTBACK_RD = -1001961232607
loop_to_send = asyncio.new_event_loop()
ID_TO_CHECK = {
    
}


def ids_checker():
    while True:
        time.sleep(.5)
        arr_to_del = []
        for i in ID_TO_CHECK:
            if time.time() - ID_TO_CHECK[i][0] > 2:
                try:
                    arr_to_del.append(i)
                    # is_register = db_api.get_site_id(i)
                    db_api.update_user_dep_tries(0, i)

                    bot_for_send.send_message(i, "You can play again!", reply_markup=keyboard.try_again)
                except Exception as e:
                    print(str(e))
        
        for i in arr_to_del:
            del ID_TO_CHECK[i]


def site_id_in_checher(site_id):
    for i in ID_TO_CHECK:
        if ID_TO_CHECK[i][1] == site_id:
            return i
    return False


class EnterPassword(StatesGroup):
    enter_1win_id = State()


class EnterDep(StatesGroup):
    enter_dep = State()


@dp.channel_post_handler(lambda message: message.chat.id == CHANNEL_ID_POSTBACK_RD)
async def channel_re_dep(message: Message):
    data = message.text.split(':')
    if len(data) == 2:
        if float(data[1].replace(',', '.')) >= 3.4:
            user = db_api.get_user_by_site_id(int(data[0]))
            db_api.set_re_dep(int(data[0]), 1)
            if user[0][3] == 30:
                db_api.update_user_dep_tries(-1, user[0][0])
                return await bot.send_message(
                    int(user[0][0]),
                    f'ID {data[0]} 1win - Deposit successfully ✅.\nOperation in bot is correctly again'
                )


@dp.channel_post_handler(lambda message: message.chat.id == CHANNEL_ID_POSTBACK_FD)
async def handler_postback(message: Message):
    data = message.text.split(':')
    if len(data) == 1:
        db_api.add_register_user(data[0])
        r = site_id_in_checher(data[0])
        if r:
            del ID_TO_CHECK[r]
            return await bot.send_message(r, f'ID {data[0]}\n1win - Registered successfully ✅.\n'
                                      f'Connection is possible ✅.\nAccount activation is required ⌛️', reply_markup=keyboard.start)
            # return await bot.send_message(r, 'For activation bot you need make deposit 500 ₹')

    if len(data) == 2 or len(data) == 3:
        if data[1] == '35':
            return

        if data[1].isdigit():
            if float(data[1].replace(',', '.')) >= 3.4:
                user = db_api.get_user_by_site_id(int(data[0]))
                db_api.set_re_dep(int(data[0]), 1)
                if user[0][3] == 30:
                    db_api.update_user_dep_tries(-1, user[0][0])
                    return await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} 1win - Deposit successfully ✅.\nOperation in bot is correctly again'
                    )

        if data[1] == 'registration':
            db_api.add_register_user(data[0])
            r = site_id_in_checher(data[0])
            if r:
                del ID_TO_CHECK[r]
                return await bot.send_message(r, f'ID {data[0]}\n1win - Registered successfully ✅.\n'
                                 f'Connection is possible ✅.\nAccount activation is required ⌛️', reply_markup=keyboard.start)
                # return await bot.send_message(r, 'For activation bot you need make deposit 500 ₹')

        if data[1] == 'deposit':
            user = db_api.get_user_by_site_id(int(data[0]))
            db_api.set_re_dep(int(data[0]), 1)
            if user[0][3] == 30:
                db_api.update_user_dep_tries(-1, user[0][0])
                return await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} 1win - Deposit successfully ✅.\nOperation in bot is correctly again'
                    )

        if data[1] == 'fdp':
            user = db_api.get_site_id(int(data[0]))
            deposit = float(data[2]) + user[0][1]
            db_api.set_deposit(int(data[0]), deposit)
            user = db_api.get_user_by_site_id(int(data[0]))
            if user:
                # if user[0][3] == 30 and float(data[2]) >= 3.5:
                    # db_api.update_user_dep_tries(-1, user[0][0])
                    # return await bot.send_message(
                        # int(user[0][0]),
                        # f'ID {data[0]} 1win - Deposit successfully ✅.\nOperation in bot is correctly again'
                    # )
                # if user[0][3] == 30 and float(data[2]) < 3.5:
                    # return await bot.send_message(
                        # int(user[0][0]),
                        # f'ID {data[0]} 1win - Deposit unsuccessfully ❌. Deposit is too small.\n'
                        # f'<b>Minimum 300₹</b>',
                        # parse_mode='html'
                    # )

                if deposit >= 6:
                    await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} 1win - Deposit successfully ✅.',
                        parse_mode='html',
                    )
                    await bot.send_message(
                        int(user[0][0]),
                        'The bot will give you the odds at which you should bet Auto Cash Out. You must strictly '
                        'follow the odds given by the bot. If you deviate from the bot\'s strategy, you may lose.\n'
                        'Before you start, click the Help button.',
                        reply_markup=keyboard.instruction
                    )
                else:
                    await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} 1win - Deposit unsuccessfully ❌. Deposit is too small.\n'
                        f'<b>Minimum 500₹</b>',
                        parse_mode='html'
                    )


@dp.callback_query_handler(lambda call: call.data == 'help')
async def get_help(call: CallbackQuery):
    await call.message.edit_text(
        'The minimum balance to play with the bot is 1000.\n\n'
        'The process of using the bot: \n'
        'The bot gives you the odds you should use in the next round. Just follow the given odds. Don\'t worry if you '
        'lose in a round, just click the "NEXT ROUND" button and continue playing next. '
        'In the end, you will always end up with a win.\n\n'
        'You have to use the Auto Cash Out feature.\n'
        'You can only play for one bet.\n'
        'You can skip rounds\n'
        '⚠️Play only with the Auto Cash Out odds given to you by the bot!  Do NOT change the Auto Cash Out odds! ⚠️\n\n'
        'Good luck😉',
        reply_markup=keyboard.ok_button
    )


@dp.callback_query_handler(lambda call: call.data == 'Ok')
async def ok_answer(call: CallbackQuery):
    await call.message.edit_text(
        'The bot will give you the odds at which you should bet Auto Cash Out. You must strictly follow the odds given'
        ' by the bot. If you deviate from the bot\'s strategy, you may lose.\n'
        'Before you start, click the Help button.',
        reply_markup=keyboard.instruction
    )


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()
    db_api.add_user(message.chat.id)
    await message.answer(
        'Welcome to VISHAL HACK BOT. Is bot se aapko AVIATOR game ke upcoming rounds ke liye accurate '
        'coefficients milenge. Please read the instructions below to properly connect to the bot. '
        'https://telegra.ph/FULL-GUIDE-TO-VISHAL-HACK-BOT-23-09-27',
        reply_markup=keyboard.start
    )


@dp.callback_query_handler(lambda call: call.data == 'demo', state='*')
@dp.callback_query_handler(lambda call: call.data == 'win', state='*')
@dp.callback_query_handler(lambda call: call.data == 'lose', state='*')
async def start_demo(call: CallbackQuery, state: FSMContext):
    await state.finish()
    tries = db_api.get_tries(call.message.chat.id)

    if tries < 3:
        db_api.set_tries(tries, call.message.chat.id)
        await call.message.answer(
            f'ID: DEMO MODE, NO NEED TO PLACE BETS. NEED ACTIVATION PLAYER ID.\n'
            f'coef {random.randint(100, 200)/100}',
            reply_markup=keyboard.bet
        )
    else:
        await call.message.answer(
            'DEMONSTRATION COMPLETED ✅. BOT KA ISTEMAAL KARNE KE LIYE APNE ACCOUNT KO AKTIVATE KAREIN. AKTIVATION '
            'KE BAAD, PLAYER ID DIKHEGI AUR AAP APNI ID KO BOT KE SAATH JOD SAKTE HAIN, AGAMI ROUNDS KE LIYE SAHI '
            'COEFFICIENTS PRAPT KARNE KE LIYE.',
            reply_markup=keyboard.demo_end
        )


@dp.callback_query_handler(lambda call: call.data == 'start')
async def inline_start(call: CallbackQuery):
    user = db_api.get_user(call.message.chat.id)
    site_id = user[2]
    dep_tries = user[3]

    if site_id and dep_tries == -1:
        deposit = db_api.get_site_id(site_id)
        if deposit:
            if deposit[0][1] >= 6:
                return await call.message.answer(
                    f'PLAYER ID: {deposit[0][0]}\n'
                    f'CASHOUT {random.randint(110, 220) / 100} ✅',
                    reply_markup=keyboard.real_bet
                )
    if site_id and dep_tries > 20:
        user = db_api.get_user(call.message.chat.id)
    
        if user[2]:
            r = db_api.get_site_id(user[2])
            if r[0][2]:
                db_api.update_user_dep_tries(-1, call.message.chat.id)
                return await real_bet(call)

        db_api.update_user_dep_tries(30, call.message.chat.id)

        if call.message.chat.id not in list(ID_TO_CHECK.keys()):
            ID_TO_CHECK[call.message.chat.id] = [time.time(), call.message.text]

        return await call.message.answer(
            "⚠️The CASINO system, noticed suspicious!⚠️\n\n"
            "🛑Signals are limited to 4 hours!🛑\n\n"
            "🟢Make a deposit 400 rupees to continue receiving signals!🟢\n\n"
            "Or wait for 4 hours - the bot will restore the work, so as not to arouse suspicion of CASINO⚠",
            parse_mode='html',
            reply_markup=keyboard.enter_dep
        )
    if site_id:
        deposit = db_api.get_site_id(site_id)
        print(dep_tries + 1, call.message.chat.id)
        db_api.update_user_dep_tries(dep_tries + 1, call.message.chat.id)
        return await call.message.answer(
            f'PLAYER ID: {deposit[0][0]}\n'
            f'CASHOUT {random.randint(110, 220) / 100} ✅',
            reply_markup=keyboard.real_bet
        )

    await EnterPassword.enter_1win_id.set()
    await call.message.answer(
        'Bro😎\n'
        'I can see you\'re serious🔥\n'
        'Read the article and let\'s start earning!💸\n'
        'Enter your ID and bet on the signals on the 🟢NEXT ROUND🟢\n'
        '🤑 Success!👍\n\n'
        'For activation bot register here and enter account ID✅\n\n'
        '<b>LINK</b>: https://bit.ly/vishalhack\n'
        '<b>PROMOCODE:\n' 
        'NAKAT77</b>\n'
        'Use promocode it’s very important for activation bot\n\n'
        '🆔Enter 1Win ID:',
        parse_mode='html',
        disable_web_page_preview=True
    )
    # await call.message.answer(
    #     '🆔Enter 1win ID:'
    # )


@dp.callback_query_handler(lambda call: call.data == 'enter_dep_id')
async def enter_dep_id(call: CallbackQuery):
    await call.message.answer('Enter your PLAYER ID:')
    await EnterDep.enter_dep.set()


@dp.message_handler(state=EnterDep.enter_dep)
async def enter_dep(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Wait you\'r deposit')


@dp.message_handler(state=EnterPassword.enter_1win_id)
async def enter_1win_id_by_user(message: Message, state: FSMContext):
    user_id = message.text

    if user_id.isdigit():
        is_register = db_api.get_site_id(user_id)

        if is_register:
            db_api.set_site_id(message.chat.id, user_id)
        
            if is_register[0][2]:
                db_api.update_user_dep_tries(-1, message.chat.id)

            await state.finish()
            if is_register[0][1] >= 6:
                return await bot.send_message(
                    message.chat.id,
                    f'ID {is_register[0][0]} 1win - Deposit successfully ✅.',
                    parse_mode='html',
                    reply_markup=keyboard.demo_end
                )
            

            return await message.answer(f'ID {is_register[0][0]}\n1win - Registered successfully ✅.\n'
                                 f'Connection is possible ✅.\nAccount activation is required ⌛️', reply_markup=keyboard.start)
            # return await message.answer('For activation bot you need make deposit 500 ₹')

    # ID_TO_CHECK[message.chat.id] = [time.time(), message.text]
    # db_api.set_site_id(message.chat.id, user_id)
    await message.answer('Wrong PLAYER ID')
    await message.answer('Enter PLAYER ID')
    # await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'real_win')
@dp.callback_query_handler(lambda call: call.data == 'real_lose')
async def real_bet(call: CallbackQuery):
    user = db_api.get_user(call.message.chat.id)
    site_id = user[2]
    dep_tries = user[3]

    if site_id and dep_tries == -1:
        deposit = db_api.get_site_id(site_id)
        if deposit:
            if deposit[0][1] >= 6:
                return await call.message.answer(
                    f'PLAYER ID: {deposit[0][0]}\n'
                    f'CASHOUT {random.randint(110, 220) / 100} ✅',
                    reply_markup=keyboard.real_bet
                )
    if site_id and dep_tries > 20:
        user = db_api.get_user(call.message.chat.id)

        if user[2]:
            r = db_api.get_site_id(user[2])
            if r[0][2]:
                db_api.update_user_dep_tries(-1, call.message.chat.id)
                return await real_bet(call)

        db_api.update_user_dep_tries(30, call.message.chat.id)
        ID_TO_CHECK[call.message.chat.id] = [time.time(), call.message.text]
        return await call.message.answer(
                    "⚠The CASINO system, noticed suspicious!⚠\n\n"
                    "🛑Signals are limited to 4 hours!🛑\n\n"
                    "🟢Make a deposit 400 rupees to continue receiving signals!🟢\n\n"
                    "Or wait for 4 hours - the bot will restore the work, so as not to arouse suspicion of CASINO⚠",
                    parse_mode='html',
                    reply_markup=keyboard.enter_dep
                )

    if site_id:
        deposit = db_api.get_site_id(site_id)
        print(dep_tries + 1, call.message.chat.id)
        db_api.update_user_dep_tries(dep_tries + 1, call.message.chat.id)
        await call.message.answer(
            f'PLAYER ID: {deposit[0][0]}\n'
            f'CASHOUT {random.randint(110, 220) / 100} ✅',
            reply_markup=keyboard.real_bet
        )


t = threading.Thread(target=ids_checker)
t.start()
executor.Executor(dp).start_polling()
