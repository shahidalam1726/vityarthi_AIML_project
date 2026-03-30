import cv2
import mediapipe as mp
import numpy as np
import os

# 1. Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

path =r'C:\Users\shahi\OneDrive\Desktop\aiml\sunglasses.png'

filter_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

# 2. Add this "Safety Check" immediately after loading
if filter_img is None:
    print(f"!!! ERROR !!!: Could not find image at: {path}")
    print("Make sure the file name is correct and the file is in that folder.")
    exit() # This stops the code here instead of crashing at line 85
img_path = 'sunglasses.png'
if not os.path.exists(img_path):
    print(f"Error: File {img_path} not found!")
    exit()

filter_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

def overlay_image(background, overlay, x, y, width, height):
    """Safe overlay that handles screen boundaries and transparency."""
    if width <= 0 or height <= 0: return background
    
    # Resize the filter to the target size
    overlay_resized = cv2.resize(overlay, (width, height))
    
    # Calculate boundaries
    h, w = background.shape[:2]
    
    # Clip coordinates to screen limits
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + width, w), min(y + height, h)
    
    # Calculate the portion of the overlay to use
    overlay_x1 = x1 - x
    overlay_y1 = y1 - y
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)
    
    # Extract slices
    background_roi = background[y1:y2, x1:x2]
    overlay_roi = overlay_resized[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
    
    # Safety check for empty ROI
    if background_roi.shape[0] <= 0 or background_roi.shape[1] <= 0:
        return background

    # Extract transparency (Alpha channel)
    if overlay_roi.shape[2] == 4:
        alpha_mask = overlay_roi[:, :, 3] / 255.0
        alpha_inv = 1.0 - alpha_mask
        
        for c in range(3):
            background[y1:y2, x1:x2, c] = (alpha_mask * overlay_roi[:, :, c] +
                                           alpha_inv * background[y1:y2, x1:x2, c])
    else:
        # Fallback if image isn't a transparent PNG
        background[y1:y2, x1:x2] = overlay_roi[:, :, :3]
        
    return background

# 3. Start Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            ih, iw, _ = frame.shape
            
            # Landmarks for eyes/nose
            left_eye = face_landmarks.landmark[234]
            right_eye = face_landmarks.landmark[454]
            nose = face_landmarks.landmark[6]

            # Calculate width based on eye distance
            x1, x2 = int(left_eye.x * iw), int(right_eye.x * iw)
            filter_width = x2 - x1
            
            if filter_width > 0:
                # Calculate height based on image aspect ratio
                aspect_ratio = filter_img.shape[0] / filter_img.shape[1]
                filter_height = int(filter_width * aspect_ratio)

                # Positioning: Center the glasses on the nose bridge
                start_x = x1
                start_y = int(nose.y * ih) - (filter_height // 2)

                # Call the safe overlay function
                frame = overlay_image(frame, filter_img, start_x, start_y, filter_width, filter_height)

    cv2.imshow('AI Face Filter', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()