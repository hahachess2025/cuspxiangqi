"""
All moves are recorded using Standard Algebraic Notation (SAN), 
except in Decision Phase. 
The notation system is designed to be Redundant on purpose. 
It is clear and intuitive.

All notations in Decision Phase start with “CX”, which means “Cusp Xiangqi”. 
The notation in the Decision Phase has two lines at most. 
If a player chooses a color directly, it has only one line. 
There are four different notations in the Decision Phase:
•	Move a piece. 
For example, in the notation “CX {RS e0e1 BWBN} {0.91}”, 
“RS e0e1 BWBN” means tentative Red (R) player set (S) up a fight-starting position by moving a piece from e0 to e1. 
“BW” means the Black (B) color must win (W). 
“BN” means the Black (B) color moves next (N). 
{0.91} is the position score calculated by tentative Red player. 
Because it is 0.91 for Black, it is reasonable for the tentative Red player to set Black must win.
•	Remove a piece. 
For example, in the notation “CX {RS f0xx BWBN} {0.92}”, 
“RS f0xx” means tentative Red player set up a fight-starting position by removing a piece at f0 from the xiangqi board. 
“BW” means the Black color must win, and “BN” means the Black color moves next. 
The position score is 0.92 for the Black, that is why Black must win.
•	Choose a color when the opponent set up a fight-starting Position. 
For example, in the notation “CX {BCBW} {1.08}”, After tentative Red player set up a fight-starting Position, 
“BCB” means tentative Black player chose Black color. 
“BW” means that Black must win and draw means win for Red. 
{1.08} is the position score calculated by the tentative Black player. 
Because the position score was 1.08 for Black, 
then the tentative Black player thought the win rate of Black is over 50%. 
Choosing Black is a reasonable choice here.
•	Choose a color directly.  
For example, in the notation “CX {BC none BWBN} {1.15}”, 
“BC” means tentative Black player chose a color directly. 
"none" means the player can't make a move when choosing a color directly. 
“BW” means the Black color must win. Here we know the tentative Black player can only choose Black color. 
His/her opponent will be the Red color. “BN” means the Black color moves next. 
The position score is 1.15 for Black, which means the win rate of Black is over 50%. 
That is also why the player chose Black directly.

"""


import datetime
import logging
import pathlib
import time
from tkinter import *
from tkinter import filedialog, messagebox

import cchess
import regex
from PIL import Image as PILImage

import ui.setting_panel
import ui.ui_utils
import utils.game_results
import utils.tournament

logger = logging.getLogger(__name__)

