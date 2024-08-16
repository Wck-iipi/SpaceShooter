# SpaceShooter: A Pygame-based Scrolling Shooter Game
[![Watch the video](https://img.youtube.com/vi/B7rLfLCiMxI/maxresdefault.jpg)](https://youtu.be/B7rLfLCiMxI)
You can watch demo above.


This project is a side-scrolling shooter game implemented in Python using the Pygame library. Players control a spaceship and battle against waves of enemy ships, aiming for the highest score possible.

## Features

- **Scrolling Background:** A visually appealing background that continuously scrolls downwards, creating an illusion of movement.
- **Animated Sprites:** Player and enemy ships are animated, enhancing the game's visual presentation.
- **Multiple Enemy Types:** The game features different enemy ship types, each with unique behaviors and attack patterns.
- **Projectile System:** Both the player and enemy ships can fire projectiles, adding a dynamic element to the gameplay.
- **Collision Detection:** Detects and handles collisions between sprites, determining hits and game over scenarios.
- **Scorekeeping:**  Tracks and displays the player's score, increasing with each successful enemy takedown.
- **Start and Game Over Screens:** Presents the player with a starting screen and a game-over screen with retry and exit options.
- **Shared State Management:**  Utilizes a shared state module to manage and synchronize game data across different components.


## Implementation Details

- The game is built using Pygame, handling rendering, input, and game loop management.
- Sprites are implemented as objects with properties for animation, position, and movement. 
- Animation is achieved by cycling through frames of sprite sheets.
- Collision detection is implemented using Pygame's rectangle collision functions.
- A shared state module facilitates communication and data sharing between different game components.
