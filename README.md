# OpenGL-Catch-The-Diamonds-Game

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenGL](https://img.shields.io/badge/Library-PyOpenGL-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

**Repository Link:** [https://github.com/rfuadur/OpenGL-Catch-The-Diamonds-Game](https://github.com/rfuadur/OpenGL-Catch-The-Diamonds-Game)

## 📝 Project Overview
This project is a 2D interactive arcade game developed using **Python** and **OpenGL**. Unlike standard sprite-based games, this engine manually renders all geometric shapes (diamonds, catcher, buttons) using the **Midpoint Line Drawing Algorithm**.

The objective is simple: control the catcher at the bottom of the screen to collect falling diamonds while avoiding misses. The game features dynamic difficulty scaling, state management (Pause/Play), and custom UI buttons.

## ✨ Key Technical Features
* **Midpoint Line Algorithm:** All visual elements are drawn pixel-by-pixel using the 8-way symmetry Midpoint Line Drawing Algorithm (converted from Zone 0).
* **AABB Collision Detection:** Implements Axis-Aligned Bounding Box logic to detect intersections between the falling diamonds and the catcher.
* **State Management:** Handles multiple game states including `PLAYING`, `PAUSED`, and `GAME_OVER`.
* **Dynamic Difficulty:** The speed of falling diamonds increases automatically as the player's score rises.
* **Interactive UI:** Features clickable buttons (Restart, Pause, Exit) rendered directly in the OpenGL window.

## 🎮 Controls
The game supports Keyboard and Mouse interactions:

| Input | Action | Description |
| :--- | :--- | :--- |
| **Left Arrow (←)** | Move Left | Moves the catcher to the left. |
| **Right Arrow (→)** | Move Right | Moves the catcher to the right. |
| **Mouse Click** | Interact UI | Click the on-screen buttons (Restart ⟳, Pause ⏯, Exit ✖). |

## 🛠️ Prerequisites
To run this project, you need the following installed:
* **Python 3.x**
* **PyOpenGL**

## 🚀 How to Run

### 1. Install Dependencies
If you haven't installed the OpenGL library yet, run this command in your terminal:

```bash
pip install PyOpenGL PyOpenGL_accelerate
