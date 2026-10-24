import time
from tools import hashtag_generator

start = time.time()
print(hashtag_generator("YOLOv8 helmet detection project", "LinkedIn"))
print(f"[{time.time() - start:.1f} seconds]")