def save_PGN_and_output_move_history(cusp_app, active=False):
    logger.info("save_PGN_and_output_move_history")

    if cusp_app.setting_up_in_cusp_chess:
        cusp_app.pgn_one_player_one_line = False
        # a player set up a Cusp Position or choose a color directly
        if active:
            # it is OK to set up without any move
            if cusp_app.move_str == "":
                move_str = "none"
            else:
                move_str = str(cusp_app.move_str)
            # if a play believe a Color can win without changing board turn
            if cusp_app.choose_color_directly:
                choose_action = "C"
            else:
                choose_action = "S"
            # the first move in fight phase. It can be set when set up a Cusp Position
            # change chess PGN notation to xiangqi notation 
            if cusp_app.color_to_move_in_fight_phase == "W":
                color_to_move = "R"
            elif cusp_app.color_to_move_in_fight_phase == "B":
                color_to_move = "B"
               
            if cusp_app.active_color_in_cusp_setup == "W":
                active_color_in_cusp_setup = "R"
            elif cusp_app.active_color_in_cusp_setup == "B":
                active_color_in_cusp_setup = "B" 
                
            if cusp_app.color_must_win_in_cusp_chess == "W":
                color_must_win_in_cusp_chess = "R"
            elif cusp_app.color_must_win_in_cusp_chess == "B":
                color_must_win_in_cusp_chess = "B"     

            
            action_str = ( "CX {" + active_color_in_cusp_setup + choose_action + " " + move_str + " " + color_must_win_in_cusp_chess + "W" + color_to_move + "N" + "}" )
        # when someone set up a Cusp Position, the other player choose which color to play
        else:
            if cusp_app.active_color_in_cusp_setup == "W":
                passive_side_in_cusp_setup = "B"
            elif cusp_app.active_color_in_cusp_setup == "B":
                passive_side_in_cusp_setup = "R"
            # whether the color is a must-win color, or a draw-means-win color
            if cusp_app.color_chosen_in_setup_phase == "W":
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    color_and_result = "RW"
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    color_and_result = "RD"
            elif cusp_app.color_chosen_in_setup_phase == "B":
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    color_and_result = "BD"
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    color_and_result = "BW"

            action_str = ( "CX {" + passive_side_in_cusp_setup + "C" + color_and_result + "}" )
    # just like normal xiangqi
    else:
        if cusp_app.move_str == "" or cusp_app.move_str== 'none':
            action_str = "none"
        else:
            if cusp_app.current_lang == "cn":
                action_str = str(cusp_app.board.move_to_notation(cusp_app.move_str))
            else:
                action_str = str(cusp_app.move_str)
    if cusp_app.blindfold_mode:
        cusp_app.blindfold_move_notice_label["text"] = str(action_str)
    # if a engine is playing
    if cusp_app.move_score_set:
        if cusp_app.eval_show_enable:
            action_str = action_str + " {" + str(cusp_app.move_score) + "}"
    if utils.game_results.check_early_stop_results(cusp_app):
        utils.game_results.check_game_early_stop(cusp_app)
        return
    if cusp_app.game_in_progress:   
        write_to_scrolledtext(cusp_app, action_str)
        
        # output PGN
        # create PGN folder
        pathlib.Path("PGN/").mkdir(parents=True, exist_ok=True)
        if cusp_app.output_PGN_enable:
            if cusp_app.PGN_header == False:
                game_Date = str(datetime.date.today().strftime("%Y-%m-%d"))

                gamer_Red = cusp_app.player_one_name

                gamer_Black = cusp_app.player_two_name

                writeFile = open(cusp_app.PGN_save_path, "w")
                writeFile.writelines('[Date "' + game_Date + '"]' + "\n")
                writeFile.writelines('[Red "' + gamer_Red + '"]' + "\n")
                writeFile.writelines('[Black "' + gamer_Black + '"]' + "\n")
                if cusp_app.adjudicator_engine_enable:
                    if set_adjudicator_engine_name(cusp_app):
                        writeFile.writelines('[Adjudicator Engine "{}"]'.format(str(cusp_app.adjudicator_engine_name)))
                writeFile.writelines("\n")                
                if cusp_app.chess_game_variant_mode == "CuspXiangqi":
                    writeFile.writelines('[Variant "Cusp Xiangqi"]' + "\n")
                
                writeFile.close()

            write_to_PGN(cusp_app, action_str)
            
        # if there is a new move, then it will be reset.
        cusp_app.move_str = ""
        # if there is a new engine move, then it will be reset.
        cusp_app.move_score_set = False

def set_adjudicator_engine_name(cusp_app):
    logger.info("set_adjudicator_engine_name") 
    if cusp_app.adjudicator_name_input == '':
        if cusp_app.engine_adjudicator_path:
            if "/" in cusp_app.engine_adjudicator_path:
                engine_adjudicator_path = cusp_app.engine_adjudicator_path.split("/")[-1]   
            if len(engine_adjudicator_path) > 30:
                engine_adjudicator_path = engine_adjudicator_path[:30]
            if  " " in engine_adjudicator_path: 
                engine_adjudicator_path = engine_adjudicator_path.split(" ")[0]
            if  "-" in engine_adjudicator_path: 
                engine_adjudicator_path = engine_adjudicator_path.split("-")[0]  
            cusp_app.adjudicator_engine_name=engine_adjudicator_path
    else:
        cusp_app.adjudicator_engine_name = cusp_app.adjudicator_name_input
    if cusp_app.adjudicator_engine_name:  
        return True
        

