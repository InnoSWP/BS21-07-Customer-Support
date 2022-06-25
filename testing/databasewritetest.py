import databaseHandler

def setup():
    print("WRITE TESTING")

def test_write():
    assert databaseHandler.sheetWriteSmth('Test') == [['Test']]
    print("Database writing is accessible!")
