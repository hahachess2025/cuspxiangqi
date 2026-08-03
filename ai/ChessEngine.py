import logging
import threading
import time
from tkinter import *
from tkinter import messagebox

import cchess
import cchess.engine
from typing import Tuple, Optional
from PIL import Image as PILImage

logger = logging.getLogger(__name__)

class ChessEngine:
    def __init__(self, app, engine_path, options=None, info_handler=None, limit=0.1):
        super().__init__()
        logger.info("ChessEngine __init__") 
        self.app = app
        self.daemon = True
        self.engine_path = engine_path
        self.options = options or {}
        self.info_handler = info_handler
        self.limit = limit
        self.engine = None
        self._stop_flag = threading.Event()   
        self.run()  # Initialize the engine
        logger.info("ChessEngine initialization success")

    def run(self):
        try:
            self.engine = cchess.engine.SimpleEngine.popen_uci(self.engine_path)
            self.engine.configure({"Hash": 512, "Threads": 1, })
        except Exception as e:
            logger.exception(f"engine initialization error {self.engine_path}")
            messagebox.showerror("Error", f"Engine initialization error: {e}" )
        for option, value in self.options.items():
            self.engine.setoption({option: value})
        if self.info_handler:
            self.engine.info_handlers.append(self.info_handler)

    def go(self, board, limit):
        logger.info("ChessEngine go")     
        if self.app.engine_time_limit_enable:
            search_limit=cchess.engine.Limit(time=limit)
        else:
            search_limit=cchess.engine.Limit(depth=limit)
  
           
        restart_number = 0
        while not self._stop_flag.is_set():
            restart_number+=1
            if restart_number>3:
                return
            try:
                if self.engine:
                    if self.app.legacy_engine_mode:
                        result = self.engine.analyse(board, search_limit)
                        if self._stop_flag.is_set():
                            return
                        if "score" in result and "pv" in result:    
                            return result

                    last_info_with_score = None
                    with self.engine.analysis(board, search_limit) as analysis:
                        for info in analysis:
                            if "score" in info and "pv" in info:
                                last_info_with_score = info  
                            
                            if self._stop_flag.is_set():
                                logger.info("Engine stopped by user")
                                return


                    if last_info_with_score is not None:
                        return last_info_with_score
                    logger.info("Fallback: engine.analyse() called for newer engine")  
                   
                    result = self.engine.analyse(board, search_limit)
                    if self._stop_flag.is_set():
                        logger.info("chess engine stopped by user")
                        return
                    if "score" in result and "pv" in result:    
                        return result
                    logger.info('the engine can not return score and pv ')
            except (cchess.engine.EngineTerminatedError, BrokenPipeError, OSError) as e:
                logger.exception(f"Engine crashed: {e}. Restarting...")
                try:
                    self.engine.quit()
                except Exception as e:
                    pass  # engine might already be dead
                time.sleep(0.2)
                self.engine = cchess.engine.SimpleEngine.popen_uci(self.engine_path)
                logger.info("Engine restarted, continuing search...")

            
    def score_and_top_moves(self, board, limit,multipv=1):
        logger.info("score_and_top_moves go") 
        if self.app.engine_time_limit_enable:
            search_limit = cchess.engine.Limit(time=limit)
        else:
            search_limit = cchess.engine.Limit(depth=limit)

        try:
            if self.engine:
                supported, default_mpv, max_mpv = self.query_multipv_support(self.engine)

                if supported:
                    multipv= int(min(multipv, max_mpv))
                    if multipv<1:
                        multipv=1
                
                    info = self.engine.analyse(board, search_limit, multipv=multipv)
                    if self._stop_flag.is_set():
                        logger.info("Engine stopped by user")
                    return info
                    
                else:
                    info = self.app.analyse( board, search_limit )
                    if self.app.editor_engine_multipv>0: 
                        if "pv" not in info or not info["pv"]:
                            best_move = self.app.app.play(board, search_limit).move
                            info["pv"] = [best_move]
                    info_list = [info]
                    return info_list
        except (cchess.engine.EngineTerminatedError, BrokenPipeError, OSError) as e:
            logger.exception(f"Engine crashed: {e} ")
            try:
                self.engine.quit()
            except Exception as e:
                pass  # engine might already be dead

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
              
               
    def stop(self):
        self._stop_flag.set()
        logger.info("chess engine stop command")  

    def reset(self):
        self._stop_flag.clear()
        logger.info("chess engine reset command")  

        
    def quit(self):
        if self.engine:
            try:
                self.engine.quit()
            except cchess.engine.EngineTerminatedError:
                pass 
            self.engine = None
 
    def __del__(self):
        self.quit()
