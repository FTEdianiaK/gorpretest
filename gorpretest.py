# Gorpretest: A nutty taste test of running software.
# Copyright (C) 2024  Foxie EdianiaK a.k.a. F_TEK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
from time import time
from sys import argv, platform
from pathlib import Path
from difflib import Differ


# Inititate the dividor constant
DIV = "- ~ - ~ - ~ - ~ - ~ -"


# PRE-RUN CHECKS #
if len(argv) == 1:
    # If no arguments were given, display help
    print("gorpretest <COMPILED C> <TEST DIRECTORY>"
          + " <NUMBER START> <NUMBER END>"
          + " [INSTRUCT SUFFIX] [ASSUME SUFFIX]")
elif argv[1] in ["-h", "--help"]:
    # Allow for displaying full help
    print("gorpretest <COMPILED C> <TEST DIRECTORY>"
          + " <NUMBER START> <NUMBER END>"
          + " [INSTRUCT SUFFIX] [ASSUME SUFFIX]")
    print("""
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
       sample/0001_in.txt -- sample/0011_out_win.txt""")
elif argv[1] in ["-v", "--version"]:
    # Allow for displaying the current version and license info
    print("Gorpretest [1.0.0] - A nutty taste test of running software.")
    print()
    print("""Copyright (C) 2024  Foxie EdianiaK a.k.a. F_TEK
This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions.
For more details refer to the LICENSE file in the GitHub repository.""")
elif len(argv) < 5:
    # Check the minimum amount of required arguments.
    print("\nErr: Wrong amount of arguments.")
