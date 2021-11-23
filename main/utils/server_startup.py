import logging
import os
import coloredlogs

from main.utils.fonbet_parser import EventsParser
from main.utils.model_updates import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger)


def on_startup():
    init_db_clean()
    logger.info("DB cleanup complete")
    parser = EventsParser()
    initial_updates = parser.get_updates()
    os.environ['current_version'] = str(parser.current_version)

    for sport in initial_updates.get('sports'):
        init_sport(sport)
    logger.info("SportKind/segment models initialization complete")

    for event in initial_updates.get('events'):
        init_event(event)
    logger.info("Events/EventSegments models initialization complete")

    for misc in initial_updates.get('eventMiscs'):
        init_event_misc(misc)
    logger.info("Miscs initialization complete")

    for factor in initial_updates.get('customFactors'):
        init_factors(factor)
    logger.info("Factors initialization complete")

    for block in initial_updates.get('eventBlocks'):
        init_event_block(block)
    logger.info("Event blocks initialization complete")

    logger.info("All models initialization complete")
