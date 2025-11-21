import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import ttkbootstrap as tb

# ================================
# Heat Transfer Tab
# ================================
class HeatTransferTab:
    def __init__(self, parent):
        self.frame = tb.Frame(parent, bootstyle="dark")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.label = tb.Label(self.frame, text="🔥 Heat Transfer Between Two Objects 🔥",
                              font=("Segoe UI", 18, "bold"), bootstyle="info-inverse")
        self.label.pack(pady=15)

        # Canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="#222222", highlightthickness=0)
        self.canvas.pack(pady=15)

        # Objects
        self.obj1 = self.canvas.create_rectangle(150,150,300,300, fill="#ff4d4d", outline="#ff9999")
        self.obj2 = self.canvas.create_rectangle(400,150,550,300, fill="#4d4dff", outline="#9999ff")

        # Initial temps
        self.initial_temp1 = 80
        self.initial_temp2 = 20

        # Info label
        self.info = tb.Label(self.frame, text="", font=("Segoe UI", 12), bootstyle="light")
        self.info.pack(pady=5)

        # Buttons
        btn_frame = tb.Frame(self.frame)
        btn_frame.pack(pady=10)

        self.start_btn = tb.Button(btn_frame, text="Start Heat Transfer", bootstyle="success", command=self.start_transfer)
        self.start_btn.grid(row=0, column=0, padx=10)
        self.reset_btn = tb.Button(btn_frame, text="Reset", bootstyle="danger", command=self.reset_state)
        self.reset_btn.grid(row=0, column=1, padx=10)

        self.running = False
        self.reset_state()

    def reset_state(self):
        self.temp1 = self.initial_temp1
        self.temp2 = self.initial_temp2
        self.time = 0
        self.times, self.t1_vals, self.t2_vals = [], [], []
        self.running = False

        self.canvas.itemconfig(self.obj1, fill="#ff4d4d")
        self.canvas.itemconfig(self.obj2, fill="#4d4dff")
        self.info.config(text=f"Obj1: {self.temp1}°C | Obj2: {self.temp2}°C")

    def start_transfer(self):
        if not self.running:
            self.running = True
            self.simulate_step()

    def simulate_step(self):
        if not self.running:
            return
        k = 0.1
        dt = 1
        q = k * (self.temp1 - self.temp2) * dt
        self.temp1 -= q
        self.temp2 += q
        self.time += dt

        self.times.append(self.time)
        self.t1_vals.append(self.temp1)
        self.t2_vals.append(self.temp2)

        self.info.config(text=f"t={self.time}s | Obj1: {self.temp1:.1f}°C | Obj2: {self.temp2:.1f}°C")

        # Smooth color update
        red1 = min(255, int(3 * self.temp1))
        blue1 = max(0, 255 - int(3 * self.temp1))
        self.canvas.itemconfig(self.obj1, fill=f"#{red1:02x}4d{blue1:02x}")

        red2 = min(255, int(3 * self.temp2))
        blue2 = max(0, 255 - int(3 * self.temp2))
        self.canvas.itemconfig(self.obj2, fill=f"#{red2:02x}4d{blue2:02x}")

        if abs(self.temp1 - self.temp2) <= 0.5:
            self.running = False
            self.info.config(text=f"Simulation complete! Equilibrium ~{(self.temp1+self.temp2)/2:.1f}°C")
            plt.figure(figsize=(6,4))
            plt.plot(self.times, self.t1_vals, 'r-', label="Hot Object")
            plt.plot(self.times, self.t2_vals, 'b-', label="Cold Object")
            plt.xlabel("Time (s)")
            plt.ylabel("Temperature (°C)")
            plt.title("Heat Transfer Between Two Objects")
            plt.legend()
            plt.grid(True)
            plt.show()
            return

        self.frame.after(400, self.simulate_step)

