import logging
from tkinter import *
from tkinter import messagebox
from PIL import Image as PILImage
from datetime import datetime
import utils.config
import utils.game_results
import ai.stop_threads

logger = logging.getLogger(__name__)

def start_tournament(cusp_app):
    logger.info("start_tournament")
    cusp_app.tournament_start = True
    cusp_app.player_one_tournament_score = 0
    cusp_app.player_two_tournament_score = 0
    cusp_app.tournament_game_number_started = 0
    cusp_app.tournament_white_active_count = 0
    cusp_app.game_early_stop_count_adjudicator = []
    cusp_app.move_history_text.insert(END, cusp_app.translations[cusp_app.current_lang]['Tournament_score']+": 0-0" + "\n")
    cusp_app.tournamtent_time_stamp=f'{datetime.now():%Y%m%d_%H%M%S}'
    try:
        if cusp_app.tournament_game_number_entry.get() != "":
            cusp_app.tournament_game_number = int( cusp_app.tournament_game_number_entry.get() )
            if cusp_app.tournament_game_number < 0:
                cusp_app.tournament_game_number = 0
            if ( (cusp_app.game_early_stop_draw_enable or cusp_app.game_early_stop_win_enable) and cusp_app.game_early_stop_entry.get() != "" ):
                cusp_app.game_early_stop_score_difference = float( cusp_app.game_early_stop_entry.get() )
                if cusp_app.game_early_stop_score_difference < 0.1:
                    cusp_app.game_early_stop_score_difference = 0.1
                elif cusp_app.game_early_stop_score_difference > 0.8:
                    cusp_app.game_early_stop_score_difference = 0.8
                cusp_app.game_early_stop_minimum_moves = int( cusp_app.game_early_stop_minimum_moves_entry.get() )
                if cusp_app.game_early_stop_minimum_moves < 0:
                    cusp_app.game_early_stop_minimum_moves = 0
            utils.config.save_setting_in_config_file(cusp_app)
            update_tournament(cusp_app)
    except Exception as e:
        logger.exception("tournament start error")
        messagebox.showerror("Tournament start error", str(e))


def update_tournament(cusp_app):
    logger.info("update_tournament")   
    if cusp_app.tournament_start and (cusp_app.tournament_game_number > (cusp_app.player_one_tournament_score + cusp_app.player_two_tournament_score)):
        if cusp_app.engine_one_path != "" and cusp_app.engine_two_path != "":
            try:
                cusp_app.reset()
                cusp_app.move_history_text.insert( END, cusp_app.translations[cusp_app.current_lang]['Tournament_score']+": " + str(cusp_app.player_one_tournament_score)+ " - " + str(cusp_app.player_two_tournament_score)+ "\n",)

                cusp_app.start_game()
                check_tournament_result(cusp_app)
            except Exception as e:
                logger.exception(f"tournament game {cusp_app.tournament_game_number} error")
                messagebox.showerror("Tournament game error", f"tournament game {cusp_app.tournament_game_number} error, {str(e)}")


def check_tournament_result(cusp_app):
    logger.info("check_tournament_result")  
    if cusp_app.tournament_start and not cusp_app.game_in_progress:
        if cusp_app.active_color_in_cusp_setup == "W":
            cusp_app.tournament_white_active_count = ( cusp_app.tournament_white_active_count + 1 )
        logger.info( f"tournament_game_number_started: { cusp_app.tournament_game_number_started+1}")    
        logger.info( f"tournament_white_active_count: { cusp_app.tournament_white_active_count}")
        
        logger.info( f" tournament game, only { cusp_app.player_one_tournament_score + cusp_app.player_two_tournament_score} finished")
        logger.info( f"Tournament score: { cusp_app.player_one_tournament_score} - { cusp_app.player_two_tournament_score}")

        cusp_app.move_history_text.insert(
            END,
            "\n"
            + "\n"
            + cusp_app.translations[cusp_app.current_lang]['Tournament_score'] +': '
            + str(cusp_app.player_one_tournament_score)
            + " - "
            + str(cusp_app.player_two_tournament_score),
        )
        cusp_app.move_history_text.see("end")
        cusp_app.tournament_game_number_started = ( cusp_app.tournament_game_number_started + 1 )
        logger.info( f"game_early_stop_count_adjudicator { cusp_app.game_early_stop_count_adjudicator}")
        utils.config.save_setting_in_config_file(cusp_app)
        config_with_pgn_path=cusp_app.PGN_folder_path+'/'+ cusp_app.tournamtent_time_stamp+'config.ini'
        utils.config.save_setting_in_config_file(cusp_app,config_with_pgn_path)        
        cusp_app.stop_game_in_tournament()
        cusp_app.after(5000, lambda: update_tournament(cusp_app))

def stop_tournament(cusp_app):
    logger.info("stop_tournament") 
    cusp_app.stop_game()
    logger.info( f"Tournament score: { cusp_app.player_one_tournament_score} - { cusp_app.player_two_tournament_score} ")


def update_tournament_result(cusp_app):
    logger.info("update_tournament_result")
    if cusp_app.tournament_start:
        if cusp_app.chess_game_variant_mode != "Normal":
            if cusp_app.color_must_win_in_cusp_chess == "W":
                if cusp_app.game_result == "1-0":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                    else:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
                elif cusp_app.game_result == "0-1":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
                    else:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                elif cusp_app.game_result == "1/2-1/2":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
                    else:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
            elif cusp_app.color_must_win_in_cusp_chess == "B":
                if cusp_app.game_result == "1-0":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                    else:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
                elif cusp_app.game_result == "0-1":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
                    else:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                elif cusp_app.game_result == "1/2-1/2":
                    if cusp_app.player_swap_side == False:
                        cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                    else:
                        cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
            else:
                # no one set up a fight starting position. draw means loss for the first player.
                if cusp_app.game_result == "1-0":
                    cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
                else:
                    cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )

        else:
            if cusp_app.game_result == "1-0":
                cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 1 )
            elif cusp_app.game_result == "0-1":
                cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 1 )
            elif cusp_app.game_result == "1/2-1/2":
                cusp_app.player_one_tournament_score = ( cusp_app.player_one_tournament_score + 0.5 )
                cusp_app.player_two_tournament_score = ( cusp_app.player_two_tournament_score + 0.5 )

    utils.config.save_setting_in_config_file(cusp_app)
        