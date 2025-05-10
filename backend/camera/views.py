import cv2
import base64
import threading
import time
from io import BytesIO
from PIL import Image
import numpy as np

from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Global variables to store camera connections
camera_streams = {}
camera_locks = {}

class CameraStream:
    def __init__(self, camera_id=0, resolution=(640, 480), fps=30):
        self.camera_id = camera_id
        self.resolution = resolution
        self.fps = fps
        self.cap = None
        self.is_running = False
        
    def start(self):
        if not self.is_running:
            try:
                # For webcam or USB camera, use camera_id directly
                # For IP camera, use URL string like "rtsp://user:pass@ip:port/path"
                self.cap = cv2.VideoCapture(self.camera_id)
                if not self.cap.isOpened():
                    raise Exception(f"Failed to open camera {self.camera_id}")
                
                # Set resolution
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                # Set FPS
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                
                self.is_running = True
                return True
            except Exception as e:
                print(f"Error starting camera: {e}")
                return False
        return True
    
    def stop(self):
        if self.is_running and self.cap is not None:
            self.is_running = False
            self.cap.release()
    
    def get_frame(self):
        if not self.is_running or self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        return frame
    
    def get_jpeg_frame(self):
        frame = self.get_frame()
        if frame is None:
            return None
        
        # Convert from BGR (OpenCV format) to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to JPEG
        img = Image.fromarray(frame_rgb)
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        
        return buffer.getvalue()
    
    def get_base64_frame(self):
        jpeg_data = self.get_jpeg_frame()
        if jpeg_data is None:
            return None
        
        return base64.b64encode(jpeg_data).decode('utf-8')

def get_stream(camera_id):
    """Get or create a camera stream for the given camera ID"""
    if camera_id not in camera_streams:
        # Get camera config from database
        try:
            camera = Camera.objects.get(pk=camera_id)
            resolution = (camera.resolution_width, camera.resolution_height)
            fps = camera.frame_rate
            
            # Create stream and lock
            camera_streams[camera_id] = CameraStream(camera_id=0, resolution=resolution, fps=fps)
            camera_locks[camera_id] = threading.Lock()
            
            # Update camera status
            camera.status = Camera.STATUS_ON
            camera.save()
            
        except Camera.DoesNotExist:
            # Use default settings if camera not in database
            camera_streams[camera_id] = CameraStream(camera_id=0)
            camera_locks[camera_id] = threading.Lock()
    
    return camera_streams[camera_id], camera_locks[camera_id]

def generate_frames(camera_id):
    """Generator function to yield camera frames for streaming"""
    stream, lock = get_stream(camera_id)
    
    if not stream.start():
        yield b'--frame\r\nContent-Type: text/plain\r\n\r\nCamera Error\r\n'
        return
    
    try:
        while True:
            with lock:
                jpeg_frame = stream.get_jpeg_frame()
            
            if jpeg_frame is None:
                time.sleep(0.1)  # Sleep to prevent CPU overuse
                continue
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame + b'\r\n')
            
            # Control frame rate
            time.sleep(1/stream.fps)
            
    except Exception as e:
        print(f"Error in frame generation: {e}")
    finally:
        # Don't stop the stream here - it will be managed separately
        pass

@require_http_methods(["GET"])
def camera_stream(request, camera_id=1):
    """Stream camera frames as multipart HTTP response"""
    return StreamingHttpResponse(
        generate_frames(camera_id),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

@require_http_methods(["GET"])
def camera_frame(request, camera_id=1):
    """Return a single frame as base64 encoded JPEG"""
    stream, lock = get_stream(camera_id)
    
    if not stream.is_running and not stream.start():
        return JsonResponse({'error': 'Failed to start camera'}, status=500)
    
    with lock:
        base64_frame = stream.get_base64_frame()
    
    if base64_frame is None:
        return JsonResponse({'error': 'Failed to capture frame'}, status=500)
    
    return JsonResponse({
        'camera_id': camera_id,
        'frame': base64_frame,
        'timestamp': time.time(),
        'content_type': 'image/jpeg'
    })

@require_http_methods(["GET"])
def camera_status(request, camera_id=1):
    """Get camera status"""
    try:
        camera = Camera.objects.get(pk=camera_id)
        return JsonResponse({
            'camera_id': camera_id,
            'status': camera.status,
            'name': camera.name,
            'resolution': f"{camera.resolution_width}x{camera.resolution_height}",
            'frame_rate': camera.frame_rate,
            'last_active': camera.last_active.isoformat()
        })
    except Camera.DoesNotExist:
        return JsonResponse({
            'camera_id': camera_id,
            'status': 'not_found'
        }, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def camera_control(request, camera_id=1):
    """Control camera (start/stop)"""
    action = request.POST.get('action')
    
    if action not in ['start', 'stop']:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    try:
        camera = Camera.objects.get(pk=camera_id)
        stream, lock = get_stream(camera_id)
        
        if action == 'start':
            result = stream.start()
            if result:
                camera.status = Camera.STATUS_ON
                camera.save()
                return JsonResponse({'status': 'started'})
            else:
                return JsonResponse({'error': 'Failed to start camera'}, status=500)
        
        elif action == 'stop':
            with lock:
                stream.stop()
            camera.status = Camera.STATUS_OFF
            camera.save()
            return JsonResponse({'status': 'stopped'})
            
    except Camera.DoesNotExist:
        return JsonResponse({'error': 'Camera not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
