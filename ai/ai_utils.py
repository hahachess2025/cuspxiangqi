"""
ai_utils.py
This module is about how to search for a fight starting position based on setup rules. 
A fight starting position is found by brute force.
In this program, we randomize searching orders to make the games more interesting.

"""

import copy
import logging
import random
import time
from tkinter import *
from tkinter import messagebox

import cchess

from PIL import Image as PILImage

import ui.ui_utils
import utils.game_results

logger = logging.getLogger(__name__)
"""
Two search modes: one_cusp and all_cusps
One_cusp is for Cusp Xiangqi game. 
All_cusps is for searching all cusps. It is a education tool to show all good fight starting positions.
the results are shown in editor board.
"""
def search_for_cusp_positions_for_CC( cusp_app, board_fen, AI_engine, search_mode,stop_flag ):
    logger.info("search_for_cusp_positions_for_CC")
    cusp_app.FEN_checked = []
    cusp_app.cusp_position_fen = ""
    if search_mode == "one_cusp":
        if cusp_app.game_in_progress == False:
            return
    if stop_flag.is_set():
        return
    try:
        new_board = cchess.Board(board_fen)

    except Exception as e:
        logger.exception(f"search_for_cusp_positions_for_CC error, board_fen is {board_fen}")
        cusp_app.after(0, lambda err=e: messagebox.showerror("FEN Error", f"FEN error when searching for a fight starting position: {err}"))
        return
        
    if search_mode == "all_cusps":    
        if new_board.turn:
            cusp_app.active_color_in_cusp_setup = "W"
        else:
            cusp_app.active_color_in_cusp_setup = "B"          
    # Randomlize the game
    if search_mode == "all_cusps": 
        early_check_enable = 1
    elif search_mode == "one_cusp":    
        early_check_enable = random.randint(0, 3)
        
    if early_check_enable ==1:
       
        if legal_moves_and_check_CC(cusp_app,new_board, AI_engine, search_mode, stop_flag):
            return True 

    position_list = list(new_board.piece_map().keys())
    random.shuffle(position_list)
    # Randomlize the game
    #remove_a_piece_and_change_turn = random.randint(0, 1)
    if cusp_app.game_in_progress or search_mode == "all_cusps":
        for start_piece_position in position_list:
            if search_mode == "one_cusp":
                if cusp_app.game_in_progress == False:
                    return
                if utils.game_results.check_game_result(cusp_app):
                    return
            if stop_flag.is_set():
                return
            if new_board.piece_at(start_piece_position):
                logger.info(f"start_piece_position is {start_piece_position}")
                
                if new_board.fen() == cchess.Board().fen() and ( start_piece_position >= 5 and ( start_piece_position != 19 and start_piece_position != 27 and start_piece_position != 29 and start_piece_position != 31 ) ):
                    continue
                cusp_app.selected_piece = str(new_board.piece_at(start_piece_position))                    
               
                # remove the piece and change board turn to check singualrity

                if early_check_enable:
                    if remove_a_piece_and_check_CC(cusp_app,new_board,start_piece_position, AI_engine, search_mode, stop_flag):
                        return True

                early_check_enable = 1
                #setup-ruleto find a Cusp Position.
                piece=new_board.piece_at(start_piece_position) 
                if not cusp_app.engine_test_mode_enable:    
                    if (new_board.turn and str(piece).islower()) or ( (not new_board.turn) and str(piece).isupper()):
                        continue
					# relocating a pawn	
                    if cusp_app.cusp_pawn_setup_enable:
                        if str(piece)!='P'and str(piece)!='p': continue 
                    else:
					# relocating a non-pawn piece
                        if str(piece)=='P'or str(piece)=='p': continue 
                if one_free_move_CC(cusp_app,new_board, start_piece_position, AI_engine, search_mode, stop_flag):
                    logger.info("found a fight starting position")
                    return True

               

