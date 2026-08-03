"""
update_editor_score_thread.py

This module is for updating score for board editor.

"""
import cchess
import cchess.engine
from typing import Tuple, Optional

import ctypes
import logging
import threading
from tkinter import *
from tkinter import messagebox

import ui.ui_utils

logger = logging.getLogger(__name__)

class UpdateEditorScoreThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self._stop_flag = threading.Event() 

    def run(self):
        logger.info("UpdateEditorScoreThread run")
        if self.app.editor_engine_analyse_enable and self.app.editor_engine_exist:
            
            try:
                supported, default_mpv, max_mpv = self.query_multipv_support(self.app.editor_engine.engine)
                multipv=1
                if self.app.editor_engine_multipv>0 and supported:
                    multipv= int(min(self.app.editor_engine_multipv, max_mpv))
                    if multipv<1:
                        multipv=1
                info_result =self.app.editor_engine.score_and_top_moves( self.app.board, limit=self.app.editor_engine_evaluation_limit, multipv=multipv )
                info_list = info_result if isinstance(info_result, list) else [info_result]

                for i, entry in enumerate(info_list):
                    move = entry["pv"][0]
                    score = entry["score"].red().score(mate_score=10000) / 100.0
                    if i==0:
                        position_score = score 
                        if self.app.editor_engine_multipv>0:
                            if len(self.app.editor_fen_text.get("1.0", END)) > 1:
                                self.app.editor_fen_text.insert(END, "\n" + "-" * 30 + "\n")
                            else:
                                self.app.editor_fen_text.insert(END, "-" * 30 + "\n")                         
                    # output moves
                    if self.app.editor_engine_multipv>0:     
                        move_score_str=f'{i+1}, {move}, Eval: {score}'                     
                        self.app.editor_fen_text.insert(END, str(move_score_str)+ "\n")  
                        self.app.editor_fen_text.see("end")    
            except Exception as e:
                logger.exception('UpdateEditorScoreThread, engine error')
                if self._stop_flag.is_set(): return
                self.app.after(0, lambda err=e: messagebox.showerror("Engine Error", f"When updating editor board score bar: {err}"))
                return
            self.app.editor_engine_score_label["text"] = self.app.translations[self.app.current_lang]['Now_Score_is'] + str( position_score )

            # eval bar from Red perspective

            player_one_white_top = ui.ui_utils.convert_score_to_eval_bar( self.app, -position_score, self.app.editor_canvas_size )
            self.app.editor_player_one_bar.delete("all")
            self.app.editor_player_one_bar.create_rectangle(
                0, 0, 20, player_one_white_top, fill="#000000", outline=""
            )
            self.app.editor_player_one_bar.create_rectangle(
                0,
                player_one_white_top,
                20,
                int(self.app.editor_canvas_size * 10 / 9),
                fill="#FFFFFF",
                outline="",
            )

            self.app.editor_player_one_bar.update()
            self.app.update()


    def query_multipv_support(self, engine: cchess.engine.SimpleEngine) -> Tuple[bool, int, Optional[int]]:
        """
        Return (supported, default_value, max_value_or_None).

        - supported: True if an option with name 'multipv' (case-ins) is present.
        - default_value: default value reported by the engine (int) or 1 if unknown.
        - max_value_or_None: max allowed value (int) or None if engine didn't report.
        """
        try:
            opts = engine.options  # may raise if engine dead
        except Exception:
            return False, 1, None

        # keys are usually strings; do a case-insensitive search
        for name, opt in opts.items():
            try:
                if isinstance(name, str) and name.lower() == "multipv":
                    # opt is an Option-like object from python-chess
                    # It usually has attributes: name, type, default, min, max
                    default = None
                    maxv = None
                    # get default
                    if hasattr(opt, "default") and opt.default is not None:
                        try:
                            default = int(opt.default)
                        except Exception:
                            default = None
                    # get max (some engines set opt.max, sometimes opt.max is None)
                    if hasattr(opt, "max") and opt.max is not None:
                        try:
                            maxv = int(opt.max)
                        except Exception:
                            maxv = None

                    # fallback defaults
                    if default is None:
                        default = 1
                    return True, int(default), (int(maxv) if maxv is not None else None)
            except Exception:
                # defensive: some engines/options may be weird objects; ignore and continue
                continue

        return False, 1, None

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc( thread_id, ctypes.py_object(SystemExit) )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            logger.info("Exception raise failure")

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def stop(self):
        self._stop_flag.set()
        logger.info("UpdateEditorScoreThread _stop_flag set")