def write_to_scrolledtext(cusp_app, action_str):
    logger.info("write_to_scrolledtext")
    if cusp_app.board.turn:
        cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
        # file is not empty
        if len(cusp_app.move_history_text.get("1.0", END)) > 1:
            cusp_app.move_history_text.insert(
                END, "\n" + str(cusp_app.move_history_text_number) + ". " + action_str
            )

        else:
            cusp_app.move_history_text.insert( END, str(cusp_app.move_history_text_number) + ". " + action_str )

    elif action_str[0:2] == "CX":
        # print(f'action start with CX')
        cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
        cusp_app.move_history_text.insert(
            END, "\n" + str(cusp_app.move_history_text_number) + ". " + action_str
        )
    else:
        # black moves first in fight phase
        # or set up a board in board editor and black to move
        last_line = cusp_app.move_history_text.get("end-1c linestart", "end-1c lineend")
        if ("CX" in last_line) or len(cusp_app.move_history_text.get("1.0", END)) <= 1:
            cusp_app.move_history_text_number = cusp_app.move_history_text_number + 1
            cusp_app.move_history_text.insert(
                END,
                "\n" + str(cusp_app.move_history_text_number) + ". ... " + action_str,
            )
        else:
            cusp_app.move_history_text.insert(END, "  " + action_str)
    cusp_app.move_history_text.see("end")



def write_to_PGN(cusp_app, action_str):
    logger.info("write_to_PGN") 
    with open(cusp_app.PGN_save_path, "a", encoding="utf-8") as write_PGN:
        if cusp_app.board.turn:
            print("\n" + str(cusp_app.move_history_text_number) +
                  ". " + action_str, file=write_PGN, end=" ", )

        elif action_str[0:2] == "CX":
            print("\n" + str(cusp_app.move_history_text_number) +
                  ". " + action_str, file=write_PGN, end=" ", )

        else:
            last_line = ""
            with open(cusp_app.PGN_save_path, "r") as file:
                lines = [line.rstrip() for line in file]
                for line in lines:
                    last_line = line
            if ("CX" in last_line) or cusp_app.PGN_header == False:
                print(
                    "\n"
                    + str(cusp_app.move_history_text_number)
                    + ". ... "
                    + action_str,
                    file=write_PGN,
                    end=" ",
                )
            else:
                print(" " + action_str, file=write_PGN, end=" ")
    cusp_app.PGN_header = True

def check_pgn_game_variant(cusp_app):
    logger.info("check_pgn_game_variant")
    if cusp_app.reload_PGN:
        return
    if not cusp_app.PGN_file_path:
        return
    if not cusp_app.pgn_auto_game_variant_detection: return
    cusp_app.chess_game_variant_mode_value.set(1)    
    with open(cusp_app.PGN_file_path) as file:
        lines = [line.rstrip() for line in file]
        for line in lines:        
            if 'Cusp Xiangqi' in line:
                cusp_app.chess_game_variant_mode_value.set(2)
                break
    ui.setting_panel.chess_game_variant_mode_change(cusp_app) 
        


def load_PGN(cusp_app):
    logger.info("load_PGN") 
    if cusp_app.reload_PGN:
        cusp_app.reset()
        cusp_app.reload_PGN = True
    else:
        cusp_app.reset()
        
    if not cusp_app.reload_PGN:
        cusp_app.PGN_file_path = filedialog.askopenfilename( filetypes=[("PGN files", "*.PGN"), ("All files", "*.*")] )
    if not cusp_app.PGN_file_path:
        return
    check_pgn_game_variant(cusp_app)

    cusp_app.pgn_movestack = []
    cusp_app.pgn_fen_history_stack = []
    cusp_app.pgn_move_history_stack = []
    cusp_app.game_player_mode = "HvH"
    try:
        with open(cusp_app.PGN_file_path,"r", encoding="utf-8") as file:
            lines = [line.rstrip() for line in file]
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.exception("PGN file read error")
        messagebox.showerror("PGN Error", f"Could not open file: {e}")
        return None      
    try:    
        check_pgn(cusp_app,lines )    
    except ValueError as e:   # bad syntax, wrong format
        logger.exception("PGN parse error")
        messagebox.showerror("PGN Error", f"Invalid PGN format: {e}")
        return None
    except Exception as e:    # fallback catch-all
        logger.exception("Unexpected PGN parse error")
        messagebox.showerror("PGN Error", f"Unexpected error: {e}")
        return None
        
    # reset board
    cusp_app.board = cchess.Board()
    ui.ui_utils.update_color_to_move_label(cusp_app)
    # create two fake player
    cusp_app.engine_one = "cusp_app_engine1"
    cusp_app.engine_two = "cusp_app_engine2"
    cusp_app.player_swap_side = False
    cusp_app.player_one_timer_label.config(text="       ")
    cusp_app.player_two_timer_label.config(text="       ")
    ui.ui_utils.initialize_piece_images(cusp_app, cusp_app.chess_game_variant_mode)

