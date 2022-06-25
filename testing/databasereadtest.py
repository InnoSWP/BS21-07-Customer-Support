import databaseHandler
import pytest

def setup():
    print("READ TESTING")


def read_test():
    assert databaseHandler.sheetReadFirst() == ([['Questions']])
    print("Database reading is accessible!")
