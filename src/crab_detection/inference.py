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

def run_inference(image_path):
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return
    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=image_path, 
        conf=CONFIDENCE_THRESHOLD, 
        iou=0.7,           
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
                "image": image_path,
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
    
    output_img_path = os.path.join(output_dir, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_img_path, annotated_frame)
    
    print(f"\n--- MISSION SUMMARY ---\nDetected: {crab_count} European Green Crabs.")
    print(f"Annotated image saved as: {output_img_path}")

    if detection_data:
        csv_path = os.path.join(output_dir, f"{EXPORT_FILE_PREFIX}.csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=detection_data[0].keys())
            writer.writeheader()
            writer.writerows(detection_data)

   
    print("\n[KEYBOARD] Press 'q' to close the image and terminate.")
    cv2.imshow("MATE ROV 2026 - Invasive Species Task", annotated_frame)
    

    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        print("Termination signal received. Closing...")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    TEST_IMAGE = os.path.join(BASE_DIR, "assets", "crab_detection", "test_images", "Crab_test_1.jpg") 
    run_inference(TEST_IMAGE)