import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

def save_setting_in_config_file(cusp_app,config_path="config.ini"):
    logger.info("save_setting_in_config_file")
    config_object = ConfigParser()
    config_object["saved_user_setting"] = {
        "current_lang":cusp_app.current_lang,
        "chess_game_variant_mode": cusp_app.chess_game_variant_mode,
        "legacy_engine_mode": cusp_app.legacy_engine_mode,
        "player_one_name_input":cusp_app.player_one_name_input,
        "player_two_name_input":cusp_app.player_two_name_input,
        "adjudicator_name_input":cusp_app.adjudicator_name_input,
        "engine_one_path": cusp_app.engine_one_path,
        "engine_two_path": cusp_app.engine_two_path,
        "engine_adjudicator_path": cusp_app.engine_adjudicator_path,
        "PGN_folder_path": cusp_app.PGN_folder_path,
        "editor_engine_path": cusp_app.editor_engine_path,
        #"endgame_tablebase_enable": cusp_app.endgame_tablebase_enable,
        "maximum_ply_before_setup": cusp_app.maximum_ply_before_setup,

        "engine_score_difference_maximum": cusp_app.engine_score_difference_maximum,
        "engine_score_difference_minimum": cusp_app.engine_score_difference_minimum,
        "engine_safe_move_score_maximum": cusp_app.engine_safe_move_score_maximum,        
        "engine_score_cusp_outer_range_enable": cusp_app.engine_score_cusp_outer_range_enable,
        "engine_score_cusp_inner_range_enable": cusp_app.engine_score_cusp_inner_range_enable,
        "only_engine_one_setup_enable": cusp_app.only_engine_one_setup_enable,

        "choose_the_recommended_color_enable": cusp_app.choose_the_recommended_color_enable,
        "no_choosing_color_directly_enable": cusp_app.no_choosing_color_directly_enable,
        "engine_test_mode_enable":cusp_app.engine_test_mode_enable,     
        "cusp_pawn_setup_enable": cusp_app.cusp_pawn_setup_enable,        
        "engine_time_limit_enable": cusp_app.engine_time_limit_enable,
        "engine_evaluation_limit_for_each_cusp_candidate": cusp_app.engine_evaluation_limit_for_each_cusp_candidate,
        "engine_one_searching_limit_for_best_move": cusp_app.engine_one_searching_limit_for_best_move,
        "engine_two_searching_limit_for_best_move": cusp_app.engine_two_searching_limit_for_best_move,
        "time_for_each_player": cusp_app.time_for_each_player,
        "output_PGN_enable": cusp_app.output_PGN_enable,
        "pgn_auto_game_variant_detection":cusp_app.pgn_auto_game_variant_detection,
        "play_sound_enable": cusp_app.play_sound_enable,
        "eval_show_enable": cusp_app.eval_show_enable,
        "editor_engine_evaluation_limit": cusp_app.editor_engine_evaluation_limit,
        "editor_engine_multipv":cusp_app.editor_engine_multipv,
        "tournament_game_number": cusp_app.tournament_game_number,
        "tournament_game_number_started": cusp_app.tournament_game_number_started,
        "tournament_start": cusp_app.tournament_start,
        "player_one_tournament_score": cusp_app.player_one_tournament_score,
        "player_two_tournament_score": cusp_app.player_two_tournament_score,
        "game_early_stop_score_difference": cusp_app.game_early_stop_score_difference,
        "game_early_stop_minimum_moves": cusp_app.game_early_stop_minimum_moves,
        "game_early_stop_draw_enable": cusp_app.game_early_stop_draw_enable,
        "game_early_stop_win_enable": cusp_app.game_early_stop_win_enable,
        "tournament_white_active_count": cusp_app.tournament_white_active_count,
        "game_early_stop_count_adjudicator": cusp_app.game_early_stop_count_adjudicator,
        "adjudicator_engine_enable": cusp_app.adjudicator_engine_enable,

    }
    with open(config_path, "w") as conf:
        config_object.write(conf)


