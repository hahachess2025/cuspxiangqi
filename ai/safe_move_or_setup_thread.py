"""
safe_move_or_setup_thread.py - for Safe Move Phase and Decision Phase.
This module manages how AI players play the Cusp Chess during Safe Move and Decision Phases.

At first, an AI player need to evaluate the current position whether a color's win rate is over 50%.
For Pikafish engine, +1 means win rate is aournd 50%, and -1 means loss rate is 50%.

If a color's win rate is over 50%, the AI will choose the color directly and set the color as color-must-win. 
The game goes into Fight phase.

If both colors' win rate are less than 50%, the AI can decide whether it wants to set up a fight starting position, 
or make a safe move.
In this program, the choice is done randomly for engine players.

For a safe move, the AI need check the score of the position after a move. 
For example, -0.8<score<+0.8 is a safe choice.
If it can't find a Safe Move, it will try to set up a good fight-starting position.

Setting up a good fight starting position, a short name can be cusp setup.
For Cusp Setup, the AI needs to search for a good fight starting position by setup rules.
If a good fight starting position is found, the AI needs to set color-to-move and color-must-win (if in Engine-Test-Mode).
Then, another AI player or a human player chooses a color to play.
If the AI can't find a good fight starting position, it will find a Safe Move instead.

A player who set up a fight starting position is the active player in the game. 
The other player is the passive player.

To do: Now the search algorithm for Cusp Setup is done by brute force. It is slow. 
       A better algorithm should find all good fight starting position fast, so we can choose one randomly.

"""

import ctypes
import logging
import random
import threading
from tkinter import *
from tkinter import messagebox

import cchess
from PIL import Image as PILImage

import ai.ai_utils
import ai.ChessEngine
import ui.language
import ui.setting_panel
import ui.ui_utils
import utils.game_results
import utils.pgnhistory

logger = logging.getLogger(__name__)

class SafeMoveOrSetupThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self._stop_flag = threading.Event() 

    def run(self):
        logger.info("safe_move_or_setup_in_cusp_chess")
        # This is to make sure get into the loop at least once when there is one AI player.
        both_AI_players = True

        if self.app.chess_game_variant_mode != "Normal":
            while both_AI_players and self.app.game_in_progress:
                if self._stop_flag.is_set():
                    return
                if utils.game_results.check_game_result(self.app):
                    return
                # check if both players are AI
                if self.app.game_player_mode == "AvA":
                    both_AI_players = True
                else:
                    both_AI_players = False
               # When self.app.cusp_chess_phase=="Decision", board's turn cannot tell now which player needs to choose a color, because it means the color-to-move in Fight phase. 
                
                cusp_chess_player_one_turn = ( self.app.chess_game_variant_mode == "CuspXiangqi" and self.app.board.turn ) 
                cusp_chess_player_two_turn = ( self.app.chess_game_variant_mode == "CuspXiangqi" and not self.app.board.turn )

                if ( self.app.cusp_chess_phase == "SafeMove" and ( ( self.app.player_one == "AI" and cusp_chess_player_one_turn  ) or ( self.app.player_two == "AI" and  cusp_chess_player_two_turn ) ) ) or self.app.cusp_chess_phase == "Decision":
                    # reset for human player
                    self.app.human_no_move_this_round = True
                    # The default phase of a Cusp Chess game is "SafeMove"
                    if self.app.cusp_chess_phase == "SafeMove":
                        if cusp_chess_player_one_turn:
                            self.app.engine = self.app.engine_one

                        elif cusp_chess_player_two_turn:
                            self.app.engine = self.app.engine_two

                    # For Cusp Setup phase, we need to know the color who set up a Cusp Position.
                    # Then, we know who we are.
                    elif self.app.cusp_chess_phase == "Decision":
                        if self.app.active_color_in_cusp_setup == "W":
                            self.app.engine = self.app.engine_two

                        elif self.app.active_color_in_cusp_setup == "B":
                            self.app.engine = self.app.engine_one
                    # We need to evaluate the current position before making a move.
                    if ( self.app.cusp_chess_phase == "SafeMove" and self.app.no_choosing_color_directly_enable == False ) or self.app.cusp_chess_phase == "Decision":
                        try:
                            info = self.app.engine.go( self.app.board, limit=self.app.engine_evaluation_limit_for_each_cusp_candidate, )
                            position_score = info["score"].relative.score( mate_score=10000)
                            position_score = position_score / 100
                        except Exception as e:
                            logger.exception('SafeMoveOrSetupThread engine error')
                            if self._stop_flag.is_set(): return
                            self.app.after(0, lambda err=e: messagebox.showerror("Engine Error", f"Engine error when evaluating a position: {err}"))
                            return
                        logger.info( f"self.cusp_chess_phase = {self.app.cusp_chess_phase}, position_score is {position_score}" )

                    if self.app.cusp_chess_phase == "SafeMove":
                        # based on  engine pikafish, score 1 means winning rate is around 50% for the color to move
                        # so now engine can choose the color directly.
                        # This can only happen when one player made a mistake to let score >1 or <-1

                        if ( self.app.no_choosing_color_directly_enable == False and position_score >= 1 ):
                            self.choose_the_current_color_directly(position_score )
                        # choose your opponent's color
                        elif ( self.app.no_choosing_color_directly_enable == False and position_score <= -1 ):
                            self.choose_the_opposite_color_directly(position_score )
                        else:
                            # AI will search for a Cusp Position when on its
                            # turn and board ply is not smaller than maximum ply.
                            self.choose_safe_move_or_setup()

                    elif self.app.cusp_chess_phase == "Decision":
                        # The score is the only reason which color a player will choose after its opponent set up a Cusp Position.                       
                        # It is drawed as green mark on the player's eval bar.

                        self.passive_AI_player_set_cusp_score(position_score)
                        # A player chooses a color, when his/her opponent set up a Cusp Position
                        self.passive_AI_player_choose_color(position_score)
                        
                        if self._stop_flag.is_set():
                            return
                        self.game_get_into_fight_phase()
        else:
            logger.info(" safe_move_or_setup_in_cusp_chess error")

    """
    A player can only choose a color on his/her turn.
    He/she can't not make a move or change color-to-move when he/she wants to choose a color directly.
    Otherwise, the game is not fair.
    So when a player chooses a color, the color-must-win color-to-move are set. 
    He/she must win with the color, and draw means loss.
    """    
    def choose_the_current_color_directly(self,position_score ):
        logger.info("choose_the_current_color_directly")                                 
        self.app.choose_color_directly = True
        self.app.cusp_chess_phase = "Fight"
        # Engine_one is player one in Safe Move phase. It is tentative white player.
        if self.app.engine == self.app.engine_one:
            # the score worths remembered, draw red mark
            # for active color and green mark for passive
            # color on eval bars
            self.app.player_one_score_on_the_cusp_set = True
            self.app.active_color_in_cusp_setup = "W"
        # Engine_two is player two, and tentative black player.
        elif self.app.engine == self.app.engine_two:
            self.app.player_two_score_on_the_cusp_set = True
            self.app.active_color_in_cusp_setup = "B"
        # Cusp Chess              
        if self.app.chess_game_variant_mode == "CuspXiangqi":
            # Now score > 1, it means white can win. That is why we choose white now.
            # After we choose white directly, white must win.
            if self.app.board.turn:
                self.app.color_must_win_in_cusp_chess = "W"
                # Because white didn't make a move on its turn, and we can't change the order,
                # white will still move first in Fight phase.
                self.app.color_to_move_in_fight_phase = "W"
                self.app.player_one_value_on_the_cusp = ( position_score )
            # Now score > 1, it means black can win. 
            else:
                self.app.color_must_win_in_cusp_chess = "B"
                # Because black didn't make a move on its turn, black will move first in Fight phase.
                self.app.color_to_move_in_fight_phase = "B"
                self.app.player_two_value_on_the_cusp = ( position_score )
            ui.ui_utils.update_two_player_scores_bar( self.app, position_score)

        # set the CX prefix in move notation
        self.app.setting_up_in_cusp_chess = True

        # score for move notation
        self.app.move_score = position_score
        self.app.move_score_set = True
        # When choosing a color directly, you cannot make a move on board
        # The 'none' is for PGN.

        self.app.move_str = "none"

        if self._stop_flag.is_set():
            return
        if self.app.game_in_progress:
            utils.pgnhistory.save_PGN_and_output_move_history( self.app, True)
            ui.ui_utils.draw_pieces( self.app, self.app.chess_game_variant_mode)
            self.app.update()
            # After choosing a color directly, the game goes into Fight phase.
            # Board's turn can not be changed
            self.app.AI_searching_best_move()

    def choose_the_opposite_color_directly(self,position_score ):
        logger.info("choose_the_opposite_color_directly") 
        self.app.choose_color_directly = True
        self.app.cusp_chess_phase = "Fight"
        if self.app.engine == self.app.engine_one:
            self.app.active_color_in_cusp_setup = "W"

            self.app.player_one_score_on_the_cusp_set = True
        elif self.app.engine == self.app.engine_two:
            self.app.active_color_in_cusp_setup = "B"
            self.app.player_two_score_on_the_cusp_set = True
        if self.app.chess_game_variant_mode == "CuspXiangqi":
            if self.app.board.turn:
                # score is <-1, means the opposite color score> 1
                self.app.color_must_win_in_cusp_chess = "B"
                self.app.color_to_move_in_fight_phase = "W"
                self.app.player_one_value_on_the_cusp = ( position_score )

            else:
                self.app.color_must_win_in_cusp_chess = "W"
                self.app.color_to_move_in_fight_phase = "B"
                self.app.player_two_value_on_the_cusp = ( position_score )
            # Unlike gomoku, when a Cusp Chess player chooses the opposite color, the chess board is flipped. 
            # Now engine one plays black and engine two plays white.
            self.app.player_swap_side = True
            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
            self.app.rotate_board = True
            ui.ui_utils.update_two_player_scores_bar( self.app, position_score)

        self.app.setting_up_in_cusp_chess = True

        self.app.move_score = position_score
        self.app.move_score_set = True

        self.app.move_str = "none"
        if self._stop_flag.is_set():
            return
        if self.app.game_in_progress:
            utils.pgnhistory.save_PGN_and_output_move_history( self.app, True)

            logger.info( f"swap side, color_must_win_in_cusp_chess = { self.app.color_must_win_in_cusp_chess},choose { not self.app.board.turn} directly,")
            ui.ui_utils.draw_pieces( self.app, self.app.chess_game_variant_mode)
            # now it is time for the opponent to move,
            self.app.update()
            if ( self.app.color_to_move_in_fight_phase == "W" and self.app.player_two == "AI" ) or ( self.app.color_to_move_in_fight_phase == "B" and self.app.player_one == "AI" ):
                self.app.AI_searching_best_move()
    """            
    In a real Cusp Chess tournament, a player will decide when and how to set up a fight starting position  
    based on his/her xiangqi skill and his/her opponents. 
    Here we randomly choose to make a Safe Move or set up a fight starting position. Engines don't know the difference.
    To get into Fight phase faster, we set some constraints in the program, which is not necessary in Cusp Chess game.
    """

    def choose_safe_move_or_setup(self):
        logger.info("choose_safe_move_or_setup")
        if ( ( self.app.chess_game_variant_mode == "CuspXiangqi" and self.app.board.ply() < self.app.maximum_ply_before_setup ) 
        or ( self.app.only_engine_one_setup_enable and self.app.engine == self.app.engine_two ) ):
            if self.app.chess_game_variant_mode == "CuspXiangqi":
                difference_number = max( 0, self.app.maximum_ply_before_setup - self.app.board.ply(), )

            # uniform distribution
            random_number = random.randint( 0, difference_number)
            logger.info(f"random_number  {random_number} ")
            if ( random_number != 0 or ( self.app.only_engine_one_setup_enable and self.app.engine == self.app.engine_two ) ):
                if self.app.chess_game_variant_mode == "CuspXiangqi":
                    self.make_a_safe_move_for_CC()
            else:
                if self.app.chess_game_variant_mode == "CuspXiangqi":
                    self.setup_cusp_postion_for_CC()

        else:
            if self.app.chess_game_variant_mode == "CuspXiangqi":
                self.setup_cusp_postion_for_CC()

    def passive_AI_player_set_cusp_score(self, position_score):
        logger.info( f"now self.cusp_chess_phase==CS, time to choose Color, position_score: {position_score}")

        self.app.setting_up_in_cusp_chess = True
        self.app.cusp_chess_phase = "Fight"
        # engine one means player one
        if self.app.engine == self.app.engine_one:
            self.app.player_one_score_on_the_cusp_set = True
            if self.app.board.turn:
                self.app.player_one_value_on_the_cusp = position_score
                ui.ui_utils.update_two_player_scores_bar( self.app, position_score)
            else:
                self.app.player_one_value_on_the_cusp = -position_score
                ui.ui_utils.update_two_player_scores_bar( self.app, -position_score)

        elif self.app.engine == self.app.engine_two:
            self.app.player_two_score_on_the_cusp_set = True
            if not self.app.board.turn:
                self.app.player_two_value_on_the_cusp = position_score
                ui.ui_utils.update_two_player_scores_bar( self.app, position_score)
            else:
                self.app.player_two_value_on_the_cusp = -position_score
                ui.ui_utils.update_two_player_scores_bar( self.app, -position_score)

        self.app.move_score = position_score
        self.app.move_score_set = True

    """  
    The scores of the fight starting position are keys in the Cusp Chess game.
    A player sets up a fight starting position based on the score.
    His/her opponent choose which color to play based on his/her own calculation.
    For example, it is possible one AI player thinks the score is 0.98 when setting up a fight starting position, 
    and the other AI believes the score is 0.5 or 1.5.
    Which one is right? The game result will tell. 
    
    When choosing a color, we need to check which color must win.
    If the color's score > 1, the color can win, and the AI will choose the color. 
    Otherwise, the AI will choose the oppsite color and draw also means win for the color.
    """ 
    def passive_AI_player_choose_color(self, position_score):
        logger.info("passive_AI_player_choose_color")
        if not self.app.choose_the_recommended_color_enable:        
            if self.app.color_must_win_in_cusp_chess == "W":
                # The board's turn is true doesn't mean it is the player one choosing a color now.
                # The board's FEN is set as a Cusp Position. It only means white to move in Fight phase.
                if self.app.board.turn:
                    # white will win
                    if position_score >= 1:
                        self.app.color_chosen_in_setup_phase = "W"
                        # Player two is choosing a color
                        if self.app.engine == self.app.engine_two:
                            # Player two choose white. It means the board must be flipped.
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        # Player one is choosing a color    
                        else:
                            self.app.player_swap_side = False

                    # white will lose
                    else:
                        self.app.color_chosen_in_setup_phase = "B"
                        if self.app.engine == self.app.engine_one:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False

                else:
                    # white will win
                    if position_score <= -1:
                        self.app.color_chosen_in_setup_phase = "W"
                        if self.app.engine == self.app.engine_two:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False
                    # white will lose
                    else:
                        self.app.color_chosen_in_setup_phase = "B"
                        if self.app.engine == self.app.engine_one:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False
            # black must win
            elif self.app.color_must_win_in_cusp_chess == "B":
                if not self.app.board.turn:
                    # black will win
                    if position_score >= 1:
                        self.app.color_chosen_in_setup_phase = "B"
                        if self.app.engine == self.app.engine_one:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True

                        else:
                            self.app.player_swap_side = False

                    # black will lose
                    else:
                        self.app.color_chosen_in_setup_phase = "W"
                        if self.app.engine == self.app.engine_two:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False

                else:
                    # black will win
                    if position_score <= -1:
                        self.app.color_chosen_in_setup_phase = "B"
                        if self.app.engine == self.app.engine_one:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False

                    # black will lose
                    else:
                        self.app.color_chosen_in_setup_phase = "W"
                        if self.app.engine == self.app.engine_two:
                            self.app.player_swap_side = True
                            self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                            self.app.rotate_board = True
                        else:
                            self.app.player_swap_side = False
        # useful for two engines to play handicap games
        else:
            if self.app.color_recommended_for_opponent == 'W':
                self.app.color_chosen_in_setup_phase = "W"
                if self.app.engine == self.app.engine_two:
                    self.app.player_swap_side = True
                    self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                    self.app.rotate_board = True
                else:
                    self.app.player_swap_side = False
                    
            elif  self.app.color_recommended_for_opponent == 'B':       
                self.app.color_chosen_in_setup_phase = "B"
                if self.app.engine == self.app.engine_one:
                    self.app.player_swap_side = True
                    self.app.flip_board_enable = ( self.app.flip_board_enable ^ 1 )
                    self.app.rotate_board = True
                else:
                    self.app.player_swap_side = False
                    
    def game_get_into_fight_phase(self):                          
        logger.info("game_get_into_fight_phase")
        if self.app.game_in_progress:
            utils.pgnhistory.save_PGN_and_output_move_history( self.app)
            ui.ui_utils.draw_pieces( self.app, self.app.chess_game_variant_mode)
            if self.app.chess_game_variant_mode == "CuspXiangqi":
                ui.ui_utils.draw_arrows_with_two_indexes( self.app, self.app.piece_move_start_square, self.app.to_sq, )

            self.app.update()
            if not self.app.player_swap_side:
                if ( self.app.color_to_move_in_fight_phase == "W" and self.app.player_one == "AI" ) or ( self.app.color_to_move_in_fight_phase == "B" and self.app.player_two == "AI" ):
                    self.app.AI_searching_best_move()
            else:
                if ( self.app.color_to_move_in_fight_phase == "W" and self.app.player_two == "AI" ) or ( self.app.color_to_move_in_fight_phase == "B" and self.app.player_one == "AI" ):
                    self.app.AI_searching_best_move()
    # If not setting up a Cusp Position, we can make a Safe Move: -1<score< 1.
    # Here we set a margin of safety:  -1+0.2 < score< 1-0.2.                    


    def make_a_safe_move_for_CC(self):
        logger.info("make_a_safe_move_for_CC")
        if self.app.game_in_progress == False:
            return
        if self._stop_flag.is_set():
            return   
        list_legal_moves = list(self.app.board.legal_moves)
        random.shuffle(list_legal_moves)
        
        if len(list_legal_moves) > 0:
            for move in list_legal_moves:
                if self._stop_flag.is_set(): return
                if self.app.game_in_progress:
                    self.app.board.push(move)
                    try:
                        if self.app.engine_time_limit_enable:
                            info = self.app.engine.go( self.app.board, limit=0.1)
                        else:
                            info = self.app.engine.go( self.app.board, limit=15)
                        position_score = info["score"].relative.score( mate_score=10000 )
                        position_score = position_score / 100
                    except Exception as e:
                        logger.exception('make_a_safe_move_for_CC, engine error')
                        if self._stop_flag.is_set(): return
                        self.app.after(0, lambda err=e: messagebox.showerror("Engine Error", f"Engine error when making a Safe Move: {err}"))
                        return
                    # to show how to choose a color directly    
                    if self.app.engine_safe_move_score_maximum > position_score > -self.app.engine_safe_move_score_maximum:
                        self.app.board.pop()
                        start_sq = move.from_square
                        to_sq = move.to_square
                        piece = str(self.app.board.piece_at(start_sq))
                        ui.ui_utils.animate_piece_move(self.app, piece, start_sq, to_sq)

                        self.app.move_str = move
                        self.app.move_score = -position_score
                        self.app.move_score_set = True
                        utils.pgnhistory.save_PGN_and_output_move_history(self.app)

                        ui.ui_utils.update_two_player_scores_bar(self.app, -position_score)
                        self.app.board.push(move)

                        ui.ui_utils.clear_board_move_history(self.app)

                        #time.sleep(0.02)
                        ui.ui_utils.draw_pieces(self.app, self.app.chess_game_variant_mode)

                        return
                    else:
                        self.app.board.pop()
        logger.info("no Safe Move. It is going to set up a fight starting position")
        self.setup_cusp_postion_for_CC()

    # Search for a Cusp Position and set color-to-move and color-must-win etc.
    def setup_cusp_postion_for_CC(self):
        logger.info("setup_cusp_postion_for_CC") 
        if self.app.game_in_progress == False:
            return
        if self._stop_flag.is_set():return
        self.app.game_status_label_state = "game_status_label_searching"
        ui.language.update_widget(self.app, self.app.game_status_label)

        board_fen = self.app.board.fen()

        # find a cusp Position in real time based on current board position. 
        if ai.ai_utils.search_for_cusp_positions_for_CC( self.app, board_fen, self.app.engine, "one_cusp",self._stop_flag ):
            self.app.cusp_chess_phase = "Decision"
            self.app.setting_up_in_cusp_chess = True

            self.app.choose_color_directly = False
            if self._stop_flag.is_set():
                return

            if self.app.game_in_progress:
                utils.pgnhistory.save_PGN_and_output_move_history(self.app, True)
                self.app.board.set_fen(self.app.cusp_position_fen)

                ui.ui_utils.animate_piece_move( self.app, self.app.selected_piece, self.app.piece_move_start_square, self.app.to_sq, )
                #time.sleep(0.02)
                ui.ui_utils.draw_pieces(self.app, self.app.chess_game_variant_mode)
                self.app.update()
                 # If both players are AI players, the program will stay in the while loop in SafeMoveOrSetupThread.run.  
                if ( self.app.game_player_mode == "AvH" or self.app.game_player_mode == "HvA" ):
                    ui.setting_panel.human_player_choose_color(self.app) 
                    

                    self.app.AI_searching_best_move()
        else:
            logger.info("can not find a cusp FEN, now we make a Safe Move")
            self.make_a_safe_move_for_CC()

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc( thread_id, ctypes.py_object(SystemExit) )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            logger.info("Exception raise failure")

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def stop(self):
        self._stop_flag.set()
        logger.info("SafeMoveOrSetupThread _stop_flag set")