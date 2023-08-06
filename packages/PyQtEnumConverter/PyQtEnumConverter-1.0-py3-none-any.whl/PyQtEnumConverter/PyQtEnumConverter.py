import PyQt6.QtWidgets
import PyQt6.QtCore
import PyQt6.QtGui
import enum
import sys
import os

def get_enums_of_object(obj,data):
    data[obj.__name__] = {}
    for key,value in obj.__dict__.items():
        if isinstance(getattr(obj,key),enum.EnumMeta):
            data[obj.__name__][key] = []
            for i in getattr(obj,key):
                a,b = str(i).split(".")
                data[obj.__name__][key].append(b)

def parse_pyqt_object(obj,data):
    for i in obj.__dir__():
        if i.startswith("_"):
            continue
        try:
            get_enums_of_object(getattr(obj,i),data)
        except:
            pass

def replace_in_file(path,data):
    try:
        with open(path,"r") as f:
            content = f.read()
    except:
        print(f"Can't read {path}",file=sys.stderr)
        return
    for classes, enum in data.items():
        for name,value in enum.items():
            for i in value:
                old = classes + "." + i
                new = classes + "." + name + "." + i
                content = content.replace(old,new)
    with open(path,"w") as f:
        f.write(content)

def loop_directory(path,data):
    for i in os.listdir(path):
        current = os.path.join(path,i)
        if os.path.isdir(current):
            loop_directory(current,data)
        else:
            replace_in_file(current,data)

def main():
    if len(sys.argv) < 2:
        print("Usage: PyQtEnumConverter <file/directory>",file=sys.stderr)
        sys.exit(1)
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"{target} does not exists",file=sys.stderr)
        sys.exit(1)
    data = {}
    parse_pyqt_object(PyQt6.QtWidgets,data)
    parse_pyqt_object(PyQt6.QtCore,data)
    parse_pyqt_object(PyQt6.QtGui,data)
    try:
        from PyQt6 import Qsci
        parse_pyqt_object(Qsci,data)
    except:
        pass
    if os.path.isdir(target):
        loop_directory(target,data)
    else:
        replace_in_file(target,data)
