game_name = 'Tic Tac Toe'
help_description = '/help - display available commands and information about current screen'
msg_select_mark = 'Would you like to play for "X" or "O"?'
expression_format = 'number1 <operator> number2'
help_main = f"""/start - main menu
{help_description}
/calculator - perform simple arithmetic operations (very simple)
/ttt - start game '{game_name}'
/contacts - show simple phonebook
"""

calc_input_description = f"""Supported arithmetic operations - '+', '-', '*', '/'.
The expression for calculation must be in following format:
'{expression_format}'
Numbers and operation sign must be separated by space.
Also, you may use complex numbers in calculation, common format is x+yj. 
Do NOT separate parts of the complex number by space.
"""

help_calculator = f"""{help_description}
/exit - return to main menu

{calc_input_description}
"""

help_ttt = f"""
/restart, /ttt - start new game
{help_description}
/exit - return to main menu

Classic game '{game_name}', where you will play against the Bot.
The game fields are numbered from 1 through 9, you will need to send the field number where you would like to place your mark.
The first move is randomly determined.
"""

help_contacts = f"""
{help_description}
/exit - return to main menu
"""
