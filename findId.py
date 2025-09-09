from evdev import InputDevice, list_devices

def findTouchpad():
    devices = [InputDevice(path) for path in list_devices()]
    for dev in devices:
        # print(dev.path,"---", dev.name,"---", dev.phys)
        if ("Touchpad" in dev.name):
            print("Touchpad path found!!")
            print("Touchpad path : " + dev.path)
            return dev.path
    else:
        print("Error : Couldn't resolve path of the touchpad ")
