# Why am I not using Make?
# 1.)   I want total control over the system.
#       Occassionally I want to have some logic
#       in my compilation process.
# 2.)   Realistically our projects are 'small' enough
#       this will not matter.
# 3.)   Feel free to implement your own make files.
# 4.)   It is handy to know Python

# python3.10 linuxbuild.py

import os

COMPILER="g++"

SOURCE="./src/*.cpp"

# You can can add other arguments as you see fit.
# What does the "-D LINUX" command do?
ARGUMENTS="-D LINUX -std=c++17 -shared -fPIC"

# Which directories do we want to include.
INCLUDE_DIR="-I ./include/ -I./pybind11/include/ `python3.10 -m pybind11 --includes`"

# What libraries do we want to include
LIBRARIES="-lSDL2 -ldl `python3.10-config --ldflags`"

# The name of our module
EXECUTABLE="bobotronEngine.so"

# Build a string of our compile commands that we run in the terminal
compileString=COMPILER+" "+ARGUMENTS+" -o "+EXECUTABLE+" "+" "+INCLUDE_DIR+" "+SOURCE+" "+LIBRARIES

# Print out the compile string
print(compileString)

# Run our command
os.system(compileString)