def remove_a_piece_and_check_CC(cusp_app,new_board, start_piece_position, AI_engine, search_mode, stop_flag):
    logger.info("remove_a_piece_and_check_CC")
    output_board = new_board.copy()
    if check_end_position_king(output_board,start_piece_position): return
    output_board.remove_piece_at(start_piece_position)
    output_board.turn = 1 ^ output_board.turn
    if piece_removed_check_fen_cusp_for_CC( cusp_app, output_board.fen(), start_piece_position,AI_engine, search_mode, stop_flag):
        if search_mode == "one_cusp":
            return True
        elif search_mode == "all_cusps":
            output_notation_for_cusp_position( cusp_app)
    if not cusp_app.engine_test_mode_enable:return
    output_board.turn = 1 ^ output_board.turn

    if piece_removed_check_fen_cusp_for_CC( cusp_app, output_board.fen(), start_piece_position,AI_engine, search_mode, stop_flag):
        if search_mode == "one_cusp":
            return True
        elif search_mode == "all_cusps":
            output_notation_for_cusp_position( cusp_app)
def legal_moves_and_check_CC(cusp_app,new_board, AI_engine, search_mode, stop_flag):
    logger.info("legal_moves_and_check_CC") 
    output_board = new_board.copy()
    list_legal_moves = list(output_board.legal_moves)
    random.shuffle(list_legal_moves)
    for move in list_legal_moves:
    #for move in  output_board.legal_moves:
        output_board.push(move)
        if check_fen_cusp( cusp_app, output_board.fen(), AI_engine, search_mode, stop_flag):
            start_sq = move.from_square
            to_sq = move.to_square
            piece = str(new_board.piece_at(start_sq))
            cusp_app.selected_piece = piece
            convert_start_end_postion_uci( cusp_app, start_sq, to_sq )
            cusp_app.move_str = str( move)
            if search_mode == "one_cusp":
                return True
            elif search_mode == "all_cusps":
                output_notation_for_cusp_position( cusp_app)
        output_board.pop()
        
def piece_removed_check_fen_cusp_for_CC( cusp_app, output_board_fen, start_piece_position,AI_engine, search_mode, stop_flag):
    logger.info("piece_removed_check_fen_cusp_for_CC")
    if check_fen_cusp( cusp_app, output_board_fen, AI_engine, search_mode,stop_flag ):
        convert_start_end_postion_uci( cusp_app, start_piece_position, -1 )
        if search_mode == "one_cusp":
            return True
        elif search_mode == "all_cusps":
            output_notation_for_cusp_position(cusp_app)
            
