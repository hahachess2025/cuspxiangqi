import datetime
import logging
import math
import time
from tkinter import *
from tkinter import messagebox

import cchess
from PIL import Image as PILImage
from PIL import ImageDraw, ImageTk

import ai.ChessEngine
import ai.stop_threads
import ui.editor
import utils.config
import utils.game_results
import utils.game_state
import utils.pgnhistory as pgnhistory

logger = logging.getLogger(__name__)




def widget_initialization(cusp_app):
    logger.info("widget_initialization")
    clear_scrolltext_move_history(cusp_app)
    update_player_board_label(cusp_app)
    clear_board_move_history(cusp_app)

    cusp_app.Human_setup_confirmation_checkbox_var.set(0)


def draw_pieces(cusp_app, chess_board_variant, sound_play=True):
    logger.info("draw_pieces")
    if chess_board_variant == "Editor":
        canvas = cusp_app.editor_board_canvas
        canvas_size = cusp_app.editor_canvas_size
        piece_id=cusp_app.editor_img
    elif chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        piece_id=cusp_app.img
    if chess_board_variant != "Editor":
        update_player_board_label(cusp_app)
        update_game_status_label(cusp_app)
        update_color_to_move_label(cusp_app)
        # When players swap sides, we just rotate the board
        if cusp_app.rotate_board:
            if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
                img = PILImage.open("assets/xiangqiboardRotated.png")
                img = img.resize( (canvas_size, int(canvas_size * 10 / 9)), PILImage.Resampling.LANCZOS, )
            boardImg = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(0, 0, image=boardImg, anchor=NW)
            cusp_app.boardImg = boardImg

            if cusp_app.blindfold_mode:
                img = PILImage.open("assets/xiangqiboardRotatedBig.png")
                img = img.resize( ( cusp_app.blindfold_canvas_size, int(cusp_app.blindfold_canvas_size * 10 / 9), ), PILImage.Resampling.LANCZOS, )
                boardImg = ImageTk.PhotoImage(img)
                cusp_app.blindfold_board_canvas.delete("all")
                cusp_app.blindfold_board_canvas.create_image( 0, 0, image=boardImg, anchor=NW )
                cusp_app.blindfold_boardImg = boardImg
            cusp_app.rotate_board = False

    count = 0
    for i in range(90):
        piece = str(cusp_app.board.piece_at(i))
        if piece:
            if chess_board_variant == "Editor":
                piece_draw_x = (i % 9) * (canvas_size / 9)
                piece_draw_y = (10 - i // 9) * (canvas_size / 9)
            elif chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
                if not cusp_app.flip_board_enable:
                    piece_draw_x = (i % 9) * (canvas_size / 9)
                    piece_draw_y = (9 - i // 9) * (canvas_size / 9)
                else:
                    piece_draw_x = (8 - i % 9) * (canvas_size / 9)
                    piece_draw_y = (i // 9) * (canvas_size / 9)

            piece_img = ""

            if piece == "R":
                piece_img = "assets/Pieces/rr.png"
            if piece == "N":
                piece_img = "assets/Pieces/rn.png"
            if piece == "B":
                piece_img = "assets/Pieces/rb.png"
            if piece == "A":
                piece_img = "assets/Pieces/ra.png"
            if piece == "K":
                piece_img = "assets/Pieces/rk.png"
            if piece == "P":
                piece_img = "assets/Pieces/rp.png"
            if piece == "C":
                piece_img = "assets/Pieces/rc.png"

            if piece == "r":
                piece_img = "assets/Pieces/br.png"
            if piece == "n":
                piece_img = "assets/Pieces/bn.png"
            if piece == "b":
                piece_img = "assets/Pieces/bb.png"
            if piece == "a":
                piece_img = "assets/Pieces/ba.png"
            if piece == "k":
                piece_img = "assets/Pieces/bk.png"
            if piece == "p":
                piece_img = "assets/Pieces/bp.png"
            if piece == "c":
                piece_img = "assets/Pieces/bc.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 9), int(canvas_size / 9)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
        else:
            piece_id[count] = None
        count = count + 1

    if chess_board_variant == "Editor" :
        if chess_board_variant == "Editor":
            extra_pieces = 7
        else:
            extra_pieces = 6
            check_all_pieces_on_board(cusp_app, cusp_app.board)

        for i in range(extra_pieces):
            piece = ""
            piece_draw_x = (i + 1) * (canvas_size / 9)
            piece_draw_y = 11 * (canvas_size / 9)
            if i == 0:
                if ( chess_board_variant == "Editor" or "R" in cusp_app.board_dict_all_available ):
                    piece = "R"
            elif i == 1:
                if ( chess_board_variant == "Editor" or "N" in cusp_app.board_dict_all_available ):
                    piece = "N"
            elif i == 2:
                if ( chess_board_variant == "Editor" or "B" in cusp_app.board_dict_all_available ):
                    piece = "B"
            elif i == 3:
                if ( chess_board_variant == "Editor" or "A" in cusp_app.board_dict_all_available ):
                    piece = "A"
            elif i == 4:
                if ( chess_board_variant == "Editor" or "C" in cusp_app.board_dict_all_available ):
                    piece = "C"
            elif i == 5:
                if ( chess_board_variant == "Editor" or "P" in cusp_app.board_dict_all_available ):
                    piece = "P"
            elif i == 6:
                if chess_board_variant == "Editor":
                    piece = "K"
            piece_img = ""
            if piece == "R":
                piece_img = "assets/Pieces/rr.png"
            if piece == "N":
                piece_img = "assets/Pieces/rn.png"
            if piece == "B":
                piece_img = "assets/Pieces/rb.png"
            if piece == "A":
                piece_img = "assets/Pieces/ra.png"
            if piece == "K":
                piece_img = "assets/Pieces/rk.png"
            if piece == "P":
                piece_img = "assets/Pieces/rp.png"
            if piece == "C":
                piece_img = "assets/Pieces/rc.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 9), int(canvas_size / 9)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
            count = count + 1
        for i in range(extra_pieces):
            piece = ""
            piece_draw_x = (i + 1) * (canvas_size / 9)
            piece_draw_y = 0
            if i == 0:
                if ( chess_board_variant == "Editor" or "r" in cusp_app.board_dict_all_available ):
                    piece = "r"
            elif i == 1:
                if ( chess_board_variant == "Editor" or "n" in cusp_app.board_dict_all_available ):
                    piece = "n"
            elif i == 2:
                if ( chess_board_variant == "Editor" or "b" in cusp_app.board_dict_all_available ):
                    piece = "b"
            elif i == 3:
                if ( chess_board_variant == "Editor" or "a" in cusp_app.board_dict_all_available ):
                    piece = "a"
            elif i == 4:
                if ( chess_board_variant == "Editor" or "c" in cusp_app.board_dict_all_available ):
                    piece = "c"
            elif i == 5:
                if ( chess_board_variant == "Editor" or "p" in cusp_app.board_dict_all_available ):
                    piece = "p"
            elif i == 6:
                if chess_board_variant == "Editor":
                    piece = "k"
            piece_img = ""
            if piece == "r":
                piece_img = "assets/Pieces/br.png"
            if piece == "n":
                piece_img = "assets/Pieces/bn.png"
            if piece == "b":
                piece_img = "assets/Pieces/bb.png"
            if piece == "a":
                piece_img = "assets/Pieces/ba.png"
            if piece == "k":
                piece_img = "assets/Pieces/bk.png"
            if piece == "p":
                piece_img = "assets/Pieces/bp.png"
            if piece == "c":
                piece_img = "assets/Pieces/bc.png"

            if piece_img != "":
                img = PILImage.open(piece_img)
                img = img.resize( (int(canvas_size / 9), int(canvas_size / 9)), PILImage.Resampling.LANCZOS, )
                img_piece = ImageTk.PhotoImage(img)
                canvas.create_image( piece_draw_x, piece_draw_y, image=img_piece, anchor=NW )
                piece_id[count] = img_piece
            else:
                piece_id[count] = None
            count = count + 1
    while count < 108:
        piece_id[count] = None
        count = count + 1

    if cusp_app.play_sound_enable and cusp_app.game_in_progress and sound_play:
        cusp_app.move_sound.play()

    cusp_app.update()


# draw a arrow when dragging mouse
def left_button_motion(cusp_app, event, chess_board_variant):
    logger.info("left_button_motion")
    if cusp_app.mouse_drag == False:
        return

    mouse_x, mouse_y = event.x, event.y

    if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        if ( canvas_size < mouse_x or mouse_x < 0 or mouse_y > canvas_size * 10 / 9 or mouse_y < 0 ):
            return
    elif chess_board_variant == "Blindfold":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size
        if ( cusp_app.blindfold_canvas_size < mouse_x or mouse_x < 0 or mouse_y > cusp_app.blindfold_canvas_size * 10 / 9 or mouse_y < 0 ):
            return
        size_ratio = canvas_size / cusp_app.blindfold_canvas_size
        mouse_x = size_ratio * mouse_x
        mouse_y = size_ratio * mouse_y

    SQUARE_SIZE = int(canvas_size / 9)
    if cusp_app.selected_piece:
        canvas.delete("drag_piece")
        if str(cusp_app.selected_piece).isupper():
            color = "r"
        else:
            color = "b"
        kind = str(cusp_app.selected_piece).lower()
        key = color + kind
        canvas.create_image( mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2, image=cusp_app.piece_images[key], anchor="nw", tags="drag_piece", )


# remove one piece to set up a Cusp Position in cusp chess
def right_click(cusp_app, event, chess_board_variant):
    logger.info("right_click")
    clear_board_move_history(cusp_app)
    if chess_board_variant != "Editor":
        if not cusp_app.game_in_progress:
            return

    if chess_board_variant == "CuspXiangqi":
        if not cusp_app.human_no_move_this_round:
            return
        canvas_size = cusp_app.canvas_size
    elif chess_board_variant == "Editor":
        ai.stop_threads.stop_editor_threads(cusp_app)
        canvas_size = cusp_app.editor_canvas_size
    elif chess_board_variant == "Blindfold":
        canvas_size = cusp_app.blindfold_canvas_size

    mouse_x, mouse_y = event.x, event.y
    canvas_x = mouse_x // int(canvas_size / 9)
    canvas_y = mouse_y // int(canvas_size / 9)

    chessboard_x = canvas_x

    if mouse_x > canvas_size or mouse_x < 0:
        return
    if chess_board_variant == "CuspXiangqi" or chess_board_variant == "Blindfold":
        if mouse_y < 0 or mouse_y > canvas_size * 10 / 9:
            return
        chessboard_y = 9 - canvas_y
    elif chess_board_variant == "Editor":
        if mouse_y < canvas_size / 9 or mouse_y > canvas_size * 11 / 9:
            return
        chessboard_y = 11 - canvas_y

    if chess_board_variant == "CuspXiangqi":
        chessboard_index = chessboard_x + chessboard_y * 9
        player_one_turn = cusp_app.board.turn
    elif chess_board_variant == "Editor":
        chessboard_index = chessboard_x + chessboard_y * 9 - 9
        player_one_turn = cusp_app.board.turn

    piece = cusp_app.board.piece_at(chessboard_index)
    if not piece:
        if chess_board_variant == "Blindfold":
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
        return

    if ( ( cusp_app.chess_game_variant_mode == "CuspXiangqi" ) and cusp_app.cusp_chess_phase == "SafeMove" and ( (cusp_app.player_one == "Human" and player_one_turn) or (cusp_app.player_two == "Human" and not player_one_turn) ) ) or chess_board_variant == "Editor":
        if chess_board_variant != "Editor":
            cusp_app.Human_must_set_up = True
            if chess_board_variant == "CuspXiangqi" or chess_board_variant == "Blindfold":
                draw_rectangle(cusp_app, canvas_x, canvas_y)
                cusp_app.human_no_move_this_round = False
                cusp_app.move_str = str(cchess.square_name(chessboard_index)) + "xx"
            cusp_app.board.remove_piece_at(chessboard_index)
            draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
        else:
            cusp_app.board.remove_piece_at(chessboard_index)
            draw_pieces(cusp_app, "Editor")
            ui.editor.editor_update_player_score_bar(cusp_app)


def draw_all_legal_moves_for_selected_piece( cusp_app, legal_moves, SQUARE_SIZE, RANKS, chess_board_variant ):
    logger.info("draw_all_legal_moves_for_selected_piece")
    if ( chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi" or chess_board_variant == "Blindfold" ):
        canvas = cusp_app.board_canvas

    for move in legal_moves:
        to_sq = move.to_square
        tf = to_sq % 9  # 0 = 'a', 4 = 'e'
        tr = to_sq // 9
        if cusp_app.flip_board_enable:
            tf = 8 - tf
            tr = 9 - tr
        canvas_x0 = tf * SQUARE_SIZE
        canvas_y0 = (RANKS - 1 - tr) * SQUARE_SIZE
        canvas_x1 = canvas_x0 + SQUARE_SIZE
        canvas_y1 = canvas_y0 + SQUARE_SIZE
        canvas.create_oval( canvas_x0 + SQUARE_SIZE // 4, canvas_y0 + SQUARE_SIZE // 4, canvas_x1 - SQUARE_SIZE // 4, canvas_y1 - SQUARE_SIZE // 4, fill="green", outline="", tags="highlight", )


def legal_moves_at(cusp_app, board: cchess.Board, square: cchess.Square):
    logger.info("legal_moves_at")

    moves = [move for move in board.legal_moves if move.from_square == square]

    return moves


# when setup-rule, both kings cannot meet each other
def two_kings_meet(cusp_app, move_start_index, move_end_index, new_board):
    logger.info("two_kings_meet")
    board = new_board.copy()
    piece = board.piece_at(move_start_index)
    board.remove_piece_at(move_start_index)
    board.set_piece_at(move_end_index, piece)

    if board.is_king_line_of_sight():
        return True

# whensetup-ruleto set up a Cusp Position, both kings are checked is
# not allowed.

def both_kings_checked(cusp_app, move_start_index, move_end_index, new_board):
    logger.info("both_kings_checked")
    board = new_board.copy()
    piece = board.piece_at(move_start_index)
    board.remove_piece_at(move_start_index)
    board.set_piece_at(move_end_index, piece)

    changed_turn_board = board.copy()
    changed_turn_board.turn = 1 ^ changed_turn_board.turn

    if board.is_check() and changed_turn_board.is_check():
        return True


def legal_moves_by_human(cusp_app, move, chess_board_variant):
    logger.info("legal_moves_by_human")
    if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
        canvas = cusp_app.board_canvas
        start_index = cusp_app.piece_move_start_square
        end_index = cusp_app.to_sq

    if cusp_app.move_str_legal:
        cusp_app.move_str = str(move)
        cusp_app.setting_up_in_cusp_chess = False
        pgnhistory.utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)

        cusp_app.board.push(move)
        draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
        draw_arrows_with_two_indexes(cusp_app, start_index, end_index)
        utils.game_results.check_game_result(cusp_app)

        cusp_app.update()



def update_color_to_move_label(cusp_app):
    logger.info("update_color_to_move_label")
    if cusp_app.cusp_chess_phase != "Decision":
        if cusp_app.board.turn:
            cusp_app.color_to_move_label_state = "White"  
        else:
            cusp_app.color_to_move_label_state = "Black" 
        ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
    else:
        if cusp_app.active_color_in_cusp_setup == "W":
            cusp_app.color_to_move_label_state = "Black"
            ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
        else:
            cusp_app.color_to_move_label_state = "White"
            ui.language.update_widget(cusp_app, cusp_app.color_to_move_label)
    if cusp_app.blindfold_mode:
        ui.language.update_widget(cusp_app, cusp_app.blindfold_color_to_move_label)


    cusp_app.update()



# at the top and bottom of the chess board
def update_player_board_label(cusp_app):
    logger.info("update_player_board_label")

    cusp_app.player_one_board_label.configure(image=cusp_app.play_one_logo)
    cusp_app.player_two_board_label.configure(image=cusp_app.play_two_logo)
    if ( cusp_app.chess_game_variant_mode == "Normal" or cusp_app.cusp_chess_phase == "SafeMove" ):
        cusp_app.player_one_label_state = "player_one_board_label_show_name"
        cusp_app.player_two_label_state = "player_two_board_label_show_name"
        
    elif ( cusp_app.cusp_chess_phase == "Decision" or cusp_app.cusp_chess_phase == "Fight" ):
        if not cusp_app.choose_color_directly:
            if cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_one_label_state = "player_one_board_label_setup"
                cusp_app.player_two_label_state = "player_two_board_label_passively_choose"
            elif cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_two_label_state = "player_two_board_label_setup"
                cusp_app.player_one_label_state = "player_one_board_label_passively_choose"
        else:
            if cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_one_label_state = "player_one_board_label_directly_choose"
                
            elif cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_two_label_state = "player_two_board_label_directly_choose"

    ui.language.update_widget(cusp_app, cusp_app.player_one_board_label) 
    ui.language.update_widget(cusp_app, cusp_app.player_two_board_label)
        
    if cusp_app.blindfold_mode:
        cusp_app.blindfold_player_one_board_label.configure( image=cusp_app.play_one_logo )
        cusp_app.blindfold_player_two_board_label.configure( image=cusp_app.play_two_logo )

        ui.language.update_widget(cusp_app, cusp_app.blindfold_player_one_board_label) 
        ui.language.update_widget(cusp_app, cusp_app.blindfold_player_two_board_label)
    cusp_app.update()


def update_game_status_label(cusp_app, RESET=False):
    logger.info("update_game_status_label")  

    if RESET:
        cusp_app.game_status_label.config(font=("Arial", 20))
        if cusp_app.chess_game_variant_mode == "CuspXiangqi":
            cusp_app.game_status_label_state = "game_status_label_ready_CC"
        else:
            cusp_app.game_status_label_state = "game_status_label_ready"
    
    elif cusp_app.game_in_progress:
        if cusp_app.chess_game_variant_mode == "CuspXiangqi":
            if cusp_app.Human_must_set_up:
                if cusp_app.board.turn:
                    cusp_app.game_status_label_player_name=cusp_app.player_one_name
                else:
                    cusp_app.game_status_label_player_name=cusp_app.player_two_name
                cusp_app.game_status_label_state = "game_status_label_player_must_setup"
            elif cusp_app.cusp_chess_phase == "SafeMove":
                cusp_app.game_status_label_state = "game_status_label_safe_CC"
            else:
                cusp_app.game_status_label_state = "game_status_label_player_must_win"
        else:
            cusp_app.game_status_label_state = "game_status_label_ready"

    else:
        utils.game_results.show_game_result(cusp_app)
    ui.language.update_widget(cusp_app, cusp_app.game_status_label)    
    cusp_app.update()



def update_two_player_scores_bar(cusp_app, score=0):
    logger.info("update_two_player_scores_bar")

    if cusp_app.flip_board_enable:
        score = -score
    # cusp value is the score of the fight starting position
    # when a player chooses a color directly, the opponent's cusp value is the previous score.
    # so we can see what the opponent missed.
    if cusp_app.choose_color_directly and cusp_app.set_cusp_value == False:
        if cusp_app.active_color_in_cusp_setup == "W":
            cusp_app.player_two_value_on_the_cusp = cusp_app.previous_move_score
            cusp_app.player_two_score_on_the_cusp_set = True
        elif cusp_app.active_color_in_cusp_setup == "B":
            cusp_app.player_one_value_on_the_cusp = cusp_app.previous_move_score
            cusp_app.player_one_score_on_the_cusp_set = True
        cusp_app.set_cusp_value = True
    cusp_app.previous_move_score = score

    if cusp_app.eval_show_enable:
        set_original_score = score
        if cusp_app.engine == cusp_app.engine_one:
            player_one_white_top = convert_score_to_eval_bar( cusp_app, -set_original_score, cusp_app.canvas_size )
            if not cusp_app.flip_board_enable:
                cusp_app.player_one_bar.create_rectangle(
                    0, 0, 20, player_one_white_top, fill="#000000", outline=""
                )
                cusp_app.player_one_bar.create_rectangle(
                    0,
                    player_one_white_top,
                    20,
                    int(cusp_app.canvas_size * 10 / 9),
                    fill="#FFFFFF",
                    outline="",
                )
            else:
                cusp_app.player_one_bar.create_rectangle(
                    0, 0, 20, player_one_white_top, fill="#FFFFFF", outline=""
                )
                cusp_app.player_one_bar.create_rectangle(
                    0,
                    player_one_white_top,
                    20,
                    int(cusp_app.canvas_size * 10 / 9),
                    fill="#000000",
                    outline="",
                )

        elif cusp_app.engine == cusp_app.engine_two:
            player_two_white_top = convert_score_to_eval_bar( cusp_app, set_original_score, cusp_app.canvas_size )

            if not cusp_app.flip_board_enable:
                cusp_app.player_two_bar.create_rectangle(
                    0, 0, 20, player_two_white_top, fill="#000000", outline=""
                )
                cusp_app.player_two_bar.create_rectangle(
                    0,
                    player_two_white_top,
                    20,
                    int(cusp_app.canvas_size * 10 / 9),
                    fill="#FFFFFF",
                    outline="",
                )
            else:
                cusp_app.player_two_bar.create_rectangle(
                    0, 0, 20, player_two_white_top, fill="#FFFFFF", outline=""
                )
                cusp_app.player_two_bar.create_rectangle(
                    0,
                    player_two_white_top,
                    20,
                    int(cusp_app.canvas_size * 10 / 9),
                    fill="#000000",
                    outline="",
                )

        # draw two marks for the two cusp value.
        if ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.cusp_chess_phase != "SafeMove" ):
            if cusp_app.engine == cusp_app.engine_one:
                if cusp_app.player_one_score_on_the_cusp_set:
                    mark_player_one_score = cusp_app.player_one_value_on_the_cusp
                    if cusp_app.flip_board_enable:
                        mark_player_one_score = -mark_player_one_score
                    mark_player_one_score = convert_score_to_eval_bar( cusp_app, -mark_player_one_score, cusp_app.canvas_size )

                    if cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.player_one_bar.create_rectangle(
                            0,
                            mark_player_one_score - 2,
                            20,
                            mark_player_one_score + 2,
                            fill="#EF0C0C",
                            outline="",
                        )
                    elif cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.player_one_bar.create_rectangle(
                            0,
                            mark_player_one_score - 2,
                            20,
                            mark_player_one_score + 2,
                            fill="#00FF00",
                            outline="",
                        )
            else:
                if cusp_app.player_two_score_on_the_cusp_set:
                    mark_player_two_score = cusp_app.player_two_value_on_the_cusp
                    if cusp_app.flip_board_enable:
                        mark_player_two_score = -mark_player_two_score
                    mark_player_two_score = convert_score_to_eval_bar( cusp_app, mark_player_two_score, cusp_app.canvas_size )
                    if cusp_app.active_color_in_cusp_setup == "B":
                        cusp_app.player_two_bar.create_rectangle(
                            0,
                            mark_player_two_score - 2,
                            20,
                            mark_player_two_score + 2,
                            fill="#EF0C0C",
                            outline="",
                        )
                    elif cusp_app.active_color_in_cusp_setup == "W":
                        cusp_app.player_two_bar.create_rectangle(
                            0,
                            mark_player_two_score - 2,
                            20,
                            mark_player_two_score + 2,
                            fill="#00FF00",
                            outline="",
                        )

    cusp_app.update()


def convert_score_to_eval_bar(cusp_app, score_to_be_converted, canvas_size):
    logger.info("convert_score_to_eval_bar")
    # Adjust maximum score based on pikafish output
    # if score equals to 0, the Red top mark is at the Xiangqi board center.
    # if score equals to 1, the mark is at fifth rank. critical area for Cusp cchess
    # if score equals to 2, the mark is at sixth rank
    # score maximum value is 10
    max_score = 10

    bar_length = canvas_size
    if 2 >= score_to_be_converted >= -2:
        eval_bar_mark = ( bar_length * 10 / 9 / 2 + bar_length / 9 * score_to_be_converted * 3 / 2 )
    elif (max_score > score_to_be_converted > 2) or ( -max_score < score_to_be_converted < -2 ):
        eval_bar_mark = ( bar_length / 2 + bar_length / 9 * 3 * math.copysign(1, score_to_be_converted) + math.copysign(1, score_to_be_converted) * (abs(score_to_be_converted) - 2) * (bar_length / 9) / 4 )
    else:
        eval_bar_mark = ( bar_length / 2 + math.copysign(1, score_to_be_converted) * bar_length * 10 / 9 / 2 )

    return eval_bar_mark


def reset_two_player_scores_bar(cusp_app):
    logger.info("reset_two_player_scores_bar")

    cusp_app.player_one_bar.delete("all")
    cusp_app.player_two_bar.delete("all")

    engine_one = cusp_app.engine_one
    engine_two = cusp_app.engine_two

    cusp_app.engine_one = "1"
    cusp_app.engine_two = "2"

    cusp_app.cusp_chess_phase = "SafeMove"

    cusp_app.engine = cusp_app.engine_one
    update_two_player_scores_bar(cusp_app, 0)

    cusp_app.engine = cusp_app.engine_two
    update_two_player_scores_bar(cusp_app, 0)

    cusp_app.engine_one = engine_one
    cusp_app.engine_two = engine_two


def initialize_piece_images(cusp_app, chess_variant):
    logger.info("initialize_piece_images")
    
    if chess_variant == "Normal" or chess_variant == "CuspXiangqi":
        canvas_size = cusp_app.canvas_size

    for color in ["r", "b"]:
        for kind in ["p", "r", "n", "b", "c", "a", "k"]:
            path = f"assets/Pieces/{color}{kind}.png"
            img = PILImage.open(path).resize( (int(canvas_size / 9), int(canvas_size / 9)), PILImage.Resampling.LANCZOS )
            cusp_app.piece_images[color + kind] = ImageTk.PhotoImage(img)
    

def animate_piece_move( cusp_app, piece, start_board_index, end_board_index, steps=10, delay=20 ):
    logger.info("animate_piece_move")
    
    if start_board_index == "":
        return
    if start_board_index == -1:
        return
    if start_board_index == end_board_index:
        return

    if end_board_index == -1:
        draw_arrows_with_two_indexes(cusp_app, start_board_index, end_board_index)

        return
    if not piece:
        return

    chessboard_move_start_x = start_board_index % 9
    chessboard_move_start_y = start_board_index // 9

    canvas_move_start_x = chessboard_move_start_x
    canvas_move_start_y = 9 - chessboard_move_start_y

    chessboard_move_end_x = end_board_index % 9
    chessboard_move_end_y = end_board_index // 9

    canvas_move_end_x = chessboard_move_end_x
    canvas_move_end_y = 9 - chessboard_move_end_y

    if not cusp_app.flip_board_enable:
        start_x = canvas_move_start_x * (cusp_app.canvas_size / 9)
        start_y = canvas_move_start_y * (cusp_app.canvas_size / 9)

        end_x = canvas_move_end_x * (cusp_app.canvas_size / 9)
        end_y = canvas_move_end_y * (cusp_app.canvas_size / 9)
    else:
        start_x = 8 * (cusp_app.canvas_size / 9) - ( canvas_move_start_x * (cusp_app.canvas_size / 9) )
        start_y = 9 * (cusp_app.canvas_size / 9) - ( canvas_move_start_y * (cusp_app.canvas_size / 9) )

        end_x = 8 * (cusp_app.canvas_size / 9) - ( canvas_move_end_x * (cusp_app.canvas_size / 9) )
        end_y = 9 * (cusp_app.canvas_size / 9) - ( canvas_move_end_y * (cusp_app.canvas_size / 9) )

    if str(piece).isupper():
        color = "r"
    else:
        color = "b"
    kind = str(piece).lower()
    key = color + kind

    piece_img = cusp_app.piece_images[key]
    piece_id = cusp_app.board_canvas.create_image( start_x, start_y, image=piece_img, anchor="nw" )

    animate_piece( cusp_app, piece_id, start_x, start_y, end_x, end_y, steps=10, delay=20 )
    cusp_app.after( steps * delay * 2, lambda: cusp_app.board_canvas.delete(piece_id) )

    cusp_app.after( steps * delay * 2, lambda: draw_arrows_with_two_indexes( cusp_app, start_board_index, end_board_index ), )


def draw_arrows_with_two_indexes(cusp_app, start_board_index, end_board_index):
    logger.info("draw_arrows_with_two_indexes")
    position_list = []
    position_list.append(start_board_index)
    position_list.append(end_board_index)
    draw_transparent_arrow(cusp_app, position_list, cusp_app.chess_game_variant_mode)


def animate_piece(cusp_app, piece_id, from_x, from_y, to_x, to_y, steps=10, delay=20):
    logger.info("animate_piece")
    dx = (to_x - from_x) / steps
    dy = (to_y - from_y) / steps

    def step(count=0):
        if count < steps:
            cusp_app.board_canvas.move(piece_id, dx, dy)
            cusp_app.board_canvas.after(delay, step, count + 1)

    step()


def draw_transparent_arrow( cusp_app, position_list, chess_board_variant, keep_others=False, arrow_color=(255, 255, 255), alpha=180, ): #79, 93, 107
    logger.info("draw_transparent_arrow") 
    if len(position_list) == 0 or (len(position_list) % 2 != 0):
        return

    if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
        canvas = cusp_app.board_canvas
        canvas_size = cusp_app.canvas_size

    for i in range(2):
        if cusp_app.transparent_arrows[i]:
            canvas.delete(cusp_app.transparent_arrows[i])

    for index in range(len(position_list) // 2):
        if position_list[index * 2] == position_list[index * 2 + 1]:
            continue
        if position_list[index * 2] == -1:
            continue

        start_board_index = position_list[index * 2]
        end_board_index = position_list[index * 2 + 1]

        chessboard_move_start_x = start_board_index % 9
        chessboard_move_start_y = start_board_index // 9

        canvas_move_start_x = chessboard_move_start_x
        canvas_move_start_y = 9 - chessboard_move_start_y

        if end_board_index == -1:
            draw_rectangle(cusp_app, canvas_move_start_x, canvas_move_start_y)
            return

        chessboard_move_end_x = end_board_index % 9
        chessboard_move_end_y = end_board_index // 9

        canvas_move_end_x = chessboard_move_end_x
        canvas_move_end_y = 9 - chessboard_move_end_y

        if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
            if not cusp_app.flip_board_enable:
                start_x = ( canvas_move_start_x * (canvas_size / 9) + (canvas_size / 9) / 2 )
                start_y = ( canvas_move_start_y * (canvas_size / 9) + (canvas_size / 9) / 2 )

                end_x = canvas_move_end_x * (canvas_size / 9) + (canvas_size / 9) / 2
                end_y = canvas_move_end_y * (canvas_size / 9) + (canvas_size / 9) / 2
            else:
                start_x = ( 9 * (canvas_size / 9) - (canvas_move_start_x * (canvas_size / 9)) - (canvas_size / 9) / 2 )
                start_y = ( 10 * (canvas_size / 9) - (canvas_move_start_y * (canvas_size / 9)) - (canvas_size / 9) / 2 )

                end_x = ( 9 * (canvas_size / 9) - (canvas_move_end_x * (canvas_size / 9)) - (canvas_size / 9) / 2 )
                end_y = ( 10 * (canvas_size / 9) - (canvas_move_end_y * (canvas_size / 9)) - (canvas_size / 9) / 2 )


        # --- compute direction vectors ---
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.hypot(dx, dy)
        if length < 1e-6:
            return None  # nothing to draw
        ux = dx / length
        uy = dy / length
        if cusp_app.cusp_chess_phase == "Decision":
            arrow_color = (255, 0, 0)

        if chess_board_variant == "Normal" or chess_board_variant == "CuspXiangqi":
            w, h = canvas_size, int(canvas_size * 10 / 9)
        
        img = PILImage.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.line( ( start_x, start_y, end_x - (canvas_size / 9) / 6 * ux, end_y - (canvas_size / 9) / 6 * uy, ), fill=arrow_color + (alpha,), width=8, )

        # Draw arrowhead (triangle)

        # perpendicular (unit)
        px = -uy
        py = ux

        # --- head / shaft sizing ---

        head_length = max(12, min(length * 0.25, 40))

        head_width = head_length * 0.6

        # base point of the head (where shaft ends)
        bx = end_x - ux * head_length
        by = end_y - uy * head_length

        # head corners (perpendicular offset from base)
        half_w = head_width / 2.0
        corner1 = (bx + px * half_w, by + py * half_w)
        corner2 = (bx - px * half_w, by - py * half_w)
        tip = (end_x, end_y)

        rgba = (arrow_color[0], arrow_color[1], arrow_color[2], int(alpha))
        draw.polygon([tip, corner1, corner2], fill=rgba)

        # Convert to Tk image and display
        arrow_img = ImageTk.PhotoImage(img)
        cusp_app.transparent_arrows[index] = canvas.create_image( 0, 0, image=arrow_img, anchor="nw" )
        cusp_app.arrow_img[index] = arrow_img
        # print('draw arrow')

        if cusp_app.blindfold_mode:
            if cusp_app.blindfold_arrow:
                cusp_app.blindfold_board_canvas.delete(cusp_app.blindfold_arrow)
            if cusp_app.blindfold_board_remove_piece_rectangle:
                cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )

            resize_img = img.resize( ( cusp_app.blindfold_canvas_size, int(cusp_app.blindfold_canvas_size * 10 / 9), ), PILImage.Resampling.LANCZOS, )
            arrow_img = ImageTk.PhotoImage(resize_img)
            cusp_app.blindfold_arrow = cusp_app.blindfold_board_canvas.create_image( 0, 0, image=arrow_img, anchor="nw" )
            cusp_app.arrow_img[1] = arrow_img

    # for a piece removed in cusp Xiangqi


def draw_rectangle(cusp_app, canvas_x, canvas_y):
    logger.info("draw_rectangle")

    if cusp_app.board_remove_piece_rectangle:
        cusp_app.board_canvas.delete(cusp_app.board_remove_piece_rectangle)

    if cusp_app.flip_board_enable:
        canvas_x = 8 - canvas_x
        canvas_y = 9 - canvas_y
    else:
        canvas_x = canvas_x
        canvas_y = canvas_y
    cusp_app.board_remove_piece_rectangle = cusp_app.board_canvas.create_rectangle(
        canvas_x * (cusp_app.canvas_size / 9),
        canvas_y * (cusp_app.canvas_size / 9),
        (canvas_x * (cusp_app.canvas_size / 9) + (cusp_app.canvas_size / 9)),
        (canvas_y * (cusp_app.canvas_size / 9) + (cusp_app.canvas_size / 9)),
        outline="#FF6666",
        width=6,
    )
    if cusp_app.blindfold_mode:
        if cusp_app.blindfold_arrow:
            cusp_app.blindfold_board_canvas.delete(cusp_app.blindfold_arrow)
        if cusp_app.blindfold_board_remove_piece_rectangle:
            cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )
        resize_coefficient = cusp_app.blindfold_canvas_size / cusp_app.canvas_size
        cusp_app.blindfold_board_remove_piece_rectangle = (
            cusp_app.blindfold_board_canvas.create_rectangle(
                resize_coefficient * canvas_x * (cusp_app.canvas_size / 9),
                resize_coefficient * canvas_y * (cusp_app.canvas_size / 9),
                (
                    resize_coefficient * canvas_x * (cusp_app.canvas_size / 9)
                    + (cusp_app.blindfold_canvas_size / 9)
                ),
                (
                    resize_coefficient * canvas_y * (cusp_app.canvas_size / 9)
                    + (cusp_app.blindfold_canvas_size / 9)
                ),
                outline="#FF0000",
                width=6,
            )
        )


def clear_board_move_history(cusp_app):
    logger.info("clear_board_move_history")
    
    if cusp_app.blindfold_arrow:
        cusp_app.blindfold_board_canvas.delete(cusp_app.blindfold_arrow)

    if cusp_app.board_remove_piece_rectangle:
        cusp_app.board_canvas.delete(cusp_app.board_remove_piece_rectangle)

    if cusp_app.blindfold_board_remove_piece_rectangle:
        cusp_app.blindfold_board_canvas.delete( cusp_app.blindfold_board_remove_piece_rectangle )
    cusp_app.update()


def clear_scrolltext_move_history(cusp_app):
    logger.info("clear_scrolltext_move_history")
    cusp_app.move_history_text.delete(1.0, END)


def generate_PGN_path(cusp_app):
    logger.info("generate_PGN_path")
    if cusp_app.chess_game_variant_mode == "Normal":
        cusp_app.PGN_save_path = ( cusp_app.PGN_folder_path + "/xiangqi_" + str(datetime.datetime.now()).replace(":", "") + ".pgn" )
    elif cusp_app.chess_game_variant_mode == "CuspXiangqi":
        cusp_app.PGN_save_path = ( cusp_app.PGN_folder_path + "/cusp_xiangqi_" + str(datetime.datetime.now()).replace(":", "") + ".pgn" )
    utils.config.save_setting_in_config_file(cusp_app)


def confirm_players(cusp_app):
    logger.info("confirm_players")
    if cusp_app.translations[cusp_app.current_lang]["AI"]== cusp_app.player_one_spinbox_var.get():
        cusp_app.player_one = "AI"
        cusp_app.player_one_spinbox_chosen=0
    else:
        cusp_app.player_one = "Human"
        cusp_app.player_one_spinbox_chosen=1
        
    if cusp_app.translations[cusp_app.current_lang]["AI"]== cusp_app.player_two_spinbox_var.get():
        cusp_app.player_two = "AI"
        cusp_app.player_two_spinbox_chosen=0
    else:
        cusp_app.player_two = "Human"
        cusp_app.player_two_spinbox_chosen=1

    logger.info( f"---now p1 is {cusp_app.player_one} and p2 is {cusp_app.player_two}")

    if cusp_app.player_one == "AI" and cusp_app.player_two == "AI":
        cusp_app.game_player_mode = "AvA"
        set_engine_one(cusp_app)
        set_engine_two(cusp_app)
    elif cusp_app.player_one == "AI" and cusp_app.player_two == "Human":
        cusp_app.game_player_mode = "AvH"
        set_engine_one(cusp_app)
    elif cusp_app.player_two == "AI" and cusp_app.player_one == "Human":
        cusp_app.game_player_mode = "HvA"
        set_engine_two(cusp_app)
    elif cusp_app.player_one == "Human" and cusp_app.player_two == "Human":
        cusp_app.game_player_mode = "HvH"

    if cusp_app.adjudicator_engine_enable and cusp_app.engine_adjudicator_path != "":
        setup_engine(cusp_app,'adjudicator_engine',cusp_app.engine_adjudicator_path)
    else:
        logger.info('no adjudicator_engine')
          
    set_player_names(cusp_app)             
    utils.config.save_setting_in_config_file(cusp_app)

def set_engine_one(cusp_app):
    logger.info('set_engine_one')
    if cusp_app.engine_one_path != "":
        setup_engine(cusp_app,'engine_one',cusp_app.engine_one_path)
        engine_one_path = cusp_app.engine_one_path
        if "/" in engine_one_path:
            engine_one_path = engine_one_path.split("/")[-1]   
        if len(engine_one_path) > 40:
            engine_one_path = engine_one_path[:40]
            if  " " in engine_one_path: 
                engine_one_path = engine_one_path.split(" ")[0]
            if  "-" in engine_one_path: 
                engine_one_path = engine_one_path.split("-")[0]
            if  "_" in engine_one_path: 
                engine_one_path = engine_one_path.split("_")[0]
        cusp_app.player_one_name_engine = engine_one_path   
    else:
        logger.info("please set engine one path in setting menu")
        return

def set_engine_two(cusp_app):
    logger.info('set_engine_two')
    if cusp_app.engine_two_path != "":
        setup_engine(cusp_app,'engine_two',cusp_app.engine_two_path) 
        engine_two_path = cusp_app.engine_two_path
        if "/" in engine_two_path:
            engine_two_path = engine_two_path.split("/")[-1]   
        if len(engine_two_path) > 40:
            engine_two_path = engine_two_path[:40]
            if  " " in engine_two_path: 
                engine_two_path = engine_two_path.split(" ")[0]
            if  "-" in engine_two_path: 
                engine_two_path = engine_two_path.split("-")[0]
            if  "_" in engine_two_path: 
                engine_two_path = engine_two_path.split("_")[0]
        cusp_app.player_two_name_engine = engine_two_path
    else:
        logger.info("please set engine two path in setting menu")
        return          
        
def set_player_names(cusp_app):
    logger.info('set_player_names')
    if cusp_app.player_one_name_input == '':
        if cusp_app.player_one == "Human":
            cusp_app.player_one_name = "Human player one"
        elif cusp_app.player_one == "AI":
            cusp_app.player_one_name = cusp_app.player_one_name_engine
    else:
        cusp_app.player_one_name = cusp_app.player_one_name_input

    if cusp_app.player_two_name_input == '':
        if cusp_app.player_two == "Human":
            cusp_app.player_two_name = "Human player two"
        elif cusp_app.player_two == "AI":
            cusp_app.player_two_name = cusp_app.player_two_name_engine
    else:
        cusp_app.player_two_name = cusp_app.player_two_name_input

                        
    
def setup_engine(cusp_app, engine_name,engine_path):
    logger.info('setup_engine')
    try:
        if engine_name=='engine_one':
            if cusp_app.engine_one:
                cusp_app.engine_one.quit()
            cusp_app.engine_one = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
        elif  engine_name=='engine_two':
            if cusp_app.engine_two:
                cusp_app.engine_two.quit()
            cusp_app.engine_two = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
        elif engine_name=='adjudicator_engine':
            if cusp_app.adjudicator_engine:
                cusp_app.adjudicator_engine.quit()    
            cusp_app.adjudicator_engine = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
            cusp_app.adjudicator_engine.engine.configure({"Hash": 512,"Threads": 1, })
            cusp_app.adjudicator_engine_last_time=time.time()            
        elif engine_name=='editor_engine':
            if cusp_app.editor_engine:
                cusp_app.editor_engine.quit()  
            cusp_app.editor_engine = ai.ChessEngine.ChessEngine( cusp_app, engine_path )
            cusp_app.editor_engine_exist = True
    except Exception as e:
        logger.exception(f'engine {engine_name} setup error')
        messagebox.showerror("Error", f"Engine setup error: {e}" )


def check_all_pieces_on_board(cusp_app, board):
    logger.info('check_all_pieces_on_board') 
    cusp_app.piece_map = board.piece_map()
    cusp_app.board_dict = {
        "p": 0,
        "P": 0,
        "a": 0,
        "A": 0,
        "b": 0,
        "B": 0,
        "n": 0,
        "N": 0,
        "c": 0,
        "C": 0,
        "r": 0,
        "R": 0,
        "k": 0,
        "K": 0,
    }
    cusp_app.board_dict_white_available = {
        "P": 5,
        "A": 2,
        "B": 2,
        "N": 2,
        "C": 2,
        "R": 2,
        "K": 1,
    }
    cusp_app.board_dict_black_available = {
        "p": 5,
        "a": 2,
        "b": 2,
        "n": 2,
        "c": 2,
        "r": 2,
        "k": 1,
    }
    cusp_app.board_dict_all_available = {
        "p": 5,
        "P": 5,
        "a": 2,
        "A": 2,
        "b": 2,
        "B": 2,
        "n": 2,
        "N": 2,
        "c": 2,
        "C": 2,
        "r": 2,
        "R": 2,
        "k": 1,
        "K": 1,
    }

    for index in cusp_app.piece_map:
        cusp_app.board_dict[str(cusp_app.piece_map[index])] += 1
        if str(cusp_app.piece_map[index]).isupper():
            cusp_app.board_dict_white_available[str(cusp_app.piece_map[index])] -= 1
        else:
            cusp_app.board_dict_black_available[str(cusp_app.piece_map[index])] -= 1
        cusp_app.board_dict_all_available[str(cusp_app.piece_map[index])] -= 1
        # no pawn promotion for placement and Cusp Position setup
        if cusp_app.board_dict_all_available[str(cusp_app.piece_map[index])] == 0:
            del cusp_app.board_dict_all_available[str(cusp_app.piece_map[index])]
            if str(cusp_app.piece_map[index]).isupper():
                del cusp_app.board_dict_white_available[str(cusp_app.piece_map[index])]
            else:
                del cusp_app.board_dict_black_available[str(cusp_app.piece_map[index])]


def count_major_pieces(cusp_app):
    logger.info('count_major_pieces') 
    board_map = cusp_app.board.piece_map()
    cusp_app.major_piece_count = 0
    for index in board_map:
        if ( str(board_map[index]) == "R" or str(board_map[index]) == "r" or str(board_map[index]) == "C" or str(board_map[index]) == "c" or str(board_map[index]) == "N" or str(board_map[index]) == "n" ):
            cusp_app.major_piece_count = cusp_app.major_piece_count + 1


def set_timer(cusp_app):
    logger.info('set_timer')
    cusp_app.player_one_remain_time = cusp_app.time_for_each_player
    cusp_app.player_two_remain_time = cusp_app.time_for_each_player
    cusp_app.player_one_new_time = cusp_app.time_for_each_player
    cusp_app.player_two_new_time = cusp_app.time_for_each_player
    initialize_player_time_label(cusp_app)

    cusp_app.start_time = time.time()
    update_timer(cusp_app)


def initialize_player_time_label(cusp_app):
    logger.info('initialize_player_time_label')
    timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.time_for_each_player // 60), int(cusp_app.time_for_each_player % 60), int((cusp_app.time_for_each_player - int(cusp_app.time_for_each_player)) * 100), )

    cusp_app.player_one_timer_label.config(text=timestr)
    cusp_app.player_two_timer_label.config(text=timestr)


def update_timer(cusp_app):
    if cusp_app.game_in_progress:
        if cusp_app.player_one_timer_on:
            cusp_app.player_two_remain_time = cusp_app.player_two_new_time
            cusp_app.player_one_new_time = cusp_app.player_one_remain_time - ( time.time() - cusp_app.start_time )
            if cusp_app.player_one_new_time <= 0:
                if cusp_app.player_swap_side == False:
                    cusp_app.time_out_result = "0-1"
                else:
                    cusp_app.time_out_result = "1-0"
                utils.game_results.check_game_result(cusp_app)
                cusp_app.player_one_new_time = 0
            timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.player_one_new_time // 60), int(cusp_app.player_one_new_time % 60), int( (cusp_app.player_one_new_time - int(cusp_app.player_one_new_time)) * 100 ), )

            update_timer_label(cusp_app, timestr)

            if cusp_app.cusp_chess_phase == "Decision":
                if cusp_app.active_color_in_cusp_setup == "W":
                    cusp_app.player_one_timer_on = False
                    cusp_app.start_time = time.time()
            else:
                if not cusp_app.player_swap_side:
                    if not cusp_app.board.turn:
                        cusp_app.player_one_timer_on = False
                        cusp_app.start_time = time.time()
                elif cusp_app.player_swap_side:
                    if cusp_app.board.turn:
                        cusp_app.player_one_timer_on = False
                        cusp_app.start_time = time.time()
        elif not cusp_app.player_one_timer_on:
            cusp_app.player_one_remain_time = cusp_app.player_one_new_time
            cusp_app.player_two_new_time = cusp_app.player_two_remain_time - ( time.time() - cusp_app.start_time )
            if cusp_app.player_two_new_time <= 0:
                if cusp_app.player_swap_side == False:
                    cusp_app.time_out_result = "1-0"
                else:
                    cusp_app.time_out_result = "0-1"
                utils.game_results.check_game_result(cusp_app)
                cusp_app.player_two_new_time = 0
            timestr = "{:02}:{:02}:{:02}".format( int(cusp_app.player_two_new_time // 60), int(cusp_app.player_two_new_time % 60), int( (cusp_app.player_two_new_time - int(cusp_app.player_two_new_time)) * 100 ), )
            update_timer_label(cusp_app, timestr)

            if cusp_app.cusp_chess_phase == "Decision":
                if cusp_app.active_color_in_cusp_setup == "B":
                    cusp_app.player_one_timer_on = True
                    cusp_app.start_time = time.time()
            else:
                if not cusp_app.player_swap_side:
                    if cusp_app.board.turn:
                        cusp_app.player_one_timer_on = True
                        cusp_app.start_time = time.time()
                else:
                    if not cusp_app.board.turn:
                        cusp_app.player_one_timer_on = True
                        cusp_app.start_time = time.time()


def update_timer_label(cusp_app, timestr):
    if cusp_app.player_one_timer_on:
        cusp_app.player_one_timer_label.config(text=timestr)
    else:
        cusp_app.player_two_timer_label.config(text=timestr)
    cusp_app.after(50, lambda: update_timer(cusp_app))

def generate_legal_positions_for_pieces(cusp_app):
    logger.info('generate_legal_positions_for_pieces')
    cusp_app.white_pawn_legal_positions = []
    cusp_app.black_pawn_legal_positions = []
    cusp_app.white_bishop__legal_positions = []
    cusp_app.black_bishop_legal_positions = []
    cusp_app.white_advisor_legal_positions = []
    cusp_app.black_advisor_legal_positions = []
    cusp_app.white_king_legal_positions = []
    cusp_app.black_king_legal_positions = []

    for cchessboard_index in range(90):
        # red pawn
        if ( cchessboard_index > 44 or cchessboard_index == 44 or cchessboard_index == 42 or cchessboard_index == 40 or cchessboard_index == 38 or cchessboard_index == 36 or cchessboard_index == 35 or cchessboard_index == 33 or cchessboard_index == 31 or cchessboard_index == 29 or cchessboard_index == 27 ):
            cusp_app.white_pawn_legal_positions.append(cchessboard_index)

        # black pawn
        if ( cchessboard_index < 45 or cchessboard_index == 45 or cchessboard_index == 47 or cchessboard_index == 49 or cchessboard_index == 51 or cchessboard_index == 53 or cchessboard_index == 54 or cchessboard_index == 56 or cchessboard_index == 58 or cchessboard_index == 60 or cchessboard_index == 62 ):
            cusp_app.black_pawn_legal_positions.append(cchessboard_index)
        # red guard
        if ( cchessboard_index == 3 or cchessboard_index == 5 or cchessboard_index == 13 or cchessboard_index == 21 or cchessboard_index == 23 ):
            cusp_app.white_advisor_legal_positions.append(cchessboard_index)

        # black guard
        if ( cchessboard_index == 84 or cchessboard_index == 86 or cchessboard_index == 76 or cchessboard_index == 66 or cchessboard_index == 68 ):
            cusp_app.black_advisor_legal_positions.append(cchessboard_index)

        # red bishop
        if ( cchessboard_index == 2 or cchessboard_index == 6 or cchessboard_index == 18 or cchessboard_index == 22 or cchessboard_index == 26 or cchessboard_index == 38 or cchessboard_index == 42 ):
            cusp_app.white_bishop__legal_positions.append(cchessboard_index)

        # black bishop
        if ( cchessboard_index == 83 or cchessboard_index == 63 or cchessboard_index == 47 or cchessboard_index == 67 or cchessboard_index == 87 or cchessboard_index == 71 or cchessboard_index == 51 ):
            cusp_app.black_bishop_legal_positions.append(cchessboard_index)

        # red king
        if ( 2 < cchessboard_index < 6 or 11 < cchessboard_index < 15 or 20 < cchessboard_index < 24 ):
            cusp_app.white_king_legal_positions.append(cchessboard_index)

        # black king
        if ( 83 < cchessboard_index < 87 or 74 < cchessboard_index < 78 or 65 < cchessboard_index < 69 ):
            cusp_app.black_king_legal_positions.append(cchessboard_index)