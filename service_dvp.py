"""
DVP Camera Service (Python 3.6)
Writes frames to Shared Memory (mmap) for high-performance IPC.
"""
import sys
import time
import argparse
import numpy as np
import cv2

# Import DVP driver
try:
    from dvp import *
except ImportError:
    print("FATAL: Could not import 'dvp'. Make sure dvp.pyd is in the python path.")
    sys.exit(1)

# Import Shared Memory Manager
try:
    from shared_memory_utils import SharedMemoryManager
except ImportError:
    print("FATAL: Could not import 'shared_memory_utils'.")
    sys.exit(1)

def frame2mat(frameBuffer):
    """Convert frame buffer to numpy array"""
    frame, buffer = frameBuffer
    bits = np.uint8 if(frame.bits == Bits.BITS_8) else np.uint16
    shape = None
    if(frame.format >= ImageFormat.FORMAT_MONO and frame.format <= ImageFormat.FORMAT_BAYER_RG):
        shape = 1
    elif(frame.format == ImageFormat.FORMAT_BGR24 or frame.format == ImageFormat.FORMAT_RGB24):
        shape = 3
    elif(frame.format == ImageFormat.FORMAT_BGR32 or frame.format == ImageFormat.FORMAT_RGB32):
        shape = 4
    else:
        return None

    mat = np.frombuffer(buffer, bits)
    mat = mat.reshape(frame.iHeight, frame.iWidth, shape)
    return mat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=65432, help="Unused in Shared Memory mode")
    parser.add_argument("--device", type=str, default=None, help="Device FriendlyName or Index")
    args = parser.parse_args()

    # 1. Setup Camera
    camera = None
    try:
        if args.device and args.device.isdigit():
             camera = Camera(int(args.device))
        elif args.device:
             camera = Camera(str(args.device))
        else:
             # Auto select first
             camera = Camera(0)
             
        camera.TriggerState = False # Continuous
        camera.Start()
        print(f"CAMERA_READY: {camera}")
    except Exception as e:
        print(f"CAMERA_ERROR: {e}")
        return

    # 2. Setup Shared Memory
    try:
        shm = SharedMemoryManager(create=True)
        print("SHARED_MEMORY_READY")
    except Exception as e:
        print(f"SHM_ERROR: {e}")
        if camera:
            camera.Stop()
            camera.Close()
        return

    frame_count = 0
    print("SERVICE_LOOP_START")

    try:
        while True:
            # Get Frame
            try:
                # Timeout 2000ms
                frame = camera.GetFrame(2000)
                if frame:
                    mat = frame2mat(frame)
                    if mat is not None:
                        # Write to Shared Memory
                        shm.write_frame(mat, frame_count)
                        frame_count += 1
                        
            except dvpException as e:
                # Timeout is normal if frame rate is low or camera hasn't started sending yet
                if e.Status != Status.DVP_STATUS_TIME_OUT:
                    print(f"DVP Warning: {e.Status}")
                    
            except Exception as e:
                print(f"Loop Error: {e}")
                # Don't break immediately, retry
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopping service...")
        
    finally:
        print("Closing resources...")
        try:
            if shm: shm.close()
        except: pass
        try:
            if camera:
                camera.Stop()
                camera.Close()
        except: pass

if __name__ == "__main__":
    main()
