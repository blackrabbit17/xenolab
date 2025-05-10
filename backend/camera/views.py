import os
import io
import base64
import threading
import time
import subprocess
import traceback
import sys
from PIL import Image

from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Get settings from environment variables
CAMERA_RESOLUTION_WIDTH = int(os.environ.get('CAMERA_RESOLUTION_WIDTH', '640'))
CAMERA_RESOLUTION_HEIGHT = int(os.environ.get('CAMERA_RESOLUTION_HEIGHT', '480'))
CAMERA_FRAMERATE = int(os.environ.get('CAMERA_FRAMERATE', '30'))
CAMERA_ROTATION = int(os.environ.get('CAMERA_ROTATION', '0'))
CAMERA_HQ = os.environ.get('CAMERA_HQ', 'false').lower() == 'true'
CAMERA_AWB_MODE = os.environ.get('CAMERA_AWB_MODE', 'auto')
CAMERA_USE_LEGACY_DRIVER = os.environ.get('CAMERA_USE_LEGACY_DRIVER', 'false').lower() == 'true'
# Skip hardware detection checks (useful for non-standard setups or when vcgencmd is unavailable)
CAMERA_SKIP_HARDWARE_CHECK = os.environ.get('CAMERA_SKIP_HARDWARE_CHECK', 'false').lower() == 'true'
# Use mock camera for development
CAMERA_MOCK_MODE = os.environ.get('CAMERA_MOCK_MODE', 'false').lower() == 'true'
# Enable autofocus for compatible cameras
CAMERA_AUTOFOCUS = os.environ.get('CAMERA_AUTOFOCUS', 'true').lower() == 'true'


