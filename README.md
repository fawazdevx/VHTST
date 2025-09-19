# 🌡️ Virtual Heat Transfer Simulation Tool (VHTS)

The **Virtual Heat Transfer Simulation Tool (VHTS)** is an interactive learning software built with **Python (Tkinter)** to help students understand the three modes of heat transfer: **Conduction, Convection, and Radiation**.  

It is designed for **SS1 Physics students** to make abstract thermodynamics concepts more engaging through **visual simulations, graphics, and interactive mode switching**.

---

## ✨ Features
- 🔥 **Conduction** → Heat transfer through solids (e.g., hot spoon in boiling water).  
- 💧 **Convection** → Heat transfer in fluids (e.g., boiling water currents).  
- ☀️ **Radiation** → Heat transfer without a medium (e.g., sun heating objects).  
- 🎨 **Student-Friendly Graphics** → Pots, boiling water, arrows, sun, etc.  
- 🖱️ **Interactive Learning** → Switch modes without restarting.  
- 📘 **Curriculum-Aligned** → Fits SS1 Physics curriculum under *Thermal Physics*.  

---

## 📂 Project Structure
```
Virtual-Heat-Transfer-Simulation/
│
├── images/              # Graphics for the simulation
│   ├── pot.png
│   ├── spoon.png
│   ├── water.png
│   ├── arrow.png
│   ├── sun.png
│   ├── human.png
│
├── main.py              # Main simulation program (all modes integrated)
└── README.md            # Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Virtual-Heat-Transfer-Simulation.git
cd Virtual-Heat-Transfer-Simulation
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```
Activate it:  
- **Windows** → `venv\Scripts\activate`  
- **Linux/Mac** → `source venv/bin/activate`

### 3️⃣ Install Dependencies
```bash
pip install Pillow matplotlib
```

> **Note:** Tkinter is part of Python’s standard library, but on Linux you may need:  
```bash
sudo apt-get install python3-tk
```

### ▶️ Run the Simulation
```bash
python main.py
```

Inside the app:
- Select **Conduction**, **Convection**, or **Radiation**.  
- View the animations and explanations.  
- Switch freely between modes.  

---

## 🖼️ Graphics Used
- **pot.png** → Pot of boiling water  
- **spoon.png** → Metal spoon (conduction)  
- **water.png** → Water surface and bubbles  
- **arrow.png** → Convection arrows  
- **sun.png** → Radiation source  
- **human.png** → Person interacting  

(All images are stored in the `images/` folder.)  

---

## 📖 Educational Context
This project was developed for the research topic:  

**“Effects of a Virtual Heat Transfer Simulation Tool on Physics Students’ Achievement and Attitude to Thermodynamics in Ibadan, LA, Oyo State.”**

It demonstrates how technology can improve learning outcomes by making Physics more practical.

---

## 🚀 Future Improvements
- Add quizzes and practice questions after each mode.  
- Upgrade visuals to 3D animations (PyQt5 or Pygame).  
- Convert into a web-based platform for accessibility.  
- Integrate student progress tracking on blockchain (ICP/ChainLearn).  

---

## 📝 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and share with attribution.

---

## 👨‍💻 Author
**Fawaz Oyebode**  
University of Ibadan  

