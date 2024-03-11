
from pathlib import Path


class Importer:
    def  __init__(self, folder: Path):
        """
        Initialiser.

        Args:
            folder:
                Directory containing IMDB data files.

        """
        self.folder = folder
        pp(self.folder)