else:
    # Display license info
    print("Gorpretest [1.0.0] - A nutty taste test of running software.")
    print()
    print("""Copyright (C) 2024  Foxie EdianiaK a.k.a. F_TEK
This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions.
For more details refer to the LICENSE file in the GitHub repository.""")

    # Initiate the error monitor
    check = True

    # GIVEN ARGUMENT/INPUT CHECK #

    """
    Executable Program Check
    - Check if the given path:
      - is valid.
      - is a file.
      - is runnable from the current platfrom.
        (.exe for Windows, not .exe for Linux)
    """
    PROGRAM = Path(argv[1])
    PROGRAM_ABS = PROGRAM.absolute()
    if not PROGRAM.is_file():
        print(f"\nErr: Entered program ({PROGRAM}) is not a file.")
        check = False
    elif (PROGRAM.suffix != ".exe" and "win" in platform):
        print(f"\nErr: This program ({PROGRAM}) isn't runnable"
              + " from a Windows console.")
        check = False
    elif (PROGRAM.suffix == ".exe" and "linux" in platform):
        print(f"\nErr: This program ({PROGRAM}) isn't runnable"
              + " from a Bash-like console.")
        check = False

    """
    Sample Directory Check
    - Check if the given path:
      - is valid.
      - is a directory.
    """
    TEST_DIRECTORY = Path(argv[2])
    if not TEST_DIRECTORY.is_dir():
        print(f"\nErr: Entered path ({TEST_DIRECTORY}) is not a directory.")
        check = False

    """
    File Range Check
    1. Check if entered numbers are valid.
    2. Add custom suffixes or uses default platform-dependant ones.
    3. Check if the first "ins" and last "as" file could be found.
    """
    TEST_INT_START = argv[3]
    try:
        TEST_INT_START = int(argv[3])
    except ValueError:
        print(f"\nErr: The entered start number ({TEST_INT_START})"
              + " is not a number.")
        check = False

    TEST_INT_END = argv[4]
    try:
        TEST_INT_END = int(argv[4])
    except ValueError:
        print(f"\nErr: The entered end number ({TEST_INT_END}) is not a number.")
        check = False

    if len(argv) == 7:
        TEST_INS_SUF = argv[5]
        TEST_AS_SUF = argv[6]
    else:
        TEST_INS_SUF = "_in.txt"
        if "win" in platform:
            TEST_AS_SUF = "_out_win.txt"
        elif "linux" in platform:
            TEST_AS_SUF = "_out.txt"

    try:
        with open(f"{TEST_DIRECTORY}/"
                  + f"{TEST_INT_START:04}{TEST_INS_SUF}", "r") as f:
            f.close()
    except FileNotFoundError:
        print("\nErr: Couldn't find file "
              + f"{TEST_INT_START:04}{TEST_INS_SUF}"
              + f" in /{str(TEST_DIRECTORY)}.")
        check = False

    try:
        with open(f"{TEST_DIRECTORY}/"
                  + f"{TEST_INT_END:04}{TEST_AS_SUF}", "r") as f:
            f.close()
    except FileNotFoundError:
        print("\nErr: Couldn't find file "
              + f"{TEST_INT_END:04}{TEST_AS_SUF}"
              + f" in /{str(TEST_DIRECTORY)}.")
        check = False

    """
    Manual User Check
    - List all the entered information.
    - Last stop before the program starts all the tests.
    """
    if check:
        print("\n" * 50)
        print("PRE-RUN CHECKS complete!")
        print(f"About to run {str(PROGRAM)}"
              + f" with files ({TEST_INT_START:04}{TEST_INS_SUF}"
              + f" // {TEST_INT_END:04}{TEST_AS_SUF})"
              + f" from /{TEST_DIRECTORY}.")
        fin = input("Continue? [Y/n] ")
        if fin.upper() == "N":
            check = False
            print("Aww, goodbye then. ;C")
        else:
            print("Yum, yum~ >o<")

    if check:
        print(DIV)

        # Initialize variables for statistics
        tests = 0
        times = []

        for i in range(TEST_INT_START, TEST_INT_END + 1):
            # Load current test's file paths
            instruct = f"{TEST_DIRECTORY}/{i:04}{TEST_INS_SUF}"
            assume = f"{TEST_DIRECTORY}/{i:04}{TEST_AS_SUF}"

            # Actually run the given program
            with open(instruct, "r") as f:
                print(f"\n>> Running TEST #{i}...")

                # Save start time, used for time calculations
                time_start = time()

                r = subprocess.run([PROGRAM_ABS],
                                   stdin=f,
                                   capture_output=True).stdout

                # Calculate the time the program took to run
                time_end = time()
                time_done = time_end - time_start

                f.close()

            """
            Compare with expected results.
            - If they match:
              - add time to average list.
              - tell the user that all is well.
            - If they do NOT match:
              - show the user a diff between
                the given output and expected output.
              - tell the user.
            """
            with open(assume, "rb") as f:
                # Load current test's assumed output
                test = f.read()

                # Rounded time for later messages
                time_done_round = round(time_done, 3)

                if r != test:
                    # Decoded bytes for Differ
                    r_raw = r.decode().splitlines(True)
                    test_raw = test.decode().splitlines(True)

                    print(''.join(Differ().compare(r_raw, test_raw)), end="")
                    input(f">> TEST {i} ({time_done_round}s) failed!")
                else:
                    print(f">> TEST #{i} done in {time_done_round}s!")
                    times.append(time_done)
                    tests += 1

                f.close()

        # Calculate time statistics
        time_avg = round((sum(times) / len(times)), 6)
        time_max = round(max(times), 6)

        # Calculate number of tests
        total_tests = len(range(TEST_INT_START, TEST_INT_END + 1))

        """
        Final Report
        - Which consists of:
          - the dividor.
          - number of successfully finished tests.
          - total number of ran tests.
          - statistics, such as:
            - the average runtime.
            - the longest runtime of all successful tests.
        """
        print("\n" + DIV)
        print(f"{tests}/{total_tests} TESTS passed!")
        print("\nRUNTIME STATISTICS")
        print(f"Average: {time_avg} seconds")
        print(f"Max: {time_max} seconds")
