import cv2
import subprocess
import sys
from ultralytics import YOLO

YOUTUBE_URL = "https://www.youtube.com/watch?v=O8xVFhgEv6Q"

# Replace with your downloaded wildlife model
MODEL_PATH = "best.pt"

CONF_THRESHOLD = 0.40


def get_stream_url(youtube_url: str) -> str:
    """
    Extract direct stream URL from YouTube using yt-dlp.
    """
    cmd = ["yt-dlp", "-g", youtube_url]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp error:\n{result.stderr}")

    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("http"):
            return line

    raise RuntimeError("No valid stream URL found.")


def draw_counts(frame, counts):
    """
    Display total and per-class counts on the frame.
    """
    y = 30
    total = sum(counts.values())

    cv2.putText(
        frame,
        f"Total animals: {total}",
        (10, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )
    y += 30

    for name, count in sorted(counts.items()):
        cv2.putText(
            frame,
            f"{name}: {count}",
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        y += 25


def main():
    try:
        print("Loading YOLO wildlife model...")
        model = YOLO(MODEL_PATH)

        print("Fetching stream URL...")
        stream_url = get_stream_url(YOUTUBE_URL)
        print("Stream ready.")

        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            raise RuntimeError("Failed to open stream.")

        print("Press 'q' to quit.")

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Stream ended or frame not received.")
                break

            # Skip frames for performance (process 1 in 5)
            frame_count += 1
            if frame_count % 5 != 0:
                continue

            # Run YOLO detection
            results = model(frame, verbose=False)
            result = results[0]

            counts = {}

            if result.boxes is not None:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    if conf < CONF_THRESHOLD:
                        continue

                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Count per class
                    counts[class_name] = counts.get(class_name, 0) + 1

                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Draw label
                    label = f"{class_name} {conf:.2f}"
                    cv2.putText(
                        frame,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            # Draw counts overlay
            draw_counts(frame, counts)

            cv2.imshow("Wildlife Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()