import logging
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext, ttk

import cchess
from PIL import Image as PILImage
from PIL import ImageTk

import ai.ChessEngine
import ai.search_for_all_cusps_for_CC_thread

import ai.stop_threads
import ai.update_editor_score_thread
import ui.ui_utils
import utils.config

logger = logging.getLogger(__name__)

def create_editor_board_frame(cusp_app):
    logger.info("create_editor_board_frame")
    cusp_app.editor_board_frame = ttk.Frame(cusp_app.editor_container)
    cusp_app.editor_board_frame.grid(column=0, row=0, rowspan=10, sticky="wens")

    cusp_app.editor_board_frame.grid_columnconfigure(0, weight=1)
    cusp_app.editor_board_frame.grid_columnconfigure(1, weight=8)
    cusp_app.editor_board_frame.grid_columnconfigure(2, weight=2)

    cusp_app.editor_board_canvas = Canvas( cusp_app.editor_board_frame, width=int(cusp_app.editor_canvas_size), height=int(cusp_app.editor_canvas_size * 12 / 9), )
    cusp_app.editor_board_canvas.grid(column=1, row=0, rowspan=8, sticky="news")

    cusp_app.editor_board_canvas.bind( "<Button-1>", lambda event: editor_board_left_click(cusp_app, event) )
    cusp_app.editor_board_canvas.bind( "<ButtonRelease-1>", lambda event: editor_board_left_button_release(cusp_app, event), )
    # right click to remove pieces
    cusp_app.editor_board_canvas.bind( "<Button-3>", lambda event: ui.ui_utils.right_click(cusp_app, event, "Editor") )

    editor_draw_chessboard(cusp_app)
    # eval bar to show score in real time
    cusp_app.editor_player_one_bar = Canvas(
        cusp_app.editor_board_frame,
        width=20,
        height=int(cusp_app.editor_canvas_size * 10 / 9),
        bg="#808080",
    )
    cusp_app.editor_player_one_bar.grid(row=0, column=0, rowspan=8, padx=5)

    ui.ui_utils.draw_pieces(cusp_app, "Editor")
    
    cusp_app.editor_color_to_move_label = ttk.Label(cusp_app.editor_board_frame, font=("Times", 12))  
    ui.language.register_widget(cusp_app, cusp_app.editor_color_to_move_label, "editor_color_to_move_label", **ui.language.editor_color_to_move_label_dynamic_kwargs(cusp_app))
    cusp_app.editor_color_to_move_label.grid( column=0, row=9,columnspan=2,  padx=5, pady=5, sticky="W")
    
    cusp_app.editor_board_frame.bind( "<Configure>", lambda event: editor_resize_board(cusp_app, event) )

    cusp_app.update()


