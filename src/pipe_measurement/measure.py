import cv2
import math
import numpy as np

ZOOM_WINDOW_SIZE = 300
ZOOM_FACTOR = 4
REQUIRED_MEASUREMENTS = 5

points = []
pixels_per_metric = None
temp_img = None
original_img = None
unknown_measurements = []
is_captured = False
need_calibration_input = False  # Flag to handle terminal input safely


def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def mouse_callback(event, x, y, flags, param):
    global points, pixels_per_metric, temp_img, unknown_measurements, original_img, need_calibration_input

    if not is_captured or original_img is None or need_calibration_input:
        return

    # --- ZOOM FEATURE ---
    pad = ZOOM_WINDOW_SIZE // (2 * ZOOM_FACTOR)
    left = max(0, x - pad)
    right = min(original_img.shape[1], x + pad)
    top = max(0, y - pad)
    bottom = min(original_img.shape[0], y + pad)

    crop = original_img[top:bottom, left:right]
    if crop.size > 0:
        h, w = crop.shape[:2]
        expected_size = pad * 2
        # Ensure fallback padding works correctly if near edges
        if h < expected_size or w < expected_size:
            padded_crop = np.zeros((expected_size, expected_size, 3), dtype=np.uint8)
            dy, dx = (expected_size - h) // 2, (expected_size - w) // 2
            padded_crop[dy:dy + h, dx:dx + w] = crop
            crop = padded_crop

        zoomed = cv2.resize(crop, (ZOOM_WINDOW_SIZE, ZOOM_WINDOW_SIZE), interpolation=cv2.INTER_LINEAR)
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

            if pixels_per_metric is None:
                # Signal the main loop to safely prompt for input
                need_calibration_input = True
            else:
                dist_px = calculate_distance(p1, p2)
                actual_len = dist_px / pixels_per_metric
                unknown_measurements.append(actual_len)
                midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2 - 10)
                cv2.putText(temp_img, f"#{len(unknown_measurements)}", midpoint,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                print(f"Measurement {len(unknown_measurements)}/{REQUIRED_MEASUREMENTS}: {actual_len:.2f}")

                if len(unknown_measurements) == REQUIRED_MEASUREMENTS:
                    avg_len = sum(unknown_measurements) / REQUIRED_MEASUREMENTS
                    print(f"\n" + "=" * 30)
                    print(f"FINAL AVERAGE: {avg_len:.4f}")
                    print("=" * 30 + "\n")

                    # Clear for next set
                    unknown_measurements = []
                    points = []
                    temp_img = original_img.copy()
                    print("Display cleared. You can start a new set of measurements.")

        cv2.imshow("Measure Tool", temp_img)


# Main Execution
if __name__ == "__main__":
    camera_index = 0
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {camera_index}. Trying index 1...")
        cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("Measure Tool")
    cv2.setMouseCallback("Measure Tool", mouse_callback)

    print("--- WEBCAM MEASUREMENT TOOL ---")
    print("1. Aim webcam and press 'SPACE' to freeze frame for measurement.")
    print("2. CLICK TWO POINTS to measure. The first pair MUST be your reference.")
    print("3. Press 'R' to reset points and return to live feed.")
    print("4. Press 'C' to clear CALIBRATION (scale) if you moved the camera.")
    print("5. Press 'ESC' to quit.")

    while True:
        if not is_captured:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # --- MIRROR THE FEED HERE ---
            # 1 means flipping horizontally around the y-axis
            frame = cv2.flip(frame, 1)

            original_img = frame.copy()
            temp_img = frame.copy()

            status = "CALIBRATED" if pixels_per_metric else "NOT CALIBRATED"
            cv2.putText(temp_img, f"LIVE FEED [{status}] - SPACE to Capture", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Measure Tool", temp_img)

        # Non-blocking GUI refresh
        key = cv2.waitKey(1) & 0xFF

        # Handle the calibration entry here in the main thread loop
        if need_calibration_input:
            p1, p2 = points[-2], points[-1]
            dist_px = calculate_distance(p1, p2)
            print("\n[REFERENCE] Reference object detected.")
            val = input("Enter its physical length: ")
            try:
                known_val = float(val)
                pixels_per_metric = dist_px / known_val
                print(f"[SCALE SET]: {pixels_per_metric:.2f} px/unit")
            except ValueError:
                print("Invalid number. Resetting calibration points.")
                points = points[:-2]
                temp_img = original_img.copy()
                cv2.imshow("Measure Tool", temp_img)

            need_calibration_input = False

        if key == ord(' '):
            is_captured = True
            temp_img = original_img.copy()
            points = []
            print("[CAPTURED] Frame frozen. Start measuring.")
            if pixels_per_metric:
                print(f"Using existing scale: {pixels_per_metric:.2f} px/unit")
            else:
                print("First measurement will be used for SCALE.")
            cv2.imshow("Measure Tool", temp_img)

        elif key == ord('r'):
            is_captured = False
            points = []
            unknown_measurements = []
            print("[RESET] Returning to live feed.")

        elif key == ord('c'):
            pixels_per_metric = None
            print("[CLEARED] Calibration reset. Next measurement will set new scale.")

        # ESC to exit
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()