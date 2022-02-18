# Make sure module files are processed
import hacks as _
import logging
from rich import pretty, traceback
from rich.logging import RichHandler
from update_offsets import update_offsets

def bootstrap():
    pretty.install()
    traceback.install()

    logging.basicConfig(format='%(message)s.', level='INFO', handlers=[RichHandler()])

    logging.info('Updating offsets')
    if not update_offsets():
        raise Exception('Failed to update offsets')
    logging.info('Offsets updated sucessfully!')