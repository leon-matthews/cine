
import builtins
from pathlib import Path
from pprint import pprint


builtins.pp = pprint                                # type: ignore[attr-defined]
DATA_FOLDER = Path(__file__).parent / 'data'
NUM_SAMPLE_ROWS = 20_000
