import cv2
import argparse
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video")
    parser.add_argument("--video", required=True, help="Path to input video, e.g. ski.MOV")
    parser.add_argument("--step", type=int, default=10, help="Save one frame every N frames")
    parser.add_argument("--fps", type=float, default=None, help="Save N frames per second (overrides --step)")
    parser.add_argument("--out", default="Output Frames", help="Output folder")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps else 0
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration:.2f} seconds")

    if args.fps is not None:
        interval = max(1, int(round(fps / args.fps)))
        print(f"Mode: time-based | target = {args.fps} fps | interval = {interval}")
    else:
        interval = args.step
        print(f"Mode: frame-based | step = {interval}")

    if args.fps is not None and args.step != 10:
        print("! Both --fps and --step provided. Using --fps")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    save_dir = f"{args.out}_{timestamp}"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    count = 0
    saved = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count%interval == 0:
            cv2.imwrite(os.path.join(save_dir, f"frame{saved:04d}.jpg"), frame)
            saved += 1
    
        count += 1
        if total_frames > 0:
            progress = (count / total_frames) * 100
            print(f"\rProcessing: {progress:.1f}%", end="")

    print("\nProcessing complete!")

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done! Saved {saved} frames to '{save_dir}'")

    import subprocess
    subprocess.run(["open", save_dir])

if __name__ == "__main__":
    main()
