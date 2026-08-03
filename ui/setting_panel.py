"""
This module is for all user settings on the GUI.

"""
import logging
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, scrolledtext, ttk

import cchess
from PIL import Image as PILImage

import ui.language

import ui.normalboard
import ui.ui_utils
import utils.config
import utils.game_results
import utils.game_state
import utils.pgnhistory
import utils.tournament

logger = logging.getLogger(__name__)

def popup_user_setting(cusp_app):
    logger.info("popup_user_setting")
    cusp_app.user_setting_window = tk.Toplevel()
    cusp_app.user_setting_window.wm_title("Setting")
    cusp_app.user_setting_window.geometry("1020x660+500+200")

    cusp_app.user_setting_window.update()
    
    UI_for_paths_for_engines_and_PGN(cusp_app)
    UI_for_cusp_searching_restrictions(cusp_app)
    UI_for_game_time_control(cusp_app)
    UI_for_game_general_setting(cusp_app)
    
    UI_for_tournament_setting(cusp_app)
    
    for widget in cusp_app.user_setting_window.winfo_children():
        widget.grid(padx=10, pady=5, sticky=W)

def UI_for_paths_for_engines_and_PGN(cusp_app):
    logger.info("UI_for_paths_for_engines_and_PGN")   
    cusp_app.engine_one_path_var = tk.StringVar()
    cusp_app.engine_one_entry = ttk.Entry(cusp_app.user_setting_window, textvariable=cusp_app.engine_one_path_var, width=130, state="readonly")
    cusp_app.engine_one_entry.grid(row=0, column=0, columnspan=3,sticky="W")

    cusp_app.engine_one_path_button = ttk.Button( cusp_app.user_setting_window, width=30, command=lambda: set_engine_one_path(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.engine_one_path_button, "engine_one_path_button")
    cusp_app.engine_one_path_button.grid(row=0, column=3)

    cusp_app.engine_two_path_var = tk.StringVar()
    cusp_app.engine_two_entry = ttk.Entry(cusp_app.user_setting_window, textvariable=cusp_app.engine_two_path_var, width=130, state="readonly")
    cusp_app.engine_two_entry.grid(row=1, column=0, columnspan=3,sticky="W")

    cusp_app.engine_two_path_button = ttk.Button( cusp_app.user_setting_window,width=30, command=lambda: set_engine_two_path(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.engine_two_path_button, "engine_two_path_button")
    cusp_app.engine_two_path_button.grid(row=1, column=3)
    
    cusp_app.engine_adjudicator_path_var = tk.StringVar()
    cusp_app.engine_adjudicator_entry = ttk.Entry(cusp_app.user_setting_window, textvariable=cusp_app.engine_adjudicator_path_var, width=130, state="readonly")
    cusp_app.engine_adjudicator_entry.grid(row=2, column=0, columnspan=3,sticky="W")

    cusp_app.engine_adjudicator_path_button = ttk.Button( cusp_app.user_setting_window,  width=30, command=lambda: set_engine_adjudicator_path(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.engine_adjudicator_path_button, "engine_adjudicator_path_button")
    cusp_app.engine_adjudicator_path_button.grid(row=2, column=3)   

    cusp_app.PGN_folder_path_var = tk.StringVar()
    cusp_app.PGN_folder_entry = ttk.Entry(cusp_app.user_setting_window, textvariable=cusp_app.PGN_folder_path_var, width=130, state="readonly")
    cusp_app.PGN_folder_entry.grid(row=3, column=0, columnspan=3,sticky="W")    
    
    cusp_app.PGN_path_button = ttk.Button( cusp_app.user_setting_window, width=30, command=lambda: set_PGN_path(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.PGN_path_button, "PGN_path_button")
    cusp_app.PGN_path_button.grid(row=3, column=3)


    panel_separator = ttk.Separator( cusp_app.user_setting_window, orient="horizontal" )
    panel_separator.grid( column=0, row=5, columnspan=4, ipadx=500)
    
   
    if cusp_app.engine_one_path:
        cusp_app.engine_one_path_var.set(cusp_app.engine_one_path)
        cusp_app.engine_one_entry.xview_moveto(1)
        
    if cusp_app.engine_two_path:        
        cusp_app.engine_two_path_var.set(cusp_app.engine_two_path)
        cusp_app.engine_two_entry.xview_moveto(1)
        
    if cusp_app.engine_adjudicator_path:  
        cusp_app.engine_adjudicator_path_var.set(cusp_app.engine_adjudicator_path)
        cusp_app.engine_adjudicator_entry.xview_moveto(1)
        
    if cusp_app.PGN_folder_path:  
        cusp_app.PGN_folder_path_var.set(cusp_app.PGN_folder_path)
        cusp_app.PGN_folder_entry.xview_moveto(1)
             
    # Engine one is player one.         
def set_engine_one_path(cusp_app):
    logger.info("set_engine_one_path")
    engine_one_path = filedialog.askopenfilename( parent=cusp_app.user_setting_window,title='Set engine one path',   filetypes=[("chess engine program", "*.exe"), ("All files", "*.*")] )
    if not engine_one_path:
        logger.info(f"wrong engine one path")
    else:
        cusp_app.engine_one_path =  engine_one_path
        cusp_app.engine_one_path_var.set(cusp_app.engine_one_path)
        cusp_app.engine_one_entry.xview_moveto(1)

        utils.config.save_setting_in_config_file(cusp_app)

    # Engine twpo is player two.
def set_engine_two_path(cusp_app):
    logger.info("set_engine_two_path")
    engine_two_path = filedialog.askopenfilename( parent=cusp_app.user_setting_window,title='Set engine two path',   filetypes=[("chess engine program", "*.exe"), ("All files", "*.*")] )
    if not engine_two_path:
        logger.info(f"wrong engine two path")
    else:
        cusp_app.engine_two_path =  engine_two_path
        cusp_app.engine_two_path_var.set(cusp_app.engine_two_path)
        cusp_app.engine_two_entry.xview_moveto(1)

        utils.config.save_setting_in_config_file(cusp_app)

    # For early stop of engine play games
def set_engine_adjudicator_path(cusp_app):
    logger.info("set_engine_adjudicator_path")
    engine_adjudicator_path = filedialog.askopenfilename( parent=cusp_app.user_setting_window,title='Set engine adjudicator path',  filetypes=[("chess engine program", "*.exe"), ("All files", "*.*")] )
    if not engine_adjudicator_path:
        logger.info(f"wrong engine adjudicator path")
    else:
        cusp_app.engine_adjudicator_path =  engine_adjudicator_path
        cusp_app.engine_adjudicator_path_var.set(cusp_app.engine_adjudicator_path)
        cusp_app.engine_adjudicator_entry.xview_moveto(1)
        utils.config.save_setting_in_config_file(cusp_app)

def set_PGN_path(cusp_app):
    logger.info("set_PGN_path")
    pgn_path = filedialog.askdirectory( parent=cusp_app.user_setting_window, title='Set PGN folder')
    if not pgn_path:
        logger.info(f"wrong pgn path")
    else:
        cusp_app.PGN_folder_path =  pgn_path
        cusp_app.PGN_folder_path_var.set(cusp_app.PGN_folder_path)
        cusp_app.PGN_folder_entry.xview_moveto(1)
        
        ui.ui_utils.generate_PGN_path(cusp_app)
        utils.config.save_setting_in_config_file(cusp_app)
 

 
def UI_for_cusp_searching_restrictions(cusp_app):
    logger.info("UI_for_cusp_searching_restrictions")
    # when playing cusp chess, an AI player randomly decides whether it will set up a Cusp Position or not on its turn, when the ply number is smaller than maximum_ply_before_setup.
    # But it will definitely do it when ply numer is equal to or over maximum_ply.
    cusp_app.maximum_ply_before_setup_label = tk.Label( cusp_app.user_setting_window)
    ui.language.register_widget(cusp_app, cusp_app.maximum_ply_before_setup_label, "maximum_ply_before_setup_label")
    cusp_app.maximum_ply_before_setup_label.grid(row=6, column=0)

    cusp_app.maximum_ply_before_setup_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.maximum_ply_before_setup_entry.grid(row=7, column=0)
    
    cusp_app.maximum_ply_before_setup_entry.delete(0, END)
    cusp_app.maximum_ply_before_setup_entry.insert( 0, str(cusp_app.maximum_ply_before_setup) )

    # Based on stockfish, 1 and -1 are cusps. But it is hard to find a FEN whose score is exactly 1 or -1.
    # So, we find a value close to 1 or -1.
    # (1 - cusp_app.engine_score_difference_maximum < score <= 1-cusp_app.engine_score_difference_minimum
    # or 1 + cusp_app.engine_score_difference_minimum <= score < 1 + cusp_app.engine_score_difference_maximum
    # or -1 - cusp_app.engine_score_difference_maximum < score <= -1-cusp_app.engine_score_difference_minimum
    # or -1 + cusp_app.engine_score_difference_minimum <= score < -1 + cusp_app.engine_score_difference_maximum):
    cusp_app.engine_score_difference_maximum_label = tk.Label( cusp_app.user_setting_window,  )
    ui.language.register_widget(cusp_app, cusp_app.engine_score_difference_maximum_label, "engine_score_difference_maximum_label")
    
    cusp_app.engine_score_difference_maximum_label.grid(row=8, column=0)

    cusp_app.engine_score_difference_maximum_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_score_difference_maximum_entry.grid(row=9, column=0)
    cusp_app.engine_score_difference_maximum_entry.delete(0, END)
    cusp_app.engine_score_difference_maximum_entry.insert( 0, str(cusp_app.engine_score_difference_maximum) )

    # Minimum set to 0 by default. Minimum should be smaller than Maximum. 
    # A human player can set a big Minimum to play against AI.

    cusp_app.engine_score_difference_minimum_label = tk.Label( cusp_app.user_setting_window, )
    ui.language.register_widget(cusp_app, cusp_app.engine_score_difference_minimum_label, "engine_score_difference_minimum_label")
    
    cusp_app.engine_score_difference_minimum_label.grid(row=10, column=0)

    cusp_app.engine_score_difference_minimum_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_score_difference_minimum_entry.grid(row=11, column=0)
    cusp_app.engine_score_difference_minimum_entry.delete(0, END)
    cusp_app.engine_score_difference_minimum_entry.insert( 0, str(cusp_app.engine_score_difference_minimum) )

    # maximum of safe move's score, increase it can add more safe move options.
    cusp_app.engine_safe_move_score_maximum_label = tk.Label( cusp_app.user_setting_window,)
    ui.language.register_widget(cusp_app, cusp_app.engine_safe_move_score_maximum_label, "engine_safe_move_score_maximum_label")
    cusp_app.engine_safe_move_score_maximum_label.grid(row=12, column=0)

    cusp_app.engine_safe_move_score_maximum_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_safe_move_score_maximum_entry.grid(row=13, column=0)
    cusp_app.engine_safe_move_score_maximum_entry.delete(0, END)
    cusp_app.engine_safe_move_score_maximum_entry.insert( 0, str(cusp_app.engine_safe_move_score_maximum) )


    # if the engine_score_difference_maximum is too big, then outer cusp
    # range and inner cusp range is not synnmetric anymore.
    cusp_app.engine_cusp_outer_range_checkbox_var = tk.IntVar()
    cusp_app.engine_cusp_outer_range_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: engine_cusp_outer_range_checkbox_change(cusp_app), variable=cusp_app.engine_cusp_outer_range_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.engine_cusp_outer_range_checkbox, "engine_cusp_outer_range_checkbox")
    cusp_app.engine_cusp_outer_range_checkbox.grid(row=14, column=0)

    if cusp_app.engine_score_cusp_outer_range_enable:
        cusp_app.engine_cusp_outer_range_checkbox_var.set(1)
    else:
        cusp_app.engine_cusp_outer_range_checkbox_var.set(0)

    cusp_app.engine_cusp_inner_range_checkbox_var = tk.IntVar()
    cusp_app.engine_cusp_inner_range_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: engine_cusp_inner_range_checkbox_change(cusp_app), variable=cusp_app.engine_cusp_inner_range_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.engine_cusp_inner_range_checkbox, "engine_cusp_inner_range_checkbox")
    cusp_app.engine_cusp_inner_range_checkbox.grid(row=15, column=0)

    if cusp_app.engine_score_cusp_inner_range_enable:
        cusp_app.engine_cusp_inner_range_checkbox_var.set(1)
    else:
        cusp_app.engine_cusp_inner_range_checkbox_var.set(0)
    # When we do engine test, we can set only one engine can set up Cusp Positions.
    cusp_app.only_engine_one_setup_checkbox_var = tk.IntVar()
    cusp_app.only_engine_one_setup_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: only_engine_one_setup_checkbox_change(cusp_app), variable=cusp_app.only_engine_one_setup_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.only_engine_one_setup_checkbox, "only_engine_one_setup_checkbox")
    cusp_app.only_engine_one_setup_checkbox.grid(row=16, column=0)

    if cusp_app.only_engine_one_setup_enable:
        cusp_app.only_engine_one_setup_checkbox_var.set(1)
    else:
        cusp_app.only_engine_one_setup_checkbox_var.set(0)

    cusp_app.the_other_engine_choose_recommended_color_checkbox_var = tk.IntVar()
    cusp_app.the_other_engine_choose_recommended_color_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: the_other_engine_choose_recommended_color_checkbox_change(cusp_app), variable=cusp_app.the_other_engine_choose_recommended_color_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.the_other_engine_choose_recommended_color_checkbox, "the_other_engine_chooses_recommended_color_checkbox")
    cusp_app.the_other_engine_choose_recommended_color_checkbox.grid(row=17, column=0)

    if cusp_app.choose_the_recommended_color_enable:
        cusp_app.the_other_engine_choose_recommended_color_checkbox_var.set(1)
    else:
        cusp_app.the_other_engine_choose_recommended_color_checkbox_var.set(0)        
       

    # This is used to find a balance score handicap between two AI engines, especially when there is a big difference between two engines.
    cusp_app.no_choosing_color_directly_enable_checkbox_var = tk.IntVar()
    cusp_app.no_choosing_color_directly_enable_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: no_choosing_color_directly_enable_checkbox_change(cusp_app), variable=cusp_app.no_choosing_color_directly_enable_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.no_choosing_color_directly_enable_checkbox, "no_choosing_color_directly_enable_checkbox")
    cusp_app.no_choosing_color_directly_enable_checkbox.grid(row=18, column=0)

    if cusp_app.no_choosing_color_directly_enable:
        cusp_app.no_choosing_color_directly_enable_checkbox_var.set(1)
    else:
        cusp_app.no_choosing_color_directly_enable_checkbox_var.set(0)


    cusp_app.engine_test_mode_enable_checkbox_var = tk.IntVar()
    cusp_app.engine_test_mode_enable_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: engine_test_mode_enable_checkbox_change(cusp_app), variable=cusp_app.engine_test_mode_enable_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.engine_test_mode_enable_checkbox, "engine_test_mode_enable_checkbox")
    cusp_app.engine_test_mode_enable_checkbox.grid(row=19, column=0)

    if cusp_app.engine_test_mode_enable:
        cusp_app.engine_test_mode_enable_checkbox_var.set(1)
        cusp_app.color_to_move_spinbox.config(state="normal")
    else:
        cusp_app.engine_test_mode_enable_checkbox_var.set(0)
        cusp_app.color_to_move_spinbox.config(state="disabled")
        
    cusp_app.cusp_pawn_setup_enable_checkbox_var = tk.IntVar()
    cusp_app.cusp_pawn_setup_enable_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: cusp_pawn_setup_enable_checkbox_change(cusp_app), variable=cusp_app.cusp_pawn_setup_enable_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.cusp_pawn_setup_enable_checkbox, "cusp_pawn_setup_enable_checkbox")
    cusp_app.cusp_pawn_setup_enable_checkbox.grid(row=20, column=0)

    if cusp_app.cusp_pawn_setup_enable:
        cusp_app.cusp_pawn_setup_enable_checkbox_var.set(1)
    else:
        cusp_app.cusp_pawn_setup_enable_checkbox_var.set(0)

    
