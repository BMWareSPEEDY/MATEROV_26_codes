import sys
import os

def main():
    print("MATE ROV 2026 - Master Control")
    print("-" * 30)
    print("1. Pipe Length Measurement Tool")
    print("2. Crab Detection (Single Image)")
    print("3. Crab Detection (Live Feed)")
    print("4. 3D Model Generation")
    print("-" * 30)
    
    choice = input("Enter your choice (1-4): ")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if choice == '1':
        os.system(f"python3 {os.path.join(script_dir, 'pipe_measurement', 'measurement_tool.py')}")
    elif choice == '2':
        os.system(f"python3 {os.path.join(script_dir, 'crab_detection', 'inference.py')}")
    elif choice == '3':
        os.system(f"python3 {os.path.join(script_dir, 'crab_detection', 'live_inference.py')}")
    elif choice == '4':
        os.system(f"python3 {os.path.join(script_dir, 'pipe_measurement', '3D_model_gen.py')}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