def check_pgn(cusp_app,lines): 
    for line in lines:
        if "Red" in line:
            player_one_string = line.split('"')[1]
            player_one_string = player_one_string.split('"')[0]
            if len(player_one_string) > 40:
                player_one_string = player_one_string[:40]
            cusp_app.player_one_name = player_one_string

        if "Black" in line:
            player_two_string = line.split('"')[1]
            player_two_string = player_two_string.split('"')[0]
            if len(player_two_string) > 40:
                player_two_string = player_two_string[:40]
            cusp_app.player_two_name = player_two_string

        if line[0:1].isdigit():
            if "CX" not in line and "..."  not in line and "result"  not in line:
                split_line = line.split("  ")
                if len(split_line) == 2:
                    move_and_score = split_line[0].split(". ")[1]
                    move = move_and_score.split(" ")[0]
                    if len(regex.findall(r"\p{Han}+", move)) > 0:
                        cusp_app.board.push_notation(move)
                    else:
                        cusp_app.board.push_uci(move)
                    cusp_app.pgn_movestack.append(move_and_score)

                    move_and_score = split_line[1]
                    move = move_and_score.split(" ")[0]

                    if len(regex.findall(r"\p{Han}+", move)) > 0:
                        cusp_app.board.push_notation(move)
                    else:
                        cusp_app.board.push_uci(move)
                    cusp_app.pgn_movestack.append(move_and_score)

                else:
                    move_and_score = split_line[0].split(". ")[1]
                    move = move_and_score.split(" ")[0]

                    if len(regex.findall(r"\p{Han}+", move)) > 0:
                        cusp_app.board.push_notation(move)
                    else:
                        cusp_app.board.push_uci(move)
                    cusp_app.pgn_movestack.append(move_and_score)

            elif "..." in line:
                split_line = line.split(".. ")
                if len(split_line) == 2:
                    move_and_score = split_line[1]
                    move = move_and_score.split(" ")[0]
                    if len(regex.findall(r"\p{Han}+", move)) > 0:
                        cusp_app.board.push_notation(move)
                    else:
                        cusp_app.board.push_uci(move)
                    cusp_app.pgn_movestack.append(move_and_score)

            elif (
                "CX" in line and len(line.split("}")[0].split("{")[1]) > 8
            ):  # long CX string, without score, minimum length
                move_and_score = line.split(". ")[1]
                move_and_score_split = move_and_score.split(" ")

                move_part = move_and_score_split[2]

                if move_part == "none" or ( len(move_part) == 4 and move_part[0:2] == move_part[2:] ):
                    pass
                elif len(move_part) == 4 and move_part[2:] == "xx":
                    cchessboard_index = cchess.parse_square(move_part[0:2])
                    cusp_app.board.remove_piece_at(cchessboard_index)

                else:
                    try:
                        if len(regex.findall(r"\p{Han}+", move_part)) > 0:
                            uci_move = cusp_app.board.push_notation(move_part)
                        else:
                            uci_move = cusp_app.board.push_uci(move_part)
                    # print('push sucess')
                    except Exception as e:
                        logger.exception("Cusp chess PGN, check PGN, one free move, push error")

                        move_start_index = cchess.parse_square(move_part[0:2])
                        move_end_index = cchess.parse_square(move_part[2:4])
                        piece = cusp_app.board.piece_at(move_start_index)
                        cusp_app.board.remove_piece_at(move_start_index)

                        if len(move_part) == 4:
                            cusp_app.board.set_piece_at(move_end_index, piece)

                # print(move_and_score_split[3])
                # when set up a Cusp Position, play can set board turn
                if move_and_score_split[3][2] == "R":
                    cusp_app.board.turn = True
                elif move_and_score_split[3][2] == "B":
                    cusp_app.board.turn = False
                cusp_app.pgn_movestack.append(move_and_score)
            else:
                move_and_score = line.split(". ")[1]
                cusp_app.pgn_movestack.append(move_and_score)
                        

