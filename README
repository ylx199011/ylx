## Overview

**AutoCheckC** is mainly written in Python (with some bash shell as complements)
to automatically check homework of C code and running screenshot.


## System requirements

- A not too ancient Linux with Python 2.7 installed (Ubuntu 16.04  is recommended).


## Usage

1. Check out the project, or download "auto_collect.py", "auto_compile_run.sh" and
"name.csv" directly into one directory (e.g. myroot).
2. Fill in No. and names of students into "name.csv". You can open csv in excel and copy two columns
in one step.
3. Create a folder named "homework" under "myroot". Unzip homework into it.
4. 
```bash
cd myroot; python auto_collect.py week_num   # set week_num=1,2,3...
```
5. Check if there is a file named "grade.csv" and see what the grades read.

**Note:** 
1. Here we only compile the codes. If you'd like to risk your computer to run the codes,
you'll have to run "auto_compile_run.sh" as follows.
```bash
cd myroot; bash auto_compile_run.sh
```
2. Change permisions if needed.
```bash
chmod 777 auto_collect.py auto_compile_run.sh
```
## Rating rules

Codes and screenshots delivered & compiled through - A
Codes and screenshots delivered & compiled failure - B
Only codes delivered & compiled through            - C
Only codes delivered & compiled failure            - D
Only screenshots delivered                         - D
Otherwise                                          - E