def read_config_file(cusp_app):
    logger.info("read_config_file") 
    config_object = ConfigParser()
    config_object.read("config.ini")

    # Get user setting
    try:
        user_setting = config_object["saved_user_setting"]
        if "current_lang" in user_setting.keys():
            cusp_app.current_lang = user_setting["current_lang"]
        if "chess_game_variant_mode" in user_setting.keys():
            cusp_app.chess_game_variant_mode = user_setting["chess_game_variant_mode"]
        if "legacy_engine_mode" in user_setting.keys():
            cusp_app.legacy_engine_mode = eval(user_setting["legacy_engine_mode"])    
        if "player_one_name_input" in user_setting.keys():
            cusp_app.player_one_name_input = user_setting["player_one_name_input"]            
        if "player_two_name_input" in user_setting.keys():
            cusp_app.player_two_name_input = user_setting["player_two_name_input"]             
        if "adjudicator_name_input" in user_setting.keys():
            cusp_app.adjudicator_name_input = user_setting["adjudicator_name_input"]                        
        if "engine_one_path" in user_setting.keys():
            cusp_app.engine_one_path = user_setting["engine_one_path"]
        if "engine_two_path" in user_setting.keys():
            cusp_app.engine_two_path = user_setting["engine_two_path"]

        if "engine_adjudicator_path" in user_setting.keys():
            cusp_app.engine_adjudicator_path = user_setting["engine_adjudicator_path"]

        if "maximum_ply_before_setup" in user_setting.keys():
            cusp_app.maximum_ply_before_setup = int( user_setting["maximum_ply_before_setup"] )
        if "engine_score_difference_maximum" in user_setting.keys():
            cusp_app.engine_score_difference_maximum = float( user_setting["engine_score_difference_maximum"] )
        if "engine_score_difference_minimum" in user_setting.keys():
            cusp_app.engine_score_difference_minimum = float( user_setting["engine_score_difference_minimum"] )
        if "engine_safe_move_score_maximum" in user_setting.keys():
            cusp_app.engine_safe_move_score_maximum = float( user_setting["engine_safe_move_score_maximum"] )   
            
        if "engine_score_cusp_outer_range_enable" in user_setting.keys():
            cusp_app.engine_score_cusp_outer_range_enable = eval( user_setting["engine_score_cusp_outer_range_enable"] )
        if "engine_score_cusp_inner_range_enable" in user_setting.keys():
            cusp_app.engine_score_cusp_inner_range_enable = eval( user_setting["engine_score_cusp_inner_range_enable"] )
        if "only_engine_one_setup_enable" in user_setting.keys():
            cusp_app.only_engine_one_setup_enable = eval( user_setting["only_engine_one_setup_enable"] )
        if "choose_the_recommended_color_enable" in user_setting.keys():
            cusp_app.choose_the_recommended_color_enable = eval( user_setting["choose_the_recommended_color_enable"] )            
            

        if "no_choosing_color_directly_enable" in user_setting.keys():
            cusp_app.no_choosing_color_directly_enable = eval( user_setting["no_choosing_color_directly_enable"] )
        if "engine_test_mode_enable" in user_setting.keys():
            cusp_app.engine_test_mode_enable = eval( user_setting["engine_test_mode_enable"] )
        if "cusp_pawn_setup_enable" in user_setting.keys():
            cusp_app.cusp_pawn_setup_enable = eval( user_setting["cusp_pawn_setup_enable"] )

        if "engine_time_limit_enable" in user_setting.keys():
            cusp_app.engine_time_limit_enable = eval( user_setting["engine_time_limit_enable"] )
        if "engine_evaluation_limit_for_each_cusp_candidate" in user_setting.keys():
            cusp_app.engine_evaluation_limit_for_each_cusp_candidate = float( user_setting["engine_evaluation_limit_for_each_cusp_candidate"] )
        if "engine_one_searching_limit_for_best_move" in user_setting.keys():
            cusp_app.engine_one_searching_limit_for_best_move = float( user_setting["engine_one_searching_limit_for_best_move"] )
        if "engine_two_searching_limit_for_best_move" in user_setting.keys():
            cusp_app.engine_two_searching_limit_for_best_move = float( user_setting["engine_two_searching_limit_for_best_move"] )

        if "time_for_each_player" in user_setting.keys():
            cusp_app.time_for_each_player = int(user_setting["time_for_each_player"])
        if "output_PGN_enable" in user_setting.keys():
            cusp_app.output_PGN_enable = eval(user_setting["output_PGN_enable"])
        if "pgn_auto_game_variant_detection" in user_setting.keys():
            cusp_app.pgn_auto_game_variant_detection = eval( user_setting["pgn_auto_game_variant_detection"])  
        if "play_sound_enable" in user_setting.keys():
            cusp_app.play_sound_enable = eval(user_setting["play_sound_enable"])
        if "eval_show_enable" in user_setting.keys():
            cusp_app.eval_show_enable = eval(user_setting["eval_show_enable"])
        if "editor_engine_evaluation_limit" in user_setting.keys():
            cusp_app.editor_engine_evaluation_limit = float( user_setting["editor_engine_evaluation_limit"] )
        if "editor_engine_multipv" in user_setting.keys():
            cusp_app.editor_engine_multipv = int( user_setting["editor_engine_multipv"] ) 
        if "tournament_game_number" in user_setting.keys():
            cusp_app.tournament_game_number = int( user_setting["tournament_game_number"] )
        if "tournament_game_number_started" in user_setting.keys():
            cusp_app.tournament_game_number_started = int( user_setting["tournament_game_number_started"] )

        if "tournament_start" in user_setting.keys():
            cusp_app.tournament_start = eval(user_setting["tournament_start"])
        if "player_one_tournament_score" in user_setting.keys():
            cusp_app.player_one_tournament_score = float( user_setting["player_one_tournament_score"] )
        if "player_two_tournament_score" in user_setting.keys():
            cusp_app.player_two_tournament_score = float( user_setting["player_two_tournament_score"] )
        if "game_early_stop_score_difference" in user_setting.keys():
            cusp_app.game_early_stop_score_difference = float( user_setting["game_early_stop_score_difference"] )
        if "game_early_stop_minimum_moves" in user_setting.keys():
            cusp_app.game_early_stop_minimum_moves = int( user_setting["game_early_stop_minimum_moves"] )
        if "game_early_stop_draw_enable" in user_setting.keys():
            cusp_app.game_early_stop_draw_enable = eval( user_setting["game_early_stop_draw_enable"] )
        if "game_early_stop_win_enable" in user_setting.keys():
            cusp_app.game_early_stop_win_enable = eval( user_setting["game_early_stop_win_enable"] )
        if "tournament_white_active_count" in user_setting.keys():
            cusp_app.tournament_white_active_count = int( user_setting["tournament_white_active_count"] )
        if "game_early_stop_count_adjudicator" in user_setting.keys():
            cusp_app.game_early_stop_count_adjudicator = eval( user_setting["game_early_stop_count_adjudicator"] )
        if "adjudicator_engine_enable" in user_setting.keys():
            cusp_app.adjudicator_engine_enable = eval( user_setting["adjudicator_engine_enable"] )

        if "PGN_folder_path" in user_setting.keys():
            cusp_app.PGN_folder_path = user_setting["PGN_folder_path"]
        if "editor_engine_path" in user_setting.keys():
            cusp_app.editor_engine_path = user_setting["editor_engine_path"]
    except Exception as e:
        # if it is the first time to save defaut value in config file
        logger.exception(f"read config file error: {e}")
        save_setting_in_config_file(cusp_app)