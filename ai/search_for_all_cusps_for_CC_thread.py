"""
search_for_all_cusps_for_CC_thread.py 
To learn Cusp Chess, we need to find all good fight starting positions based on a FEN.
for editor board.
"""

import ctypes
import logging
import threading
from tkinter import *
from tkinter import messagebox

import ai.ai_utils

logger = logging.getLogger(__name__)

class SearchForAllCuspsForCCThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self._stop_flag = threading.Event() 

    def run(self):
        logger.info("SearchForAllCuspsForCCThread, search started") 
        if len(self.app.editor_fen_text.get("1.0", END)) > 1:
            self.app.editor_fen_text.insert(END, "\n" + "fight starting positions for Cusp Xiangqi")
        else:    
            self.app.editor_fen_text.insert(END, "fight starting positions for Cusp Xiangqi")
        try:          
            ai.ai_utils.search_for_cusp_positions_for_CC( self.app, self.app.board.fen(), self.app.editor_engine, "all_cusps",self._stop_flag )
        except Exception as e:
            logger.exception('SearchForAllCuspsForCCThread, error')
            if self._stop_flag.is_set(): return
            self.app.after(0, lambda err=e: messagebox.showerror("Error", f"Searching all good fight starting positions: {err}"))
            return
        if self._stop_flag.is_set(): return    
        logger.info("SearchForAllCuspsForCCThread, search finished")
        messagebox.showinfo("Search Finished", "All good fight starting positions search finished" )

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
        logger.info("SearchForAllCuspsForCCThread _stop_flag set")