import cv2
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video")
    parser.add_argument("--video", required=True, help="Path to input video, e.g. ski.MOV")
    parser.add_argument("--step", type=int, default=10, help="Save one frame every N frames")
    parser.add_argument("--out", default="Output Frames", help="Output folder")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)
    
    step = args.step
    save_dir = args.out

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    count = 0
    saved = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count%step == 0:
            cv2.imwrite(os.path.join(save_dir, f"frame{saved:04d}.jpg"), frame)
            saved += 1
    
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done! Saved {saved} frames to '{save_dir}'")

if __name__ == "__main__":
    main()
