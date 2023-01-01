from random import randint as rnd
from texts import *


class TicTacToe:
    def __init__(self):
        self.winning_series = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        self.moves_indexes = dict()
        self.marked_areas = list()
        self.user_mark = ''
        self.first_move = -1

        self.create_moves_indexes()  # create indexes for play fields for faster search

    def set_user_mark(self, mark):
        self.user_mark = mark

    def create_moves_indexes(self):
        for i in range(len(self.winning_series)):
            for j in range(len(self.winning_series[i])):
                if self.winning_series[i][j] in self.moves_indexes:
                    self.moves_indexes[self.winning_series[i][j]].append((i, j))
                else:
                    self.moves_indexes[self.winning_series[i][j]] = [(i, j)]

    def get_playground(self):
        playground = ''
        for i in range(3):  # take only first three lists to draw a playground
            for j in range(len(self.winning_series[i])):
                playground += str(self.winning_series[i][j]) + ('\n' if j == len(self.winning_series[i])-1 else ' | ')
        playground += '\n'

        return playground

    def make_move(self, msg):
        result_message = ''

        if self.first_move == 0:  # user
            if msg.isdigit():
                n = int(msg)
                if 0 < n < 10 and n not in self.marked_areas:
                    self.marked_areas.append(n)
                    self.mark_position(n)
                else:
                    result_message = 'Selected field does not exist OR has been already marked!\n'
            else:
                result_message = 'Allowed input is an integer from 1 to 9!\n'
        elif self.first_move == 1:  # bot
            n = -1
            while n == -1 or n in self.marked_areas:
                n = rnd(1, 9)

            self.marked_areas.append(n)
            self.mark_position(n)

        return result_message

    def mark_position(self, position: int):
        for i in self.moves_indexes[position]:
            self.winning_series[i[0]][i[1]] = self.user_mark if self.first_move == 0 else ('X' if self.user_mark == 'O' else 'O')

    # return:
    # -1 -draw
    #  0 -keep playing
    #  1 -winner
    def get_result(self):
        i = 0
        iter_series = True
        total_marks = 0
        while iter_series and i < len(self.winning_series):
            cur_mark = ''
            mark_count = 0
            iter_sequence = True
            j = 0
            while iter_sequence and j < len(self.winning_series[i]):
                if self.winning_series[i][j] != 'O' and self.winning_series[i][j] != 'X':
                    iter_sequence = False
                else:
                    if cur_mark == '':
                        cur_mark = self.winning_series[i][j]
                        mark_count = 1
                    elif cur_mark == self.winning_series[i][j]:
                        mark_count += 1
                        if mark_count == 3:
                            return 1

                    total_marks += 1
                    j += 1

            i += 1

        if total_marks == 24:
            return -1

        return 0

    def play(self, msg):
        if self.user_mark == '':
            if msg.upper() == 'O' or msg.upper() == 'X':
                self.set_user_mark(msg.upper())
            else:
                return msg_select_mark

        msg_to_user = ''

        if self.first_move == -1:
            self.first_move = rnd(0, 1)  # 0 - user; 1 - bot

            if self.first_move == 0:  # user
                msg_to_user = 'You are playing first!\n'
                msg_to_user += self.get_playground()
            elif self.first_move == 1:  # bot
                msg_to_user = 'Bot is playing first!\n'

        game_over = False
        keep_playing = True
        while keep_playing and not game_over:
            returned_msg = self.make_move(msg)
            if returned_msg:
                keep_playing = False
                msg_to_user += returned_msg
            else:
                if self.first_move == 1:
                    msg_to_user += "Bot:\n"
                msg_to_user += self.get_playground()

                result = self.get_result()

                if result == 1:
                    msg_to_user += "You WIN!\n" if self.first_move == 0 else "You LOSE!\n"
                    game_over = True
                elif result == -1:
                    msg_to_user += "It's a draw!\n"
                    game_over = True
                else:
                    if self.first_move == 0:  # bot will play right after user, continue loop
                        self.first_move += 1
                    else:
                        self.first_move -= 1
                        keep_playing = False

        if game_over:
            msg_to_user += 'You may play again or return to main menu.'
        else:
            msg_to_user += f'Enter field number where to put your "{self.user_mark}"'

        return msg_to_user
