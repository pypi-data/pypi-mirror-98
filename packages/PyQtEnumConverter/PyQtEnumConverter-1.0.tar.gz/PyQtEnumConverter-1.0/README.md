# PyQtEnumConverter

PyQt6 changes the usage of enums. Here are some examples:
```python
#PyQt5
QLayout.SetFixedSize
#PyQt6
QLayout.SizeConstraint.SetFixedSize

#PyQt5
Qt.IgnoreAspectRatio
#PyQt6
Qt.AspectRatioMode.IgnoreAspectRatio
```
To change all of this is a lot of work when you port a big project from PyQt5 to PyQt6. To help porting I had written this little script that does the work for you. It works with files and directories, which are parsed recursive.
```
Usage: PyQtEnumConverter <file/directory>
```
This is a little script that I had written in a few hours. It may not work perfect and there's no warranty that it will not damage your project. It uses simple text replacement, so as imports are not supported. Please make a backup of your project before using it.
