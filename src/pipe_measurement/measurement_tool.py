import cv2
import math
import numpy as np
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'images', 'IMG_2257.jpeg')
ZOOM_WINDOW_SIZE = 300
ZOOM_FACTOR = 4
REQUIRED_MEASUREMENTS = 5

# State variables
points = []
pixels_per_metric = None
temp_img = None
original_img = None
unknown_measurements = []


def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def mouse_callback(event, x, y, flags, param):
    global points, pixels_per_metric, temp_img, unknown_measurements

    # --- ZOOM FEATURE ---
    # Create a zoomed-in crop around the mouse cursor
    pad = ZOOM_WINDOW_SIZE // (2 * ZOOM_FACTOR)
    left = max(0, x - pad)
    right = min(original_img.shape[1], x + pad)
    top = max(0, y - pad)
    bottom = min(original_img.shape[0], y + pad)

    crop = original_img[top:bottom, left:right]
    if crop.size > 0:
        # Pad crop if it's near the edges to maintain window size
        h, w = crop.shape[:2]
        expected_size = pad * 2
        if h < expected_size or w < expected_size:
            padded_crop = np.zeros((expected_size, expected_size, 3), dtype=np.uint8)
            # Center the crop in the padded view (roughly)
            dy = (expected_size - h) // 2
            dx = (expected_size - w) // 2
            padded_crop[dy:dy+h, dx:dx+w] = crop
            crop = padded_crop

        zoomed = cv2.resize(crop, (ZOOM_WINDOW_SIZE, ZOOM_WINDOW_SIZE), interpolation=cv2.INTER_LINEAR)
        # Draw a crosshair in the center of the zoom window
        cv2.line(zoomed, (ZOOM_WINDOW_SIZE // 2, 0), (ZOOM_WINDOW_SIZE // 2, ZOOM_WINDOW_SIZE), (0, 255, 255), 1)
        cv2.line(zoomed, (0, ZOOM_WINDOW_SIZE // 2), (ZOOM_WINDOW_SIZE, ZOOM_WINDOW_SIZE // 2), (0, 255, 255), 1)
        cv2.imshow("Zoom View (Precision)", zoomed)

    # --- CLICK HANDLING ---
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(temp_img, (x, y), 4, (0, 255, 0), -1)

        if len(points) % 2 == 0:
            p1, p2 = points[-2], points[-1]
            cv2.line(temp_img, p1, p2, (255, 100, 0), 2)
            dist_px = calculate_distance(p1, p2)

            if pixels_per_metric is None:
                cv2.imshow("Measure Tool", temp_img)
                # Note: input() might hang if run via some IDEs or non-interactive shells
                # But for terminal CLI use it's standard
                print("\n[REFERENCE] Reference pipe detected.")
                val = input("Enter its physical length (e.g., 100): ")
                try:
                    known_val = float(val)
                    pixels_per_metric = dist_px / known_val
                    print(f"[SCALE SET]: {pixels_per_metric:.2f} px/unit")
                    print(f"Now measure the unknown pipe {REQUIRED_MEASUREMENTS} times.\n")
                except ValueError:
                    print("Invalid number. Resetting this measurement.")
                    points = points[:-2] # Remove the last two points
                    # Redraw (approximate)
                    temp_img = original_img.copy()
                    for i in range(0, len(points), 2):
                        if i+1 < len(points):
                            cv2.circle(temp_img, points[i], 4, (0, 255, 0), -1)
                            cv2.circle(temp_img, points[i+1], 4, (0, 255, 0), -1)
                            cv2.line(temp_img, points[i], points[i+1], (255, 100, 0), 2)
            else:
                actual_len = dist_px / pixels_per_metric
                unknown_measurements.append(actual_len)

                # Visual label
                midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2 - 10)
                cv2.putText(temp_img, f"#{len(unknown_measurements)}", midpoint,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                print(f"Measurement {len(unknown_measurements)}/{REQUIRED_MEASUREMENTS}: {actual_len:.2f}")

                # --- AVERAGING LOGIC ---
                if len(unknown_measurements) == REQUIRED_MEASUREMENTS:
                    avg_len = sum(unknown_measurements) / REQUIRED_MEASUREMENTS
                    print("-" * 30)
                    print(f"FINAL AVERAGE: {avg_len:.4f}")
                    print("-" * 30)
                    # Don't reset scale, just the measurement list
                    unknown_measurements = []

        cv2.imshow("Measure Tool", temp_img)


# Main Execution
if __name__ == "__main__":
    original_img = cv2.imread(IMAGE_PATH)

    if original_img is None:
        print(f"Error: Could not find image at {IMAGE_PATH}")
        print("Please ensure 'IMG_2257.jpeg' exists in the current directory.")
    else:
        temp_img = original_img.copy()
        cv2.namedWindow("Measure Tool")
        cv2.namedWindow("Zoom View (Precision)")
        cv2.setMouseCallback("Measure Tool", mouse_callback)

        print("--- PRECISION MEASUREMENT TOOL ---")
        print("1. Use the 'Zoom View' window for pixel-perfect clicking.")
        print("2. CLICK TWO POINTS to set the scale with your KNOWN pipe first.")
        print(f"3. After scale is set, measure the unknown pipe {REQUIRED_MEASUREMENTS} times.")
        print("4. Press ANY KEY on an image window to exit.")

        cv2.imshow("Measure Tool", temp_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
