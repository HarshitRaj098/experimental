"""CPU-only person segmentation and pose preview for PyBodySwap AI.

This is an analysis/visualization stage, NOT identity or clothing replacement.
It processes video frame-by-frame and writes an annotated preview.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


def process_video(source: Path, output: Path, model_complexity: int = 1) -> None:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open input video: {source}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 25.0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        capture.release()
        raise RuntimeError("Input video has invalid dimensions.")

    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        raise RuntimeError(f"Could not create output video: {output}")

    mp_pose = mp.solutions.pose
    frame_count = 0
    try:
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            enable_segmentation=True,
            smooth_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as pose:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb.flags.writeable = False
                result = pose.process(rgb)
                rgb.flags.writeable = True

                if result.segmentation_mask is not None:
                    mask = result.segmentation_mask > 0.5
                    tint = np.zeros_like(frame)
                    tint[:, :, 1] = 180
                    frame[mask] = cv2.addWeighted(
                        frame[mask], 0.65, tint[mask], 0.35, 0
                    )

                if result.pose_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame,
                        result.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                    )

                cv2.putText(
                    frame,
                    "CPU pose + segmentation preview (not a body swap)",
                    (16, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                writer.write(frame)
                frame_count += 1
    finally:
        capture.release()
        writer.release()

    if frame_count == 0:
        output.unlink(missing_ok=True)
        raise RuntimeError("No frames were decoded from the input video.")

    print(f"Processed {frame_count} frames")
    print(f"Preview saved to: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a CPU-only pose and person-segmentation preview."
    )
    parser.add_argument("video", type=Path, help="Input video path")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("preview.mp4"),
        help="Output MP4 path (default: preview.mp4)",
    )
    parser.add_argument(
        "--model-complexity", type=int, choices=(0, 1, 2), default=1,
        help="MediaPipe pose model size; 0 is fastest, 2 is most accurate",
    )
    args = parser.parse_args()
    process_video(args.video, args.output, args.model_complexity)


if __name__ == "__main__":
    main()