# ================================
# Heat Transfer Modes Tab
# ================================
class HeatModesTab:
    def __init__(self, parent):
        self.frame = tb.Frame(parent, bootstyle="dark")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.label = tb.Label(self.frame, text="🔥 Heat Transfer Modes 🔥", font=("Segoe UI", 18, "bold"), bootstyle="info-inverse")
        self.label.pack(pady=15)

        # Canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="#222222", highlightthickness=0)
        self.canvas.pack(pady=15)

        # Info
        self.info = tb.Label(self.frame, text="Choose a mode to simulate.", font=("Segoe UI", 12), bootstyle="light")
        self.info.pack(pady=5)

        # Buttons
        btn_frame = tb.Frame(self.frame)
        btn_frame.pack(pady=10)

        tb.Button(btn_frame, text="Conduction", bootstyle="primary", command=self.show_conduction).grid(row=0, column=0, padx=10)
        tb.Button(btn_frame, text="Convection", bootstyle="primary", command=self.show_convection).grid(row=0, column=1, padx=10)
        tb.Button(btn_frame, text="Radiation", bootstyle="primary", command=self.show_radiation).grid(row=0, column=2, padx=10)

        self.images = {}  # keep refs

    def load_image(self, path, size=(150,150)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def clear_canvas(self):
        self.canvas.delete("all")

    # ------------------- Conduction -------------------
    def show_conduction(self):
        self.clear_canvas()
        self.info.config(text="Conduction: Heat flows by direct contact (Hot pot → Spoon touching it).")
        pot_img = self.load_image("images/pot.png", size=(200,200))
        self.original_spoon = Image.open("images/spoon.png").resize((160,160))
        spoon_img = ImageTk.PhotoImage(self.original_spoon)
        self.images['pot'] = pot_img
        self.images['spoon'] = spoon_img

        self.canvas.create_image(220,220,image=pot_img)
        self.spoon = self.canvas.create_image(320,100,image=spoon_img)
        self.heat_step = 0
        self.animate_spoon_heat()

    def animate_spoon_heat(self):
        if self.heat_step > 20:
            return
        red_spoon = self.original_spoon.convert("RGBA")
        pixels = red_spoon.load()
        width,height = red_spoon.size
        progress = int(width * (self.heat_step/20))
        for y in range(height):
            for x in range(width):
                r,g,b,a = pixels[x,y]
                if a>0 and x<=progress:
                    intensity=int(255*(x/width))
                    new_r=min(255,r+intensity)
                    new_g=max(0,g-intensity//3)
                    new_b=max(0,b-intensity//2)
                    pixels[x,y]=(new_r,new_g,new_b,a)
        spoon_img = ImageTk.PhotoImage(red_spoon)
        self.images['spoon']=spoon_img
        self.canvas.itemconfig(self.spoon,image=spoon_img)
        self.heat_step+=1
        self.canvas.after(300,self.animate_spoon_heat)

    # ------------------- Convection -------------------
    def show_convection(self):
        self.clear_canvas()
        self.info.config(text="Convection: Heat transfer by fluid movement (Boiling water currents).")
        pot_img = self.load_image("images/pot_c.png", size=(400,400))
        self.images['pot']=pot_img
        self.canvas.create_image(350,220,image=pot_img)

        up_arrow = self.load_image("images/arrow_up_red.png", size=(50,80))
        down_arrow = self.load_image("images/arrow_down_blue.png", size=(50,80))
        self.images['up_arrow']=up_arrow
        self.images['down_arrow']=down_arrow

        self.up_arrows=[
            self.canvas.create_image(350,270,image=up_arrow),
            self.canvas.create_image(310,270,image=up_arrow),
            self.canvas.create_image(390,270,image=up_arrow)
        ]
        self.down_arrows=[
            self.canvas.create_image(350,150,image=down_arrow),
            self.canvas.create_image(310,150,image=down_arrow),
            self.canvas.create_image(390,150,image=down_arrow)
        ]
        self.animate_convection()

    def animate_convection(self):
        for arrow in self.up_arrows:
            self.canvas.move(arrow,0,-10)
            x,y=self.canvas.coords(arrow)
            if y<100:
                self.canvas.coords(arrow,x,270)
        for arrow in self.down_arrows:
            self.canvas.move(arrow,0,10)
            x,y=self.canvas.coords(arrow)
            if y>270:
                self.canvas.coords(arrow,x,150)
        self.canvas.after(300,self.animate_convection)

    # ------------------- Radiation -------------------
    def show_radiation(self):
        self.clear_canvas()
        self.info.config(text="Radiation: Heat transfer by electromagnetic waves (Sun → Human).")
        self.heat_step=0
        self.setup_radiation()
        self.radiation_rays=[]
        self.animate_radiation_rays()

    def setup_radiation(self):
        self.sun_img = Image.open("images/sun.png").resize((80,80))
        self.sun_photo = ImageTk.PhotoImage(self.sun_img)
        self.sun = self.canvas.create_image(100,100,image=self.sun_photo,anchor="center")
        self.original_human = Image.open("images/human.png").resize((120,120))
        self.human_photo = ImageTk.PhotoImage(self.original_human)
        self.human = self.canvas.create_image(500,350,image=self.human_photo,anchor="center")

    def animate_radiation_rays(self):
        for ray in getattr(self,'radiation_rays',[]):
            self.canvas.delete(ray)
        self.radiation_rays=[]
        sun_x,sun_y=self.canvas.coords(self.sun)
        human_x,human_y=self.canvas.coords(self.human)
        for i in range(12):
            offset_x=random.randint(-40,40)
            offset_y=random.randint(-40,40)
            ray=self.canvas.create_line(sun_x,sun_y,human_x+offset_x,human_y+offset_y,fill="yellow",width=2)
            self.radiation_rays.append(ray)
        self.animate_human_tint()
        self.canvas.after(300,self.animate_radiation_rays)

    def animate_human_tint(self):
        if self.heat_step>20:
            return
        heated_human = self.original_human.convert("RGBA")
        pixels = heated_human.load()
        width,height = heated_human.size
        progress=int(height*(self.heat_step/20))
        for y in range(height):
            for x in range(width):
                r,g,b,a=pixels[x,y]
                if a>0 and y<=progress:
                    intensity=int(255*(y/height))
                    new_r=min(255,r+intensity)
                    new_g=max(0,g-intensity//3)
                    new_b=max(0,b-intensity//2)
                    pixels[x,y]=(new_r,new_g,new_b,a)
        human_img=ImageTk.PhotoImage(heated_human)
        self.images['human']=human_img
        self.canvas.itemconfig(self.human,image=human_img)
        self.heat_step+=1
        self.canvas.after(300,self.animate_human_tint)


# ================================
# Particle Simulation Tabs
# ================================
class HeatSimulationTab:
    def __init__(self, parent, state="Solid"):
        self.state=state
        self.temperature=20
        self.frame=tb.Frame(parent, bootstyle="dark")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.label = tb.Label(self.frame,text=f"{state} State Heat Simulation",
                              font=("Segoe UI",16,"bold"),bootstyle="info-inverse")
        self.label.pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400,bg="#222222", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Temperature label and slider
        self.temp_label=tb.Label(self.frame,text=f"Temperature: {self.temperature}°C",bootstyle="light")
        self.temp_label.pack(pady=5)
        self.slider = tb.Scale(self.frame,from_=0,to=100,orient="horizontal",
                               command=self.update_temperature,bootstyle="info")
        self.slider.set(self.temperature)
        self.slider.pack(pady=10,fill="x",padx=50)

        # Particles
        self.particles=[]
        self.base_positions=[]
        if state=="Solid":
            self.create_grid_particles(5,8,80)
        elif state=="Liquid":
            self.create_random_particles(40)
        elif state=="Gas":
            self.create_random_particles(25)

        self.animate()

    def create_grid_particles(self,rows,cols,spacing):
        for i in range(rows):
            for j in range(cols):
                x=80+j*spacing
                y=80+i*spacing
                particle=self.canvas.create_oval(x-10,y-10,x+10,y+10,fill="#44aaff",outline="")
                self.particles.append(particle)
                self.base_positions.append((x,y))

    def create_random_particles(self,count):
        for _ in range(count):
            x=random.randint(50,650)
            y=random.randint(50,350)
            particle=self.canvas.create_oval(x-8,y-8,x+8,y+8,fill="#44aaff",outline="")
            self.particles.append(particle)
            self.base_positions.append((x,y))

    def update_temperature(self,val):
        self.temperature=int(float(val))
        self.temp_label.config(text=f"Temperature: {self.temperature}°C")

    def animate(self):
        for idx, particle in enumerate(self.particles):
            base_x, base_y = self.base_positions[idx]
            if self.state == "Solid":
                # Amplitude proportional to temperature
                amp = int(self.temperature / 5)
                # Random displacement around base position
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)
                # Move particle to oscillate around its base position
                self.canvas.coords(particle, base_x - 10 + dx, base_y - 10 + dy, base_x + 10 + dx, base_y + 10 + dy)
            elif self.state == "Liquid":
                amp = int(self.temperature / 3)
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)
                self.canvas.move(particle, dx, dy)
            elif self.state == "Gas":
                amp = int(self.temperature / 2 + 5)
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)
                self.canvas.move(particle, dx, dy)

            # Color changes with temperature
            red = min(255, 50 + self.temperature * 2)
            blue = max(0, 255 - self.temperature * 2)
            color = f"#{red:02x}33{blue:02x}"
            self.canvas.itemconfig(particle, fill=color)

        self.frame.after(100, self.animate)


# ================================
# Main App
# ================================
class HeatSimulationApp:
    def __init__(self, root):
        self.root=root
        self.root.title("🌡️ Virtual Heat Transfer Simulation Tool (VHTST) 🌡️")
        self.root.geometry("900x700")

        notebook = tb.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.transfer_tab=HeatTransferTab(notebook)
        notebook.add(self.transfer_tab.frame,text="Heat Transfer (2 Objects)")

        self.modes_tab=HeatModesTab(notebook)
        notebook.add(self.modes_tab.frame,text="Heat Transfer Modes")

        self.solid_tab=HeatSimulationTab(notebook,state="Solid")
        notebook.add(self.solid_tab.frame,text="Solid")

        self.liquid_tab=HeatSimulationTab(notebook,state="Liquid")
        notebook.add(self.liquid_tab.frame,text="Liquid")

        self.gas_tab=HeatSimulationTab(notebook,state="Gas")
        notebook.add(self.gas_tab.frame,text="Gas")

if __name__=="__main__":
    root=tb.Window(themename="darkly")
    app=HeatSimulationApp(root)
    root.mainloop()