def play_PGN_next(cusp_app):
    logger.info("play_PGN_next")
    cusp_app.arrow_start_index = ""
    cusp_app.arrow_end_index = ""

    ui.ui_utils.clear_board_move_history(cusp_app)
    CX_passive = False
    cusp_app.game_in_progress = True
    if cusp_app.pgn_movestack:
        move_and_score = cusp_app.pgn_movestack.pop(0)
        cusp_app.pgn_fen_history_stack.append(cusp_app.board.fen())
        cusp_app.pgn_move_history_stack.append(move_and_score)
        try:
            if cusp_app.board.turn:
                cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                # file is not empty
                if len(cusp_app.move_history_text.get("1.0", END)) > 1:
                    cusp_app.move_history_text.insert(
                        END,
                        "\n"
                        + str(cusp_app.move_history_text_number)
                        + ". "
                        + move_and_score,
                    )
                else:
                    cusp_app.move_history_text.insert( END, str(cusp_app.move_history_text_number) + ". " + move_and_score, )

            elif "CX" in move_and_score or 'result' in move_and_score :
                cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                cusp_app.move_history_text.insert(
                    END,
                    "\n"
                    + str(cusp_app.move_history_text_number)
                    + ". "
                    + move_and_score,
                )
            else:
                # black moves first in fight phase
                # or set up a board in board editor and black to move
                last_line = cusp_app.move_history_text.get( "end-1c linestart", "end-1c lineend" )
                if ( "CX" in last_line or len(cusp_app.move_history_text.get("1.0", END)) <= 1 ):
                    cusp_app.move_history_text_number = ( cusp_app.move_history_text_number + 1 )
                    cusp_app.move_history_text.insert(
                        END,
                        "\n"
                        + str(cusp_app.move_history_text_number)
                        + ". ... "
                        + move_and_score,
                    )
                else:
                    cusp_app.move_history_text.insert(END, "  " + move_and_score)
            cusp_app.move_history_text.see("end")

            # print(move_and_score)
            if "CX" not in move_and_score and  "result" not in move_and_score:
                move_and_score_split = move_and_score.split(" ")
                move = move_and_score_split[0]

                # update eval bar
                if len(move_and_score_split) > 1 and move_and_score_split[1] != "":
                    score = float(move_and_score_split[1][1:-1])

                    if cusp_app.board.turn:
                        if not cusp_app.player_swap_side:
                            cusp_app.engine = cusp_app.engine_one
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, score)
                        else:
                            cusp_app.engine = cusp_app.engine_two
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                    else:
                        if cusp_app.player_swap_side:
                            cusp_app.engine = cusp_app.engine_one
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                        else:
                            cusp_app.engine = cusp_app.engine_two
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, score)

                if len(regex.findall(r"\p{Han}+", move)) > 0:
                    uci_move = cusp_app.board.push_notation(move)
                else:
                    uci_move = cusp_app.board.push_uci(move)

                uci_move = str(uci_move)

                move_start_index = cchess.parse_square(uci_move[0:2])
                move_end_index = cchess.parse_square(uci_move[2:4])
                cusp_app.arrow_start_index = move_start_index
                cusp_app.arrow_end_index = move_end_index

            elif ( "CX" in move_and_score and len(move_and_score.split("}")[0].split("{")[1]) > 8 ):
                # a player set up a Cusp Position, long CX string, without score, minimum length

                cusp_app.cusp_chess_phase = "Decision"
                move_and_score_split = move_and_score.split(" ")

                move_part = move_and_score_split[2]

                # CX {RS e0e1 BWBN} {0.91} or CX {BC none BWBN} {1.15}
                # if a player choose a Color directly, he/she can only choose the color-must-win
                if ( move_and_score_split[1][2] == "C" and move_and_score_split[1][1] != move_and_score_split[3][0] ):
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
                if move_and_score_split[3][0] == "R":
                    cusp_app.color_must_win_in_cusp_chess = "W"
                elif move_and_score_split[3][0] == "B":
                    cusp_app.color_must_win_in_cusp_chess = "B"

                # print(f'move_and_score_split[1][1] {move_and_score_split[1][1]}')
                if move_and_score_split[1][1] == "R":
                    cusp_app.engine = cusp_app.engine_one
                    cusp_app.active_color_in_cusp_setup = "W"
                elif move_and_score_split[1][1] == "B":
                    cusp_app.engine = cusp_app.engine_two
                    cusp_app.active_color_in_cusp_setup = "B"
                # update eval bar
                if move_and_score.count("}") == 2:
                    # print(move_and_score_split[4][1:-1])

                    score = float(move_and_score_split[4][1:-1])
                    # choose a color directly
                    if move_and_score_split[1][2] == "C":
                        cusp_app.cusp_chess_phase = "Fight"
                        cusp_app.choose_color_directly = True
                        if move_and_score_split[1][1] == "R":
                            cusp_app.active_color_in_cusp_setup = "W"
                            cusp_app.player_one_value_on_the_cusp = score
                            cusp_app.player_one_score_on_the_cusp_set = True
                        elif move_and_score_split[1][1] == "B":
                            cusp_app.active_color_in_cusp_setup = "B"
                            cusp_app.player_two_value_on_the_cusp = score
                            cusp_app.player_two_score_on_the_cusp_set = True
                        ui.ui_utils.update_two_player_scores_bar(cusp_app, score)
                    elif move_and_score_split[1][2] == "S":
                        cusp_app.cusp_chess_phase = "Decision"
                        # player one set up a Cusp Position
                        if move_and_score_split[1][1] == "R":
                            # Red to move
                            if move_and_score_split[3][2] == "R":
                                cusp_app.player_one_value_on_the_cusp = score
                                cusp_app.player_one_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar(cusp_app, score)
                            # black to move
                            elif move_and_score_split[3][2] == "B":
                                cusp_app.player_one_value_on_the_cusp = -score
                                cusp_app.player_one_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                        # player two set up a Cusp Position
                        elif move_and_score_split[1][1] == "B":
                            if move_and_score_split[3][2] == "R":
                                cusp_app.player_two_value_on_the_cusp = -score
                                cusp_app.player_two_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                            elif move_and_score_split[3][2] == "B":
                                cusp_app.player_two_value_on_the_cusp = score
                                cusp_app.player_two_score_on_the_cusp_set = True
                                ui.ui_utils.update_two_player_scores_bar(cusp_app, score)

                # no move, move_part[0:2]==move_part[2:] is possible, when engine search a cusp FEN
                if move_part == "none" or move_part[0:2] == move_part[2:]:
                    cusp_app.arrow_start_index = -1
                    cusp_app.arrow_end_index = -1
                # remove one piece to set up a Cusp Position
                elif len(move_part) == 4 and move_part[2:] == "xx":
                    cchessboard_index = cchess.parse_square(move_part[0:2])
                    cusp_app.board.remove_piece_at(cchessboard_index)

                    cusp_app.arrow_start_index = cchessboard_index
                    cusp_app.arrow_end_index = -1

                else:
                    try:
                        # if it is a legal move
                        if len(regex.findall(r"\p{Han}+", move_part)) > 0:
                            uci_move = cusp_app.board.push_notation(move_part)

                        else:
                            uci_move = cusp_app.board.push_uci(move_part)
                        uci_move = str(uci_move)
                        move_start_index = cchess.parse_square(uci_move[0:2])
                        move_end_index = cchess.parse_square(uci_move[2:4])

                    except Exception as e:
                        # one free move
                        logger.exception("Cusp chess PGN, one free move, push error")

                        move_start_index = cchess.parse_square(move_part[0:2])
                        move_end_index = cchess.parse_square(move_part[2:4])
                        piece = cusp_app.board.piece_at(move_start_index)
                        cusp_app.board.remove_piece_at(move_start_index)

                        cusp_app.board.set_piece_at(move_end_index, piece)

                    cusp_app.arrow_start_index = move_start_index
                    cusp_app.arrow_end_index = move_end_index

                if move_and_score_split[3][2] == "R":
                    cusp_app.board.turn = True
                elif move_and_score_split[3][2] == "B":
                    cusp_app.board.turn = False
                # CX_move=True
                # ui.ui_utils.update_game_status_label(cusp_app)
                cusp_app.update()

            # CX passive side action
            elif "CX" in move_and_score:
                cusp_app.cusp_chess_phase = "Fight"
                move_and_score_split = move_and_score.split(" ")
                if move_and_score[6] == "R":
                    cusp_app.color_chosen_in_setup_phase = "W"
                elif move_and_score[6] == "B":
                    cusp_app.color_chosen_in_setup_phase = "B"
                if move_and_score[4] != move_and_score[6]:
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
                if ( len(move_and_score.split("}")) > 1 and move_and_score.split("}")[1] != "" ):
                    score = float(move_and_score_split[2][1:-1])

                    if cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.engine = cusp_app.engine_two
                    elif cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.engine = cusp_app.engine_one

                    if cusp_app.board.turn:
                        if cusp_app.engine == cusp_app.engine_one:
                            cusp_app.player_one_value_on_the_cusp = score
                            cusp_app.player_one_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, score)
                        else:
                            cusp_app.player_two_value_on_the_cusp = -score
                            cusp_app.player_two_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                    else:
                        if cusp_app.engine == cusp_app.engine_two:
                            cusp_app.player_two_value_on_the_cusp = score
                            cusp_app.player_two_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, score)
                        else:
                            cusp_app.player_one_value_on_the_cusp = -score
                            cusp_app.player_one_score_on_the_cusp_set = True
                            ui.ui_utils.update_two_player_scores_bar(cusp_app, -score)
                CX_passive = True
            # game result
            elif "result" in move_and_score:
                cusp_app.game_in_progress = False
                if ( "adjudicator" not in move_and_score and "time out" not in move_and_score ):
                    PGN_result = move_and_score.split(" ")[1][1:-1]
                    cusp_app.game_result = PGN_result
                else:
                    PGN_result = move_and_score.split(" ")[3][0:-1]
                    cusp_app.game_result = PGN_result
                utils.game_results.show_game_result(cusp_app)
                return       
        except ValueError as e:   # bad syntax, wrong format
            logger.exception("PGN parse error")
            messagebox.showerror("CX PGN Error", f"Invalid PGN format: {e}")
            return None
        except Exception as e:    # fallback catch-all
            logger.exception("Unexpected PGN parse error")
            messagebox.showerror("CX PGN Error", f"Unexpected error: {e}")
            return None

        if CX_passive:
            cusp_app.after( 100, lambda: ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.old_arrow_start_index, cusp_app.old_arrow_end_index, ), )
        else:                
            piece = cusp_app.board.piece_at(cusp_app.arrow_end_index)
            ui.ui_utils.animate_piece_move( cusp_app, piece, cusp_app.arrow_start_index, cusp_app.arrow_end_index, )

            cusp_app.old_arrow_start_index = cusp_app.arrow_start_index
            cusp_app.old_arrow_end_index = cusp_app.arrow_end_index
        # time.sleep(0.05)
        ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
        cusp_app.update()

