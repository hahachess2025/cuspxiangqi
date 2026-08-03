"""
Cusp Xiangqi: The Ultimate Drawless Xiangqi

Author: [Lei Gao], hahachess2025 [at] gmail [dot] com
Date: August 3, 2026
Version: 0.1.0

Cusp Xiangqi is a decisive xiangqi variant based on Freestyle Player-Balancing (FSPB). 

This game is suitable for both human players and AI engines.


====================================================================

For more information about Freestyle Player-Balancing, please check my 26-page preprint paper:
Freestyle Player-Balancing: A Novel Flexible Framework for Addressing Game Balance 
and Opening Memorization in Decisive, Two-Player, Perfect-Information, Turn-Based Games
https://zenodo.org/records/21687566

====================================================================
1. Introduction

Cusp Xiangqi is a decisive xiangqi variant based on Freestyle Player-Balancing (FSPB). 
This variant aims to eliminate draws. 
By giving a color an edge, the color must win and draw means loss for it. 
Then all other standard chess rules apply.

This game is suitable for both human players and AI engines.


====================================================================

2. Components
2.1	A standard 9×10 chessboard.
2.2	Standard xiangqi pieces for each player.

====================================================================

3. Initial setup
3.1	Standard xiangqi starting position.
3.2	Determine who are tentative Red player and tentative Black player by mutual agreement or random choice.
3.3	Piece Movement: All pieces (King, Guard, Rook, Bishop, Knight, Cannon, Pawn) move and capture exactly as they do in standard FIDE chess, except in Decision Phase.

====================================================================

4. Objective
4.1	The goal of must-win color is to checkmate the opposing king. Draw means loss for the must-win color. 
4.2	The goal of the opposite color is to defend itself, and checkmate the opposing king if possible. Draw means win for it.
4.3	The default must-win color is Red. If no one set up a fight-starting position when the game is over, draw means loss for the tentative Red player.


====================================================================

5. Gameplay Overview
It usually has three phases: Safe Move Phase, Decision Phase and Fight Phase. 
The first two phases are not to restrict players’ moves. 
On the contrary, they are determined by players’ moves in games. 
When a player makes a safe move, the game is in the Safe Move Phase. 
When a player decides to set up a fight-starting position, the game goes into the Decision Phase. 
After two colors are assigned to two players, the game enters the Fight Phase. 

There are two ways to enter the Decision Phase.

A：When a player decides to set up a fight starting position, and makes a setup move, the game goes into the Decision Phase. 
After a position is set up, the player needs to specify the must-win color and color to move in the position.
Then the pie rule: the opponent can choose a color freely.

B：A player can choose a color directly, but only the must-win color. 
And the player can't change the position befor the selection. 

After two colors are assigned to two players, the game enters Fight Phase.

====================================================================

6. Positions
•	Safe position: if win rates of both color of a position are below 50%, the position is a safe position. 
    The previous player is safe, because their opponent can’t choose the must-win color directly to win easily. 
    Based on xiangqi engine Pikafish, the score of a safe position ranges from -1 to +1.
    
•	Fight-starting position: It is the starting position in the Fight Phase. 
    There is only one fight starting position in a game. 
    A player can set up a fight starting position by a legal setup move. 
    If a player chooses the must-win color directly in a position, 
    the position is the fight starting position. 
    Each player has the right to set up a fight-starting position. 
    However, this right can only be exercised once per game total. 
    It is tentative white player’s responsibility to set it up. 
    if no one did it, draw means loss for the tentative Red player.
•	Cusp position or optimal setup position: A cusp position’s score is either around -1 or +1. 
    They are optimal setup positions for fight-starting positions. 
    The name of “cusp position” is from the evaluation function of typical chess engines.

====================================================================

7. Moves
•	Legal move: In Cusp Xiangqi, there are three types of legal moves for three phases respectively: 
    legal safe moves, legal setup moves, and legal fight moves. 
    The legal safe move and legal fight move are the same as legal moves in standard xiangqi. 
    Legal setup move includes legal safe move and one-free move. 
•	Optimal safe move:  They are legal safe moves that can create safe positions in the Safe Move Phase. 
    Usually there are multiple optimal safe move options for each position.
•	Setup move: A legal move in Decision Phase is a set up move. 
    It is used to set up a fight-starting position.   
•	Optimal setup move: An optimal setup move can create an optimal setup position.
•	One-Free move: All moves that are illegal in standard xiangqi 
    designed to set up fight starting positions are One-Free move. 
    They are legal setup moves but not legal safe moves. 
    There are two modes of One-Free move: Human-Level-Mode and Engine-Test-Mode. 
    Human-level-Mode can create sufficient good fight-starting positions 
    while won’t overwhelm human players. 
    Engine-Test-Mode can create much more good fight-starting positions, 
    but not suitable for human players.
•	Direct-choice move: A player can choose a color directly after their opponent’s safe move. 
    But they can’t make a move before the selection and can only choose the must-win color. 
    They also can’t set the side to move. 
    Direct-choice move can be seen as a special setup move in the Decision Phase.

====================================================================

8. Details about three phases:

8.1    Safe Move Phase

When a player makes a legal safe move, 
they need to specify whether they want to set up a fight-starting position or not, 
because a legal safe move is also a legal setup move.
If a player doesn’t want to set up a fight-starting position now, 
they need to make an optimal safe move to make the position balanced: -1 < position score < 1. 
If a player didn’t make an optimal safe move and didn’t set up a fight starting position, 
it is possible their opponent will choose the advantaged color directly, 
because now the position is unbalanced and the advantaged color can win.
If a player is checked, the player can either resolve the check, or make a setup move, 
or choose a must-win color directly.
It is possible that no Safe Move Phase in a game. 
At the first move, a tentative white player can choose a color directly 
or set up a fight-starting position and let his/her opponent to choose a color.

8.2    Decision Phase 

A player can choose a color directly on their turn, 
if they didn’t make a move. But they must choose the must-win color. 
Then their opponent is assigned to the opposite color automatically. 
Then the game goes into Fight Phase.
A player can set up a fight-starting position by a legal setup move on their turn. 
When a player sets up a fight-starting position, the color-to-move 
and must-win color must also be specified. 
Then, his/her opponent must choose a color, 
which can be the must-win color or the opposite color. 
After a player chose a color, the opponent’s color is fixed too. 
The game goes into Fight Phase.

8.3    Fight Phase

Now two colors are set. The two players must find the best moves. 
All standard xiangqi rules apply, except draw means loss for the must-win color.

====================================================================

9. Special Mechanics: “The Fight-Starting Position Setup Rules”

9.1 Legal setup move
Legal setup moves are legal moves in Decision Phase. They include legal safe moves and One-Free moves.

9.2 One-Free move
One-Free move is illegal in standard chess. 
It is designed to create more good fight-starting positions in Cusp Xiangqi by relocating at most one piece. 
There are two modes for One-Free move in Cusp Chess: Human-Level-Mode and Engine-Test-Mode.

9.3 Human-Level-Mode of One-Free move
•	A player can make no move.
•	A player can make an illegal move by relocating one of their own pawns onto a vacant square in the opponent’s half board.
•	A player can remove one piece from the board, including his/her opponent’s piece, except the two kings.
•	A player can’t move the opponent’s pieces.
•	If a color sets up a fight-starting position to let the opponent choose a color, the opposite color automatically becomes the side to move in Fight Phase. 
    For example, a tentative Red player set up a fight-starting position to let tentative Black player choose a color. 
	In the fight-starting position, the side to move must be Black.
•	If a player chooses a must-win color directly, the side to move in the position doesn’t change. 
    For example, if a tentative Red player chose a color directly, 
	in the fight starting position the Red side is to move.
•	All moves in Human-Level-Mode can’t break the rules in 9.5.
•	Human-Level-Mode is enough for human players and engines. 
    Rules of Human-Level-Mode can be refined if necessary. 
	The goal is to maximize the good fight starting position options for most safe positions 
	while minimize the number of legal setup move options.

9.4 Engine-Test-Mode of One-Free move
•	All moves in Human-Level-Mode in 9.3.
•	A player can relocate a piece of any color to any square (either empty or occupied).
•	A bishop can’t be relocated to the opposite color square.
•	A player can set the side to move freely when setting up a fight-starting position.
•	A pawn can be promoted when relocated directly to the last rank.
•	All moves in Engine-Test-Mode can’t break the rules in 9.5.
•	Engine-Test-Mode can create much more good fight-starting positions, 
    compared to Human-Level-Mode. It is not suitable for human players.

9.5 Forbidden moves and positions
•	Neither color can be checkmated.
•	The side to move can't be checking the opposite color.
•	Both kings can not be removed.
•	Moving more than one piece is not allowed.

9.6 Legal moves if they don’t break rules in 9.5
•	A player can setup a fight-starting position when a color is checked.


====================================================================  
9.7. Endgame and Victory Conditions
•	If the must-win color checkmates the opponent, it wins. Otherwise, it loses the game. Draw means loss for the must-win color.
•	If the must-win color is not set up in a game, Red is the must-win color by default. Draw means loss for the tentative Red player, because it is the tentative Red player’s responsibility to set up a fight-starting position.

====================================================================             
Two notation examples

1. CX {RS e0e1 BWBN} {0.91} 
2. CX {BCBW} {1.08} 
3. ... h7e7 {1.04} 
4. h0g2 {-0.98}  h9g7 {1.14} 
5. i0h0 {-0.95}  i9h9 {1.12} 

1. c0e2 {0.21}  h7h6 {-0.84} 
2. h2h5 {-0.16}  b7b8 {-0.6} 
3. CX {RS f0xx BWBN} {0.92} 
4. CX {BCBW} {1.0} 
5. ... g6g5 {1.05} 
6. h5h4 {-0.99}  h9g7 {1.08} 

for more information about notations, check pgnhistory.py

====================================================================  
Note: 
In real games, human players need to make good moves on their own.
They need to evaluate the moves and positions based on their chess skills.
If they made bad choices, they will get punished by their opponents.
====================================================================
For more details, please check the paper about FSPB and Cusp Xiangqi official rulebook.           
====================================================================
PS: The Cusp Xiangqi GUI is based on my Cusp Chess GUI. 
Sometimes, you will see chess in the code, but it is just xiangqi.
Sometimes, you will see white color in the code. It just means Red in xiangqi.  
"""
import logging
import os
import pathlib
import tkinter as tk
from datetime import datetime
from logging.handlers import RotatingFileHandler
from tkinter import *
from tkinter import messagebox, ttk

