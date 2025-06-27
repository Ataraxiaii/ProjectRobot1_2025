# Author: Xuanru GUo
# Date: 2025-6-26
# Version: 1.0
# Description: Hash recognized face data

# Import necessary libraries for hardware interfacing and image processing
import sensor, image, time, lcd, gc
import uhashlib, ubinascii
from maix import KPU, GPIO, utils
from fpioa_manager import fm
from board import board_info
from modules import ybserial

# Security configuration constants
SECURITY_SALT = b"k210_secure_salt!"  # Unique salt value for hashing
HASH_ITERATIONS = 50  # Number of iterations for PBKDF2

# Initialize serial communication and display
serial = ybserial()
lcd.init()

# Camera setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=200)  # Allow camera to stabilize
clock = time.clock()

feature_img = image.Image(size=(64,64), copy_to_fb=False)
feature_img.pix_to_ai()

# Face alignment reference points
FACE_PIC_SIZE = 64
dst_point = [(int(38.2946 * FACE_PIC_SIZE / 112), int(51.6963 * FACE_PIC_SIZE / 112)),
            (int(73.5318 * FACE_PIC_SIZE / 112), int(51.5014 * FACE_PIC_SIZE / 112)),
            (int(56.0252 * FACE_PIC_SIZE / 112), int(71.7366 * FACE_PIC_SIZE / 112)),
            (int(41.5493 * FACE_PIC_SIZE / 112), int(92.3655 * FACE_PIC_SIZE / 112)),
            (int(70.7299 * FACE_PIC_SIZE / 112), int(92.2041 * FACE_PIC_SIZE / 112))]

# Load face detection model
kpu = KPU()
kpu.load_kmodel("/sd/KPU/yolo_face_detect/face_detect_320x240.kmodel")
anchor = (0.1075, 0.126875, 0.126875, 0.175, 0.1465625, 0.2246875, 
          0.1953125, 0.25375, 0.2440625, 0.351875, 0.341875, 0.4721875,
          0.5078125, 0.6696875, 0.8984375, 1.099687, 2.129062, 2.425937)
kpu.init_yolo2(anchor, anchor_num=9, img_w=320, img_h=240, net_w=320, net_h=240,
               layer_w=10, layer_h=8, threshold=0.7, nms_value=0.2, classes=1)

# Load facial landmark detection model
ld5_kpu = KPU()
ld5_kpu.load_kmodel("/sd/KPU/face_recognization/ld5.kmodel")

# Load face feature extraction model
fea_kpu = KPU() 
fea_kpu.load_kmodel("/sd/KPU/face_recognization/feature_extraction.kmodel")

def secure_hash(feature):
    """Generate secure hash of face features using PBKDF2-HMAC-SHA256"""
    quantized = bytes(int(min(max(x, 0), 1) * 255) for x in feature[:16])
    return uhashlib.pbkdf2_hmac('sha256', quantized + SECURITY_SALT, SECURITY_SALT, HASH_ITERATIONS)

# Button interrupt setup for face registration
start_processing = False
BOUNCE_PROTECTION = 50  
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)

def set_key_state(*_):
    """Interrupt handler for registration button"""
    global start_processing
    start_processing = True
    time.sleep_ms(BOUNCE_PROTECTION)

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

# Face database and recognition parameters
record_ftrs = []  
THRESHOLD = 80.5  # Minimum similarity score for recognition
recog_flag = False

def extend_box(x, y, w, h, scale):
    """Expand bounding box coordinates with safety checks"""
    x1_t = x - scale*w
    x2_t = x + w + scale*w
    y1_t = y - scale*h
    y2_t = y + h + scale*h
    x1 = int(x1_t) if x1_t>1 else 1
    x2 = int(x2_t) if x2_t<320 else 319
    y1 = int(y1_t) if y1_t>1 else 1
    y2 = int(y2_t) if y2_t<240 else 239
    return x1, y1, x2-x1+1, y2-y1+1

# Main processing loop
msg_ = ""
while True:
    gc.collect()  
    clock.tick()  
    
    # Capture and process image
    img = sensor.snapshot()
    kpu.run_with_output(img)
    dect = kpu.regionlayer_yolo2()  # Detect faces
    fps = clock.fps()  
    
    if len(dect) > 0:
        for l in dect:
            # Extract face region
            x1, y1, cut_img_w, cut_img_h = extend_box(l[0], l[1], l[2], l[3], scale=0)
            face_cut = img.cut(x1, y1, cut_img_w, cut_img_h)
            face_cut_128 = face_cut.resize(128, 128)
            face_cut_128.pix_to_ai()
            
            # Detect facial landmarks
            out = ld5_kpu.run_with_output(face_cut_128, getlist=True)
            
            # Calculate face alignment points
            face_key_point = []
            for j in range(5):
                x = int(KPU.sigmoid(out[2*j]) * cut_img_w + x1)
                y = int(KPU.sigmoid(out[2*j+1]) * cut_img_h + y1)
                face_key_point.append((x, y))
                
            # Align face and extract features
            T = image.get_affine_transform(face_key_point, dst_point)
            image.warp_affine_ai(img, feature_img, T)
            feature = fea_kpu.run_with_output(feature_img, get_feature=True)
            
            # Register new face if button pressed
            if start_processing:
                hashed = secure_hash(feature)
                record_ftrs.append(hashed)
                print("Registered face #%d" % len(record_ftrs))
                start_processing = False
                img.draw_rectangle(l[0], l[1], l[2], l[3], color=(255, 255, 255))
                msg_ = "R"
            
            # Compare with registered faces
            current_hash = secure_hash(feature)
            matched = False
            for i, saved_hash in enumerate(record_ftrs):
                if saved_hash == current_hash:
                    max_score = THRESHOLD + 1  # Show as recognized
                    index = i
                    recog_flag = True
                    matched = True
                    break
            
            # Display recognition results
            if matched:
                img.draw_string(0, 195, "person:%d,score:%2.1f" % (index+1, max_score), 
                               color=(0, 255, 0), scale=2)
                img.draw_rectangle(l[0], l[1], l[2], l[3], color=(0, 255, 0))
                msg_ = "Y%02d" % (index+1)
            else:
                img.draw_string(0, 195, "unregistered,score:0.0", color=(255, 0, 0), scale=2)
                img.draw_rectangle(l[0], l[1], l[2], l[3], color=(255, 255, 255))
                msg_ = "N"
            
            # Clean up temporary objects
            del face_cut_128, face_cut, feature, current_hash
            gc.collect()

    # Send recognition results via serial
    if len(dect) > 0:
        send_data = "$08" + msg_ + ",#"
        time.sleep_ms(5)
        serial.send(send_data)
    else:
        serial.send("#")

    # Display status information
    img.draw_string(0, 0, "%2.1ffps" % fps, color=(0, 60, 255), scale=2.0)
    img.draw_string(0, 215, "press boot key to register face", color=(255, 100, 0), scale=2.0)
    lcd.display(img)

# Clean up resources
kpu.deinit()
ld5_kpu.deinit()
fea_kpu.deinit()