def play_PGN_previous(cusp_app):
    logger.info("play_PGN_previous")
    if cusp_app.pgn_move_history_stack:
        move_and_score = cusp_app.pgn_move_history_stack.pop()
        cusp_app.pgn_movestack.insert(0, move_and_score)
        board_fen = cusp_app.pgn_fen_history_stack.pop()
        cusp_app.board.set_fen(board_fen)
    cusp_app.move_history_text.delete("end-1l linestart", "end")
    ui.ui_utils.clear_board_move_history(cusp_app)
    ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)


def PGN_back_to_beginning(cusp_app):
    logger.info("PGN_back_to_beginning")
    try:
        cusp_app.reload_PGN = True
        load_PGN(cusp_app)
        cusp_app.reload_PGN = False
    except Exception as e:
        cusp_app.reload_PGN = False
        logger.exception("PGN_back_to_beginning error")
        messagebox.showerror("Error", f"Reload PGN error: {e}" )

def initialize_auto_play_PGN_button_text(cusp_app):
    logger.info("initialize_auto_play_PGN_button_text")
    if cusp_app.auto_play_PGN == False:
        cusp_app.pgn_auto_play_label_state='stop_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)

    else:
        cusp_app.pgn_auto_play_label_state='auto_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)



def auto_play_PGN_function(cusp_app):
    logger.info("auto_play_PGN_function")
    if cusp_app.auto_play_PGN:
        cusp_app.auto_play_PGN = False
        cusp_app.pgn_auto_play_label_state='stop_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)

        play_PGN(cusp_app)
    else:
        cusp_app.auto_play_PGN = True
        cusp_app.pgn_auto_play_label_state='auto_play_PGN_button'
        ui.language.update_widget(cusp_app,cusp_app.auto_play_PGN_button)



def play_PGN(cusp_app):
    logger.info("play_PGN")
    if not cusp_app.auto_play_PGN:
        if cusp_app.pgn_movestack:
            play_PGN_next(cusp_app)
            cusp_app.after(1500, lambda: play_PGN(cusp_app))
            # time.sleep(1.5)
        else:
            cusp_app.auto_play_PGN = True
            initialize_auto_play_PGN_button_text(cusp_app)