def create_editor_setting_UI(cusp_app):
    logger.info("create_editor_setting_UI")
    cusp_app.editor_setting_UI = ttk.Frame(cusp_app.editor_container)
    cusp_app.editor_setting_UI.grid( column=1, row=0, rowspan=10, sticky="wens" )

    # start postition and clear board

    cusp_app.editor_start_position = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_starting_position_function(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_start_position, "editor_start_position")
    cusp_app.editor_start_position.grid(column=0, row=0, padx=5, pady=10)


    cusp_app.editor_clear_board = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_clear_board_function(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_clear_board, "editor_clear_board")
    cusp_app.editor_clear_board.grid(column=1, row=0, padx=5, pady=10)

    cusp_app.editor_separator = ttk.Separator( cusp_app.editor_setting_UI, orient="horizontal" )
    cusp_app.editor_separator.grid(column=0, row=1, columnspan=2, ipadx=300)

    # set which color to move
    cusp_app.editor_radio_value = tk.IntVar()

    cusp_app.editor_white_to_move_radio = tk.Radiobutton( cusp_app.editor_setting_UI, variable=cusp_app.editor_radio_value, command=lambda: editor_confirm_color_to_move(cusp_app), value=1, )
    ui.language.register_widget(cusp_app, cusp_app.editor_white_to_move_radio, "editor_white_to_move_radio")
    cusp_app.editor_white_to_move_radio.grid(column=0, row=2, padx=5, pady=10)

    cusp_app.editor_black_to_move_radio = tk.Radiobutton( cusp_app.editor_setting_UI,  variable=cusp_app.editor_radio_value, command=lambda: editor_confirm_color_to_move(cusp_app), value=0, )
    ui.language.register_widget(cusp_app, cusp_app.editor_black_to_move_radio, "editor_black_to_move_radio")
    cusp_app.editor_black_to_move_radio.grid(column=1, row=2, padx=5, pady=10)


    cusp_app.editor_auto_turn_rotation_checkbox_var = tk.IntVar()
    cusp_app.editor_auto_turn_rotation_checkbox = ttk.Checkbutton( cusp_app.editor_setting_UI, command=lambda: editor_auto_turn_rotation_checkbox_change(cusp_app), variable=cusp_app.editor_auto_turn_rotation_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.editor_auto_turn_rotation_checkbox, "editor_auto_turn_rotation_checkbox")
    cusp_app.editor_auto_turn_rotation_checkbox.grid( row=3, column=1, padx=5, pady=10)

    if cusp_app.editor_auto_turn_rotation:
        cusp_app.editor_auto_turn_rotation_checkbox_var.set(1)
    elif cusp_app.editor_auto_turn_rotation == False:
        cusp_app.editor_auto_turn_rotation_checkbox_var.set(0)

    cusp_app.editor_engine_path_var = tk.StringVar()
    cusp_app.editor_engine_path_entry = ttk.Entry(cusp_app.editor_setting_UI, textvariable=cusp_app.editor_engine_path_var, width=100, state="readonly")
    cusp_app.editor_engine_path_entry.grid(row=4, column=0, columnspan=2,)

    if cusp_app.editor_engine_path:
        cusp_app.editor_engine_path_var.set(cusp_app.editor_engine_path)
        cusp_app.editor_engine_path_entry.xview_moveto(1)


    cusp_app.editor_engine_path_button = ttk.Button( cusp_app.editor_setting_UI, width=30, command=lambda: editor_set_engine_path(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_path_button, "editor_engine_path_button")
    cusp_app.editor_engine_path_button.grid(row=5, column=0)

    if cusp_app.board.turn:
        cusp_app.editor_radio_value.set(1)
    else:
        cusp_app.editor_radio_value.set(0)
    # enable chess engine for analyse
    cusp_app.editor_engine_analyse_checkbox_var = tk.IntVar()
    cusp_app.editor_engine_analyse_checkbox = ttk.Checkbutton( cusp_app.editor_setting_UI,  command=lambda: editor_engine_analyse_checkbox_change(cusp_app), variable=cusp_app.editor_engine_analyse_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_analyse_checkbox, "editor_engine_analyse_checkbox")
    cusp_app.editor_engine_analyse_checkbox.grid(row=5, column=1, padx=5, pady=10)
    if cusp_app.editor_engine_analyse_enable:
        cusp_app.editor_engine_analyse_checkbox_var.set(1)
    elif cusp_app.editor_engine_analyse_enable == False:
        cusp_app.editor_engine_analyse_checkbox_var.set(0)

    cusp_app.editor_engine_time_or_depth_label = ttk.Label( cusp_app.editor_setting_UI, justify=LEFT, compound=LEFT,  font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_time_or_depth_label, "editor_engine_time_or_depth_label")
    cusp_app.editor_engine_time_or_depth_label.grid(column=0, row=6, padx=5, pady=10)

    cusp_app.editor_engine_time_entry = ttk.Entry(cusp_app.editor_setting_UI)
    cusp_app.editor_engine_time_entry.grid(column=1, row=6, padx=5, pady=10)
    cusp_app.editor_engine_time_entry.delete(0, END)
    cusp_app.editor_engine_time_entry.insert( 0, str(cusp_app.editor_engine_evaluation_limit) )


    cusp_app.editor_engine_top_moves_label = ttk.Label( cusp_app.editor_setting_UI, justify=LEFT, compound=LEFT,  font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_top_moves_label, "editor_engine_top_moves_label")
    cusp_app.editor_engine_top_moves_label.grid(column=0, row=7, padx=5, pady=10)

    cusp_app.editor_engine_top_moves_entry = ttk.Entry(cusp_app.editor_setting_UI)
    cusp_app.editor_engine_top_moves_entry.grid(column=1, row=7, padx=5, pady=10)
    cusp_app.editor_engine_top_moves_entry.delete(0, END)
    cusp_app.editor_engine_top_moves_entry.insert( 0, str(cusp_app.editor_engine_multipv) )
    
    # cusp_app.editor_score_separator = ttk.Separator( cusp_app.editor_setting_UI, orient="horizontal" )
    # cusp_app.editor_score_separator.grid(column=0, row=8, columnspan=2, ipadx=300)

    cusp_app.editor_engine_score_label = ttk.Label( cusp_app.editor_setting_UI, justify=LEFT, compound=LEFT,  font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_score_label, "editor_engine_score_label")
    cusp_app.editor_engine_score_label.grid(column=0, row=9, padx=5, pady=10)


    cusp_app.editor_engine_score_and_top_moves_search_button = tk.Button( cusp_app.editor_setting_UI, command=lambda: editor_engine_score_and_top_moves_search(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_score_and_top_moves_search_button, "editor_engine_score_and_top_moves_search_button")
    cusp_app.editor_engine_score_and_top_moves_search_button.grid(column=1, row=9, padx=5, pady=10)
    cusp_app.editor_cusp_separator = ttk.Separator( cusp_app.editor_setting_UI, orient="horizontal" )
    cusp_app.editor_cusp_separator.grid(column=0, row=10, columnspan=2, ipadx=300)

    cusp_app.editor_engine_search_for_cusps_for_CC_label = ttk.Label( cusp_app.editor_setting_UI, justify=LEFT, compound=LEFT, font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.editor_engine_search_for_cusps_for_CC_label, "editor_engine_search_for_cusps_label")
    cusp_app.editor_engine_search_for_cusps_for_CC_label.grid( column=0, row=11, padx=5, pady=10 )

    cusp_app.editor_search_for_cusps_for_CC_confirm_button = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_engine_search_for_cusps_confirm(cusp_app, "CuspXiangqi"), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_search_for_cusps_for_CC_confirm_button, "editor_search_for_cusps_for_CC_confirm_button")
    cusp_app.editor_search_for_cusps_for_CC_confirm_button.grid( column=1, row=11, padx=5, pady=10 )

    cusp_app.editor_cusp_stop_button = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_cusp_engine_search_stop(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_cusp_stop_button, "editor_cusp_stop_button")
    cusp_app.editor_cusp_stop_button.grid(column=1, row=13, padx=5, pady=10)

    cusp_app.editor_fen_text = scrolledtext.ScrolledText( cusp_app.editor_setting_UI, width=75, height=10, font=("Times", 12) )

    cusp_app.editor_fen_text.grid( column=0, row=14, columnspan=3, rowspan=2, padx=5, pady=10 )

    cusp_app.editor_editor_export_board_fen_button = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_export_board_fen(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_editor_export_board_fen_button, "editor_editor_export_board_fen_button")
    cusp_app.editor_editor_export_board_fen_button.grid( column=1, row=16, padx=5, pady=10 )

    cusp_app.editor_clear_fen_history_button = tk.Button( cusp_app.editor_setting_UI, command=lambda: editor_clear_history(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_clear_fen_history_button, "editor_clear_fen_history_button")
    cusp_app.editor_clear_fen_history_button.grid(column=0, row=16, padx=5, pady=10)


    cusp_app.editor_fen_entry = ttk.Entry( cusp_app.editor_setting_UI, width=75, font=("Times", 12) )
    cusp_app.editor_fen_entry.grid(column=0, row=17, columnspan=3, padx=5, pady=10)

    cusp_app.editor_set_board_fen_button = tk.Button( cusp_app.editor_setting_UI,  command=lambda: editor_set_board_fen(cusp_app), width=30, )
    ui.language.register_widget(cusp_app, cusp_app.editor_set_board_fen_button, "editor_set_board_fen_button")
    cusp_app.editor_set_board_fen_button.grid(column=1, row=18, padx=5, pady=10)



def editor_clear_history(cusp_app):
    logger.info("editor_clear_history")
    cusp_app.editor_fen_text.delete(1.0, END)
    cusp_app.editor_fen_entry.delete(0, END)


def editor_set_engine_path(cusp_app):
    logger.info("editor_set_engine_path")
    editor_engine_path = filedialog.askopenfilename( filetypes=[("chess engine program", "*.exe"), ("All files", "*.*")] )
    if not editor_engine_path:
        logger.info(f"wrong editor engine path {editor_engine_path}")

    else:
        cusp_app.editor_engine_path = editor_engine_path
        cusp_app.editor_engine_path_var.set(cusp_app.editor_engine_path)
        cusp_app.editor_engine_path_entry.xview_moveto(1)
        utils.config.save_setting_in_config_file(cusp_app)


def editor_auto_turn_rotation_checkbox_change(cusp_app):
    logger.info("editor_auto_turn_rotation_checkbox_change")
    if cusp_app.editor_auto_turn_rotation_checkbox_var.get() == 1:
        cusp_app.editor_auto_turn_rotation = True
    else:
        cusp_app.editor_auto_turn_rotation = False


def editor_engine_analyse_checkbox_change(cusp_app):
    logger.info("editor_engine_analyse_checkbox_change")
    if cusp_app.editor_engine_analyse_checkbox_var.get() == 1:
        cusp_app.editor_engine_analyse_enable = True
        if cusp_app.editor_engine_path != "":
            ui.ui_utils.setup_engine(cusp_app,'editor_engine',cusp_app.editor_engine_path)
        else:
            cusp_app.editor_engine_exist = False
            cusp_app.editor_engine_analyse_checkbox_var.set(0)
            cusp_app.editor_engine_analyse_enable = False
    else:
        cusp_app.editor_engine_analyse_enable = False
        cusp_app.editor_engine_analyse_checkbox_var.set(0)


def editor_engine_search_for_cusps_confirm(cusp_app, chess_variant):
    logger.info("editor_engine_search_for_cusps_confirm")
    if cusp_app.editor_engine_time_entry.get() != "":
        try:
            cusp_app.editor_engine_evaluation_limit = float( cusp_app.editor_engine_time_entry.get() )
            if cusp_app.editor_engine_evaluation_limit < 0:
                cusp_app.editor_engine_evaluation_limit = 0
               
            utils.config.save_setting_in_config_file(cusp_app)

            if cusp_app.editor_engine_analyse_enable:
                editor_engine_search_for_cusps(cusp_app, chess_variant)
        except Exception as e:
            logger.exception("Error: editor_engine_search_for_cusps_confirm")
            messagebox.showerror("Error", f"Error when searching all fight starting positions: {e}" )  

def editor_engine_search_for_cusps(cusp_app, chess_variant):
    logger.info("editor_engine_search_for_cusps")
    if cusp_app.editor_engine_analyse_enable:    
        ai.stop_threads.stop_editor_threads(cusp_app)        
        if cusp_app.editor_engine:
            cusp_app.editor_engine.reset()    
        cusp_app.searching_cusps_count = 0
        try:
            if chess_variant == "CuspXiangqi":
                cusp_app.search_for_all_cusps_for_CC_thread = ( ai.search_for_all_cusps_for_CC_thread.SearchForAllCuspsForCCThread(cusp_app) )
                cusp_app.search_for_all_cusps_for_CC_thread.start()

        except Exception as e:
            logger.exception("Error: editor_engine_search_for_cusps for Cusp Xiangqi")
            messagebox.showerror("Error", f"Error when searching all fight starting positions for Cusp Xiangqi: {e}" )

def editor_cusp_engine_search_stop(cusp_app):
    logger.info("editor_cusp_engine_search_stop")
    ai.stop_threads.stop_editor_threads(cusp_app)


def editor_set_board_fen(cusp_app):
    logger.info("editor_set_board_fen")
    try:
        cusp_app.board.set_fen(str(cusp_app.editor_fen_entry.get()))
        ui.ui_utils.draw_pieces(cusp_app, "Editor")
        ui.ui_utils.update_color_to_move_label(cusp_app)
        if cusp_app.board.turn:
            if cusp_app.editor_radio_value.get() == 0:
                cusp_app.editor_radio_value.set(1)
        else:
            if cusp_app.editor_radio_value.get() == 1:
                cusp_app.editor_radio_value.set(0)
        update_editor_color_to_move_label(cusp_app)  
        cusp_app.update()
        editor_update_player_score_bar(cusp_app)
    except Exception as e:
        logger.error(f"invalid editor FEN {str(cusp_app.editor_fen_entry.get())}")
        messagebox.showerror("Error", f"Error when setting a FEN: {e}" )

def editor_export_board_fen(cusp_app):
    logger.info("editor_export_board_fen")
    if len(cusp_app.editor_fen_text.get("1.0", END)) > 1:
        cusp_app.editor_fen_text.insert(END, "\n" + str(cusp_app.board.fen()))
    else:
        cusp_app.editor_fen_text.insert(END, str(cusp_app.board.fen()))

    cusp_app.editor_fen_text.see("end")


def editor_starting_position_function(cusp_app):
    logger.info("editor_starting_position_function")
    cusp_app.board.reset()
    update_editor_color_to_move_label(cusp_app)      
    if cusp_app.board.turn:
        if cusp_app.editor_radio_value.get() == 0:
            cusp_app.editor_radio_value.set(1)
    else:
        if cusp_app.editor_radio_value.get() == 1:
            cusp_app.editor_radio_value.set(0)
            
    ui.ui_utils.draw_pieces(cusp_app, "Editor")
    editor_update_player_score_bar(cusp_app)
    cusp_app.update()


def editor_clear_board_function(cusp_app):
    logger.info("editor_clear_board_function")
    for i in range(90):
        piece = cusp_app.board.piece_at(i)
        if piece:
            cusp_app.board.remove_piece_at(i)

    ui.ui_utils.draw_pieces(cusp_app, "Editor")
    cusp_app.update()


def editor_confirm_color_to_move(cusp_app):
    logger.info("editor_confirm_color_to_move")
    if cusp_app.editor_radio_value.get() == 1:
        cusp_app.board.turn = True

    elif cusp_app.editor_radio_value.get() == 0:
        cusp_app.board.turn = False
    update_editor_color_to_move_label(cusp_app)
    editor_update_player_score_bar(cusp_app)
    ui.ui_utils.update_color_to_move_label(cusp_app)


def editor_engine_score_and_top_moves_search(cusp_app):
    logger.info("editor_engine_score_and_top_moves_search")
    if cusp_app.editor_engine_time_entry.get() != "":
        try:
            cusp_app.editor_engine_evaluation_limit = float( cusp_app.editor_engine_time_entry.get() )

            if cusp_app.engine_time_limit_enable:
                if cusp_app.editor_engine_evaluation_limit < 0.02:
                    cusp_app.editor_engine_evaluation_limit = 0.02
                   
            else:
                if cusp_app.editor_engine_evaluation_limit < 2:
                    cusp_app.editor_engine_evaluation_limit = 2
            cusp_app.editor_engine_time_entry.delete(0, END)        
            cusp_app.editor_engine_time_entry.insert( 0, str(cusp_app.editor_engine_evaluation_limit))
            
            cusp_app.editor_engine_multipv = int(cusp_app.editor_engine_top_moves_entry.get())
            if cusp_app.editor_engine_multipv<0:
                cusp_app.editor_engine_multipv=0
            elif cusp_app.editor_engine_multipv>20:
                cusp_app.editor_engine_multipv=20
            cusp_app.editor_engine_top_moves_entry.delete(0, END)    
            cusp_app.editor_engine_top_moves_entry.insert( 0, str(cusp_app.editor_engine_multipv) )
                   
            utils.config.save_setting_in_config_file(cusp_app)
            editor_engine_analyse_checkbox_change(cusp_app)
            editor_update_player_score_bar(cusp_app)
        except Exception as e:
            logger.exception('Error: editor_engine_score_and_top_moves_search.')
            messagebox.showerror("Error", f"Error when updating score bar: {e}" )

def editor_draw_chessboard(cusp_app):
    logger.info("editor_draw_chessboard")
    editor_board_img = PILImage.open("assets/12rankBoardNotations.png")
    editor_board_img = editor_board_img.resize( (int(cusp_app.editor_canvas_size), int(cusp_app.editor_canvas_size * 12 / 9)), PILImage.Resampling.LANCZOS, )
    editor_board_img = ImageTk.PhotoImage(editor_board_img)

    cusp_app.editor_board_canvas.delete("all")
    cusp_app.editor_board_canvas.create_image(0, 0, image=editor_board_img, anchor=NW)
    cusp_app.editor_board_img = editor_board_img


def editor_resize_board(cusp_app, event):
    logger.info("editor_resize_board")
    appheight = cusp_app.editor_board_frame.winfo_height()
    appwidth = cusp_app.editor_board_frame.winfo_width()

    cusp_app.editor_canvas_size = appheight * (72 / 100)
    cusp_app.editor_canvas_size = int(cusp_app.editor_canvas_size / 9) * 9


    cusp_app.editor_board_canvas.config( width=cusp_app.editor_canvas_size, height=int(cusp_app.editor_canvas_size * 12 / 9), )
    cusp_app.editor_player_one_bar.config( width=20, height=int(cusp_app.editor_canvas_size * 10 / 9) )
    editor_draw_chessboard(cusp_app)
    ui.ui_utils.draw_pieces(cusp_app, "Editor")
    utils.config.save_setting_in_config_file(cusp_app)
    cusp_app.update()

def editor_board_left_click(cusp_app, event):
    logger.info("editor_board_left_click")
    mouse_x, mouse_y = event.x, event.y
    if ( mouse_x >= cusp_app.editor_canvas_size or mouse_x <= 0 or mouse_y >= cusp_app.editor_canvas_size * 12 / 9 or mouse_y <= 0 ):
        return

    canvas_x = mouse_x // (cusp_app.editor_canvas_size / 9)
    canvas_y = mouse_y // (cusp_app.editor_canvas_size / 9)
    canvas_x = int(canvas_x)
    canvas_y = int(canvas_y)

    if ( cusp_app.editor_canvas_size / 9 < mouse_y < cusp_app.editor_canvas_size * 11 / 9 ) or ( ( 0 < mouse_y < cusp_app.editor_canvas_size / 9 or cusp_app.editor_canvas_size * 11 / 9 < mouse_y < cusp_app.editor_canvas_size * 12 / 9 ) and cusp_app.editor_canvas_size * 11 / 9 > mouse_x > cusp_app.editor_canvas_size / 9 ):
        cchessboard_x = canvas_x
        cchessboard_y = 11 - canvas_y
        twelve_rank_chessboard_index = cchessboard_x + cchessboard_y * 9

        if ( cusp_app.editor_canvas_size / 9 < mouse_y < cusp_app.editor_canvas_size * 11 / 9 ):
            piece = cusp_app.board.piece_at(twelve_rank_chessboard_index - 9)
            if not piece:
                return

        cusp_app.piece_move_start_square = twelve_rank_chessboard_index

        cusp_app.mouse_drag = True


def editor_board_left_button_release(cusp_app, event):
    logger.info("editor_board_left_button_release")
    if cusp_app.mouse_drag == False:
        return
    cusp_app.mouse_drag = False

    mouse_x, mouse_y = event.x, event.y
    # only ends at the cchess board
    if ( cusp_app.editor_canvas_size / 9 < mouse_y < cusp_app.editor_canvas_size * 11 / 9 and cusp_app.editor_canvas_size > mouse_x > 0 ):
        canvas_x = mouse_x // (cusp_app.editor_canvas_size / 9)
        canvas_y = mouse_y // (cusp_app.editor_canvas_size / 9)
        canvas_x = int(canvas_x)
        canvas_y = int(canvas_y)

        cchessboard_x = canvas_x
        cchessboard_y = 11 - canvas_y
        twelve_rank_chessboard_index = cchessboard_x + cchessboard_y * 9

        if 0 < cusp_app.piece_move_start_square < 8:
            # add Red pieces
            if cusp_app.piece_move_start_square == 1:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("R") )
            elif cusp_app.piece_move_start_square == 2:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("N") )
            elif cusp_app.piece_move_start_square == 3:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("B") )
            elif cusp_app.piece_move_start_square == 4:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("A") )
            elif cusp_app.piece_move_start_square == 5:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("C") )
            elif cusp_app.piece_move_start_square == 6:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("P") )
            elif cusp_app.piece_move_start_square == 7:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("K") )

        elif 99 < cusp_app.piece_move_start_square < 107:
            # add Black pieces
            if cusp_app.piece_move_start_square == 100:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("r") )
            elif cusp_app.piece_move_start_square == 101:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("n") )
            elif cusp_app.piece_move_start_square == 102:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("b") )
            elif cusp_app.piece_move_start_square == 103:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("a") )
            elif cusp_app.piece_move_start_square == 104:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("c") )
            elif cusp_app.piece_move_start_square == 105:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("p") )
            elif cusp_app.piece_move_start_square == 106:
                cusp_app.board.set_piece_at( twelve_rank_chessboard_index - 9, cchess.Piece.from_symbol("k") )

        elif 8 < cusp_app.piece_move_start_square < 99:
            # move pieces
            piece = cusp_app.board.piece_at(cusp_app.piece_move_start_square - 9)
            if piece and cusp_app.piece_move_start_square!= twelve_rank_chessboard_index:
                if cusp_app.editor_auto_turn_rotation:
                    if str(piece).isupper():
                        cusp_app.board.turn = False 
                    else:
                        cusp_app.board.turn = True
                    update_editor_color_to_move_label(cusp_app)    
                    if cusp_app.board.turn:
                        cusp_app.editor_radio_value.set(1)
                    else:
                        cusp_app.editor_radio_value.set(0)   
                cusp_app.board.remove_piece_at(cusp_app.piece_move_start_square - 9)
                cusp_app.board.set_piece_at(twelve_rank_chessboard_index - 9, piece)

        ui.ui_utils.draw_pieces(cusp_app, "Editor")
        editor_update_player_score_bar(cusp_app)
        cusp_app.piece_move_start_square = -1


def editor_update_player_score_bar(cusp_app):
    logger.info("editor_update_player_score_bar")
    update_editor_color_to_move_label(cusp_app)
    ai.stop_threads.stop_editor_threads(cusp_app)
    if cusp_app.editor_engine_analyse_enable: 
        try:
            if cusp_app.editor_engine:
                cusp_app.editor_engine.reset() 
            cusp_app.update_editor_score_thread = ai.update_editor_score_thread.UpdateEditorScoreThread( cusp_app )
            cusp_app.update_editor_score_thread.start()
        except Exception as e:
            logger.exception('Error: editor_update_player_score_bar.')
            messagebox.showerror("Error", f"Error when updating score bar: {e}" )    
def update_editor_color_to_move_label(cusp_app):
    logger.info("update_color_to_move_label")
    if cusp_app.board.turn:
        cusp_app.editor_color_to_move_label_state = "White"  
    else:
        cusp_app.editor_color_to_move_label_state = "Black" 
    ui.language.update_widget(cusp_app, cusp_app.editor_color_to_move_label)

    cusp_app.update()   