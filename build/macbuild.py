# Why am I not using Make?
# 1.)   I want total control over the system. 
#       Occassionally I want to have some logic
#       in my compilation process.
# 2.)   Realistically our projects are 'small' enough 
#       this will not matter.
# 3.)   Feel free to implement your own make files.
# 4.)   It is handy to know Python


import os

COMPILER="g++"

SOURCE="./src/*.cpp"

# You can can add other arguments as you see fit.
# What does the "-D MAC" command do? 
ARGUMENTS="-D MAC -std=c++17 -shared -undefined dynamic_lookup" 

# Which directories do we want to include.
INCLUDE_DIR="-I ./include/ -I./pybind11/include/ -I/Library/Frameworks/SDL2.framework/Headers `python3.9 -m pybind11 --includes`"

# What libraries do we want to include
LIBRARIES="-F/Library/Frameworks -framework SDL2 `python3.9-config --ldflags`"

# The name of our executable
EXECUTABLE="bobotronEngine.so"

# Build a string of our compile commands that we run in the terminal
compileString=COMPILER+" "+ARGUMENTS+" -o "+EXECUTABLE+" "+" "+INCLUDE_DIR+" "+SOURCE+" "+LIBRARIES

# Print out the compile string
print(compileString)

# Run our command
os.system(compileString)
