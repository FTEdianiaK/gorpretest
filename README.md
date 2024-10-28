# Gorpretest

🥜 A nutty taste test of running software.

---

### How to run

![PYTHON](https://img.shields.io/badge/PYTHON-yellow?style=for-the-badge) ![WINDOWS](https://img.shields.io/badge/WINDOWS-blue?style=for-the-badge) ![LINUX](https://img.shields.io/badge/LINUX-black?style=for-the-badge)

You'll need python, then it's just the matter of correctly running the program.

For all the required arguments, look no further than the program's help page:

```
gorpretest <COMPILED C> <TEST DIRECTORY> <NUMBER START> <NUMBER END> [INSTRUCT SUFFIX] [ASSUME SUFFIX]

<>/* = required arguments

COMPILED C*
    or any other executable program

TEST DIRECTORY*
    a directory to pull the inputs and expected outputs from

NUMBER START*
    the number the tests should start at

NUMBER END*
    the number the tests should end at

INSTRUCT SUFFIX
    you can enter your own or it defaults to
    "_in.txt" (no matter the platform)

ASSUME SUFFIX
    you can enter your own or it defaults to
    "_out_win.txt" on Windows
    "_out.txt" on Linux

# FILE NAME FORMAT
  <TEST DIRECTORY>/<NUMBER ZERO-PADDDED TO FOUR><CHOSEN SUFFIX>
  e.g. gorpretest.py a.exe sample 1 11
       sample/0001_in.txt -- sample/0011_out_win.txt
```

### Credits

- [subprocess, time, sys, pathlib, difflib - from Python Standard Library - PSF](https://docs.python.org/3/library/index.html)
