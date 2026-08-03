
import logging

logger = logging.getLogger(__name__)

def inialize_luanguage_setting(cusp_app):
    logger.info("inialize_luanguage_setting")
    cusp_app.translations = {
        "en": {
            "title": "Cusp Xiangqi",
            "menu_Boards":"Boards",
            "menu_B_chess":"Xiangqi",
            "menu_B_editor":"Board editor",
            "menu_B_blindfold":"Blindfold Xiangqi",
            "menu_Setting":"Setting",
            "menu_S_Game_Setting":"Game Setting",
            
            "white": "Red",
            "black": "Black",
            "AI": "AI",
            "Human": "Human",

            "player_one_board_label_default": "Player One",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: Red or Black?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: I choose {color_must_win} directly",
                
            "player_two_board_label_default": "Player Two",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: Red or Black?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: I choose {color_must_win} directly",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "Cusp Xiangqi, draw means loss",
            "game_status_label_safe_CC": "Cusp Xiangqi, draw means loss",
            "game_status_label_searching": "Searching for a fight starting position",
            "game_status_label_player_must_setup": "{player_name} must set up now",
            "game_status_label_player_must_win": "Cusp Xiangqi, {color} must win",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "Color to move: {color}",
            "editor_color_to_move_label": "Color to move: {color}",
            
            "editor_start_position": "Starting position",
            "editor_clear_board":"Clear board",
            "editor_white_to_move_radio": "Red to move",            
            "editor_black_to_move_radio": "Black to move",
            "editor_auto_turn_rotation_checkbox":"Auto turn rotation",
            "editor_engine_path_button": "Set engine path",               
            "editor_engine_analyse_checkbox": "Engine enable?",
            "editor_engine_time_or_depth_label": "Engine search time/depth",
            "editor_engine_top_moves_label": "Top moves",
            "editor_engine_score_label": "Now score is: ",
            "editor_engine_score_and_top_moves_search_button": "Search",   
            
            "editor_engine_search_for_cusps_label": "Search for fight starting positions for Cusp Xiangqi", 
            "editor_search_for_cusps_for_CC_confirm_button": "Search",            

            "editor_cusp_stop_button": "Stop",
            "editor_editor_export_board_fen_button": "Export board FEN",
            "editor_clear_fen_history_button": "Clear history",
            "editor_set_board_fen_button": "Set board FEN",

            "engine_one_path_button": "Engine player one",
            "engine_two_path_button": "Engine player two",
            "engine_adjudicator_path_button": "Adjudicator Engine",            
            "PGN_path_button": "PGN folder",
            "Syzygy_tablebases_path_button": "Syzygy tablebase folder",
           
            "maximum_ply_before_setup_label": "Maximum plies before setup for an AI player",
            "engine_score_difference_maximum_label": "Engine maximum score difference for a Cusp",
            "engine_score_difference_minimum_label": "Engine minimum score difference for a Cusp", 
            "engine_safe_move_score_maximum_label": "Engine maximum absolute score for a safe move",            
            "engine_cusp_outer_range_checkbox": "Cusp outer range, away from 0",
            "engine_cusp_inner_range_checkbox": "Cusp inner range, closer to 0",      
            "only_engine_one_setup_checkbox": "Only engine one sets up?",
            "no_choosing_color_directly_enable_checkbox": "No choosing color directly?",
            "the_other_engine_chooses_recommended_color_checkbox": "Recommended color for the other engine?",            
            "engine_test_mode_enable_checkbox": "Engine test mode",
            "cusp_pawn_setup_enable_checkbox":"Setup pawn",
            
            "time_limit_radio": "Time",
            "depth_limit_radio": "Depth",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "Engine evaluation time/depth for a Cusp candidate",
            "engine_one_searching_limit_for_best_move_label": "Time/depth per move for engine one",   
            "engine_two_searching_limit_for_best_move_label": "Time/depth per move for engine two",
            "time_for_each_player_label": "Time for each player (seconds)",
            "reset_setting_button": "reset all",
            
            "modern_engine_mode_radio": "Modern engine",   
            "legacy_engine_mode_radio": "Legacy engine",
            "output_PGN_checkbox": "Output PGN?",
            "pgn_auto_game_variant_detection_checkbox":"change UI based on PGN",
            "play_sound_checkbox": "Play sound?",
            "eval_bar_checkbox": "Show eval?",   
            
            "player_one_name_label": "Set player one name",      
            "player_two_name_label": "Set player two name",
            "adjudicator_name_label": "Set adjudicator engine name",
            "setting_ok_button": "Save", 

            "tournament_game_number_label": "Tournament game number",
            "game_early_stop_draw_checkbox": "Early stop if draw?", 
            "game_early_stop_win_checkbox": "Early stop if win?",
            "game_early_stop_label": "Early stop score difference",   
            "game_early_stop_minimum_moves_label": "Early stop minimum moves",
            "adjudicator_engine_enable_checkbox": "Adjudicator engine?",      
            "tournament_start_button": "Start tournament",
            "stop_tournament": "Stop tournament", 
            
            "start_game_button": "Start game",
            "stop_game_button": "Stop game",     
            "reset_game_button": "Reset",
            "chess_radio": "Xiangqi", 
            "cusp_chess_radio": "Cusp Xiangqi",

            "player_one_label": "Player One",
            "player_two_label": "Player Two",  
            
            "load_PGN_button": "Load PGN",
            "play_PGN_previous_button": "Previous",   
            "play_PGN_next_button": "Next",
            "beginning_PGN_button": "Beginning",  
            "auto_play_PGN_button": "Auto play",
            "stop_play_PGN_button": "Stop play",
            "clear_history_button": "Clear history", 
            
            "move_history_label": "Move history",
            
            "setup_label_CC": "Setup for Cusp Xiangqi",   
            "setup_CC_color_to_move": "Color to move",
            "setup_CC_color_must_win": "Color must win",      
            "Human_setup_confirmation_checkbox": "Set up?",
            "Human_move_finished_button": "Move finished",   
            "Human_directly_choose_button": "Choose directly",

            "Tournament_score":"Tournament score",
            "Now_Score_is":"Now Score is",

            "White_won":"Red won. ",
            "Black_won":"Black won. ",
            "won":" won. ",
            "draw":"draw",
            "Draw_means_White_won":"Draw means Red won. ",
            "Draw_means_Black_won":"Draw means Black won. ",
            "No_one_set_up_a_cusp_position":"No one set up a Cusp Position. ",
            "The_move_is_illegal":"The move is illegal",
            "empty":"",    
            
        },
        
        "cn": {
            "title": "奇点象棋",
            
            "menu_Boards":"棋盘",
            "menu_B_chess":"中国象棋",
            "menu_B_editor":"棋盘编辑",
            "menu_B_blindfold":"盲棋",
            "menu_Setting":"设置",
            "menu_S_Game_Setting":"游戏设置",

            "white": "红方",
            "black": "黑方",
            "AI": "引擎",
            "Human": "人类玩家",

            "player_one_board_label_default": "玩家一",
            "player_one_board_label_show_name":"(p1) {player_one_name}",
            "player_one_board_label_setup":"(p1)  {player_one_name}: 红方还是黑方?",
            "player_one_board_label_passively_choose":"(p1) {player_one_name}: {color_chosen}",
            "player_one_board_label_directly_choose":"(p1) {player_one_name}: 我直接选择 {color_must_win}",
                
            "player_two_board_label_default": "玩家二",
            "player_two_board_label_show_name":"(p2) {player_two_name}",
            "player_two_board_label_setup":"(p2)  {player_two_name}: 红方还是黑方?",
            "player_two_board_label_passively_choose":"(p2) {player_two_name}: {color_chosen}",
            "player_two_board_label_directly_choose":"(p2) {player_two_name}: 我直接选择 {color_must_win}",
            
            "game_status_label_ready": " ",
            "game_status_label_ready_CC": "奇点象棋, 和棋算输",
            "game_status_label_safe_CC": "奇点象棋, 和棋算输",
            "game_status_label_searching": "正在搜索奇点",
            "game_status_label_player_must_setup": "{player_name} 现在必须设置奇点局面",
            "game_status_label_player_must_win": "奇点象棋, {color} 必须赢",
            "game_status_label_final_result":"{result}",
            
            "color_to_move_label": "下一步: {color}",
            "editor_color_to_move_label": "下一步: {color}",            
            "editor_start_position": "开始局面",
            "editor_clear_board":"清空棋盘",
            "editor_white_to_move_radio": "红方走",            
            "editor_black_to_move_radio": "黑方走",
            "editor_auto_turn_rotation_checkbox":"自动换边",
            "editor_engine_path_button": "设置引擎路径",               
            "editor_engine_analyse_checkbox": "使用引擎?",
            "editor_engine_time_or_depth_label": "引擎搜索 时间/深度",
            "editor_engine_top_moves_label": "最佳走子选项",
            "editor_engine_score_label": "当前分数是: ",
            "editor_engine_score_and_top_moves_search_button": "搜索",   
            
            "editor_engine_search_for_cusps_label": "搜索奇点象棋当前局面存在的所有奇点", 
            "editor_search_for_cusps_for_CC_confirm_button": "搜索",            

            "editor_cusp_stop_button": "停止",
            "editor_editor_export_board_fen_button": "输出当前局面 FEN",
            "editor_clear_fen_history_button": "清除输出",
            "editor_set_board_fen_button": "设置棋盘 FEN",
            
            "engine_one_path_button": "引擎一路径",
            "engine_two_path_button": "引擎二路径",
            "engine_adjudicator_path_button": "裁判引擎路径",            
            "PGN_path_button": "PGN文件夹路径",
           
            "maximum_ply_before_setup_label": "引擎设置奇点之前的步数最大值",
            "engine_score_difference_maximum_label": "引擎搜索的奇点，其绝对值分数与1的差值上限",
            "engine_score_difference_minimum_label": "引擎搜索的奇点，其绝对值分数与1的差值下限", 
            "engine_safe_move_score_maximum_label": "引擎安全走子，绝对值分数的上限",              
            "engine_cusp_outer_range_checkbox": "非0方向的取值?",
            "engine_cusp_inner_range_checkbox": "靠近0方向的取值?",      
            "only_engine_one_setup_checkbox": "只有引擎一设置奇点?",
            "the_other_engine_chooses_recommended_color_checkbox": "接受推荐的颜色?",

            "no_choosing_color_directly_enable_checkbox": "禁止引擎直接选择某方?",
            "engine_test_mode_enable_checkbox": "引擎测试模式",
            "cusp_pawn_setup_enable_checkbox":"奇点兵",
            
            "time_limit_radio": "搜索时间/秒",
            "depth_limit_radio": "搜索深度",
            "engine_evaluation_limit_for_each_cusp_candidate_label": "引擎评估某候选奇点的搜索时间/深度",
            "engine_one_searching_limit_for_best_move_label": "引擎一每步搜索时间/深度",   
            "engine_two_searching_limit_for_best_move_label": "引擎二每步搜索时间/深度",
            "time_for_each_player_label": "每个玩家的总时间(秒)",
            "reset_setting_button": "恢复默认设置",
            
            "modern_engine_mode_radio": "现代引擎",   
            "legacy_engine_mode_radio": "老版引擎",
            "output_PGN_checkbox": "输出PGN?",
            "pgn_auto_game_variant_detection_checkbox":"读取PGN时自动调整UI",
            "play_sound_checkbox": "走子声音?",
            "eval_bar_checkbox": "显示AI打分?",   
            #"endgame_tablebase_checkbox": "使用残局库?",
            "player_one_name_label": "设置玩家一的用户名",      
            "player_two_name_label": "设置玩家二的用户名",
            "adjudicator_name_label": "设置仲裁引擎的用户名",
            "setting_ok_button": "保存", 

            "tournament_game_number_label": "锦标赛总盘数",
            "game_early_stop_draw_checkbox": "可能和棋，是否提前结束?", 
            "game_early_stop_win_checkbox": "可能赢棋，是否提前结束?",
            "game_early_stop_label": "提前结束的分差",   
            "game_early_stop_minimum_moves_label": "提前结束的最少步数",
            "adjudicator_engine_enable_checkbox": "使用裁判引擎仲裁?",      
            "tournament_start_button": "开始锦标赛",
            "stop_tournament": "停止锦标赛", 
            
            "start_game_button": "开始",
            "stop_game_button": "结束",     
            "reset_game_button": "重置",
            "chess_radio": "国际象棋", 
            "cusp_chess_radio": "奇点象棋",
 
            "player_one_label": "玩家一",
            "player_two_label": "玩家二",  
            
            "load_PGN_button": "载入PGN",
            "play_PGN_previous_button": "上一步",   
            "play_PGN_next_button": "下一步",
            "beginning_PGN_button": "初始局面",  
            "auto_play_PGN_button": "自动播放",
            "stop_play_PGN_button": "停止",
            "clear_history_button": "清除输出", 
            
            "move_history_label": "棋谱",
            
            "setup_label_CC": "设置奇点局面",   
            "setup_CC_color_to_move": "下一步",
            "setup_CC_color_must_win": "必须赢的颜色",      
            "Human_setup_confirmation_checkbox": "设置奇点?",
            "Human_move_finished_button": "完成",   
            "Human_directly_choose_button": "直接选赢的颜色",
            "Tournament_score":"锦标赛比分", 
            "Now_Score_is":"当前分数是",

            "White_won":"红方赢. ",
            "Black_won":"黑方赢. ",
            "won":" 赢. ",
            "draw":"和棋",
            "Draw_means_White_won":"和棋算红棋赢. ",
            "Draw_means_Black_won":"和棋算黑棋赢. ",
            "No_one_set_up_a_cusp_position":"无人设置奇点局面. ",   
            "The_move_is_illegal":"非法走子",
            "empty":"",    
        }
    }

