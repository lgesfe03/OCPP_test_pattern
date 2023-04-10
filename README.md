"# OCPP_test_pattern" 

# Author : Mark Lin YL
# Date: 2023/04

This repository is used to search certain sum number from excel file.

# Package method
Due to "pyinstall" might pack too large size executable file, we create a virtual environment for packaging it.
Follow steps below:
1.Set python virtual environment:
  python -m pipenv --python 3.9
  
2.Start python virtual environment:
  python -m pipenv shell
  
3.Install modules python need:
	pip install pyinstaller
	pip install pandas openpyxl
  ...(else more if need)
  
4.Package Command: (set .exe file icon through first argv :XX.ico,  second argv to point out where main .py file is)
	pyinstaller -F -w -i D:\Tutorial\Python\find_sum_excel\icon\auto.ico D:\Tutorial\Python\find_sum_excel\find_sum_v2_OOP.py
	
# Output Path
Output executable file path:
	C:\Users\Mark\dist
