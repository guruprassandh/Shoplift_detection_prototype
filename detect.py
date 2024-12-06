import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize video capture
cap = cv2.VideoCapture(r' # Path to your video file') 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Perform object detection on the frame
    results = model(frame)
    labels = results.xyxy[0][:, -1].tolist()  # Object class IDs
    boxes = results.xyxy[0].tolist()  # Bounding box coordinates
    names = results.names  # Class names corresponding to the labels

    # Define suspicious activities
    thief_detected = False
    for i, label in enumerate(labels):
        class_name = names[int(label)]
        box = boxes[i]
        x1, y1, x2, y2, conf = map(int, box[:5])

        # Detect "hoodie" (simulating the condition with 'person' for this example)
        if class_name == 'person':
            # Define additional logic for suspicious behavior
            # Assuming a thief might also interact with objects like 'backpack' or 'handbag'
            suspicious = False

            # Check proximity with objects
            for j, other_label in enumerate(labels):
                other_class_name = names[int(other_label)]
                if other_class_name in ['backpack', 'handbag']:
                    # Check if person is close to the object (bounding box overlap)
                    x1_o, y1_o, x2_o, y2_o, _ = map(int, boxes[j][:5])
                    if (
                        x1 < x2_o and x2 > x1_o and  # Horizontal overlap
                        y1 < y2_o and y2 > y1_o    # Vertical overlap
                    ):
                        suspicious = True

            # Mark as thief if wearing a "hoodie" or interacting with objects
            if suspicious:
                thief_detected = True
                cv2.putText(frame, "Thief Detected!", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            else:
                # Normal person
                cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # Show frame
    cv2.imshow('Theft Detection System', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
