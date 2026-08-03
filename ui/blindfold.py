"""
it is a small trick to show your blindfold chess skill to your friends, or for streaming.

"""

import logging
from tkinter import *
from tkinter import ttk

import cchess
from PIL import Image as PILImage
from PIL import ImageTk

import ui.language
import ui.normalboard
import ui.ui_utils
import utils.config
import utils.game_results
import utils.pgnhistory

logger = logging.getLogger(__name__)

def create_blindfold_cchess_frame(cusp_app):
    logger.info("create_blindfold_chess_frame")
    cusp_app.blindfold_cchess_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.blindfold_cchess_frame.grid(column=1, row=0, rowspan=13, sticky="wens")

    cusp_app.blindfold_player_two_board_label = ttk.Label( cusp_app.blindfold_cchess_frame,  justify=LEFT, compound=LEFT, image=cusp_app.play_two_logo, font=("Times", 15), )
    ui.language.register_widget(cusp_app, cusp_app.blindfold_player_two_board_label, key=lambda:ui.language.player_two_label_dynamic_key(cusp_app), **ui.language.player_two_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_player_two_board_label.grid(column=0, row=0)
    cusp_app.blindfold_player_two_board_label.image = cusp_app.play_two_logo

    cusp_app.blindfold_player_one_board_label = ttk.Label( cusp_app.blindfold_cchess_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_one_logo, font=("Times", 15), )
    ui.language.register_widget(cusp_app,  cusp_app.blindfold_player_one_board_label, key=lambda:ui.language.player_one_label_dynamic_key(cusp_app), **ui.language.player_one_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_player_one_board_label.grid(column=0, row=7)
    cusp_app.blindfold_player_one_board_label.image = cusp_app.play_one_logo
    cusp_app.blindfold_board_canvas = Canvas( cusp_app.blindfold_cchess_frame, width=cusp_app.blindfold_canvas_size, height=int(cusp_app.blindfold_canvas_size * 10 / 9), )
    cusp_app.blindfold_board_canvas.grid(column=0, row=1, rowspan=6, sticky="news")

    cusp_app.blindfold_board_canvas.bind( "<Button-1>", lambda event: blindfold_left_click(cusp_app, event) )
    cusp_app.blindfold_board_canvas.bind( "<B1-Motion>", lambda event: ui.ui_utils.left_button_motion(cusp_app, event, "Blindfold") )
    cusp_app.blindfold_board_canvas.bind( "<ButtonRelease-1>", lambda event: blindfold_left_button_release(cusp_app, event), )
    # remove pieces when Cusp cchess
    cusp_app.blindfold_board_canvas.bind( "<Button-3>", lambda event: ui.ui_utils.right_click(cusp_app, event, "Blindfold") )

    create_blindfold_chess_board(cusp_app)

    cusp_app.blindfold_move_notice_label = ttk.Label( cusp_app.blindfold_cchess_frame, text="", font=("Times", 15) )
    ui.language.register_widget(cusp_app, cusp_app.blindfold_move_notice_label, key=lambda:ui.language.blindfold_label_dynamic_key(cusp_app),)
    cusp_app.blindfold_move_notice_label.grid(column=0, row=8)

    cusp_app.blindfold_color_to_move_label = ttk.Label( cusp_app.blindfold_cchess_frame, font=("Times", 12) )
    ui.language.register_widget(cusp_app, cusp_app.blindfold_color_to_move_label, "color_to_move_label",**ui.language.color_to_move_label_dynamic_kwargs(cusp_app))
    cusp_app.blindfold_color_to_move_label.grid( column=0, row=9, padx=5, pady=5, sticky="W" )
    ui.ui_utils.update_color_to_move_label(cusp_app)


    cusp_app.blindfold_cchess_frame.bind( "<Configure>", lambda event: resize_blindfold_cchess(cusp_app, event) )

    cusp_app.update()


def create_blindfold_chess_board(cusp_app):
    logger.info("create_blindfold_chess_board")
    img = PILImage.open("assets/xiangqiboardBig.png")
    img = img.resize( (cusp_app.blindfold_canvas_size, int(cusp_app.blindfold_canvas_size * 10 / 9)), PILImage.Resampling.LANCZOS, )
    boardImg = ImageTk.PhotoImage(img)

    cusp_app.blindfold_board_canvas.delete("all")
    cusp_app.blindfold_board_canvas.create_image(0, 0, image=boardImg, anchor=NW)
    cusp_app.blindfold_boardImg = boardImg


def resize_blindfold_cchess(cusp_app, event):
    logger.info("resize_blindfold_cchess")
    blindfold_cchess_frame_height = cusp_app.blindfold_cchess_frame.winfo_height()
    blindfold_cchess_frame_width = cusp_app.blindfold_cchess_frame.winfo_width()
    cusp_app.blindfold_canvas_size = blindfold_cchess_frame_height * 35 / 100

    cusp_app.blindfold_canvas_size = int(cusp_app.blindfold_canvas_size / 9) * 9

    cusp_app.blindfold_board_canvas.config( width=cusp_app.blindfold_canvas_size, height=int(cusp_app.blindfold_canvas_size * 10 / 9), )

    create_blindfold_chess_board(cusp_app)

    cusp_app.update()

    utils.config.save_setting_in_config_file(cusp_app)


def blindfold_left_click(cusp_app, event):
    logger.info("blindfold_left_click")
    if cusp_app.game_in_progress and ( ( cusp_app.chess_game_variant_mode == "Normal" and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and ( ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "Human" and cusp_app.board.turn) or (cusp_app.player_two == "Human" and not cusp_app.board.turn) ) ) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "Human" and not cusp_app.board.turn) or (cusp_app.player_two == "Human" and cusp_app.board.turn) ) ) ) ) ):
        if utils.game_results.check_game_result(cusp_app):
            return
        if ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
            return

        ui.ui_utils.clear_board_move_history(cusp_app)
        cusp_app.setting_up_in_cusp_chess = False

        mouse_x, mouse_y = event.x, event.y
        canvas_x = mouse_x // (cusp_app.blindfold_canvas_size / 9)
        canvas_y = mouse_y // (cusp_app.blindfold_canvas_size / 9)
        canvas_x = int(canvas_x)
        canvas_y = int(canvas_y)

        if not cusp_app.flip_board_enable:
            cchessboard_x = canvas_x
            cchessboard_y = 9 - canvas_y
        else:
            cchessboard_x = 8 - canvas_x
            cchessboard_y = canvas_y
        cchessboard_index = cchessboard_x + cchessboard_y * 9

        piece = cusp_app.board.piece_at(cchessboard_index)
        cusp_app.selected_piece = piece
        if piece:
            cusp_app.piece_move_start_square = cchessboard_index
            cusp_app.mouse_drag = True

            cusp_app.board_canvas.delete("highlight")
            legal_moves = ui.ui_utils.legal_moves_at(cusp_app, cusp_app.board, cchessboard_index)
            SQUARE_SIZE = int(cusp_app.canvas_size / 9)
            RANKS = 10
            # print(legal_moves)
            ui.ui_utils.draw_all_legal_moves_for_selected_piece( cusp_app, legal_moves, SQUARE_SIZE, RANKS, "Blindfold" )