# engine-test-mode or human-level-mode 
def one_free_move_CC(cusp_app,new_board, start_piece_position, AI_engine, search_mode, stop_flag):
    logger.info("one_free_move_CC")
    end_position_one_loop_finished = False
    piece_end_position_first_loop = True
    end_position_try_number = 0
    while end_position_one_loop_finished == False:
        # Brute force
        if not cusp_app.engine_test_mode_enable:
            output_board = new_board.copy()
            pieces_position_list = list(output_board.piece_map().keys())
            end_available_position_list = [x for x in range(0, 90) if x not in pieces_position_list]
        else:
            end_available_position_list= list(range(90))
        random.shuffle(end_available_position_list)  
        for piece_end_position in end_available_position_list:
            if search_mode == "one_cusp":
                if cusp_app.game_in_progress == False:
                    return
            if stop_flag.is_set():
                return 
            output_board = new_board.copy()

            end_position_try_number = end_position_try_number + 1

            if end_position_try_number > 90:
                end_position_one_loop_finished = True
                break
            
            if not cusp_app.engine_test_mode_enable:
                if (new_board.turn and piece_end_position<45) or (not new_board.turn and piece_end_position>44): continue

            # end position is not occupied, or not occupied by king or KING
            if check_end_position_king(output_board,piece_end_position):continue

            if ( str(output_board.piece_at(start_piece_position)) == "p" ):
                if ( piece_end_position in cusp_app.black_pawn_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "P" ):
                if ( piece_end_position in cusp_app.white_pawn_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "a" ):
                if ( piece_end_position in cusp_app.black_advisor_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "A" ):
                if ( piece_end_position in cusp_app.white_advisor_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "b" ):
                if ( piece_end_position in cusp_app.black_bishop_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "B" ):
                if ( piece_end_position in cusp_app.white_bishop__legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "k" ):
                if ( piece_end_position in cusp_app.black_king_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            elif ( str(output_board.piece_at(start_piece_position)) == "K" ):
                if ( piece_end_position in cusp_app.white_king_legal_positions ):
                    if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                        if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                            return True

            else:
                if not ui.ui_utils.both_kings_checked( cusp_app, start_piece_position, piece_end_position, output_board, ) and not ui.ui_utils.two_kings_meet( cusp_app, start_piece_position, piece_end_position, output_board, ):
                    if set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
                        return True
                                    
def set_piece_and_check_cusp_fen( cusp_app, output_board, start_piece_position, piece_end_position, AI_engine, search_mode, stop_flag ):
    logger.info("set_piece_and_check_cusp_fen")
    piece = output_board.piece_at(start_piece_position)
    output_board.remove_piece_at(start_piece_position)
    output_board.set_piece_at(piece_end_position, piece)
    output_board.turn = 1 ^ output_board.turn
    if check_cusp_and_setup(cusp_app, output_board.fen(), start_piece_position, piece_end_position, AI_engine, search_mode,stop_flag):
        return True
    if not cusp_app.engine_test_mode_enable: return    
    output_board.turn = 1 ^ output_board.turn
    if check_cusp_and_setup(cusp_app, output_board.fen(), start_piece_position, piece_end_position, AI_engine, search_mode,stop_flag):
        return True


def check_cusp_and_setup(cusp_app, output_board_fen, start_piece_position, piece_end_position, AI_engine, search_mode,stop_flag):
    logger.info("check_cusp_and_setup")
    if check_fen_cusp(cusp_app, output_board_fen, AI_engine, search_mode,stop_flag):
        convert_start_end_postion_uci( cusp_app, start_piece_position, piece_end_position )
        if search_mode == "one_cusp":
            return True
        elif search_mode == "all_cusps":
            output_notation_for_cusp_position(cusp_app)

"""
It is hard to find a position whose score is exactly +1 or -1. 
We can find a score within an acceptable range, when the Score Difference is small.
The Score Difference is abs( abs(score)-1).
We can set Maximum Score Difference and Minimum Score Difference
for searching fight starting position.
The Maximum Difference and Minimum Difference will affect search speed.
If the Maximum Difference is too small, it takes a long time to find a fight starting position.
If it is too big, the fight starting position loses sensitivity.
Usually, we can set a symmetric range, such as 0.9 < score < 1.1 or -1.05 < score <-0.95.
In general, the Maximum Difference can be set as 0.1 or 0.05.
The Minimum Difference is usually set as zero. 

For a handicap game, we can set Minimum Difference to a non-zero number.
For example, chess engine Stockfish 17.1 vs 1.0, we can set Minimum Difference to 2 and Maximum Difference to 3.
And only Stockfish 17.1 can set a fight starting position, the game is somehow balanced.

When the Maximum Difference is big, we need to consider the direction of Difference.

For example, chess engine Stockfish 17.1 vs 1.0, position A's score is 4, white to move. Stockfish 1.0 chooses white and white must win.
Position B's score is -2, white to mvoe. Stockfish 1.0 choose Black, and white must win. 
The difficulty of position A and B are different for stockfish 1.0.

We intorduced outer range and inner range.
A score is closer to zero means inner range.
In the example above, score 4 is outer range, and -2 is inner range.

So if we want to find a accurate handicap score for Stockfish 17.1 vs 1.0 game, we need to seperate outer range and inner range.
For those engines whose elos are very close, it is no necessary.

"""
def check_fen_cusp(cusp_app, old_fen, AI_engine, search_mode,stop_flag):
    logger.info("check_fen_cusp")
    cusp_app.cusp_position_fen = ""

    engine_fen = copy.copy(old_fen)

    if search_mode == "one_cusp":
        if cusp_app.game_in_progress == False:
            return
    #elif search_mode == "all_cusps":

    parts=engine_fen.split()
    short_engine_fen= " ".join(parts[:-2])
    if short_engine_fen in cusp_app.FEN_checked:
        return
    else:
        cusp_app.FEN_checked.append(short_engine_fen)
        
    if stop_flag.is_set():
        return
    
    first_threshold=0.1
    
    board = cchess.Board(engine_fen)
    board_turn_changed = cchess.Board(engine_fen)
    board_turn_changed.turn = 1 ^ board_turn_changed.turn
  
    if board.is_checkmate() == False and board_turn_changed.is_check() == False:
        # To speed up the search process, we apply two-step check.
        try:
            if cusp_app.engine_time_limit_enable:
                info = AI_engine.go(board, limit=0.1)
            else:
                info = AI_engine.go(board, limit=15)
            position_score = info["score"].relative.score(mate_score=10000)
            position_score = position_score / 100
        except Exception as e:
            logger.exception('check_fen_cusp engine error')
            if stop_flag.is_set(): return
            cusp_app.after(0, lambda err=e:  messagebox.showerror("Engine error", f"When checking whether a FEN is a Cusp Position: {err}"))
            return
        if stop_flag.is_set(): return
        if ( ( cusp_app.engine_score_cusp_inner_range_enable and 1 - cusp_app.engine_score_difference_maximum - first_threshold < position_score <= 1 - cusp_app.engine_score_difference_minimum + first_threshold ) 
            or ( cusp_app.engine_score_cusp_outer_range_enable and 1 + cusp_app.engine_score_difference_minimum - first_threshold <= position_score < 1 + cusp_app.engine_score_difference_maximum + first_threshold ) 
            or ( cusp_app.engine_score_cusp_outer_range_enable and -1 - cusp_app.engine_score_difference_maximum - first_threshold < position_score <= -1 - cusp_app.engine_score_difference_minimum + first_threshold ) 
            or ( cusp_app.engine_score_cusp_inner_range_enable and -1 + cusp_app.engine_score_difference_minimum - first_threshold <= position_score < -1 + cusp_app.engine_score_difference_maximum + first_threshold ) ):
            

            try:
                if search_mode == "one_cusp":
                    engine_evaluation_limit = ( cusp_app.engine_evaluation_limit_for_each_cusp_candidate )
                elif search_mode == "all_cusps":
                    engine_evaluation_limit = cusp_app.editor_engine_evaluation_limit
                info = AI_engine.go(board, limit=engine_evaluation_limit)
                position_score = info["score"].relative.score(mate_score=10000)
                position_score = position_score / 100
            except Exception as e:
                logger.exception('check_fen_cusp check again, engine error')
                if stop_flag.is_set(): return
                cusp_app.after(0, lambda err=e: messagebox.showerror("Engine Error", f"When checking whether a FEN is a Cusp Position: {err}"))
                return

            if ( ( cusp_app.engine_score_cusp_inner_range_enable and 1 - cusp_app.engine_score_difference_maximum < position_score <= 1 - cusp_app.engine_score_difference_minimum ) 
                or ( cusp_app.engine_score_cusp_outer_range_enable and 1 + cusp_app.engine_score_difference_minimum <= position_score < 1 + cusp_app.engine_score_difference_maximum ) 
                or ( cusp_app.engine_score_cusp_outer_range_enable and -1 - cusp_app.engine_score_difference_maximum < position_score <= -1 - cusp_app.engine_score_difference_minimum ) 
                or ( cusp_app.engine_score_cusp_inner_range_enable and -1 + cusp_app.engine_score_difference_minimum <= position_score < -1 + cusp_app.engine_score_difference_maximum ) ):
                if cusp_app.game_in_progress or search_mode == "all_cusps":
                    set_up_for_the_cusp_position(cusp_app,position_score,board,search_mode)
                    return True
                     
# When we find a Cusp Position, we need to set color-to-move and color-must-win.                     
def set_up_for_the_cusp_position(cusp_app,position_score,board,search_mode):
    logger.info('set_up_for_the_cusp_position')
    if ( 1 - cusp_app.engine_score_difference_maximum <= position_score <= 1 - cusp_app.engine_score_difference_minimum or 1 + cusp_app.engine_score_difference_minimum <= position_score <= 1 + cusp_app.engine_score_difference_maximum ):
        if board.turn:
            cusp_app.color_must_win_in_cusp_chess = "W"
            if 1 + cusp_app.engine_score_difference_minimum <= position_score <= 1 + cusp_app.engine_score_difference_maximum:
                cusp_app.color_recommended_for_opponent = "W"
            else:
                cusp_app.color_recommended_for_opponent = "B"
        else:
            cusp_app.color_must_win_in_cusp_chess = "B"
            if 1 + cusp_app.engine_score_difference_minimum <= position_score <= 1 + cusp_app.engine_score_difference_maximum:
                cusp_app.color_recommended_for_opponent = "B"
            else:
                cusp_app.color_recommended_for_opponent = "W"        
    
    else:
        if board.turn:
            cusp_app.color_must_win_in_cusp_chess = "B"
            if -1 - cusp_app.engine_score_difference_maximum < position_score <= -1 - cusp_app.engine_score_difference_minimum: 
                cusp_app.color_recommended_for_opponent = "B"
            else:
                cusp_app.color_recommended_for_opponent = "W"                          
        else:
            cusp_app.color_must_win_in_cusp_chess = "W"
            if -1 - cusp_app.engine_score_difference_maximum < position_score <= -1 - cusp_app.engine_score_difference_minimum: 
                cusp_app.color_recommended_for_opponent = "W"
            else:
                cusp_app.color_recommended_for_opponent = "B"     
    if search_mode == "one_cusp":
        cusp_app.cusp_chess_phase = "Decision"
        if cusp_app.engine == cusp_app.engine_one:
            # we need to know which color set up a Cusp Position, so we can let the other to choose a color.
            cusp_app.active_color_in_cusp_setup = "W"
            cusp_app.player_one_score_on_the_cusp_set = True
            if board.turn:
                cusp_app.player_one_value_on_the_cusp = position_score
                ui.ui_utils.update_two_player_scores_bar( cusp_app, position_score)
            else:
                cusp_app.player_one_value_on_the_cusp = -position_score
                ui.ui_utils.update_two_player_scores_bar( cusp_app, -position_score)

        elif cusp_app.engine == cusp_app.engine_two:
            cusp_app.active_color_in_cusp_setup = "B"
            cusp_app.player_two_score_on_the_cusp_set = True
            if not board.turn:
                cusp_app.player_two_value_on_the_cusp = position_score
                ui.ui_utils.update_two_player_scores_bar( cusp_app, position_score)
            else:
                cusp_app.player_two_value_on_the_cusp = -position_score
                ui.ui_utils.update_two_player_scores_bar( cusp_app, -position_score)

    if board.turn:
        cusp_app.color_to_move_in_fight_phase = "W"
    else:
        cusp_app.color_to_move_in_fight_phase = "B"
    cusp_app.move_score = position_score
    cusp_app.move_score_set = True

    cusp_app.cusp_position_fen = board.fen()





def convert_start_end_postion_uci(cusp_app, start_piece_position, piece_end_position):
    logger.info('convert_start_end_postion_uci')

    if piece_end_position != -1:
        cusp_app.move_str = str(cchess.square_name(start_piece_position)) + str( cchess.square_name(piece_end_position) )

    else:
        cusp_app.move_str = str(cchess.square_name(start_piece_position)) + "xx"

    cusp_app.piece_move_start_square = start_piece_position
    cusp_app.to_sq = piece_end_position

    if start_piece_position != piece_end_position:
        ui.ui_utils.clear_board_move_history(cusp_app)

# For searching for all Cusp Positions
def output_notation_for_cusp_position(cusp_app):
    logger.info('output_notation_for_cusp_position')
    # it is OK to get into Decision Phase without moving any piece
    if cusp_app.move_str == "":
        move_str = "none"
    else:
        move_str = str(cusp_app.move_str)

    choose_action = "S"

    if cusp_app.color_to_move_in_fight_phase == "W":
        color_to_move = "W"
    elif cusp_app.color_to_move_in_fight_phase == "B":
        color_to_move = "B"
    # a complete example "CX {RS e0e1 BWBN} ", Red set up, e0e1, Black must win, Black to move
    action_str = ( "CX {" + cusp_app.active_color_in_cusp_setup + choose_action + " " + move_str + " " + cusp_app.color_must_win_in_cusp_chess + "W" + color_to_move + "N" + "}" )

    action_str = action_str + " {" + str(cusp_app.move_score) + "}"

    cusp_app.searching_cusps_count = cusp_app.searching_cusps_count + 1

    if len(cusp_app.editor_fen_text.get("1.0", END)) > 1:
        cusp_app.editor_fen_text.insert(
            END, "\n" + str(cusp_app.searching_cusps_count) + ". " + action_str
        )
        cusp_app.editor_fen_text.insert(END, "\n" + str(cusp_app.cusp_position_fen))
    else:
        cusp_app.editor_fen_text.insert( END, str(cusp_app.searching_cusps_count) + ". " + action_str )
        cusp_app.editor_fen_text.insert(END, "\n" + str(cusp_app.cusp_position_fen))
    cusp_app.editor_fen_text.see("end")
                    
def check_end_position_king(output_board,piece_end_position):
    logger.info("check_end_position_king")
    if output_board.piece_at(piece_end_position) and ( output_board.piece_at(piece_end_position).symbol() == "k" or output_board.piece_at(piece_end_position).symbol() == "K" ):
        return True  