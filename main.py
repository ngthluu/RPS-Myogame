import os
import ctypes

# Change path to lib
os.chdir(os.getcwd() + r"\lib")

# Get main dll file
dll = ctypes.cdll.LoadLibrary(os.getcwd() + r"\MyoData.dll")


if dll.myo_init() :

    try:
        while True:
            dll.myo_run()
            pointer_emg = dll.get_emg_data()
            arr = (ctypes.c_int * 8).from_address(pointer_emg)
            data_list = [arr[i] for i in range(8)]
            print(data_list)
        dll.myo_exit()

    except KeyboardInterrupt as e:
        print("Exiting...")
        dll.myo_exit()
    