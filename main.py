import telebot
from telebot import types
from bot_mode import *
from calculator import calculate
from tic_tac_toe import TicTacToe
from texts import *
from message_logger import log
from contacts import Phonebook


def get_keyboard(mode=BotModes.MAIN):
    btn_help = types.KeyboardButton('Help')
    btn_exit = types.KeyboardButton('Exit')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if mode == BotModes.MAIN:
        btn_calculator = types.KeyboardButton('Calculator')
        btn_game = types.KeyboardButton(game_name)
        btn_contacts = types.KeyboardButton('Contacts')

        markup.row(btn_calculator, btn_game, btn_contacts)
        markup.row(btn_help)
    elif mode == BotModes.CALCULATOR:
        markup.row(btn_help, btn_exit)
    elif mode == BotModes.TIC_TAC_TOE:
        btn_restart = types.KeyboardButton('Restart')
        markup.row(btn_restart, btn_help, btn_exit)
    elif mode == BotModes.CONTACTS:
        btn_show = types.KeyboardButton('Show')
        btn_add = types.KeyboardButton('Add')
        btn_delete = types.KeyboardButton('Delete')
        btn_search = types.KeyboardButton('Search')

        markup.row(btn_show, btn_add, btn_search, btn_delete)
        markup.row(btn_help, btn_exit)

    return markup


def start_bot_server():
    bot = telebot.TeleBot("5856704254:AAHqxHI6GphS9zeROEXnt4L2GhbSZ2FkBdk")  # , parse_mode=None
    bot_mode = BotMode()
    tic_tac_toe = TicTacToe()
    phonebook = Phonebook()

    @bot.message_handler(commands=['start', 'exit'])
    @bot.message_handler(func=lambda message: message.text == 'Exit')
    def send_menu(message):
        log(message, 'send_menu', bot_mode.current_mode)
        if bot_mode.current_mode == BotModes.CONTACTS and (message.text == 'Exit' or message.text == '/exit'):
            phonebook.save_contacts()

        bot_mode.set_mode(BotModes.MAIN)
        bot.send_message(message.chat.id,
                         "Use the navigation buttons below " + u'\U0001F447' * 3,
                         reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda message: message.text == 'Help')
    def send_help(message):
        log(message, 'send_help', bot_mode.current_mode)
        txt = ''
        match bot_mode.current_mode:
            case BotModes.MAIN:
                txt = help_main
            case BotModes.CALCULATOR:
                txt = help_calculator
            case BotModes.TIC_TAC_TOE:
                txt = help_ttt
            case BotModes.CONTACTS:
                txt = help_contacts
            case _:
                txt = 'Cannot help you((('
        bot.send_message(message.chat.id, txt, reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['calculator'])
    @bot.message_handler(func=lambda message: message.text == 'Calculator')
    def calculator(message):
        log(message, 'calculator', bot_mode.current_mode)
        bot_mode.set_mode(BotModes.CALCULATOR)
        bot.send_message(message.chat.id,
                         f"You can calculate simple mathematical expression in format '{expression_format}'",
                         reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['ttt', 'restart'])
    @bot.message_handler(func=lambda message: message.text == game_name or message.text == 'Restart')
    def play_game(message):
        log(message, 'play_game', bot_mode.current_mode)
        bot_mode.set_mode(BotModes.TIC_TAC_TOE)
        tic_tac_toe.__init__()
        bot.send_message(message.chat.id,
                         f"Let's play '{game_name}'!\n{msg_select_mark}",
                         reply_markup=get_keyboard(bot_mode.current_mode))

    #
    # Contacts
    #
    @bot.message_handler(commands=['contacts'])
    @bot.message_handler(func=lambda message: message.text == 'Contacts')
    def contacts(message):
        log(message, 'contacts', bot_mode.current_mode)
        phonebook.__init__()
        phonebook.read_contacts()
        bot_mode.set_mode(BotModes.CONTACTS)
        bot.send_message(message.chat.id,
                         "> Simple phonebook <",
                         reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['add'])
    @bot.message_handler(func=lambda message: message.text == 'Add')
    def add(message):
        log(message, 'add', bot_mode.current_mode)
        if bot_mode.current_mode == BotModes.CONTACTS:
            sent_message = bot.send_message(message.chat.id,
                                            "Enter contact's name and phone number separated by comma:\n<name>,<phone_number>",
                                            reply_markup=get_keyboard(bot_mode.current_mode))
            bot.register_next_step_handler(sent_message, add_contact)

    def add_contact(message):
        log(message, 'add_contact', bot_mode.current_mode)
        result = phonebook.add_contact(message.text)
        msg_to_user = '--> Contact is added to the phonebook!'
        if not result:
            msg_to_user = 'Something is wrong with the input format! Try again by pressing the "Add" button.'

        bot.send_message(message.chat.id,
                         msg_to_user,
                         reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['delete'])
    @bot.message_handler(func=lambda message: message.text == 'Delete')
    def delete(message):
        log(message, 'delete', bot_mode.current_mode)
        if bot_mode.current_mode == BotModes.CONTACTS:
            sent_message = bot.send_message(message.chat.id,
                                            "Enter contact's id to delete:",
                                            reply_markup=get_keyboard(bot_mode.current_mode))
            bot.register_next_step_handler(sent_message, delete_contact)

    def delete_contact(message):
        log(message, 'delete_contact', bot_mode.current_mode)
        result = phonebook.delete_contact(message.text)
        msg_to_user = '--> Contact is deleted!'
        if not result:
            msg_to_user = 'Input is not an integer or id is not in the list!\n' \
                          'Please, press "Show" button to see the full list of contacts and their ids.',

        bot.send_message(message.chat.id,
                         msg_to_user,
                         reply_markup=get_keyboard(bot_mode.current_mode))

    @bot.message_handler(commands=['search'])
    @bot.message_handler(func=lambda message: message.text == 'Search')
    def search(message):
        log(message, 'search', bot_mode.current_mode)
        if bot_mode.current_mode == BotModes.CONTACTS:
            sent_message = bot.send_message(message.chat.id,
                                            "Enter name or part of the name to search for:",
                                            reply_markup=get_keyboard(bot_mode.current_mode))
            bot.register_next_step_handler(sent_message, search_contacts)

    def search_contacts(message):
        log(message, 'search_contact', bot_mode.current_mode)
        result = phonebook.search_contacts(message.text)
        bot.send_message(message.chat.id,
                         result,
                         reply_markup=get_keyboard(bot_mode.current_mode))

    #
    # common
    #
    @bot.message_handler()
    def process_message(message):
        log(message, 'process_message', bot_mode.current_mode)
        msg_to_user = ''

        if bot_mode.current_mode == BotModes.CALCULATOR:
            msg_to_user = calculate(message.text)
        elif bot_mode.current_mode == BotModes.TIC_TAC_TOE:
            msg_to_user = tic_tac_toe.play(message.text)
        elif bot_mode.current_mode == BotModes.CONTACTS:
            msg_to_user = phonebook.perform_command(message.text)

        bot.send_message(message.chat.id, msg_to_user, reply_markup=get_keyboard(bot_mode.current_mode))

    print('server started...')

    bot.infinity_polling()


if __name__ == '__main__':
    start_bot_server()