def UI_for_game_time_control(cusp_app):
    logger.info("UI_for_game_time_control")
    # set chess engine time limit or depth limit
    cusp_app.time_or_depth_value = tk.IntVar()

    cusp_app.time_limit_radio = tk.Radiobutton( cusp_app.user_setting_window, variable=cusp_app.time_or_depth_value, command=lambda: set_time_limit_or_depth_limit(cusp_app), value=1, )
    ui.language.register_widget(cusp_app, cusp_app.time_limit_radio, "time_limit_radio")
    cusp_app.time_limit_radio.grid(column=1, row=6)

    cusp_app.depth_limit_radio = tk.Radiobutton( cusp_app.user_setting_window,  variable=cusp_app.time_or_depth_value, command=lambda: set_time_limit_or_depth_limit(cusp_app), value=0, )
    ui.language.register_widget(cusp_app, cusp_app.depth_limit_radio, "depth_limit_radio")
    cusp_app.depth_limit_radio.grid(column=1, row=7)

    if cusp_app.engine_time_limit_enable:
        cusp_app.time_or_depth_value.set(1)
    else:
        cusp_app.time_or_depth_value.set(0)

    # when AI setting up a Cusp Position, it needs to check the position's
    # score to decide whether it is a Cusp Position or not.
    # The search limit is also used to evaluate a position in Safe Move Phase, in case we can choose a color directly.
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_label = tk.Label( cusp_app.user_setting_window, )
    ui.language.register_widget(cusp_app, cusp_app.engine_evaluation_limit_for_each_cusp_candidate_label, "engine_evaluation_limit_for_each_cusp_candidate_label")

    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_label.grid( row=8, column=1)

    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.grid( row=9, column=1)
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.delete( 0, END)
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.insert( 0, str(cusp_app.engine_evaluation_limit_for_each_cusp_candidate) )

    # AI in fight phase, just like normal chess, find the best move.
    cusp_app.engine_one_searching_limit_for_best_move_label = tk.Label( cusp_app.user_setting_window, )
    ui.language.register_widget(cusp_app, cusp_app.engine_one_searching_limit_for_best_move_label, "engine_one_searching_limit_for_best_move_label")
    cusp_app.engine_one_searching_limit_for_best_move_label.grid( row=10, column=1)

    cusp_app.engine_one_searching_limit_for_best_move_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_one_searching_limit_for_best_move_entry.grid( row=11, column=1)
    cusp_app.engine_one_searching_limit_for_best_move_entry.delete(0, END)
    cusp_app.engine_one_searching_limit_for_best_move_entry.insert( 0, str(cusp_app.engine_one_searching_limit_for_best_move) )
    # AI in fight phase, just like normal chess, find the best move.
    cusp_app.engine_two_searching_limit_for_best_move_label = tk.Label( cusp_app.user_setting_window,  )
    ui.language.register_widget(cusp_app, cusp_app.engine_two_searching_limit_for_best_move_label, "engine_two_searching_limit_for_best_move_label")
    cusp_app.engine_two_searching_limit_for_best_move_label.grid( row=12, column=1)

    cusp_app.engine_two_searching_limit_for_best_move_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.engine_two_searching_limit_for_best_move_entry.grid( row=13, column=1)
    cusp_app.engine_two_searching_limit_for_best_move_entry.delete(0, END)
    cusp_app.engine_two_searching_limit_for_best_move_entry.insert( 0, str(cusp_app.engine_two_searching_limit_for_best_move) )

    cusp_app.time_for_each_player_label = tk.Label( cusp_app.user_setting_window,  )
    ui.language.register_widget(cusp_app, cusp_app.time_for_each_player_label, "time_for_each_player_label")
    cusp_app.time_for_each_player_label.grid(row=14, column=1)

    cusp_app.time_for_each_player_entry = ttk.Entry( cusp_app.user_setting_window, width=30, font=("Times", 12) )
    cusp_app.time_for_each_player_entry.grid(row=15, column=1)
    cusp_app.time_for_each_player_entry.delete(0, END)
    cusp_app.time_for_each_player_entry.insert( 0, str(cusp_app.time_for_each_player))

    cusp_app.reset_setting_button = ttk.Button( cusp_app.user_setting_window,  width=39, command=lambda: reset_setting_to_default(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.reset_setting_button, "reset_setting_button")
    cusp_app.reset_setting_button.grid(row=16, column=1)
 

def engine_cusp_outer_range_checkbox_change(cusp_app):
    logger.info("engine_cusp_outer_range_checkbox_change")
    if cusp_app.engine_cusp_outer_range_checkbox_var.get() == 1:
        cusp_app.engine_score_cusp_outer_range_enable = True
    else:
        cusp_app.engine_score_cusp_outer_range_enable = False
    utils.config.save_setting_in_config_file(cusp_app)


def engine_cusp_inner_range_checkbox_change(cusp_app):
    logger.info("engine_cusp_inner_range_checkbox_change")
    if cusp_app.engine_cusp_inner_range_checkbox_var.get() == 1:
        cusp_app.engine_score_cusp_inner_range_enable = True
    else:
        cusp_app.engine_score_cusp_inner_range_enable = False
    utils.config.save_setting_in_config_file(cusp_app)
 
    
def only_engine_one_setup_checkbox_change(cusp_app):
    logger.info("only_engine_one_setup_checkbox_change")
    if cusp_app.only_engine_one_setup_checkbox_var.get() == 1:
        cusp_app.only_engine_one_setup_enable = True
    else:
        cusp_app.only_engine_one_setup_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

def the_other_engine_choose_recommended_color_checkbox_change(cusp_app):
    logger.info("the_other_engine_choose_recommended_color_checkbox_change")
    if cusp_app.the_other_engine_choose_recommended_color_checkbox_var.get() == 1:
        cusp_app.choose_the_recommended_color_enable = True
    else:
        cusp_app.choose_the_recommended_color_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

def no_choosing_color_directly_enable_checkbox_change(cusp_app):
    logger.info("no_choosing_color_directly_enable_checkbox_change")
    if cusp_app.no_choosing_color_directly_enable_checkbox_var.get() == 1:
        cusp_app.no_choosing_color_directly_enable = True
    else:
        cusp_app.no_choosing_color_directly_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

def engine_test_mode_enable_checkbox_change(cusp_app):
    logger.info("engine_test_mode_enable_checkbox_change")
    if cusp_app.engine_test_mode_enable_checkbox_var.get() == 1:
        cusp_app.engine_test_mode_enable = True
        cusp_app.color_to_move_spinbox.config(state="normal")
    else:
        cusp_app.engine_test_mode_enable = False
        cusp_app.color_to_move_spinbox.config(state="disabled")
    utils.config.save_setting_in_config_file(cusp_app)    
  
# there are two Human-level-modes in One-Free move in Cusp Xiangqi, 
# one is relocationg a pawn, 
# the other is relocating a major piece. 
# personally, i think relocating a pawn is better.
   
def cusp_pawn_setup_enable_checkbox_change(cusp_app): 
    logger.info("cusp_pawn_setup_enable_checkbox_change")
    if cusp_app.cusp_pawn_setup_enable_checkbox_var.get() == 1:
        cusp_app.cusp_pawn_setup_enable = True
    else:
        cusp_app.cusp_pawn_setup_enable = False
    utils.config.save_setting_in_config_file(cusp_app)
     
def set_time_limit_or_depth_limit(cusp_app):
    logger.info("set_time_limit_or_depth_limit")
    if cusp_app.time_or_depth_value.get() == 1:
        cusp_app.engine_time_limit_enable = True
    else:
        cusp_app.engine_time_limit_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

def reset_setting_to_default (cusp_app):
    logger.info("reset_setting_to_default")
    reset_all = messagebox.askyesno(parent=cusp_app.user_setting_window, title="Reset all?", message="All settings will be set to default" )
    if reset_all:
        utils.game_state.initalize_basic_setting(cusp_app)
        utils.game_state.user_setting_initialization(cusp_app)            
        utils.config.save_setting_in_config_file(cusp_app)
        ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
        cusp_app.user_setting_window.destroy()
        popup_user_setting(cusp_app)
def UI_for_game_general_setting(cusp_app):
    logger.info("UI_for_game_general_setting")
   # set chess engine legacy_engine_mode
    cusp_app.legacy_engine_mode_radio_value = tk.IntVar()

    cusp_app.modern_engine_mode_radio = tk.Radiobutton( cusp_app.user_setting_window,  variable=cusp_app.legacy_engine_mode_radio_value, command=lambda: set_legacy_engine_mode(cusp_app), value=0, )
    ui.language.register_widget(cusp_app, cusp_app.modern_engine_mode_radio, "modern_engine_mode_radio")
    cusp_app.modern_engine_mode_radio.grid(column=2, row=6)
    # Non-streaming engine – in the context of python-chess, do not support
    # analysis() streaming and only support blocking analyse().
    cusp_app.legacy_engine_mode_radio = tk.Radiobutton( cusp_app.user_setting_window, variable=cusp_app.legacy_engine_mode_radio_value, command=lambda: set_legacy_engine_mode(cusp_app), value=1, )
    ui.language.register_widget(cusp_app, cusp_app.legacy_engine_mode_radio, "legacy_engine_mode_radio")
    cusp_app.legacy_engine_mode_radio.grid(column=2, row=7)

    if cusp_app.legacy_engine_mode:
        cusp_app.legacy_engine_mode_radio_value.set(1)
    else:
        cusp_app.legacy_engine_mode_radio_value.set(0)
        
    # output a PGN file in PGN folder
    cusp_app.output_PGN_checkbox_var = tk.IntVar()
    cusp_app.output_PGN_checkbox = ttk.Checkbutton( cusp_app.user_setting_window,  command=lambda: output_PGN_checkbox_change(cusp_app), variable=cusp_app.output_PGN_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.output_PGN_checkbox, "output_PGN_checkbox")
    cusp_app.output_PGN_checkbox.grid(row=8, column=2)
    if cusp_app.output_PGN_enable:
        cusp_app.output_PGN_checkbox_var.set(1)
    else:
        cusp_app.output_PGN_checkbox_var.set(0)

    cusp_app.pgn_auto_game_variant_detection_var = tk.IntVar()
    cusp_app.pgn_auto_game_variant_detection_checkbox= ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: pgn_auto_game_variant_detection_checkbox_change(cusp_app), variable=cusp_app.pgn_auto_game_variant_detection_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.pgn_auto_game_variant_detection_checkbox, "pgn_auto_game_variant_detection_checkbox")
    cusp_app.pgn_auto_game_variant_detection_checkbox.grid(row=9, column=2)
    if cusp_app.pgn_auto_game_variant_detection:
        cusp_app.pgn_auto_game_variant_detection_var.set(1)
    else:
        cusp_app.pgn_auto_game_variant_detection_var.set(0)
    # play sound when a piece moved
    cusp_app.play_sound_checkbox_var = tk.IntVar()
    cusp_app.play_sound_checkbox = ttk.Checkbutton( cusp_app.user_setting_window,  command=lambda: play_sound_checkbox_change(cusp_app), variable=cusp_app.play_sound_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.play_sound_checkbox, "play_sound_checkbox")
    cusp_app.play_sound_checkbox.grid(row=10, column=2)

    if cusp_app.play_sound_enable:
        cusp_app.play_sound_checkbox_var.set(1)
    else:
        cusp_app.play_sound_checkbox_var.set(0)

    # Eval bars can be disabled.
    cusp_app.eval_bar_checkbox_var = tk.IntVar()
    cusp_app.eval_bar_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: eval_bar_checkbox_change(cusp_app), variable=cusp_app.eval_bar_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.eval_bar_checkbox, "eval_bar_checkbox")
    cusp_app.eval_bar_checkbox.grid(row=11, column=2)

    if cusp_app.eval_show_enable:
        cusp_app.eval_bar_checkbox_var.set(1)
    else:
        cusp_app.eval_bar_checkbox_var.set(0)


    # set player name
    cusp_app.player_one_name_label = tk.Label(cusp_app.user_setting_window, )
    cusp_app.player_one_name_label .grid(row=12, column=2)
    ui.language.register_widget(cusp_app, cusp_app.player_one_name_label, "player_one_name_label")
    cusp_app.player_one_name_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.player_one_name_entry.grid(row=13, column=2)

    cusp_app.player_one_name_entry.delete(0, END)
    cusp_app.player_one_name_entry.insert( 0, str(cusp_app.player_one_name_input) )
    
    cusp_app.player_two_name_label = tk.Label(cusp_app.user_setting_window, )
    cusp_app.player_two_name_label.grid(row=14, column=2)
    ui.language.register_widget(cusp_app, cusp_app.player_two_name_label, "player_two_name_label")
    cusp_app.player_two_name_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.player_two_name_entry.grid(row=15, column=2)

    cusp_app.player_two_name_entry.delete(0, END)
    cusp_app.player_two_name_entry.insert( 0, str(cusp_app.player_two_name_input) )
    
    cusp_app.adjudicator_name_label = tk.Label(cusp_app.user_setting_window, )
    cusp_app.adjudicator_name_label.grid(row=16, column=2)
    ui.language.register_widget(cusp_app, cusp_app.adjudicator_name_label, "adjudicator_name_label")
    cusp_app.adjudicator_name_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.adjudicator_name_entry.grid(row=17, column=2)

    cusp_app.adjudicator_name_entry.delete(0, END)
    cusp_app.adjudicator_name_entry.insert( 0, str(cusp_app.adjudicator_name_input) )
    # Save setting
    cusp_app.setting_ok_button = ttk.Button( cusp_app.user_setting_window, width=30, command=lambda: save_user_setting(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.setting_ok_button, "setting_ok_button")
    cusp_app.setting_ok_button.grid(row=18, column=2)    

  

def set_legacy_engine_mode(cusp_app):
    logger.info("set_legacy_engine_mode")
    if cusp_app.legacy_engine_mode_radio_value.get() == 1:
        cusp_app.legacy_engine_mode = True
    else:
        cusp_app.legacy_engine_mode = False
    utils.config.save_setting_in_config_file(cusp_app)

# output a pgn file in the PGN folder
def output_PGN_checkbox_change(cusp_app):
    logger.info("output_PGN_checkbox_change")
    if cusp_app.output_PGN_checkbox_var.get() == 1:
        cusp_app.output_PGN_enable = True
    else:
        cusp_app.output_PGN_enable = False
    utils.config.save_setting_in_config_file(cusp_app)


def pgn_auto_game_variant_detection_checkbox_change(cusp_app):
    logger.info("pgn_auto_game_variant_detection_checkbox_change")
    if cusp_app.pgn_auto_game_variant_detection_var.get() == 1:
        cusp_app.pgn_auto_game_variant_detection = True
    else:
        cusp_app.pgn_auto_game_variant_detection = False
    utils.config.save_setting_in_config_file(cusp_app)
# sound when move a piece
def play_sound_checkbox_change(cusp_app):
    logger.info("play_sound_checkbox_change")
    if cusp_app.play_sound_checkbox_var.get() == 1:
        cusp_app.play_sound_enable = True
    else:
        cusp_app.play_sound_enable = False
    utils.config.save_setting_in_config_file(cusp_app)


# disable eval bar?
def eval_bar_checkbox_change(cusp_app):
    logger.info("eval_bar_checkbox_change")
    if cusp_app.eval_bar_checkbox_var.get() == 1:
        cusp_app.eval_show_enable = True
    else:
        cusp_app.eval_show_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

     
        
def save_user_setting(cusp_app):
    logger.info("save_user_setting")
    save_inputs_on_setting_panel(cusp_app)
    show_inputs_on_setting_panel(cusp_app)
    


def save_inputs_on_setting_panel(cusp_app):
    logger.info("save_inputs_on_setting_panel")
    if cusp_app.maximum_ply_before_setup_entry.get() != "":
        try:
            cusp_app.maximum_ply_before_setup = int( cusp_app.maximum_ply_before_setup_entry.get() )
            if cusp_app.maximum_ply_before_setup < 0:
                cusp_app.maximum_ply_before_setup = 0
        except Exception as e:
            logger.exception("cusp_app.maximum_ply_before_setup_entry error")
            messagebox.showerror("Error", f"Maximum plies for Safe Moves must be a number: {e}" )

    if cusp_app.engine_score_difference_maximum_entry.get() != "":
        try:
            cusp_app.engine_score_difference_maximum = float( cusp_app.engine_score_difference_maximum_entry.get() )
            if cusp_app.engine_score_difference_maximum < 0.01:
                cusp_app.engine_score_difference_maximum = 0.01

            elif cusp_app.engine_score_difference_maximum > 10:
                cusp_app.engine_score_difference_maximum = 10

        except Exception as e:
            logger.exception("cusp_app.engine_score_difference_maximum_entry error")
            messagebox.showerror("Error", f"Score difference upper bound must be a number: {e}" )
    if cusp_app.engine_score_difference_minimum_entry.get() != "":
        try:
            cusp_app.engine_score_difference_minimum = float( cusp_app.engine_score_difference_minimum_entry.get() )
            if cusp_app.engine_score_difference_minimum < 0:
                cusp_app.engine_score_difference_minimum = 0
            if ( cusp_app.engine_score_difference_minimum + 0.01 > cusp_app.engine_score_difference_maximum ):
                cusp_app.engine_score_difference_minimum = 0

        except Exception as e:
            logger.exception("cusp_app.engine_score_difference_minimum_entry error")
            messagebox.showerror("Error", f"Score difference lower bound must be a number: {e}" )

    if cusp_app.engine_safe_move_score_maximum_entry.get() != "":
        try:
            cusp_app.engine_safe_move_score_maximum = float( cusp_app.engine_safe_move_score_maximum_entry.get() )
            if ( cusp_app.engine_safe_move_score_maximum <0.2 ):
                cusp_app.engine_safe_move_score_maximum = 0.2
        except Exception as e:
            logger.exception("cusp_app.engine_safe_move_score_maximum error")
            messagebox.showerror("Error", f"Maximum of safe move score must be a number: {e}" )


    if cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.get() != "":
        try:
            cusp_app.engine_evaluation_limit_for_each_cusp_candidate = float( cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.get())
            if cusp_app.engine_time_limit_enable:
                if cusp_app.engine_evaluation_limit_for_each_cusp_candidate < 0.01:
                    cusp_app.engine_evaluation_limit_for_each_cusp_candidate = 0.01
            else:
                if cusp_app.engine_evaluation_limit_for_each_cusp_candidate < 1:
                    cusp_app.engine_evaluation_limit_for_each_cusp_candidate = 1
        except Exception as e:
            logger.exception( "cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry error" )
            messagebox.showerror("Error", f"Engine evaluation search limit be a number: {e}" )
    if cusp_app.engine_one_searching_limit_for_best_move_entry.get() != "":
        try:
            cusp_app.engine_one_searching_limit_for_best_move = float( cusp_app.engine_one_searching_limit_for_best_move_entry.get() )
            if cusp_app.engine_time_limit_enable:
                if cusp_app.engine_one_searching_limit_for_best_move < 0.01:
                    cusp_app.engine_one_searching_limit_for_best_move = 0.01
            else:
                if cusp_app.engine_one_searching_limit_for_best_move < 1:
                    cusp_app.engine_one_searching_limit_for_best_move = 1
        except Exception as e:
            logger.exception("cusp_app.engine_one_searching_limit_for_best_move_entry error")
            messagebox.showerror("Error", f"Search limit for player one must be a number: {e}" )
    if cusp_app.engine_two_searching_limit_for_best_move_entry.get() != "":
        try:
            cusp_app.engine_two_searching_limit_for_best_move = float( cusp_app.engine_two_searching_limit_for_best_move_entry.get() )
            if cusp_app.engine_time_limit_enable:
                if cusp_app.engine_two_searching_limit_for_best_move < 0.01:
                    cusp_app.engine_two_searching_limit_for_best_move = 0.01
            else:
                if cusp_app.engine_two_searching_limit_for_best_move < 1:
                    cusp_app.engine_two_searching_limit_for_best_move = 1
        except Exception as e:
            logger.exception("cusp_app.engine_two_searching_limit_for_best_move_entry error")
            messagebox.showerror("Error", f"Search limit for player two must be a number: {e}" )
    if cusp_app.time_for_each_player_entry.get() != "":
        try:
            cusp_app.time_for_each_player = int( cusp_app.time_for_each_player_entry.get() )
            if cusp_app.time_for_each_player < 5:
                cusp_app.time_for_each_player = 5


        except Exception as e:
            logger.exception("cusp_app.time_for_each_player_entry error")
            messagebox.showerror("Error", f"Time must be a number: {e}" )
   
    try:
        cusp_app.player_one_name_input = str( cusp_app.player_one_name_entry.get() )
        if len(cusp_app.player_one_name_input) > 30:
            cusp_app.player_one_name_input = cusp_app.player_one_name_input[:30]
    except Exception as e:
        logger.exception("cusp_app.player_one_name_entry error")
        messagebox.showerror("Error", f"Input player one name: {e}" )
   
    try:
        cusp_app.player_two_name_input = str( cusp_app.player_two_name_entry.get() )
        if len(cusp_app.player_two_name_input) > 30:
            cusp_app.player_two_name_input = cusp_app.player_two_name_input[:30]
    except Exception as e:
        logger.exception("cusp_app.player_two_name_entry error")
        messagebox.showerror("Error", f"Input player two name: {e}" )
    try:
        cusp_app.adjudicator_name_input = str( cusp_app.adjudicator_name_entry.get() )
        if len(cusp_app.adjudicator_name_input) > 30:
            cusp_app.adjudicator_name_input = cusp_app.adjudicator_name_input[:30]
    except Exception as e:
        logger.exception("cusp_app.adjudicator_name_input error")
        messagebox.showerror("Error", f"Input adjudicator name: {e}" )


    if cusp_app.tournament_game_number_entry.get() != "":
        try:
            cusp_app.tournament_game_number = int( cusp_app.tournament_game_number_entry.get() )
            if cusp_app.tournament_game_number < 0:
                cusp_app.tournament_game_number = 0
        except Exception as e:
            logger.exception("tournament_game_number error")
            messagebox.showerror("Error", f"Tournament game number must be a number: {e}" )
    if cusp_app.game_early_stop_entry.get() != "":
        try:
            cusp_app.game_early_stop_score_difference = float( cusp_app.game_early_stop_entry.get() )
            if cusp_app.game_early_stop_score_difference > 0.8:
                cusp_app.game_early_stop_score_difference = 0.8

            elif cusp_app.game_early_stop_score_difference < 0.1:
                cusp_app.game_early_stop_score_difference = 0.1

        except Exception as e:
            logger.exception("cusp_app.game_early_stop_score_difference error")
            messagebox.showerror("Error", f"Score difference for early stop must be a number: {e}" )
    if cusp_app.game_early_stop_minimum_moves_entry.get() != "":
        try:
            cusp_app.game_early_stop_minimum_moves = int( cusp_app.game_early_stop_minimum_moves_entry.get() )
            if cusp_app.game_early_stop_minimum_moves < 0:
                cusp_app.game_early_stop_minimum_moves = 0

        except Exception as e:
            logger.exception("cusp_app.game_early_stop_minimum_moves error")
            messagebox.showerror("Error", f"Minimum move for early stop must be a number: {e}" )
    utils.config.save_setting_in_config_file(cusp_app)

def show_inputs_on_setting_panel(cusp_app):
    logger.info("show_inputs_on_setting_panel")
    # show the result
    cusp_app.maximum_ply_before_setup_entry.delete(0, END)
    cusp_app.maximum_ply_before_setup_entry.insert( 0, str(cusp_app.maximum_ply_before_setup) )

    cusp_app.engine_score_difference_maximum_entry.delete(0, END)
    cusp_app.engine_score_difference_maximum_entry.insert( 0, str(cusp_app.engine_score_difference_maximum) )

    cusp_app.engine_score_difference_minimum_entry.delete(0, END)
    cusp_app.engine_score_difference_minimum_entry.insert( 0, str(cusp_app.engine_score_difference_minimum) )

    cusp_app.engine_safe_move_score_maximum_entry.delete(0, END)
    cusp_app.engine_safe_move_score_maximum_entry.insert( 0, str(cusp_app.engine_safe_move_score_maximum) )

    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.delete( 0, END)
    cusp_app.engine_evaluation_limit_for_each_cusp_candidate_entry.insert( 0, str(cusp_app.engine_evaluation_limit_for_each_cusp_candidate) )

    cusp_app.engine_one_searching_limit_for_best_move_entry.delete(0, END)
    cusp_app.engine_one_searching_limit_for_best_move_entry.insert( 0, str(cusp_app.engine_one_searching_limit_for_best_move) )

    cusp_app.engine_two_searching_limit_for_best_move_entry.delete(0, END)
    cusp_app.engine_two_searching_limit_for_best_move_entry.insert( 0, str(cusp_app.engine_two_searching_limit_for_best_move) )
    cusp_app.time_for_each_player_entry.delete(0, END)
    cusp_app.time_for_each_player_entry.insert( 0, str(cusp_app.time_for_each_player))

    cusp_app.player_one_name_entry.delete(0, END)
    cusp_app.player_one_name_entry.insert( 0, str(cusp_app.player_one_name_input))

    cusp_app.player_two_name_entry.delete(0, END)
    cusp_app.player_two_name_entry.insert( 0, str(cusp_app.player_two_name_input))

    cusp_app.adjudicator_name_entry.delete(0, END)
    cusp_app.adjudicator_name_entry.insert( 0, str(cusp_app.adjudicator_name_input))

    cusp_app.tournament_game_number_entry.delete(0, END)
    cusp_app.tournament_game_number_entry.insert( 0, str(cusp_app.tournament_game_number) )

    cusp_app.game_early_stop_entry.delete(0, END)
    cusp_app.game_early_stop_entry.insert( 0, str(cusp_app.game_early_stop_score_difference) )

    cusp_app.game_early_stop_minimum_moves_entry.delete(0, END)
    cusp_app.game_early_stop_minimum_moves_entry.insert( 0, str(cusp_app.game_early_stop_minimum_moves) )
 
# This is the simplest tournament. Engine one is always white player and engine two is black player.
# In Cusp Chess, no problem, because they may swap side in Fight phase.  
def UI_for_tournament_setting(cusp_app):
    logger.info("UI_for_tournament_setting")
    cusp_app.tournament_game_number_label = tk.Label( cusp_app.user_setting_window,)
    ui.language.register_widget(cusp_app, cusp_app.tournament_game_number_label, "tournament_game_number_label")
    cusp_app.tournament_game_number_label.grid(row=6, column=3)

    cusp_app.tournament_game_number_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.tournament_game_number_entry.grid(row=7, column=3)
    cusp_app.tournament_game_number_entry.delete(0, END)
    cusp_app.tournament_game_number_entry.insert( 0, str(cusp_app.tournament_game_number) )

    cusp_app.game_early_stop_draw_checkbox_var = tk.IntVar()
    cusp_app.game_early_stop_draw_checkbox = ttk.Checkbutton( cusp_app.user_setting_window,  command=lambda: game_early_stop_draw_checkbox_var_change(cusp_app), variable=cusp_app.game_early_stop_draw_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.game_early_stop_draw_checkbox, "game_early_stop_draw_checkbox")
    cusp_app.game_early_stop_draw_checkbox.grid(row=8, column=3)

    if cusp_app.game_early_stop_draw_enable:
        cusp_app.game_early_stop_draw_checkbox_var.set(1)
    else:
        cusp_app.game_early_stop_draw_checkbox_var.set(0)

    cusp_app.game_early_stop_win_checkbox_var = tk.IntVar()
    cusp_app.game_early_stop_win_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: game_early_stop_win_checkbox_var_change(cusp_app), variable=cusp_app.game_early_stop_win_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.game_early_stop_win_checkbox, "game_early_stop_win_checkbox")
    cusp_app.game_early_stop_win_checkbox.grid(row=9, column=3)

    if cusp_app.game_early_stop_win_enable:
        cusp_app.game_early_stop_win_checkbox_var.set(1)
    else:
        cusp_app.game_early_stop_win_checkbox_var.set(0)

    cusp_app.game_early_stop_label = tk.Label( cusp_app.user_setting_window,)
    ui.language.register_widget(cusp_app, cusp_app.game_early_stop_label, "game_early_stop_label")
    cusp_app.game_early_stop_label.grid(row=10, column=3)

    cusp_app.game_early_stop_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.game_early_stop_entry.grid(row=11, column=3)
    cusp_app.game_early_stop_entry.delete(0, END)
    cusp_app.game_early_stop_entry.insert( 0, str(cusp_app.game_early_stop_score_difference) )

    cusp_app.game_early_stop_minimum_moves_label = tk.Label( cusp_app.user_setting_window, )
    ui.language.register_widget(cusp_app, cusp_app.game_early_stop_minimum_moves_label, "game_early_stop_minimum_moves_label")
    cusp_app.game_early_stop_minimum_moves_label.grid(row=12, column=3)

    cusp_app.game_early_stop_minimum_moves_entry = ttk.Entry( cusp_app.user_setting_window, width=23, font=("Times", 12) )
    cusp_app.game_early_stop_minimum_moves_entry.grid(row=13, column=3)
    cusp_app.game_early_stop_minimum_moves_entry.delete(0, END)
    cusp_app.game_early_stop_minimum_moves_entry.insert( 0, str(cusp_app.game_early_stop_minimum_moves) )

    cusp_app.adjudicator_engine_enable_checkbox_var = tk.IntVar()
    cusp_app.adjudicator_engine_enable_checkbox = ttk.Checkbutton( cusp_app.user_setting_window, command=lambda: adjudicator_engine_enable_checkbox_change(cusp_app), variable=cusp_app.adjudicator_engine_enable_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.adjudicator_engine_enable_checkbox, "adjudicator_engine_enable_checkbox")
    cusp_app.adjudicator_engine_enable_checkbox.grid(row=14, column=3)
    if cusp_app.adjudicator_engine_enable:
        cusp_app.adjudicator_engine_enable_checkbox_var.set(1)
    else:
        cusp_app.adjudicator_engine_enable_checkbox_var.set(0)

    cusp_app.tournament_start_button = ttk.Button( cusp_app.user_setting_window,  width=30, command=lambda: utils.tournament.start_tournament(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.tournament_start_button, "tournament_start_button")
    cusp_app.tournament_start_button.grid(row=15, column=3)

    cusp_app.tournament_stop_button = ttk.Button( cusp_app.user_setting_window, width=30, command=lambda: utils.tournament.stop_tournament(cusp_app), )
    ui.language.register_widget(cusp_app, cusp_app.tournament_stop_button, "stop_tournament")
    cusp_app.tournament_stop_button.grid(row=16, column=3)

# early stop if the game is going to draw.
# check utils.game_results.check_early_stop_results for more details.

def game_early_stop_draw_checkbox_var_change(cusp_app):
    logger.info("game_early_stop_draw_checkbox_var_change")
    if cusp_app.game_early_stop_draw_checkbox_var.get() == 1:
        cusp_app.game_early_stop_draw_enable = True
    else:
        cusp_app.game_early_stop_draw_enable = False

# early stop if a color is going to win.
# check utils.game_results.check_early_stop_results for more details.
def game_early_stop_win_checkbox_var_change(cusp_app):
    logger.info("game_early_stop_win_checkbox_var_change")
    if cusp_app.game_early_stop_win_checkbox_var.get() == 1:
        cusp_app.game_early_stop_win_enable = True
    else:
        cusp_app.game_early_stop_win_enable = False


def adjudicator_engine_enable_checkbox_change(cusp_app):
    logger.info("adjudicator_engine_enable_checkbox_change")
    if cusp_app.adjudicator_engine_enable_checkbox_var.get() == 1:
        cusp_app.adjudicator_engine_enable = True
    else:
        cusp_app.adjudicator_engine_enable = False
    utils.config.save_setting_in_config_file(cusp_app)

def UI_game_play_setting(cusp_app):
    logger.info("UI_game_play_setting")
    cusp_app.game_player_setting_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.game_player_setting_frame.grid( column=2, row=1, sticky="wens")

    cusp_app.start_game_button = tk.Button( cusp_app.game_player_setting_frame,  command=cusp_app.start_game, width=13, )
    ui.language.register_widget(cusp_app, cusp_app.start_game_button, "start_game_button")
    cusp_app.start_game_button.grid(column=0, row=6)

    cusp_app.stop_game_button = tk.Button( cusp_app.game_player_setting_frame,command=cusp_app.stop_game, width=13, )
    ui.language.register_widget(cusp_app, cusp_app.stop_game_button, "stop_game_button")
    cusp_app.stop_game_button.grid(column=0, row=7)

    # cusp_app.stop_tournament_button_two = tk.Button( cusp_app.game_player_setting_frame,command=lambda: utils.tournament.stop_tournament(cusp_app), width=13, )
    # ui.language.register_widget(cusp_app, cusp_app.stop_tournament_button_two, "stop_tournament")
    # cusp_app.stop_tournament_button_two.grid(column=0, row=8)
    
    cusp_app.reset_game_button = tk.Button( cusp_app.game_player_setting_frame, command=cusp_app.reset, width=13, )
    ui.language.register_widget(cusp_app, cusp_app.reset_game_button, "reset_game_button")
    cusp_app.reset_game_button.grid(column=0, row=8)
    # user adjudication
    cusp_app.adjudicator_zero_to_one_button = tk.Button( cusp_app.game_player_setting_frame, text="0-1", command=lambda: adjudicator_zero_to_one(cusp_app), width=13, )

    cusp_app.adjudicator_zero_to_one_button.grid(column=1, row=6)

    cusp_app.adjudicator_draw_button = tk.Button( cusp_app.game_player_setting_frame, text="1/2-1/2", command=lambda: adjudicator_draw(cusp_app), width=13, )
    cusp_app.adjudicator_draw_button.grid(column=1, row=7)

    cusp_app.adjudicator_one_to_zero_button = tk.Button( cusp_app.game_player_setting_frame, text="1-0", command=lambda: adjudicator_one_to_zero(cusp_app), width=13, )
    cusp_app.adjudicator_one_to_zero_button.grid(column=1, row=8)

    cusp_app.chess_game_variant_mode_value = tk.IntVar()

    cusp_app.chess_radio = tk.Radiobutton( cusp_app.game_player_setting_frame,variable=cusp_app.chess_game_variant_mode_value, command=lambda: chess_game_variant_mode_change(cusp_app), value=1, )
    ui.language.register_widget(cusp_app, cusp_app.chess_radio, "chess_radio")
    cusp_app.chess_radio.grid(column=0, row=0, columnspan=2)

    cusp_app.cusp_chess_radio = tk.Radiobutton( cusp_app.game_player_setting_frame, variable=cusp_app.chess_game_variant_mode_value, command=lambda: chess_game_variant_mode_change(cusp_app), value=2, )
    ui.language.register_widget(cusp_app, cusp_app.cusp_chess_radio, "cusp_chess_radio")
    cusp_app.cusp_chess_radio.grid(column=0, row=1, columnspan=2)

    if cusp_app.chess_game_variant_mode == "Normal":
        cusp_app.chess_game_variant_mode_value.set(1)
    elif cusp_app.chess_game_variant_mode == "CuspXiangqi":
        cusp_app.chess_game_variant_mode_value.set(2)

    cusp_app.basic_setting_separator = ttk.Separator( cusp_app.game_player_setting_frame, orient="horizontal" )
    cusp_app.basic_setting_separator.grid( column=0, row=3, columnspan=2, ipadx=100)

    cusp_app.player_one_label = ttk.Label( cusp_app.game_player_setting_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_one_logo, font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.player_one_label, "player_one_label")
    cusp_app.player_one_label.grid(column=0, row=4)

    cusp_app.player_two_label = ttk.Label( cusp_app.game_player_setting_frame, justify=LEFT, compound=LEFT, image=cusp_app.play_two_logo, font=("Times", 12), )
    ui.language.register_widget(cusp_app, cusp_app.player_two_label, "player_two_label")
    cusp_app.player_two_label.grid(column=1, row=4)

    # AI players or human players
    #players = ("AI", "Human")
    players=(cusp_app.translations[cusp_app.current_lang]["AI"],cusp_app.translations[cusp_app.current_lang]["Human"])
    
    cusp_app.player_one_spinbox_var = StringVar()
    cusp_app.player_one_spinbox = Spinbox( cusp_app.game_player_setting_frame, values=players, textvariable=cusp_app.player_one_spinbox_var, width=13, wrap=True, )
    cusp_app.player_one_spinbox.grid(column=0, row=5)

    cusp_app.player_one_spinbox_var.set(players[0])

    cusp_app.player_two_spinbox_var = StringVar()
    cusp_app.player_two_spinbox = Spinbox( cusp_app.game_player_setting_frame, values=players, textvariable=cusp_app.player_two_spinbox_var, width=13, wrap=True, )
    cusp_app.player_two_spinbox.grid(column=1, row=5)

    cusp_app.player_two_spinbox_var.set(players[0])

    for widget in cusp_app.game_player_setting_frame.winfo_children():
        widget.grid(padx=10, pady=5)

# Set which game we are going to play: Normal chess, Cusp Chess
def chess_game_variant_mode_change(cusp_app):
    logger.info("chess_game_variant_mode_change")
    if cusp_app.chess_game_variant_mode_value.get() == 1:
        cusp_app.stop_game()
        cusp_app.board = cchess.Board()

        cusp_app.chess_game_variant_mode = "Normal"
        ui.normalboard.redraw_chess_board(cusp_app)
        ui.ui_utils.initialize_piece_images( cusp_app, cusp_app.chess_game_variant_mode)

        cusp_app.game_status_label_state='game_status_label_ready'
        ui.language.update_widget(cusp_app,cusp_app.game_status_label)
    elif cusp_app.chess_game_variant_mode_value.get() == 2:
        cusp_app.stop_game()
        cusp_app.board = cchess.Board()

        cusp_app.chess_game_variant_mode = "CuspXiangqi"
        ui.normalboard.redraw_chess_board(cusp_app)
        ui.ui_utils.initialize_piece_images( cusp_app, cusp_app.chess_game_variant_mode)
        cusp_app.game_status_label_state='game_status_label_ready_CC'
        ui.language.update_widget(cusp_app,cusp_app.game_status_label)

    cusp_app.chess_game_variant_mode_saved = cusp_app.chess_game_variant_mode
    utils.config.save_setting_in_config_file(cusp_app)


def adjudicator_zero_to_one(cusp_app):
    logger.info("adjudicator_zero_to_one")
    ui.ui_utils.clear_board_move_history(cusp_app)
    cusp_app.user_adjudicator_result = "0-1"
    utils.game_results.check_game_result(cusp_app)
  
def adjudicator_draw(cusp_app):
    logger.info("adjudicator_draw")
    ui.ui_utils.clear_board_move_history(cusp_app)
    cusp_app.user_adjudicator_result = "1/2-1/2"
    utils.game_results.check_game_result(cusp_app)

def adjudicator_one_to_zero(cusp_app):
    logger.info("adjudicator_one_to_zero")
    ui.ui_utils.clear_board_move_history(cusp_app)
    cusp_app.user_adjudicator_result = "1-0"
    utils.game_results.check_game_result(cusp_app)

def UI_PGN_setting(cusp_app):
    logger.info("UI_PGN_setting")
    cusp_app.PGNboard_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.PGNboard_frame.grid(column=2, row=2, sticky="wens")

    cusp_app.pgn_separator = ttk.Separator( cusp_app.PGNboard_frame, orient="horizontal")
    cusp_app.pgn_separator.grid(column=0, row=0, columnspan=2, ipadx=100)

    cusp_app.load_PGN_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: utils.pgnhistory.load_PGN(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.load_PGN_button, "load_PGN_button")
    cusp_app.load_PGN_button.grid(column=0, row=1)

    cusp_app.play_PGN_previous_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: utils.pgnhistory.play_PGN_previous(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.play_PGN_previous_button, "play_PGN_previous_button")
    cusp_app.play_PGN_previous_button.grid(column=0, row=2)

    cusp_app.play_PGN_next_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: utils.pgnhistory.play_PGN_next(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.play_PGN_next_button, "play_PGN_next_button")
    cusp_app.play_PGN_next_button.grid(column=1, row=1)

    cusp_app.beginning_PGN_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: utils.pgnhistory.PGN_back_to_beginning(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.beginning_PGN_button, "beginning_PGN_button")
    cusp_app.beginning_PGN_button.grid(column=0, row=3)

    cusp_app.auto_play_PGN_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: utils.pgnhistory.auto_play_PGN_function(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.auto_play_PGN_button, key=lambda:ui.language.pgn_auto_play_label_dynamic_key(cusp_app))
    cusp_app.auto_play_PGN_button.grid(column=1, row=2)

    cusp_app.clear_history_button = tk.Button( cusp_app.PGNboard_frame, command=lambda: ui.ui_utils.clear_scrolltext_move_history(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.clear_history_button, "clear_history_button")
    cusp_app.clear_history_button.grid(column=1, row=3)

    for widget in cusp_app.PGNboard_frame.winfo_children():
        widget.grid(padx=10, pady=5)


def UI_move_history(cusp_app):
    logger.info("UI_move_history")
    cusp_app.move_history_frame = ttk.Frame(cusp_app.chess_container)

    cusp_app.move_history_frame.grid(column=1, row=0, rowspan=8, sticky="wens")
    cusp_app.move_history_label = ttk.Label( cusp_app.move_history_frame, font=("Times", 12) )
    cusp_app.move_history_label.pack()
    ui.language.register_widget(cusp_app, cusp_app.move_history_label, "move_history_label")
    cusp_app.move_history_text = scrolledtext.ScrolledText( cusp_app.move_history_frame, width=30, height=40, font=("Times", 12))
    cusp_app.move_history_text.pack(fill=BOTH, side=LEFT, expand=True)


# When setting up a Cusp Position, a player must set which color to move and which color must win.
# If a player chooses a color directly, he can only set which color must win.

def UI_cusp_chess_setup(cusp_app):
    logger.info("UI_cusp_chess_setup")
    cusp_app.cusp_chess_setting_frame = ttk.Frame(cusp_app.chess_container)
    cusp_app.cusp_chess_setting_frame.grid( column=2, row=0, sticky="wens")

    cusp_app.setup_label_CC = ttk.Label( cusp_app.cusp_chess_setting_frame, font=("Times", 12), )
    cusp_app.setup_label_CC.grid(column=0, columnspan=2, row=0)
    ui.language.register_widget(cusp_app, cusp_app.setup_label_CC, "setup_label_CC")
    
    separator = ttk.Separator( cusp_app.cusp_chess_setting_frame, orient="horizontal")
    separator.grid(column=0, row=1, columnspan=2, ipadx=100)
    # when a human player sets up a Cusp Position, he/she needs to set the
    # color-to-move and color-must-win
    cusp_app.setup_CC_color_to_move = ttk.Label( cusp_app.cusp_chess_setting_frame, font=( "Times", 12))
    cusp_app.setup_CC_color_to_move.grid( column=0, row=2)
    ui.language.register_widget(cusp_app, cusp_app.setup_CC_color_to_move, "setup_CC_color_to_move")
    
    cusp_app.setup_CC_color_must_win = ttk.Label( cusp_app.cusp_chess_setting_frame, font=( "Times", 12))
    cusp_app.setup_CC_color_must_win.grid( column=1, row=2)
    ui.language.register_widget(cusp_app, cusp_app.setup_CC_color_must_win, "setup_CC_color_must_win")
    
    #side = ("White", "Black")
    side=(cusp_app.translations[cusp_app.current_lang]["white"],cusp_app.translations[cusp_app.current_lang]["black"])
    
    cusp_app.color_to_move_spinbox_var = StringVar()
    cusp_app.color_to_move_spinbox = Spinbox( cusp_app.cusp_chess_setting_frame, values=side, textvariable=cusp_app.color_to_move_spinbox_var, width=13, wrap=True, )
    cusp_app.color_to_move_spinbox.grid(column=0, row=3)
    v = side[0]
    cusp_app.color_to_move_spinbox_var.set(v)

    if cusp_app.engine_test_mode_enable:
        cusp_app.color_to_move_spinbox.config(state="normal")
    else:
        cusp_app.color_to_move_spinbox.config(state="disabled")
        
    cusp_app.color_must_win_spinbox_var = StringVar()
    cusp_app.color_must_win_spinbox = Spinbox( cusp_app.cusp_chess_setting_frame, values=side, textvariable=cusp_app.color_must_win_spinbox_var, width=13, wrap=True, )
    cusp_app.color_must_win_spinbox.grid(column=1, row=3)
    v = side[0]
    cusp_app.color_must_win_spinbox_var.set(v)

    # the setup confirmation checkbox let human player tell the program he/she
    # is setting up a Cusp Position when he/she presss move-finished button
    cusp_app.Human_setup_confirmation_checkbox_var = tk.IntVar()
    cusp_app.Human_setup_confirmation_checkbox = ttk.Checkbutton( cusp_app.cusp_chess_setting_frame, command=lambda: Human_setup_confirmation_check_changed(cusp_app), variable=cusp_app.Human_setup_confirmation_checkbox_var, onvalue=1, offvalue=0, )
    ui.language.register_widget(cusp_app, cusp_app.Human_setup_confirmation_checkbox, "Human_setup_confirmation_checkbox")
    cusp_app.Human_setup_confirmation_checkbox.grid(column=0, row=4)
    cusp_app.Human_setup_confirmation_checkbox_var.set(0)

    # When playing Cusp Chess, a player can set up a Cusp Position by his move.
    # So it is nacessary to tell his/her opponent: it is your turn now(choose a color or make a move).
    # When playing Cusp Chess in person, you can just press the timer button.
    cusp_app.Human_move_finished_button = tk.Button( cusp_app.cusp_chess_setting_frame, command=lambda: Human_move_finished_confirmation(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.Human_move_finished_button, "Human_move_finished_button")
    cusp_app.Human_move_finished_button.grid(column=0, row=5)
    # when choosing a color directly, a player can only set the color must
    # win, and he/she will play as the color.
    cusp_app.Human_directly_choose_button = tk.Button( cusp_app.cusp_chess_setting_frame, command=lambda: Human_choose_color_directly(cusp_app), width=13, )
    ui.language.register_widget(cusp_app, cusp_app.Human_directly_choose_button, "Human_directly_choose_button")
    cusp_app.Human_directly_choose_button.grid(column=1, row=5)

    cusp_app.cusp_separator = ttk.Separator( cusp_app.cusp_chess_setting_frame, orient="horizontal" )
    cusp_app.cusp_separator.grid(column=0, row=6, columnspan=2, ipadx=100)

    for widget in cusp_app.cusp_chess_setting_frame.winfo_children():
        widget.grid(padx=10, pady=5)
    # checkbox for human to set up a Cusp Position
    # get the color-to-move and color-must-win.

def Human_setup_confirmation_check_changed(cusp_app):
    logger.info("Human_setup_confirmation_check_changed")
    if cusp_app.Human_setup_confirmation_checkbox_var.get() == 1:
        cusp_app.Human_setup = True
        if cusp_app.engine_test_mode_enable:
            if cusp_app.translations[cusp_app.current_lang]["white"]== cusp_app.color_to_move_spinbox_var.get():
                cusp_app.Human_setup_color_to_move = "White"
                cusp_app.color_to_move_spinbox_chosen=0
            else:
                cusp_app.Human_setup_color_to_move = "Black"
                cusp_app.color_to_move_spinbox_chosen=1
            
        if cusp_app.translations[cusp_app.current_lang]["white"]== cusp_app.color_must_win_spinbox_var.get():
            cusp_app.Human_setup_color_must_win = "White"
            cusp_app.color_must_win_spinbox_chosen=0
        else:
            cusp_app.Human_setup_color_must_win = "Black"    
            cusp_app.color_must_win_spinbox_chosen=1
            
        logger.info(f"Human_setup {cusp_app.Human_setup}, Human_setup_color_to_move {cusp_app.Human_setup_color_to_move}, Human_setup_color_must_win {cusp_app.Human_setup_color_must_win}")
    else:
        cusp_app.Human_setup = False



# human player must press the button when in Safe Move Phase and Decision Phase.
# In Safe Move Phase, it let the opponent move
# In Decision Phase, it let the opponent choose a color. But he/she needs to
# check the Human_setup_confirmation_checkbox first.


def Human_move_finished_confirmation(cusp_app):
    logger.info("Human_move_finished_confirmation")
    cusp_chess_player_one_turn = ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.board.turn )

    cusp_chess_player_two_turn = ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and not cusp_app.board.turn )

    if ( ( cusp_app.player_one == "Human" and cusp_chess_player_one_turn  ) or ( cusp_app.player_two == "Human" and  cusp_chess_player_two_turn ) ) and cusp_app.cusp_chess_phase == "SafeMove":
        if cusp_app.Human_setup:
            cusp_app.Human_must_set_up = False
            # get the color-to-move and color-must-win.        
            if cusp_app.engine_test_mode_enable:
                if cusp_app.translations[cusp_app.current_lang]["white"]== cusp_app.color_to_move_spinbox_var.get():
                    cusp_app.Human_setup_color_to_move = "White"
                    cusp_app.color_to_move_spinbox_chosen=0
                else:
                    cusp_app.Human_setup_color_to_move = "Black"
                    cusp_app.color_to_move_spinbox_chosen=1
                
            if cusp_app.translations[cusp_app.current_lang]["white"]== cusp_app.color_must_win_spinbox_var.get():
                cusp_app.Human_setup_color_must_win = "White"
                cusp_app.color_must_win_spinbox_chosen=0
            else:
                cusp_app.Human_setup_color_must_win = "Black"    
                cusp_app.color_must_win_spinbox_chosen=1
            # for notation                  
            cusp_app.setting_up_in_cusp_chess = True
            # because the board turn is unchanged, even when a move pushed.

            if cusp_app.board.turn:
                cusp_app.active_color_in_cusp_setup = "W"
            else:
                cusp_app.active_color_in_cusp_setup = "B"

            # let opponent choose a color
            cusp_app.cusp_chess_phase = "Decision"

            if cusp_app.Human_setup_color_must_win == "White":
                cusp_app.color_must_win_in_cusp_chess = "W"
            elif cusp_app.Human_setup_color_must_win == "Black":
                cusp_app.color_must_win_in_cusp_chess = "B"


            cusp_app.choose_color_directly = False
            if not cusp_app.engine_test_mode_enable:
                if cusp_app.board.turn:
                    cusp_app.color_to_move_in_fight_phase = "B"
                else:
                    cusp_app.color_to_move_in_fight_phase = "W"
                cusp_app.board.turn= 1^cusp_app.board.turn   
            else:  
                if cusp_app.Human_setup_color_to_move == "White":
                    cusp_app.color_to_move_in_fight_phase = "W"
                elif cusp_app.Human_setup_color_to_move == "Black":
                    cusp_app.color_to_move_in_fight_phase = "B"
            # True means active setup  
            utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)

            # set board turn first, and then let the opponent choose on color
            if cusp_app.engine_test_mode_enable:
                if cusp_app.Human_setup_color_to_move == "White":
                    cusp_app.board.turn = True
                elif cusp_app.Human_setup_color_to_move == "Black":
                    cusp_app.board.turn = False
            ui.ui_utils.update_color_to_move_label(cusp_app)

            logger.info( f"human sets up a fight starting position, color to move { cusp_app.color_to_move_in_fight_phase} and color_must_win_in_cusp_chess { cusp_app.color_must_win_in_cusp_chess}")
            logger.info(cusp_app.board.fen())
            # reset
            if cusp_app.chess_game_variant_mode == "CuspXiangqi":
                cusp_app.human_no_move_this_round = True
            ui.ui_utils.update_game_status_label( cusp_app, )

            # one human player and one AI player
            if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
                cusp_app.safe_move_or_setup_in_cusp_chess()
            # two human players
            elif cusp_app.game_player_mode == "HvH":
                human_player_choose_color(cusp_app)
        # just a Safe Move in Safe Move Phase
        elif cusp_app.Human_must_set_up == False and cusp_app.Human_setup == False:
            utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)
            # change board turn and add board ply number
            move = cchess.Move.from_uci("0000")
            cusp_app.board.push(move)
            ui.ui_utils.update_color_to_move_label(cusp_app)
            if cusp_app.chess_game_variant_mode == "CuspXiangqi":
                cusp_app.human_no_move_this_round = True
            if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
                cusp_app.safe_move_or_setup_in_cusp_chess()