def register_widget(cusp_app, widget, key, **kwargs):
    logger.info("register_widget")
    """
    key may be a string (translation key) or a callable returning the key.
    kwargs values may be plain values or callables returning the value.
    """
    cusp_app.widget_registry[widget] = (key, kwargs)
    update_widget(cusp_app, widget)

def resolve( maybe_callable):
    return maybe_callable() if callable(maybe_callable) else maybe_callable

def update_widget(cusp_app, widget):
    """Update just one registered widget"""
    # for widget in list(cusp_app.widget_registry.keys()):
        # if not widget.winfo_exists():
            # cusp_app.widget_registry.pop(widget)
        
    if widget not in cusp_app.widget_registry:
        logger.info('no widget now')
        return
    if widget is None or not widget.winfo_exists():
        logger.info('widget does not exist anymore')
        return
    key_or_callable, kwargs = cusp_app.widget_registry[widget]
    key = resolve(key_or_callable)
    lang_dict = cusp_app.translations[cusp_app.current_lang]
    template = lang_dict.get(key, f"[{key}]")
    resolved_kwargs = {k: resolve(v) for k, v in kwargs.items()}
    try:
        widget.config(text=template.format(**resolved_kwargs))
    except KeyError as e:
        logger.exception(f"update_widget, [Missing {e.args[0]}]")
        widget.config(text=f"[Missing {e.args[0]}]")
        
