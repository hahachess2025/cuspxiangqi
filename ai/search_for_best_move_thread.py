"""
search_for_best_move_thread.py

This module is for Fight Phase of Cusp Xiangqi or standard xiangqi.

"""
import ctypes
import logging
import threading
from tkinter import *
from tkinter import messagebox

from PIL import Image as PILImage


import ui.ui_utils
import utils.game_results
import utils.pgnhistory

logger = logging.getLogger(__name__)

class SearchForBestMoveThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self._stop_flag = threading.Event() 

    def run(self):
        logger.info("SearchForBestMoveThread, search started")

        self.app.setting_up_in_cusp_chess = False
        both_AI_players = True

        while both_AI_players and self.app.game_in_progress:
            if self._stop_flag.is_set():
                return
            if self.app.game_player_mode == "AvA":
                both_AI_players = True
            else:
                both_AI_players = False

            if (( self.app.chess_game_variant_mode == "Normal" and ( (self.app.player_one == "AI" and self.app.board.turn) or (self.app.player_two == "AI" and not self.app.board.turn) ) ) 
                or ( self.app.chess_game_variant_mode != "Normal" and ( ( self.app.player_swap_side == False and ( (self.app.player_one == "AI" and self.app.board.turn) or (self.app.player_two == "AI" and not self.app.board.turn) ) ) 
                or ( self.app.player_swap_side and ( (self.app.player_one == "AI" and not self.app.board.turn) or (self.app.player_two == "AI" and self.app.board.turn) ) ) ) )):
                if self.app.board.turn:
                    if self.app.player_swap_side == False:
                        self.app.engine = self.app.engine_one
                        search_limit=self.app.engine_one_searching_limit_for_best_move
                    else:
                        self.app.engine = self.app.engine_two
                        search_limit=self.app.engine_two_searching_limit_for_best_move
                elif self.app.board.turn == False:
                    if self.app.player_swap_side == False:
                        self.app.engine = self.app.engine_two
                        search_limit=self.app.engine_two_searching_limit_for_best_move
                    else:
                        self.app.engine = self.app.engine_one
                        search_limit=self.app.engine_one_searching_limit_for_best_move
                try:
                    info = self.app.engine.go( self.app.board, limit=search_limit, )
                    position_score = info["score"].relative.score(mate_score=10000)
                    position_score = position_score / 100
                except Exception as e:
                    logger.exception('SearchForBestMoveThread, engine error')
                    if self._stop_flag.is_set(): return
                    self.app.after(0, lambda err=e: messagebox.showerror("Engine Error", f"Engine error when searching the best move: {err}"))
                    return

                if ( self.app.chess_game_variant_mode != "Normal" and self.app.player_swap_side ):
                    ui.ui_utils.update_two_player_scores_bar(self.app, -position_score)
                else:
                    ui.ui_utils.update_two_player_scores_bar(self.app, position_score)

                self.app.move_score = position_score
                self.app.move_score_set = True

                move = info.get("pv")[0]

                start_sq = move.from_square
                to_sq = move.to_square
                piece = str(self.app.board.piece_at(start_sq))

                self.app.move_str = move
                utils.pgnhistory.save_PGN_and_output_move_history(self.app, True)
                if self.app.game_in_progress:
                    ui.ui_utils.animate_piece_move(self.app, piece, start_sq, to_sq)


                    self.app.board.push(move)

                    ui.ui_utils.clear_board_move_history(self.app)

                    # time.sleep(0.01)
                    ui.ui_utils.draw_pieces(self.app, self.app.chess_game_variant_mode)

                    if utils.game_results.check_game_result(self.app):
                        return

        if not self.app.game_in_progress:
            self.app.stop_game_in_tournament()



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
        logger.info("SearchForBestMoveThread _stop_flag set")