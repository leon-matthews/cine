"""
Help with importing movies and shows into collection.
"""

import re


class MovieImporter(object):
    """
    Import new, often poorly named files, into collection.

    Uses IMDb look-ups, heuristics, and plain-old user intervention to
    identify and rename movie files and folders.
    """
    def __init__(self):
        pass

    def clean_name(self, name):
        """
        Clean given folder or file name.

        Best-effort tidy-up of file or folder name before passing it on to
        the lookup layer.
        """
        # Trim any excess white-space
        clean = name.strip()
        # Drop 3 or 4 character extension
        clean = re.sub(r'\.\w{3,4}$', '', clean)
        # Year should be wrapped in parethesises
        clean = re.sub(r'[\[](\d{4})[\]]', r'(\1)', clean)
        return clean