import cchess
from PIL import Image as PILImage

import ai.ai_utils
import ai.ChessEngine
import ai.safe_move_or_setup_thread
import ai.search_for_all_cusps_for_CC_thread

import ai.search_for_best_move_thread
import ai.stop_threads
import ai.update_editor_score_thread
import ui.blindfold
import ui.create_UI
import ui.editor
import ui.language

import ui.normalboard
import ui.setting_panel
import ui.ui_utils
import utils.config
import utils.game_state
import utils.pgnhistory
import utils.tournament

log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log_dir = "logs" 
os.makedirs(log_dir, exist_ok=True) 
log_file = os.path.join(log_dir, "app.log")

handler = RotatingFileHandler(
    log_file,
    maxBytes=1_000_000,
    backupCount=10
)
handler.setFormatter(log_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("tkinter").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.info("Application started")


class CuspXiangqiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cusp Xiangqi")
        self.geometry("1420x900")
        self.resizable(True, True)
        self.resizing_enabled = False
        self.icon_img = PhotoImage(file="assets/cuspXiangqiLogo.png")
        self.iconphoto(False, self.icon_img)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chess_container = ttk.Frame(self)
        self.chess_container.grid(row=0, column=0, sticky="nsew")
        self.chess_container.grid_propagate(False)  

        self.chess_container.grid_columnconfigure(0, weight=9)
        self.chess_container.grid_columnconfigure(1, weight=2)
        self.chess_container.grid_columnconfigure(2, weight=2)

        for i in range(10):
            self.chess_container.grid_rowconfigure(i, weight=1)

        self.editor_container = ttk.Frame(self)
        self.editor_container.grid(row=0, column=0, sticky="nsew")
        self.editor_container.grid_propagate(False)
        for i in range(10):
            self.editor_container.grid_rowconfigure(i, weight=1)
        ui.create_UI.create_UI(self)
 
        self.update()

    def create_Boards_menu(self):
        logger.info("create_Boards_menu")
        self.menubar = Menu(self)
        self.Boards_menu = Menu(self.menubar, tearoff=0)
        self.Boards_menu.add_command(label="Xiangqi", command=self.go_back_to_chess)
        self.Boards_menu.add_command( label="Board editor", command=self.go_to_editor_board )
        self.Boards_menu.add_command( label="Blindfold Xiangqi", command=self.go_to_blindfold_chess )
        self.config(menu=self.menubar)
        self.menubar.add_cascade(label="Boards", menu=self.Boards_menu)


    def create_setting_menu(self):
        logger.info("create_setting_menu")
        self.setting_menu = Menu(self.menubar, tearoff=0)
        self.setting_menu.add_command( label="Game Setting", command=lambda: ui.setting_panel.popup_user_setting(self) )

        self.menubar.add_cascade(label="Setting", menu=self.setting_menu)


    def create_language_menu(self):
        logger.info("create_language_menu")
        self.language_menu = Menu(self.menubar, tearoff=0)
        self.language_menu.add_command( label="English", command=self.set_to_English )
        self.language_menu.add_command( label="中文", command=self.set_to_Chinese )
        self.menubar.add_cascade(label="Language/语言", menu=self.language_menu)

    def set_to_English(self):
        logger.info("set_to_English")
        self.current_lang = "en"
        utils.config.save_setting_in_config_file(self)
        ui.language.update_texts(self)
        logger.info(f"self.current_lang: {self.current_lang}")

    def set_to_Chinese(self):
        logger.info("set_to_Chinese")
        self.current_lang = "cn"
        utils.config.save_setting_in_config_file(self)
        ui.language.update_texts(self)
        logger.info(f"self.current_lang: {self.current_lang}")

    def create_about_program_menu(self):
        logger.info("create_about_program_menu")
        self.game_menu = Menu(self.menubar, tearoff=0)
        self.game_menu.add_command(label="About", command=self.about_program)
        self.menubar.add_cascade(label="Help", menu=self.game_menu)

    def about_program(self):
        messagebox.showinfo(
            "About Cusp Xiangqi",
            "Cusp Chess 0.1.0 \n\nDesigner: Lei Gao, \nhahachess2025@gmail.com  \
            \n\nThis is open-source software. Please check readme.txt for more information \
            \n\nCopyright 2026 [Lei Gao], Licensed under the Apache License, Version 2.0",
        )

    def go_back_to_chess(self):
        logger.info("go_back_to_chess")
        self.blindfold_mode = False
        ai.stop_threads.stop_editor_threads(self)

        self.board_frame.tkraise()
        ui.normalboard.draw_chess_board(self)
        ui.ui_utils.draw_pieces(self, self.chess_game_variant_mode, False)
        ui.ui_utils.initialize_piece_images(self, self.chess_game_variant_mode)

        self.move_history_frame.tkraise()
        self.chess_container.tkraise()


    def go_to_editor_board(self):
        logger.info("go_to_editor_board")
        self.blindfold_mode = False
        self.tournament_start = False
        self.stop_game()

        ui.editor.create_editor_setting_UI(self)
        ui.editor.create_editor_board_frame(self)
        self.editor_container.tkraise()

        if self.board.turn:
            self.editor_radio_value.set(1)
        else:
            self.editor_radio_value.set(0)
        ui.editor.update_editor_color_to_move_label(self)

    def go_to_blindfold_chess(self):
        logger.info("go_to_blindfold_chess")
        self.tournament_start = False
        self.blindfold_mode = True
        ai.stop_threads.stop_editor_threads(self)
        self.stop_game()

        if not self.blindfold_cchess_frame:
            ui.blindfold.create_blindfold_cchess_frame(self)
        else:
            self.blindfold_cchess_frame.tkraise()

        self.board_frame.tkraise()
        self.chess_container.tkraise()
        self.board = cchess.Board()

        ui.normalboard.draw_chess_board(self)
        ui.ui_utils.draw_pieces(self, self.chess_game_variant_mode, False)
        ui.ui_utils.initialize_piece_images(self, self.chess_game_variant_mode)


    def start_game(self):
        logger.info("Start game")
        self.game_in_progress = True
        try:
            ui.ui_utils.confirm_players(self)
            ui.ui_utils.update_player_board_label(self)
            utils.config.read_config_file(self)
            #ui.ui_utils.initialize_piece_images( self, self.chess_game_variant_mode) 
            ui.ui_utils.generate_PGN_path(self)
            ui.ui_utils.set_timer(self)
        except Exception as e:    
            logger.exception("Start game error")
            self.after(0, lambda err=e: messagebox.showerror("Start game error", str(err)))
            return
        self.update()
        # press the "move finished" button.
        if self.chess_game_variant_mode == "CuspXiangqi":
            if self.player_one != "AI" or self.player_two != "AI":
                self.after(0,lambda:messagebox.showinfo("Notification about the \"Move finished\" button","After your move in the Safe Move or Decision Phases, please press the \"Move finished\" button on the top right to stop the timer."))

        if self.chess_game_variant_mode == "Normal":
            if (self.player_one == "AI" and self.board.turn) or ( self.player_two == "AI" and not self.board.turn ):
                self.AI_searching_best_move()
        elif self.chess_game_variant_mode != "Normal":
            if self.cusp_chess_phase == "SafeMove" or self.cusp_chess_phase == "Decision":
                if self.player_one == "AI" or self.player_two == "AI":
                    self.safe_move_or_setup_in_cusp_chess()
            elif self.cusp_chess_phase == "Fight":
                if (( self.player_swap_side == False and ( (self.player_one == "AI" and self.board.turn) or (self.player_two == "AI" and not self.board.turn) ) ) 
                or ( self.player_swap_side and ( (self.player_one == "AI" and not self.board.turn) or (self.player_two == "AI" and self.board.turn) ) )):
                    self.AI_searching_best_move()

      
    def stop_game(self):
        logger.info("Stop game")
        self.tournament_start = False 
        self.stop_game_in_tournament()
        utils.config.save_setting_in_config_file(self) 
        
    def stop_game_in_tournament(self):
        logger.info("stop_game_in_tournament")
        self.game_in_progress = False
        try:
            ai.stop_threads.stop_game_threads(self, 'QUIT')
        except Exception as e:
            logger.exception("Stop game error")
            self.after(0, lambda err=e: messagebox.showerror("Stop game error", str(err)))

    def reset(self):
        logger.info("Reset game")
        self.stop_game_in_tournament()
        if self.blindfold_mode:
            blindfold_mode = True
        else:
            blindfold_mode = False
        ui.ui_utils.clear_board_move_history(self)
        utils.game_state.initalize_basic_setting(self)
        ui.ui_utils.widget_initialization(self)
        utils.config.read_config_file(self)
        pathlib.Path(self.PGN_folder_path).mkdir(parents=True, exist_ok=True)
        ui.ui_utils.generate_PGN_path(self)

        ui.ui_utils.initialize_player_time_label(self)
        utils.pgnhistory.initialize_auto_play_PGN_button_text(self)

        if blindfold_mode:
            self.blindfold_mode = True
            cusp_app.blindfold_label_state='empty'
            ui.language.update_widget(cusp_app,cusp_app.blindfold_move_notice_label)
        else:
            self.blindfold_mode = False
        
        ui.normalboard.redraw_chess_board(self)
        ui.ui_utils.reset_two_player_scores_bar(self)
        ui.ui_utils.update_game_status_label(self, True)
        self.update()

    # Safe Move and Decision Phases.
    def safe_move_or_setup_in_cusp_chess(self):
        logger.info("safe_move_or_setup_in_cusp_chess")
        try:
            self.safe_move_or_setup_thread = ( ai.safe_move_or_setup_thread.SafeMoveOrSetupThread( app=self))
            self.safe_move_or_setup_thread.start()
            logger.info("self.safe_move_or_setup_thread started")
        except Exception as e:
            logger.exception("safe_move_or_setup_thread error")
            self.after(0, lambda err=e: messagebox.showerror("safe_move_or_setup_thread", str(err)))

    def AI_searching_best_move(self):
        logger.info("AI_searching_best_move")
        try:
            self.search_for_best_move_thread = ai.search_for_best_move_thread.SearchForBestMoveThread( app=self)
            self.search_for_best_move_thread.start()
            if self.safe_move_or_setup_thread and self.safe_move_or_setup_thread.is_alive():
                self.safe_move_or_setup_thread.stop()
                logger.info("self.safe_move_or_setup_thread stopped") 
            logger.info("self.search_for_best_move_thread started")    
        except Exception as e:
            logger.exception("search_for_best_move_thread error")
            self.after(0, lambda err=e: messagebox.showerror("search_for_best_move_thread", str(err)))

    def on_quit(self):
        logger.info("on_quit")
        ai.stop_threads.stop_game_threads(self,'QUIT')
        ai.stop_threads.stop_editor_threads(self,'QUIT')
        logger.info("cusp_chess program quit")
        self.destroy()


if __name__ == "__main__":
    try:
        cusp_app = CuspXiangqiApp()
        cusp_app.protocol("WM_DELETE_WINDOW", cusp_app.on_quit)
        cusp_app.mainloop()
    except Exception as e:  
        logger.critical("Unhandled exception in main loop", exc_info=True)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Fatal Error", str(e))
        except:
            pass