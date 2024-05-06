
import builtins
from pathlib import Path
from pprint import pprint

builtins.pp = pprint

DATA_FOLDER = Path(__file__).parent / 'data'
NUM_SAMPLE_ROWS = 10_000 - 1
