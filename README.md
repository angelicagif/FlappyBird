Side Scroller (Python + Pygame)
================================

This is my first attempt at creating a pygame.
I followed a tutorial from Coding with Russ for the beginning but after the core game, 
it is created by myself, so expect quirks, experiments, and plenty of “could be betters.”  

------------------------------------------------------------
🚀 Features / Systems
------------------------------------------------------------
This project is more of modge-podge of elements to help me learn. 
- Start screen
- End screen
- Sound
- .JSON highscore saving
- Medal system
- Basic movement mechanics

------------------------------------------------------------
📸 Screenshots
------------------------------------------------------------
<p align="left">
  <img alt="Start" src="https://github.com/user-attachments/assets/b5140e45-028e-4524-b8ec-b881a8fdc72d" width="35%">
&nbsp;
  <img alt="Mid" src="https://github.com/user-attachments/assets/d445a0bc-22d8-4c9c-99fc-aeb974223df4" width="33%">
&nbsp;
  <img alt="End" src="https://github.com/user-attachments/assets/06b67f6e-f4a7-4bad-a2d3-cf771b93d1e6" width="35%">
</p>



------------------------------------------------------------
🎮 Gameplay
------------------------------------------------------------


https://github.com/user-attachments/assets/bd3ad45a-dc6b-48e9-bc0d-3b122b782b0f



------------------------------------------------------------
📦 Installation
------------------------------------------------------------
You’ll need Python installed.

Dependencies:
    pygame-ce,
    numpy,
    psutil

Install them with:
    pip install pygame-ce numpy psutil

------------------------------------------------------------
🛠️ Current Quirks / Notes
------------------------------------------------------------
- No dedicated render() function in main.py (everything’s inline)
- main.py is in the /scripts folder instead of project root (gulp)
- Some things are loaded into memory more than once
- Using self.game.screen_width / height for rendering bounds (can switch to self.game.screen.get_size())
- Entity hitboxes aren’t stored in their list → can’t reference them across classes
- Sliding after jumps is intentional (for now)

------------------------------------------------------------
📝 TODO
------------------------------------------------------------
- Implement weapon system + weapon stats JSON
- Load level info from JSON (entities, spawn points, death barriers, etc.)
- Replace temporary values (e.g., friction, attack damage) with proper configs
- Rework all attacks to be projectile-based
- Rewrite player hitbox system
- Rewrite entities + entities.json format
- Add can_walk_off_edge and height check settings per-entity
- Use spatial grid partitioning for entities + player (not just tiles)
- Centralize asset loading and rendering
- Add a shop system