def update_texts(cusp_app):
    logger.info("update_texts")
    """Refresh all registered widgets"""
    cusp_app.title(cusp_app.translations[cusp_app.current_lang]["title"])
    update_menus(cusp_app)
    update_spinboxes(cusp_app)       
           
    for widget in cusp_app.widget_registry.keys():
        update_widget(cusp_app, widget)
        #print(cusp_app.widget_registry[widget])

def update_menus(cusp_app):
    logger.info("update_menus")
    cusp_app.menubar.entryconfig(1, label=cusp_app.translations[cusp_app.current_lang]["menu_Boards"])
    cusp_app.menubar.entryconfig(2, label=cusp_app.translations[cusp_app.current_lang]["menu_Setting"])

    cusp_app.Boards_menu.entryconfig(0, label=cusp_app.translations[cusp_app.current_lang]["menu_B_chess"])
    cusp_app.Boards_menu.entryconfig(1, label=cusp_app.translations[cusp_app.current_lang]["menu_B_editor"])
    cusp_app.Boards_menu.entryconfig(2, label=cusp_app.translations[cusp_app.current_lang]["menu_B_blindfold"])

    cusp_app.setting_menu.entryconfig(0, label=cusp_app.translations[cusp_app.current_lang]["menu_S_Game_Setting"])

