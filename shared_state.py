from collections import deque
from typing import List
from settings import pygame

frame_number = 0
scroll = 0
last_update = 0
animation_list = [None for _ in range(500)]  # type: List[pygame.Surface]
x_coordinates = [0 for _ in range(500)]  # type: List[int]
y_coordinates = [0 for _ in range(500)]  # type: List[int]
empty_index = deque(r for r in range(500))  # type: deque
filled_index = deque()  # type: deque
