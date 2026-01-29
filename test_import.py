import sys
import os

print("Testing import of src.agent_camera.base_widget...")
try:
    from src.agent_camera.base_widget import BaseCameraWidget
    print("Success: Imported BaseCameraWidget")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")

print("\nTesting import of src.agent_camera...")
try:
    import src.agent_camera
    print("Success: Imported src.agent_camera")
except Exception as e:
    print(f"Exception importing package: {e}")