def blindfold_left_button_release(cusp_app, event):
    logger.info("blindfold_left_button_release")
    cusp_app.board_canvas.delete("drag_piece")
    cusp_app.board_canvas.delete("highlight")
    if ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.cusp_chess_phase == "SafeMove" and cusp_app.human_no_move_this_round == False ):
        return

    if cusp_app.mouse_drag == False:
        return
    cusp_app.mouse_drag = False
    ui.ui_utils.clear_board_move_history(cusp_app)
    mouse_x, mouse_y = event.x, event.y
    if ( mouse_x >= cusp_app.blindfold_canvas_size or mouse_x < 0 or mouse_y >= cusp_app.blindfold_canvas_size * 10 / 9 or mouse_y < 0 ):
        return
    canvas_x = mouse_x // (cusp_app.blindfold_canvas_size / 9)
    canvas_y = mouse_y // (cusp_app.blindfold_canvas_size / 9)
    canvas_x = int(canvas_x)
    canvas_y = int(canvas_y)

    if not cusp_app.flip_board_enable:
        cchessboard_x = canvas_x
        cchessboard_y = 9 - canvas_y
    else:
        cchessboard_x = 8 - canvas_x
        cchessboard_y = canvas_y
    cchessboard_index = cchessboard_x + cchessboard_y * 9

    move = cchess.Move( from_square=cusp_app.piece_move_start_square, to_square=cchessboard_index )
    if move in cusp_app.board.legal_moves:
        cusp_app.move_str_legal = True
    else:
        cusp_app.move_str_legal = False
    # normal cchess move
    if ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.cusp_chess_phase == "Fight" ) or cusp_app.chess_game_variant_mode == "Normal":
        if cusp_app.move_str_legal:
            cusp_app.move_str = str(move)
            cusp_app.setting_up_in_cusp_chess = False
            utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)
            # save befor push move

            cusp_app.board.push(move)
            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index )
            utils.game_results.check_game_result(cusp_app)

        else:
            # output 'The move is illegal'
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
        cusp_app.update()

    # Cusp Xiangqi and cusp_app.cusp_chess_phase=="SafeMove", one free move is allowed
    elif ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.cusp_chess_phase == "SafeMove" ):
        illegal_move = False

        if cusp_app.move_str_legal:
            cusp_app.Human_must_set_up = False

            cusp_app.move_str = move
            cusp_app.board.push(move)
            cusp_app.board.turn = (
                1 ^ cusp_app.board.turn
            )  # because it is easier to process when pressing the move confirmation button
            # if a player has made a move, he/she can't choose color directly.
            cusp_app.human_no_move_this_round = False
            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index )

            utils.game_results.check_game_result(cusp_app)

        elif ( str(cusp_app.board.piece_at(cchessboard_index)) != "k" and str(cusp_app.board.piece_at(cchessboard_index)) != "K" ):
            if cusp_app.piece_move_start_square != cchessboard_index:
                if ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "p" ):
                    if cchessboard_index in cusp_app.black_pawn_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)

                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "P" ):
                    if cchessboard_index in cusp_app.white_pawn_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "a" ):
                    if cchessboard_index in cusp_app.black_advisor_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "A" ):
                    if cchessboard_index in cusp_app.white_advisor_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "b" ):
                    if cchessboard_index in cusp_app.black_bishop_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "B" ):
                    if cchessboard_index in cusp_app.white_bishop__legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "k" ):
                    if cchessboard_index in cusp_app.black_king_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move
                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                elif ( str(cusp_app.board.piece_at(cusp_app.piece_move_start_square)) == "K" ):
                    if cchessboard_index in cusp_app.white_king_legal_positions:
                        if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                            piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.remove_piece_at( cusp_app.piece_move_start_square )
                            cusp_app.board.set_piece_at(cchessboard_index, piece)

                            cusp_app.Human_must_set_up = True
                            print("Human_must_set_up=True")
                            cusp_app.human_no_move_this_round = False
                            cusp_app.move_str = move

                            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                            ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                        else:
                            illegal_move = True
                    else:
                        illegal_move = True

                else:
                    if not ui.ui_utils.both_kings_checked( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ) and not ui.ui_utils.two_kings_meet( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, cusp_app.board, ):
                        piece = cusp_app.board.piece_at( cusp_app.piece_move_start_square )
                        cusp_app.board.remove_piece_at(cusp_app.piece_move_start_square)
                        cusp_app.board.set_piece_at(cchessboard_index, piece)

                        cusp_app.Human_must_set_up = True
                        print("Human_must_set_up=True")
                        cusp_app.human_no_move_this_round = False
                        cusp_app.move_str = move

                        ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
                        ui.ui_utils.draw_arrows_with_two_indexes( cusp_app, cusp_app.piece_move_start_square, cchessboard_index, )

                    else:
                        illegal_move = True
            else:
                illegal_move = True
        else:
            illegal_move = True
        if illegal_move:
            cusp_app.blindfold_label_state='The_move_is_illegal'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)

    cusp_app.piece_move_start_square = -1
    # in Safe Move and setup phase, human player needs to click move-finished button
    if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
        if cusp_app.chess_game_variant_mode == "Normal":
            if (cusp_app.player_one == "AI" and cusp_app.board.turn) or ( cusp_app.player_two == "AI" and not cusp_app.board.turn ):
                cusp_app.AI_searching_best_move()
        elif cusp_app.chess_game_variant_mode == "CuspXiangqi":
            if cusp_app.cusp_chess_phase == "Fight":
                if ( cusp_app.player_swap_side == False and ( (cusp_app.player_one == "AI" and cusp_app.board.turn) or (cusp_app.player_two == "AI" and not cusp_app.board.turn) ) ) or ( cusp_app.player_swap_side and ( (cusp_app.player_one == "AI" and not cusp_app.board.turn) or (cusp_app.player_two == "AI" and cusp_app.board.turn) ) ):
                    cusp_app.AI_searching_best_move()