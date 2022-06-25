import databaseHandler
import pytest

def setup():
    print("WRITE TESTING")

def write_test():
    assert databaseHandler.sheetWriteSmth('Test') == [['Test']]
    print("Database writing is accessible!")
