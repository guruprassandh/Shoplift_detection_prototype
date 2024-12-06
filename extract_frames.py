import cv2
import os

def extract_frames(video_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break  # Exit when there are no more frames

        # Save the frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f"Frames extracted: {frame_count}")
    print(f"Frames are saved in the folder: {output_folder}")

# Example usage
video_path = r"C:\Users\gurup\OneDrive\Desktop\AI-Theft-Detection-System\WIN_20240123_10_54_08_Pro.mp4"  # Replace with your video path
output_folder = r"C:\Users\gurup\OneDrive\Desktop\AI-Theft-Detection-System\output_images"       # Folder to save frames
extract_frames(video_path, output_folder)
