# Python 3.4
import os

# Windows uses backward slash; Mac & Linux uses forward slash
# But python will always recognise forward slash

# Python recognises everything as a sequence of unicode characters (string)
# Computer manages directories as a sequence of bytes (byte stream)\
# To read or write unicode characters from byte stream, encoding is required
# Different OS use different methods for encoding
# Windows might use CP-1252; Unix/ Mac might use "utf-8"
# To make the code platform independent use "utf-8" for encoding

my_file_path = "D://Vinoth//LEARNING//Python//PROJECTS//test//test.txt"


def readfile(fpath):
    # using "with:" will ensure that the file object is closed
    # #automatically by python after the loop is executed
    with open(fpath, "r", encoding="utf-8") as myfile:
        for each_line in myfile:
            print(each_line.rstrip())


def writefile(fpath, mode, text):
    # using "with:" will ensure that the file object is closed
    # automatically by python after the loop is executed
    with open(fpath, mode, encoding="utf-8") as myfile:
        myfile.write(text)


if os.path.isfile(my_file_path):
    readfile(my_file_path)
    writefile(my_file_path, "w", "Hello")
    readfile(my_file_path)
    writefile(my_file_path, "a", "there")
    readfile(my_file_path)
    writefile("test//test.log", "a", "Hello")
    writefile("test//test.log", "a", "world")
    readfile("test//test.log")
else:
    print("File not found")
