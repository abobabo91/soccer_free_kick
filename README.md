# ⚽ Free Kick Simulator — Dual Mode (HTML Version)

This project simulates **soccer free kicks** with realistic physics, providing both analytical (no-drag) and numerical (with-drag) modes.  
It features a fully interactive **HTML visualization** that lets users compare the **optimal shot** to a **manual custom kick** in real time.

---

## 🌟 Key Features

- **Two Physics Modes**
  - **No Drag (Analytical)** – Uses closed-form projectile motion equations.
  - **With Drag (Numerical)** – Uses a Runge–Kutta 4 (RK4) integration method with quadratic air resistance.

- **Dual Trajectories**
  - **Optimal shot (cyan)** — automatically calculated to clear the wall and hit just under the crossbar.
  - **Manual shot (yellow)** — defined by user-adjustable angle and velocity, showing where the ball would actually go.

- **Dynamic Visualization**
  - Displays field, wall, goal, and the “goes-in” target line (bottom of the ball under the crossbar).
  - Shows both trajectories simultaneously with smooth, responsive animation.
  - Small teal markers represent the **top of the ball** along the optimal trajectory for accuracy.

- **Real-time Controls**
  - Adjustable **goal distance**, **wall distance**, **wall height**, and **drag coefficient**.
  - Adjustable **manual angle** and **velocity (km/h)**.
  - Fixed constants for gravity, air density, ball size, and goal dimensions (authentic FIFA specs).

- **Reference Links**
  - [Drag on a Soccer Ball (NASA)](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-on-a-soccer-ball/)
  - [Forces on a Soccer Ball (NASA)](https://www.grc.nasa.gov/www/k-12/airplane/socforce.html)
  - [Flight Equations with Drag (NASA)](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/flight-equations-with-drag/)

---

## 🧮 What It Calculates

| Metric | Optimal Shot | Manual Shot |
|---------|---------------|--------------|
| Angle (°) | Computed by solver | User-set |
| Velocity (km/h) | Computed by solver | User-set |
| Time to Goal (s) | Computed from solution | Derived from trajectory |

---

## 🖼️ Visualization Highlights

- **Cyan line** → solver’s optimal free kick trajectory  
- **Yellow line** → your manual kick  
- **Dashed teal line** → target “goes-in” height at the goal  
- **Red rectangle** → defensive wall  
- **Green rectangle** → goalposts  
- **Blue circles** → top of the ball along optimal flight  

---

## 🚀 Usage

Simply open the `free_kick_simulator.html` file in any modern browser (Chrome, Edge, Firefox).  
No installation required.

Move the sliders to change wall and goal parameters, adjust your manual angle and power, and see both trajectories update instantly.

---

## 🧠 Technical Overview

- **Physics engine**
  - No-drag: analytical parabolic motion.
  - With-drag: 4th-order Runge–Kutta integrator solving velocity-dependent differential equations.
- **Canvas rendering**
  - Auto-scaled coordinate system based on field geometry.
  - Smooth drawing with adjustable scaling and ratio.
- **Interactivity**
  - Linked sliders and numeric inputs.
  - Metrics update dynamically with every adjustment.

---

## 📁 Project Structure

free-kick-simulator/
├── README.md
├── src/
│ ├── free_kick_calculator.py
│ ├── free_kick_with_drag.py
│ ├── free_kick_simulator.html ← interactive HTML visualization
└── examples/
└── screenshots/


---

## 🧩 Notes

- This version intentionally fixes constants like gravity, air density, and goal dimensions to keep the model consistent.  
- The optimal solver ensures the ball clears the wall and lands just below the crossbar.  
- The manual mode allows experimentation with real-world free kick parameters (20–150 km/h, 0–60°).  
- Ball spin and Magnus effect are **not yet implemented**.

---

## 🪶 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## 🙌 Credits

Developed as an educational and visualization tool to explore the physics of soccer free kicks and to make the math behind the beautiful game **visual, interactive, and fun**.
