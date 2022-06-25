import databaseHandler
import pytest

def setup():
    print("READ TESTING")


def test_read():
    assert databaseHandler.sheetReadFirst() == ([['Questions']])
    print("Database reading is accessible!")