def update_spinboxes(cusp_app):
    logger.info("update_spinboxes")
    players=(cusp_app.translations[cusp_app.current_lang]["AI"],cusp_app.translations[cusp_app.current_lang]["Human"])
    cusp_app.player_one_spinbox.config(values=players)
    cusp_app.player_two_spinbox.config(values=players)
    p=players[cusp_app.player_one_spinbox_chosen]
    cusp_app.player_one_spinbox_var.set(p)
    
    p=players[cusp_app.player_two_spinbox_chosen]
    cusp_app.player_two_spinbox_var.set(p)

    side=(cusp_app.translations[cusp_app.current_lang]["white"],cusp_app.translations[cusp_app.current_lang]["black"])
    cusp_app.color_to_move_spinbox.config(values=side)
    cusp_app.color_must_win_spinbox.config(values=side)
    
    v = side[cusp_app.color_to_move_spinbox_chosen]
    cusp_app.color_to_move_spinbox_var.set(v)
    
    v = side[cusp_app.color_must_win_spinbox_chosen]
    cusp_app.color_must_win_spinbox_var.set(v)
    
def player_one_label_dynamic_key(cusp_app):
    logger.info("player_one_label_dynamic_key")
    return cusp_app.player_one_label_state

            
def player_one_label_dynamic_kwargs(cusp_app):
    logger.info("player_one_label_dynamic_kwargs")
    return{"player_one_name":lambda:cusp_app.player_one_name,
            "color_chosen": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_chosen_in_setup_phase == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_chosen_in_setup_phase == "B" else None ),
            "color_must_win": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_must_win_in_cusp_chess == "B" else None)
            }