class PiCameraStream:
    def __init__(self, resolution=(640, 480), framerate=30, rotation=0, hq=True, awb_mode='auto', use_legacy=False, autofocus=True):
        self.resolution = resolution
        self.framerate = framerate
        self.rotation = rotation
        self.hq = hq
        self.awb_mode = awb_mode
        self.camera = None
        self.is_running = False
        self.output = None
        self.use_legacy = use_legacy
        self.last_error = None
        self.mock_mode = CAMERA_MOCK_MODE
        self.autofocus = autofocus
        
    def check_camera_present(self):
        """Check if the Raspberry Pi camera module is properly connected"""
        if CAMERA_SKIP_HARDWARE_CHECK:
            return True, "Hardware check skipped due to CAMERA_SKIP_HARDWARE_CHECK=true"
            
        if self.mock_mode:
            return True, "Using mock camera mode"
            
        try:
            # First, check if we're on a Raspberry Pi
            if not os.path.exists('/opt/vc/bin/vcgencmd') and not os.path.exists('/usr/bin/vcgencmd'):
                return False, "vcgencmd not found - may not be running on a Raspberry Pi or VC tools not installed"
            
            # Check for the camera using vcgencmd
            cmd = '/opt/vc/bin/vcgencmd' if os.path.exists('/opt/vc/bin/vcgencmd') else '/usr/bin/vcgencmd'
            result = subprocess.run([cmd, 'get_camera'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                universal_newlines=True)
            if result.returncode != 0:
                return False, f"vcgencmd failed with return code {result.returncode}: {result.stderr}"
                
            output = result.stdout.strip()
            
            # Output should be "supported=1 detected=1" if camera is present
            if "detected=1" in output:
                return True, output
            return False, f"Camera not detected in vcgencmd output: {output}"
        except Exception as e:
            error_trace = traceback.format_exc()
            return False, f"Error checking camera presence: {str(e)}\n{error_trace}"
    
    def create_test_image(self):
        """Create a test image with timestamp for mock mode"""
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Create a gradient background
        width, height = self.resolution
        image = Image.new('RGB', (width, height), color=(64, 64, 64))
        draw = ImageDraw.Draw(image)
        
        # Draw timestamp and info
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        text = f"MOCK CAMERA\n{timestamp}\n{width}x{height} @ {self.framerate}fps"
        
        # Try to use a system font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            try:
                # Fallback to a different common font location
                font = ImageFont.truetype("/usr/share/fonts/TTF/Arial.ttf", 20)
            except:
                font = ImageFont.load_default()
        
        # Center the text
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Add the text
        draw.text(position, text, fill=(255, 255, 255), font=font)
        
        # Add some random colored squares for visual interest
        for i in range(10):
            x = random.randint(0, width - 50)
            y = random.randint(0, height - 50)
            size = random.randint(20, 50)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.rectangle([x, y, x + size, y + size], fill=color)
        
        return image
    
    def start(self):
        if not self.is_running:
            # For mock mode, just set is_running to True and return
            if self.mock_mode:
                print("Starting in mock camera mode")
                self.is_running = True
                self.last_error = None
                return True
                
            try:
                # First check if camera is present
                is_present, msg = self.check_camera_present()
                if not is_present and not CAMERA_SKIP_HARDWARE_CHECK:
                    self.last_error = msg
                    print(f"Camera module not detected: {msg}")
                    return False
                
                # Import libraries inside try block to handle import errors
                if self.use_legacy:
                    # Use legacy picamera module for older Raspberry Pi models/OS
                    try:
                        import picamera
                        import picamera.array
                    except ImportError as e:
                        self.last_error = f"Failed to import picamera: {str(e)}. Try installing with 'pip install picamera'."
                        print(self.last_error)
                        return False
                    
                    # Initialize the camera
                    self.camera = picamera.PiCamera()
                    self.camera.resolution = self.resolution
                    self.camera.framerate = self.framerate
                    self.camera.rotation = self.rotation
                    self.camera.awb_mode = self.awb_mode
                    
                    # Set camera mode for better quality if hq is True
                    if self.hq:
                        self.camera.sensor_mode = 3  # High quality mode
                else:
                    # Use picamera2 for newer Raspberry Pi models/OS
                    try:
                        from picamera2 import Picamera2
                        from picamera2.controls import Controls
                    except ImportError as e:
                        self.last_error = f"Failed to import picamera2: {str(e)}. Try installing with 'pip install picamera2'."
                        print(self.last_error)
                        return False
                    
                    try:
                        # Initialize the camera
                        self.camera = Picamera2()
                        config = self.camera.create_still_configuration(
                            main={"size": self.resolution},
                            lores={"size": (320, 240)},
                            display="lores",
                            queue=False
                        )
                        self.camera.configure(config)
                        
                        # Handle AWB mode conversion - in picamera2 this needs numeric constants
                        controls = {}
                        
                        # Convert string AWB mode to the appropriate picamera2 constant
                        # AWB modes in picamera2 are integers, not strings
                        try:
                            # Common AWB modes
                            awb_mode_map = {
                                'auto': 0,         # LIBCAMERA_AWB_AUTO
                                'incandescent': 1, # LIBCAMERA_AWB_INCANDESCENT 
                                'tungsten': 1,     # Alias for incandescent
                                'fluorescent': 2,  # LIBCAMERA_AWB_FLUORESCENT
                                'indoor': 2,       # Alias for fluorescent
                                'daylight': 3,     # LIBCAMERA_AWB_DAYLIGHT
                                'outdoor': 3,      # Alias for daylight
                                'cloudy': 4,       # LIBCAMERA_AWB_CLOUDY
                                'custom': 5,       # LIBCAMERA_AWB_CUSTOM
                                'off': 6           # Not an official mode but some cameras support it
                            }
                            
                            if isinstance(self.awb_mode, str) and self.awb_mode.lower() in awb_mode_map:
                                controls["AwbMode"] = awb_mode_map[self.awb_mode.lower()]
                            elif isinstance(self.awb_mode, int):
                                controls["AwbMode"] = self.awb_mode
                            else:
                                # Default to auto if not found
                                controls["AwbMode"] = 0
                                print(f"Warning: Unknown AWB mode '{self.awb_mode}'. Using 'auto' instead.")
                        except Exception as e:
                            print(f"Warning: Error setting AWB mode: {e}. Using default.")
                        
                        # Set rotation if needed
                        if self.rotation != 0:
                            controls["RotationDegrees"] = self.rotation
                        
                        # Set autofocus if enabled
                        if self.autofocus:
                            # Enable continuous autofocus (value 2)
                            controls["AfMode"] = 2  # LIBCAMERA_AF_CONTINUOUS
                            print("Enabling continuous autofocus")
                        else:
                            # Default to fixed focus (value 0)
                            controls["AfMode"] = 0  # LIBCAMERA_AF_MANUAL
                            
                        # Apply all controls
                        if controls:
                            self.camera.set_controls(controls)
                            
                        self.camera.start()
                    except Exception as e:
                        # If picamera2 fails with specific error messages, provide helpful guidance
                        error_msg = str(e).lower()
                        if "no cameras available" in error_msg:
                            self.last_error = (
                                f"No cameras found by picamera2. Error: {str(e)}\n"
                                "Make sure the camera is enabled with 'sudo raspi-config' -> Interface Options -> Camera\n"
                                "Also ensure the ribbon cable is properly connected and not damaged.\n"
                                "You may need to reboot after enabling the camera."
                            )
                        elif "permission" in error_msg:
                            self.last_error = (
                                f"Permission error accessing camera: {str(e)}\n"
                                "Make sure your user has permissions to access the camera.\n"
                                "Try adding your user to the 'video' group: sudo usermod -a -G video $USER"
                            )
                        else:
                            self.last_error = f"Error initializing picamera2: {str(e)}"
                        
                        print(self.last_error)
                        return False
                
                # Warm up the camera
                time.sleep(2)
                
                self.is_running = True
                self.last_error = None
                return True
            except Exception as e:
                error_trace = traceback.format_exc()
                self.last_error = f"Error starting Pi camera: {str(e)}\n{error_trace}"
                print(self.last_error)
                return False
        return True
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            
            # No need to close anything in mock mode
            if self.mock_mode:
                return
            
            if self.camera is not None:
                try:
                    if self.use_legacy:
                        self.camera.close()
                    else:
                        self.camera.stop()
                        self.camera.close()
                except Exception as e:
                    print(f"Error closing camera: {str(e)}")
                self.camera = None
    
    def get_jpeg_frame(self):
        if not self.is_running:
            return None
        
        # In mock mode, generate a test pattern
        if self.mock_mode:
            try:
                image = self.create_test_image()
                stream = io.BytesIO()
                image.save(stream, format='JPEG')
                stream.seek(0)
                return stream.getvalue()
            except Exception as e:
                self.last_error = f"Error creating mock frame: {str(e)}"
                print(self.last_error)
                return None
        
        if self.camera is None:
            return None
            
        try:
            if self.use_legacy:
                # For legacy picamera
                stream = io.BytesIO()
                self.camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                return stream.getvalue()
            else:
                # For picamera2
                array = self.camera.capture_array()
                image = Image.fromarray(array)
                stream = io.BytesIO()
                image.save(stream, format='JPEG')
                stream.seek(0)
                return stream.getvalue()
        except Exception as e:
            error_trace = traceback.format_exc()
            self.last_error = f"Error capturing frame: {str(e)}\n{error_trace}"
            print(self.last_error)
            return None
    
    def get_base64_frame(self):
        jpeg_data = self.get_jpeg_frame()
        if jpeg_data is None:
            return None
        
        return base64.b64encode(jpeg_data).decode('utf-8')

# Global camera instance and lock
_pi_camera = None
_camera_lock = threading.Lock()

def _get_pi_camera():
    """Get the Pi camera instance (singleton)"""
    global _pi_camera
    if _pi_camera is None:
        _pi_camera = PiCameraStream(
            resolution=(CAMERA_RESOLUTION_WIDTH, CAMERA_RESOLUTION_HEIGHT),
            framerate=CAMERA_FRAMERATE,
            rotation=CAMERA_ROTATION,
            hq=CAMERA_HQ,
            awb_mode=CAMERA_AWB_MODE,
            use_legacy=CAMERA_USE_LEGACY_DRIVER,
            autofocus=CAMERA_AUTOFOCUS
        )
    return _pi_camera

def generate_frames():
    """Generator function to yield camera frames for streaming"""
    camera = _get_pi_camera()
    
    if not camera.start():
        error_message = camera.last_error or "Unknown error"
        yield f'--frame\r\nContent-Type: text/plain\r\n\r\nCamera Error: Failed to start Pi Camera\n{error_message}\r\n'.encode('utf-8')
        return
    
    try:
        while True:
            with _camera_lock:
                jpeg_frame = camera.get_jpeg_frame()
            
            if jpeg_frame is None:
                time.sleep(0.1)  # Sleep to prevent CPU overuse
                continue
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame + b'\r\n')
            
            # Control frame rate
            time.sleep(1/camera.framerate)
            
    except Exception as e:
        error_trace = traceback.format_exc()
        error_message = f"Error in frame generation: {str(e)}\n{error_trace}"
        print(error_message)
        yield f'--frame\r\nContent-Type: text/plain\r\n\r\nCamera Error: Stream interrupted\n{error_message}\r\n'.encode('utf-8')
    finally:
        # Don't stop the stream here - it will be managed separately
        pass

