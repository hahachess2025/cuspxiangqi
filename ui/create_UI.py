import logging
import pathlib

import ui.language

import ui.normalboard
import ui.setting_panel
import ui.ui_utils
import utils.config
import utils.game_state

logger = logging.getLogger(__name__)

def create_UI(cusp_app):
        utils.game_state.initalize_basic_setting(cusp_app)
        utils.game_state.user_setting_initialization(cusp_app)
        cusp_app.widget_registry = {}
        ui.language.inialize_luanguage_setting(cusp_app)
        utils.config.read_config_file(cusp_app)
        pathlib.Path(cusp_app.PGN_folder_path).mkdir(parents=True, exist_ok=True)
        ui.ui_utils.generate_PGN_path(cusp_app)

        cusp_app.create_Boards_menu()
        cusp_app.create_setting_menu()
        cusp_app.create_language_menu()
        cusp_app.create_about_program_menu()

        cusp_app.editor_board_frame = None
        cusp_app.editor_setting_UI = None
        cusp_app.blindfold_cchess_frame = None
        cusp_app.board_frame = None

        ui.normalboard.create_cusp_chess_UI(cusp_app)
        logger.info("normal UI created")
        ui.setting_panel.UI_move_history(cusp_app)
        ui.setting_panel.UI_game_play_setting(cusp_app)
        ui.setting_panel.UI_cusp_chess_setup(cusp_app)
        ui.setting_panel.UI_PGN_setting(cusp_app)
        ui.ui_utils.widget_initialization(cusp_app)
        ui.ui_utils.initialize_player_time_label(cusp_app)

        cusp_app.chess_container.tkraise()
        ui.language.update_texts(cusp_app)
        ui.ui_utils.generate_legal_positions_for_pieces(cusp_app)
        logger.info("All UIs created")
        cusp_app.update_idletasks()
        cusp_app.resizing_enabled = True
        ui.normalboard.redraw_chess_board(cusp_app)

        ui.ui_utils.update_game_status_label(cusp_app, True)   
        