# When a player set up a Cusp Position, the opponent needs to choose a color to play.

def human_player_choose_color(cusp_app):
    logger.info("human_player_choose_color")
    while cusp_app.game_in_progress:
        if cusp_app.color_must_win_in_cusp_chess == "W":
            color_must_win = "Red"
        elif cusp_app.color_must_win_in_cusp_chess == "B":
            color_must_win = "Black"

        if cusp_app.color_to_move_in_fight_phase == "W":
            color_to_move = "Red"
        elif cusp_app.color_to_move_in_fight_phase == "B":
            color_to_move = "Black"
        # another human player to choose a color
        color_chosen = messagebox.askyesno( title="{} must win, {} to move.  Choose Red color?".format( color_must_win, color_to_move), message="{} must win, {} to move.  Choose Red color? No means Black".format( color_must_win, color_to_move), )
        if color_chosen:
            if cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_swap_side = True
                cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                cusp_app.rotate_board = True
                ui.ui_utils.clear_board_move_history(cusp_app)
                logger.info("now another Human plays Red color")
            elif cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_swap_side = False
            cusp_app.cusp_chess_phase = "Fight"

            cusp_app.color_chosen_in_setup_phase = "W"
            if cusp_app.game_in_progress:
                utils.pgnhistory.save_PGN_and_output_move_history( cusp_app, False)
                ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)
                cusp_app.update()
                break
        elif not color_chosen:
            if cusp_app.active_color_in_cusp_setup == "B":
                cusp_app.player_swap_side = True
                cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                cusp_app.rotate_board = True
                ui.ui_utils.clear_board_move_history(cusp_app)
                logger.info("now another Human plays black color")

            elif cusp_app.active_color_in_cusp_setup == "W":
                cusp_app.player_swap_side = False

            # fight phase
            cusp_app.cusp_chess_phase = "Fight"

            cusp_app.color_chosen_in_setup_phase = "B"
            if cusp_app.game_in_progress:
                utils.pgnhistory.save_PGN_and_output_move_history( cusp_app, False)
                ui.ui_utils.draw_pieces( cusp_app, cusp_app.chess_game_variant_mode)
                cusp_app.update()
                break
        else:
            logger.info( " error, you must choose one color, yes means White, no means Black" )

    # A player can choose one color directly, if he/she think the color is going to win,
    # and he/she only need to set the color-must-win in the spinbox