@require_http_methods(["GET"])
def camera_stream(request, camera_id=None):
    """Stream camera frames as multipart HTTP response"""
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

@require_http_methods(["GET"])
def camera_frame(request, camera_id=None):
    """Return a single frame as base64 encoded JPEG"""
    camera = _get_pi_camera()
    
    if not camera.is_running and not camera.start():
        return JsonResponse({
            'error': 'Failed to start Pi camera', 
            'details': camera.last_error or "Unknown error"
        }, status=500)
    
    with _camera_lock:
        base64_frame = camera.get_base64_frame()
    
    if base64_frame is None:
        return JsonResponse({
            'error': 'Failed to capture frame',
            'details': camera.last_error or "Unknown error"
        }, status=500)
    
    return JsonResponse({
        'frame': base64_frame,
        'timestamp': time.time(),
        'content_type': 'image/jpeg'
    })

@require_http_methods(["GET"])
def camera_status(request, camera_id=None):
    """Get camera status"""
    camera = _get_pi_camera()
    
    # Check if camera hardware is present
    is_present, msg = camera.check_camera_present()
    
    # Get system information that might be helpful for debugging
    system_info = {
        'platform': sys.platform,
        'python_version': sys.version,
        'environment_vars': {
            key: value for key, value in os.environ.items() 
            if key.startswith('CAMERA_') or key in ['PATH', 'PYTHONPATH']
        }
    }
    
    # Try to get more detailed info about the system
    try:
        uname_output = subprocess.check_output(['uname', '-a']).decode('utf-8').strip()
        system_info['uname'] = uname_output
    except:
        pass
        
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                system_info['os_release'] = f.read()
    except:
        pass
    
    return JsonResponse({
        'status': 'on' if camera.is_running else 'off',
        'hardware_detected': is_present,
        'hardware_info': msg,
        'resolution': f"{camera.resolution[0]}x{camera.resolution[1]}",
        'framerate': camera.framerate,
        'rotation': camera.rotation,
        'hq_mode': camera.hq,
        'awb_mode': camera.awb_mode,
        'using_legacy_driver': camera.use_legacy,
        'mock_mode': camera.mock_mode,
        'autofocus': camera.autofocus,
        'skip_hardware_check': CAMERA_SKIP_HARDWARE_CHECK,
        'last_error': camera.last_error,
        'system_info': system_info
    })

