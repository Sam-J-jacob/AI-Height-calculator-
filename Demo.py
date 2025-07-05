import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import cv2
import mediapipe as mp
import math

def calculate_real_height(distance_m, angle_deg_from_ground, camera_height_m, image_path):
    angle_deg = angle_deg_from_ground - 90
    angle_rad = math.radians(angle_deg)

    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Could not load image. Check the file path.")
        return

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)

    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        head_y = int(landmarks[mp_pose.PoseLandmark.NOSE].y * image_height)
        foot_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HEEL].y * image_height)
        pixel_height = abs(foot_y - head_y)

        estimated_height = distance_m * math.tan(angle_rad) + camera_height_m

        messagebox.showinfo("Result",
            f"Pixel height of person: {pixel_height} px\nEstimated real height: {estimated_height:.2f} meters")
    else:
        messagebox.showinfo("Result", "No person detected in the image.")

def main():
    root = tk.Tk()
    root.withdraw()

    distance_m = simpledialog.askfloat("Input", "Enter distance to person (meters):")
    if distance_m is None:
        return

    angle_deg = simpledialog.askfloat("Input", "Enter camera angle from ground (degrees):")
    if angle_deg is None:
        return

    camera_height = simpledialog.askfloat("Input", "Enter camera height from ground (meters):")
    if camera_height is None:
        return

    messagebox.showinfo("Select Image", "Please select an image file...")
    image_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not image_path:
        messagebox.showwarning("No file", "No file selected. Exiting.")
        return

    calculate_real_height(distance_m, angle_deg, camera_height, image_path)

if __name__ == "__main__":
    main()
