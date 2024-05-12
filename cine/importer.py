
from pathlib import Path


class Importer:
    """
    Manages the process of importing IMDB data from its TSV files into
    our SQLite database.
    """
    def  __init__(self, folder: Path):
        """
        Initialiser.

        Args:
            folder:
                Directory containing IMDB data files.

        """
        self.folder = folder
        pp(self.folder)