@csrf_exempt
@require_http_methods(["POST"])
def camera_control(request, camera_id=None):
    """Control camera (start/stop)"""
    action = request.POST.get('action')
    
    if action not in ['start', 'stop', 'toggle_driver', 'toggle_mock', 'toggle_autofocus']:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    camera = _get_pi_camera()
    
    try:
        if action == 'start':
            with _camera_lock:
                result = camera.start()
            if result:
                return JsonResponse({'status': 'started'})
            else:
                return JsonResponse({
                    'error': 'Failed to start Pi camera',
                    'details': camera.last_error or "Unknown error"
                }, status=500)
        
        elif action == 'stop':
            with _camera_lock:
                camera.stop()
            return JsonResponse({'status': 'stopped'})
            
        elif action == 'toggle_driver':
            global _pi_camera
            with _camera_lock:
                if camera.is_running:
                    camera.stop()
                
                # Reset the camera with opposite driver setting
                _pi_camera = None
                global CAMERA_USE_LEGACY_DRIVER
                CAMERA_USE_LEGACY_DRIVER = not CAMERA_USE_LEGACY_DRIVER
                
                # Get new camera instance with toggled driver
                camera = _get_pi_camera()
                result = camera.start()
                
                if result:
                    return JsonResponse({
                        'status': 'driver_toggled',
                        'using_legacy_driver': CAMERA_USE_LEGACY_DRIVER
                    })
                else:
                    return JsonResponse({
                        'error': 'Failed to start camera with new driver',
                        'details': camera.last_error or "Unknown error"
                    }, status=500)
        
        elif action == 'toggle_mock':
            global CAMERA_MOCK_MODE
            with _camera_lock:
                if camera.is_running:
                    camera.stop()
                
                # Reset the camera with opposite mock setting
                _pi_camera = None
                CAMERA_MOCK_MODE = not CAMERA_MOCK_MODE
                
                # Get new camera instance with toggled mock mode
                camera = _get_pi_camera()
                result = camera.start()
                
                if result:
                    return JsonResponse({
                        'status': 'mock_mode_toggled',
                        'mock_mode': CAMERA_MOCK_MODE
                    })
                else:
                    return JsonResponse({
                        'error': 'Failed to start camera in mock mode',
                        'details': camera.last_error or "Unknown error"
                    }, status=500)
        
        elif action == 'toggle_autofocus':
            global CAMERA_AUTOFOCUS
            with _camera_lock:
                if camera.is_running:
                    camera.stop()
                
                # Reset the camera with opposite autofocus setting
                _pi_camera = None
                CAMERA_AUTOFOCUS = not CAMERA_AUTOFOCUS
                
                # Get new camera instance with toggled autofocus
                camera = _get_pi_camera()
                result = camera.start()
                
                if result:
                    return JsonResponse({
                        'status': 'autofocus_toggled',
                        'autofocus': CAMERA_AUTOFOCUS
                    })
                else:
                    return JsonResponse({
                        'error': 'Failed to start camera with new autofocus setting',
                        'details': camera.last_error or "Unknown error"
                    }, status=500)
            
    except Exception as e:
        error_trace = traceback.format_exc()
        return JsonResponse({
            'error': str(e),
            'details': error_trace
        }, status=500)
