import logging

logger = logging.getLogger(__name__)

def stop_editor_threads(cusp_app, engine_action='STOP'):
    logger.info("stop_editor_threads")
    CC_thread = cusp_app.search_for_all_cusps_for_CC_thread

    score_thread = cusp_app.update_editor_score_thread

    if CC_thread and CC_thread.is_alive():
        CC_thread.stop()
        logger.info('search_for_all_cusps_for_CC_thread stopped')

    if score_thread and score_thread.is_alive():
        score_thread.stop()
        logger.info('update_editor_score_thread stopped')
        
    if cusp_app.editor_engine: 
        if engine_action == 'STOP':
            cusp_app.editor_engine.stop()
            logger.info('editor_engine stopped')
        elif engine_action == 'QUIT':
            cusp_app.editor_engine.quit()
            logger.info('editor_engine quit')


def stop_game_threads(cusp_app, engine_action='STOP'):
    logger.info('stop_game_threads')
    fight_thread = cusp_app.search_for_best_move_thread
    before_fight_thread = cusp_app.safe_move_or_setup_thread

    if fight_thread and fight_thread.is_alive():
        fight_thread.stop()
        logger.info('search_for_best_move_thread stopped')
        
    if before_fight_thread and before_fight_thread.is_alive():
        before_fight_thread.stop()
        logger.info('safe_move_or_setup_thread stopped')
        
    if engine_action == 'STOP':
        if cusp_app.engine_one and not isinstance(cusp_app.engine_one, str):
            cusp_app.engine_one.stop()
            logger.info('engine_one stopped')
            
        if cusp_app.engine_two and not isinstance(cusp_app.engine_two, str):
            cusp_app.engine_two.stop()
            logger.info('engine_two stopped')
            
        if cusp_app.adjudicator_engine:
            cusp_app.adjudicator_engine.stop()
            logger.info('adjudicator_engine stopped')
            
    elif engine_action == 'QUIT':
        if cusp_app.engine_one and not isinstance(cusp_app.engine_one, str):
            cusp_app.engine_one.quit()
            logger.info('engine_one quit')
            
        if cusp_app.engine_two and not isinstance(cusp_app.engine_two, str):
            cusp_app.engine_two.quit()
            logger.info('engine_two quit')
            
        if cusp_app.adjudicator_engine:
            cusp_app.adjudicator_engine.quit()
            logger.info('adjudicator_engine quit')