def player_two_label_dynamic_key(cusp_app):
    logger.info("player_two_label_dynamic_key")
    return cusp_app.player_two_label_state
    
def player_two_label_dynamic_kwargs(cusp_app):
    logger.info("player_two_label_dynamic_kwargs")
    return{"player_two_name":lambda:cusp_app.player_two_name,
        "color_chosen": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_chosen_in_setup_phase == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_chosen_in_setup_phase == "B" else None ),
        "color_must_win": lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else ( cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_must_win_in_cusp_chess == "B" else None )
    }
  
def game_status_label_dynamic_key(cusp_app):
    logger.info("game_status_label_dynamic_key")
    return cusp_app.game_status_label_state

def game_status_label_dynamic_kwargs(cusp_app):
    logger.info("game_status_label_dynamic_kwargs")
    return {"player_name": lambda:cusp_app.game_status_label_player_name,
            "color" : lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_must_win_in_cusp_chess == "W" else cusp_app.translations[cusp_app.current_lang]["black"],
            "result": lambda: cusp_app.result_str
    }
   
def color_to_move_label_dynamic_kwargs(cusp_app):
    logger.info("color_to_move_label_dynamic_kwargs")
    return{"color":lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.color_to_move_label_state=='White' else (cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.color_to_move_label_state=='Black' else None)}
    
def editor_color_to_move_label_dynamic_kwargs(cusp_app):
    logger.info("editor_color_to_move_label_dynamic_kwargs")
    return{"color":lambda: cusp_app.translations[cusp_app.current_lang]["white"] if cusp_app.editor_color_to_move_label_state=='White' else (cusp_app.translations[cusp_app.current_lang]["black"] if cusp_app.editor_color_to_move_label_state=='Black' else None)}
       
def pgn_auto_play_label_dynamic_key(cusp_app):
    logger.info("pgn_auto_play_label_dynamic_key")
    return cusp_app.pgn_auto_play_label_state
    
def blindfold_label_dynamic_key(cusp_app):
    logger.info("blindfold_label_dynamic_key")
    return cusp_app.blindfold_label_state    