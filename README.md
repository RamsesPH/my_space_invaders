# Space Invaders (Python + Pygame)

A modernized remake of the classic 1978 *Space Invaders*, built using Python and Pygame.  
This version includes smooth movement, animated explosions, bunkers, alien laser attacks, and the iconic accelerating “marching” sound as invaders are destroyed.

## 🎮 Features

- Player movement and laser firing  
- Alien formation with horizontal movement + descent  
- Invaders shoot back using randomized attackers  
- Bunkers that absorb damage and break apart  
- Explosion animations  
- Win/Lose overlay with restart/quit options  
- Authentic 4‑step alien marching sound  
- Invaders speed up as their numbers decrease  
- Clean modular code structure

## 🧩 Project Structure

my_space_invaders/
│── assets.py
│── game.py
│── settings.py
│── player.py
│── invaders.py
│── laser.py
│── bunker.py
│── explosion.py
│── sounds/
│── images/


## 🔊 Alien Marching Sound

The original arcade game used a 4‑tone loop that speeds up as invaders die.  
This project recreates that effect using four generated WAV files:
step1.wav
step2.wav
step3.wav
step4.wav


These are played in sequence and accelerate based on remaining invaders.

## 🚀 How to Run

```bash
pip install pygame numpy
python game.py

📘 License
MIT License — feel free to modify and expand.

🧪 Tested On

- macOS
- Python 3.9
- Pygame 2.6