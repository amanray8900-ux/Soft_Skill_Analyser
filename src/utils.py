import os
import tempfile
import subprocess
import shutil
import imageio_ffmpeg
import platform
import stat

def setup_ffmpeg():
    """
    Ensures ffmpeg is available in the system PATH.
    If not found, it tries to use imageio-ffmpeg's bundled binary.
    """
    # 1. Check if ffmpeg is already in PATH
    if shutil.which("ffmpeg"):
        return True

    # 2. Try to use imageio-ffmpeg
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_exe)
        ffmpeg_name = os.path.basename(ffmpeg_exe)

        # If the binary name is precisely "ffmpeg" (or "ffmpeg.exe" on Windows),
        # we can just add its directory to PATH.
        target_name = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
        
        if ffmpeg_name.lower() == target_name.lower():
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        else:
            # Different name (e.g., ffmpeg-win64-v7.1.exe). Create a wrapper.
            tmp_dir = tempfile.mkdtemp(prefix="ffmpeg_wrapper_")
            
            if platform.system() == "Windows":
                wrapper_path = os.path.join(tmp_dir, "ffmpeg.bat")
                with open(wrapper_path, "w") as f:
                    f.write(f'@echo off\n"{ffmpeg_exe}" %*\n')
            else:
                # Unix-like (Linux/MacOS)
                wrapper_path = os.path.join(tmp_dir, "ffmpeg")
                with open(wrapper_path, "w") as f:
                    f.write(f'#!/bin/sh\n"{ffmpeg_exe}" "$@"\n')
                # Make the wrapper executable
                st = os.stat(wrapper_path)
                os.chmod(wrapper_path, st.st_mode | stat.S_IEXEC)
            
            # Prepend the wrapper directory to PATH
            os.environ["PATH"] = tmp_dir + os.pathsep + os.environ.get("PATH", "")
        
        return True
    except Exception as e:
        print(f"Warning: Could not setup bundled FFmpeg: {e}")
    
    # 3. Fallback to common library paths (like Anaconda on Windows)
    common_paths = [
        r"C:\Users\amanr\anaconda3\Library\bin",
        r"C:\anaconda3\Library\bin",
        "/usr/local/bin",
        "/usr/bin"
    ]
    for p in common_paths:
        if os.path.isdir(p) and (shutil.which("ffmpeg", path=p)):
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
            return True

    return False
