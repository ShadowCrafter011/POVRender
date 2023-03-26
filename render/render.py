from moviepy.editor import ImageSequenceClip
from datetime import datetime
from time import sleep
import numpy as np
import subprocess
import keyboard
import sys
import cv2
import os

def wait_exit():
	print("Press q to exit")
	while not keyboard.is_pressed("q"):
		sleep(.01)
	exit()

def main():
	if len(sys.argv) < 2:
		print("No path supplied exiting...")
		wait_exit()

	path = sys.argv[1]
	print(f"Render video out of files in {path}...\n")

	pngs = sorted(list(filter(lambda p: p.endswith(".png"), os.listdir(path))))
	file_paths = [os.path.join(path, png) for png in pngs]

	if len(file_paths) < 24:
		print("At least 24 frames must be provided to render the animation")
		print("Exiting...")
		wait_exit()

	render_path = os.path.join(path, "renders")
	if not os.path.exists(render_path):
		os.mkdir(render_path)

	video_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
	video_path = os.path.join(render_path, f"{video_name}.mp4")
	ImageSequenceClip(file_paths, fps=24).write_videofile(video_path)

	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		print("Could not open video file, exiting...")
		wait_exit()

	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			cv2.imshow("Video", frame)

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break

			if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
				break
		else:
		    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

	cap.release()
	cv2.destroyAllWindows()

	subprocess.Popen(rf'explorer /select,"{video_path}"')

if __name__ == "__main__":
	main()
