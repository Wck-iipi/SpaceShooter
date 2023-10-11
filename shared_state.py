from collections import deque
from typing import List

frame_number = [0 for _ in range(500)]  # type: List[int]
sprite_name = ["" for _ in range(500)]  # type: List[str]
scroll = 0
last_update = 0
animation_list = [None for _ in range(500)]
rotation = [0 for _ in range(500)]  # type: List[int]
x_coordinates = [0 for _ in range(500)]  # type: List[int]
x_coordinates[0] = 400
y_coordinates = [0 for _ in range(500)]  # type: List[int]
y_coordinates[0] = 780
empty_index = deque(r for r in range(500))  # type: deque
filled_index = deque()  # type: deque
score = 0
screen_number = 0
start_again = True
