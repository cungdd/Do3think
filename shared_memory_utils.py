import mmap
import struct
import numpy as np
import platform

SHM_SIZE = 32 * 1024 * 1024  # 32 MB
SHM_NAME = "Local\\DvpCamFrame_v3" # v3 to force fresh memory

class SharedMemoryManager:
    def __init__(self, create=False):
        self.shm = None
        self.create = create
        
        if platform.system() != "Windows":
             raise RuntimeError("SharedMemoryManager only supports Windows for now due to named mmap.")

        if create:
            # Create a new memory mapping - RW access
            self.shm = mmap.mmap(-1, SHM_SIZE, tagname=SHM_NAME, access=mmap.ACCESS_WRITE)
        else:
            try:
                # Try to open existing mapping with fixed size
                self.shm = mmap.mmap(-1, SHM_SIZE, tagname=SHM_NAME, access=mmap.ACCESS_READ)
            except (FileNotFoundError, OSError) as e:
                print(f"[SHM Debug] Failed to connect: {e}")
                self.shm = None

    def ensure_connected(self):
        """Attempts to connect to the shared memory if not already connected."""
        if self.shm:
            return True
        try:
            self.shm = mmap.mmap(-1, SHM_SIZE, tagname=SHM_NAME, access=mmap.ACCESS_READ)
            return True
        except (FileNotFoundError, OSError):
            return False

    def write_frame(self, frame, frame_id):
        if not self.shm:
            return
        
        height, width, channels = frame.shape
        # Header: Magic(4), FrameID(4), Width(4), Height(4), Channels(4), DataLen(4)
        header_size = 24
        # Calculate data length
        data_len = height * width * channels
        
        if header_size + data_len > SHM_SIZE:
             # Just print once or limit spam?
             return

        # 1. Write Header
        self.shm.seek(0)
        self.shm.write(struct.pack('IIIIII', 0xDEADBEEF, frame_id, width, height, channels, data_len))
        
        # 2. Write Data (Direct Copy)
        # Create a numpy array that points directly to the shm buffer at offset 24
        # This allows us to copy frame data directly into SHM without intermediate bytes object
        try:
            dst = np.ndarray(frame.shape, dtype=frame.dtype, buffer=self.shm, offset=header_size)
            dst[:] = frame[:] 
        except Exception as e:
            # Fallback (safer but slower)
            self.shm.seek(header_size)
            self.shm.write(frame.tobytes())

    def read_frame(self):
        if not self.ensure_connected():
            return None, None

        try:
            # Direct read from buffer (Zero copy read)
            # Create a view of the header
            header_view = self.shm[:24]
            magic, frame_id, width, height, channels, data_len = struct.unpack('IIIIII', header_view)
            
            if magic != 0xDEADBEEF:
                return None, None

            # Create a numpy view directly on the shared memory
            # Note: This view is Read-Only if opened with ACCESS_READ
            src = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.shm, offset=24)
            
            # We must return a COPY because:
            # 1. OpenCV functions often need writable arrays
            # 2. We don't want the image to change while we process it (tearing from writer)
            # This is the ONLY copy operation in the read process now.
            return src.copy(), frame_id

        except Exception as e:
            return None, None

    def close(self):
        if self.shm:
            self.shm.close()
            self.shm = None
