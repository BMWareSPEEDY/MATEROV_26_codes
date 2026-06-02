import cv2
import json
import csv
import os
import torch
from ultralytics import YOLO

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
MODEL_PATH = os.path.join(BASE_DIR, "assets", "crab_detection", "models", "best.pt")
CONFIDENCE_THRESHOLD = 0.45
EXPORT_FILE_PREFIX = "detection_results"

DEVICE = 'mps' if torch.backends.mps.is_available() else 'cpu'


def run_inference(frame):
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=frame,
        conf=CONFIDENCE_THRESHOLD,
        iou=0.6,
        device=DEVICE,
        classes=[0],
        line_width=3,
        imgsz=800,
        agnostic_nms=False
    )

    detection_data = []
    for result in results:
        annotated_frame = result.plot(font_size=1.0, line_width=2)

        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0].item())
            conf = box.conf[0].item()
            class_name = model.names[cls_id]

            detection_data.append({
                "image": "live_capture.jpg",
                "class": class_name,
                "confidence": round(conf, 4)
            })

    crab_count = len(detection_data)
    label_text = f"TOTAL INVASIVE CRABS: {crab_count}"

    cv2.rectangle(annotated_frame, (5, 5), (450, 60), (0, 0, 0), -1)
    cv2.putText(annotated_frame, label_text, (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    output_dir = os.path.join(BASE_DIR, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_img_path = os.path.join(output_dir, "detected_live_capture.jpg")
    cv2.imwrite(output_img_path, annotated_frame)

    print(f"\n--- MISSION SUMMARY ---\nDetected: {crab_count} European Green Crabs.")
    print(f"Annotated image saved as: {output_img_path}")

    if detection_data:
        csv_path = os.path.join(output_dir, f"{EXPORT_FILE_PREFIX}.csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=detection_data[0].keys())
            writer.writeheader()
            writer.writerows(detection_data)

    print("\n[RESULT WINDOW] Press 'c' to close result and return to live feed.")
    while True:
        cv2.imshow("MATE ROV 2026 - Detection Result", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cv2.destroyWindow("MATE ROV 2026 - Detection Result")


def start_video_stream():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera index 1. Check your connections.")
        return

    print("\n--- LIVE VIDEO STREAM STARTED ---")
    print("Press [SPACEBAR] to grab a frame and run crab detection.")
    print("Press [q] to quit the application.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame from camera.")
            break

        cv2.imshow("MATE ROV 2026 - Live Video Feed Camera 1", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            print("\nSpacebar pressed! Freezing frame and running inference...")
            run_inference(frame)
            print("\nReturned to live video feed.")

        elif key == ord('q'):
            print("Termination signal received. Exiting...")
            break

    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_video_stream()