def Human_choose_color_directly(cusp_app):
    logger.info("Human_choose_color_directly")
    cusp_chess_player_one_turn = ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and cusp_app.board.turn )

    cusp_chess_player_two_turn = ( cusp_app.chess_game_variant_mode == "CuspXiangqi" and not cusp_app.board.turn )

    if ( ( cusp_app.player_one == "Human" and cusp_chess_player_one_turn  ) or ( cusp_app.player_two == "Human" and  cusp_chess_player_two_turn ) ) and cusp_app.cusp_chess_phase == "SafeMove":
        # you can not choose a color directly after making a move
        if ( cusp_app.human_no_move_this_round and cusp_app.chess_game_variant_mode == "CuspXiangqi" ):
            cusp_app.Human_setup_color_must_win = ( cusp_app.color_must_win_spinbox_var.get() )
            if cusp_app.Human_setup_color_must_win == "White":
                cusp_app.color_must_win_in_cusp_chess = "W"
            elif cusp_app.Human_setup_color_must_win == "Black":
                cusp_app.color_must_win_in_cusp_chess = "B"
            # when choose color directly, you cannot change board.turn.
            # Otherwise the cusp chess will not work.
            if cusp_app.board.turn:
                cusp_app.color_to_move_in_fight_phase = "W"
            else:
                cusp_app.color_to_move_in_fight_phase = "B"

            cusp_app.choose_color_directly = True
            # human can only choose the color which must win, and cannot change
            # move order

            if cusp_chess_player_one_turn:
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    cusp_app.player_swap_side = False
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
            elif cusp_chess_player_two_turn:
                if cusp_app.color_must_win_in_cusp_chess == "W":
                    cusp_app.player_swap_side = True
                    cusp_app.flip_board_enable = cusp_app.flip_board_enable ^ 1
                    cusp_app.rotate_board = True
                elif cusp_app.color_must_win_in_cusp_chess == "B":
                    cusp_app.player_swap_side = False

            cusp_app.setting_up_in_cusp_chess = True
            if cusp_app.board.turn:
                cusp_app.active_color_in_cusp_setup = "W"
            elif not cusp_app.board.turn:
                cusp_app.active_color_in_cusp_setup = "B"
            cusp_app.move_str = "none"
            cusp_app.cusp_chess_phase = "Fight"
            utils.pgnhistory.save_PGN_and_output_move_history(cusp_app, True)
            logger.info("human choose a color directly")

            ui.ui_utils.draw_pieces(cusp_app, cusp_app.chess_game_variant_mode)
            cusp_app.update()
            if cusp_app.game_player_mode == "AvH" or cusp_app.game_player_mode == "HvA":
                cusp_app.AI_searching_best_move()