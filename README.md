# TouchpadDrawer
It is a simple python project that draws what you draw on the touch pad on a canvas using tutle.

# Important points
1. It is developed in linux environment and pretty sure it wont work with other systems.
2. python-evdev package has to installed for this to work.

# Execution Instruction
1. You have to know the device ID of the touchpad for execution.
2. To find the device id run the findId.py program to list out all the input devices.
3. It is in the format "/dev/input/eventx" where x is a number and is referred as device ID here.
4. Once the device ID is known, run the main.py file and enter the device ID (The number x).

# Operation Instruction
1. Have fun drawing stuff on the touchpad.
2. Press 'c' to clear the screen.
3. Press 'q' to quit the program.
