# vityarthi_AIML_project
Smart "Face Filter" App.  Just like Instagram or Snapchat, you can make a program that puts a hat, glasses, or a mask on your face in real-time.
AI Face Filter with MediaPipe & OpenCV
This project is a real-time computer vision application that detects facial landmarks and overlays a digital filter (like sunglasses) onto a user's face using their webcam. It leverages MediaPipe's Face Mesh for high-precision tracking and OpenCV for image processing.

Features
Real-time Tracking: Smoothly tracks facial movements using 468+ facial landmarks.

Dynamic Scaling: The filter automatically resizes based on the user's distance from the camera.

Alpha Blending: Supports transparent PNG images for a seamless "sticker" effect.

Boundary Safety: Includes a robust overlay function that prevents crashes if the filter moves off-screen.

Prerequisites
Before running the script, ensure you have Python installed along with the following libraries:

Bash
pip install opencv-python mediapipe numpy
Project Structure
main.py: The primary Python script.

sunglasses.png: The transparent overlay image (ensure this is in your project directory).

How It Works
Face Landmark Detection: The script uses mp.solutions.face_mesh to locate specific points on the face. It specifically tracks landmarks near the eyes and the bridge of the nose.

Distance Calculation: It measures the distance between the left and right eye landmarks to determine how wide the sunglasses should be.

Alpha Overlaying: Since standard OpenCV cv2.addWeighted doesn't support transparency masks easily, the overlay_image function manually blends the PNG's alpha channel with the webcam's BGR frames.

Transformation: It calculates the aspect ratio of the filter image to ensure it doesn't look stretched when resized.

Usage
Prepare your filter: Place a transparent .png image (e.g., sunglasses.png) in the same folder as the script.

Set the path: Update the path variable in the code with your image's location:

Python
path = r'C:\Your\Path\To\sunglasses.png'
Run the script:

Bash
python main.py
Controls:

Point the webcam at your face.

Press 'q' to quit the application.

Troubleshooting
Image Not Found: Ensure the path to your PNG file is absolute or correctly relative. The script includes a "Safety Check" that will alert you if the file isn't loading.

Webcam Access: Make sure no other application (like Zoom or Teams) is using your webcam while running the script.

Performance: If the video is laggy, ensure your laptop is plugged in or try reducing the max_num_faces to 1.

License
This project is open-source. Feel free to modify it to add hats, masks, or other fun AR effe
