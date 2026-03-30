import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# 1. Load the "Pre-trained Brain" (MobileNetV2)
model = MobileNetV2(weights='imagenet')

# 2. Start the Webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit the scanner")

while True:
    ret, frame = cap.get_read()
    if not ret:
        break

    # 3. Prepare the image for the AI (it likes 224x224 pixels)
    resized_frame = cv2.resize(frame, (224, 224))
    img_array = image.img_to_array(resized_frame)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 4. Ask the AI to "Predict" what it sees
    predictions = model.predict(img_array)
    label = decode_predictions(predictions, top=1)[0][0]
    
    # Extract the name and the confidence score
    fruit_name = label[1]
    confidence = label[2]

    # 5. Display the result on the screen
    display_text = f"{fruit_name}: {confidence*100:.2f}%"
    cv2.putText(frame, display_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('AI Fruit Scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()