
from unittest import TestCase

from cine.tables import TableBase


class TableBaseTest(TestCase):
    def test_bad_child_error(self) -> None:
        """
        Produce nice error if child class missing required attributes.
        """
        message = (
            r"BadChild missing required attributes: "
            r"insert_query, table_name, table_query$"
        )
        with self.assertRaisesRegex(NotImplementedError, message):
            class BadChild(TableBase):
                pass
