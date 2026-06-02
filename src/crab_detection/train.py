from ultralytics import YOLO
import os
import torch

def train_model():
    if not torch.backends.mps.is_available():
        print("Warning: MPS not available. Training will be slow on CPU.")
        device = 'cpu'
    else:
        device = 'mps'
        print(f"Using device: {device} (Apple Silicon GPU)")

    model = YOLO("yolov8s.pt")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_yaml_path = os.path.join(script_dir, "data.yaml")

    model.train(
        data=data_yaml_path,
        epochs=100,
        imgsz=800,            
        device=device,        
        batch=8,              
        workers=5,            
        project="crab_detection",
        name="mate_rov_training",
        exist_ok=True,        
        pretrained=True,
    )

if __name__ == "__main__":
    train_model()