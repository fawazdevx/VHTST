import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


# ================================
# Tab 1: Heat Transfer Between 2 Objects
# ================================
class HeatTransferTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill="both", expand=True)

        # Title
        self.label = tk.Label(self.frame, text="Heat Transfer Between Two Objects",
                              font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1e1e1e")
        self.label.pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Create two objects
        self.obj1 = self.canvas.create_rectangle(150, 150, 300, 300, fill="#ff3333")  # hot
        self.obj2 = self.canvas.create_rectangle(400, 150, 550, 300, fill="#3333ff")  # cold

        # Initial temperatures
        self.initial_temp1 = 80
        self.initial_temp2 = 20

        # Info label
        self.info = tk.Label(self.frame,
                             font=("Segoe UI", 12), fg="#ffffff", bg="#1e1e1e")
        self.info.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self.frame, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Heat Transfer",
                                   command=self.start_transfer,
                                   bg="#444444", fg="white", font=("Segoe UI", 12))
        self.start_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = tk.Button(btn_frame, text="Reset",
                                   command=self.reset_state,
                                   bg="#666666", fg="white", font=("Segoe UI", 12))
        self.reset_btn.grid(row=0, column=1, padx=10)

        # Prepare simulation variables
        self.running = False
        self.reset_state()

    def reset_state(self):
        """Reset simulation to initial conditions"""
        self.temp1 = self.initial_temp1
        self.temp2 = self.initial_temp2
        self.time = 0
        self.times, self.t1_vals, self.t2_vals = [], [], []
        self.running = False

        # to Reset colors
        self.canvas.itemconfig(self.obj1, fill="#ff3333")
        self.canvas.itemconfig(self.obj2, fill="#3333ff")

        # to Reset info text
        self.info.config(text=f"Object1: {self.temp1}°C | Object2: {self.temp2}°C")

    def start_transfer(self):
        """Start animated heat transfer"""
        if not self.running:
            self.running = True
            self.simulate_step()

    def simulate_step(self):
        """One step of simulation (runs repeatedly with after)"""
        if not self.running:
            return

        k = 0.1  # thermal conductivity factor
        dt = 1   # time step

        # for heat flow
        q = k * (self.temp1 - self.temp2) * dt
        self.temp1 -= q
        self.temp2 += q
        self.time += dt

        # to store values
        self.times.append(self.time)
        self.t1_vals.append(self.temp1)
        self.t2_vals.append(self.temp2)

        # to update info
        self.info.config(text=f"t={self.time}s | Obj1: {self.temp1:.1f}°C | Obj2: {self.temp2:.1f}°C")

        # to update colors gradually (hot = more red, cold = more blue)
        red1 = min(255, int(5 * self.temp1))
        blue1 = max(0, 255 - int(5 * self.temp1))
        self.canvas.itemconfig(self.obj1, fill=f"#{red1:02x}33{blue1:02x}")

        red2 = min(255, int(5 * self.temp2))
        blue2 = max(0, 255 - int(5 * self.temp2))
        self.canvas.itemconfig(self.obj2, fill=f"#{red2:02x}33{blue2:02x}")

        # to check for equilibrium
        if abs(self.temp1 - self.temp2) <= 0.5:
            self.running = False
            self.info.config(text=f"Simulation complete! Equilibrium ~{(self.temp1+self.temp2)/2:.1f}°C")

            # Show cooling curve
            plt.figure(figsize=(6, 4))
            plt.plot(self.times, self.t1_vals, 'r-', label="Hot Object")
            plt.plot(self.times, self.t2_vals, 'b-', label="Cold Object")
            plt.xlabel("Time (s)")
            plt.ylabel("Temperature (°C)")
            plt.title("Heat Transfer Between Two Objects")
            plt.legend()
            plt.grid(True)
            plt.show()
            return

        # to schedule next step
        self.frame.after(500, self.simulate_step)

# ================================
# Tab: Heat Transfer Modes (Conduction, Convection and Radiation)
# ================================
class HeatModesTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill="both", expand=True)

        # setting title
        self.label = tk.Label(self.frame, text="Heat Transfer Modes",
                              font=("Segoe UI", 16, "bold"),
                              fg="#ffffff", bg="#1e1e1e")
        self.label.pack(pady=10)

        # the canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400,
                                bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Info Label
        self.info = tk.Label(self.frame, text="Choose a mode to simulate.",
                             font=("Segoe UI", 12), fg="#ffffff", bg="#1e1e1e")
        self.info.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.frame, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Conduction",
                  command=self.show_conduction,
                  bg="#444444", fg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Convection",
                  command=self.show_convection,
                  bg="#444444", fg="white", font=("Segoe UI", 12)).grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="Radiation",
                  command=self.show_radiation,
                  bg="#444444", fg="white", font=("Segoe UI", 12)).grid(row=0, column=2, padx=10)

        self.images = {}  # keep references so images don’t get garbage collected

    def load_image(self, path, size=(150, 150)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def clear_canvas(self):
        self.canvas.delete("all")

    # -------------------- Conduction --------------------
    def show_conduction(self):
        self.clear_canvas()
        self.info.config(text="Conduction: Heat flows by direct contact (Hot pot → Spoon touching it).")

        # Load pot and spoon (keep original spoon for recoloring)
        pot_img = self.load_image("images/pot.png", size=(200, 200))
        self.original_spoon = Image.open("images/spoon.png").resize((160, 160))
        spoon_img = ImageTk.PhotoImage(self.original_spoon)

        self.images['pot'] = pot_img
        self.images['spoon'] = spoon_img

        # Place pot
        self.canvas.create_image(220, 220, image=pot_img)
        # Place spoon touching the pot
        self.spoon = self.canvas.create_image(320, 100, image=spoon_img)

        # Start conduction animation
        self.heat_step = 0
        self.animate_spoon_heat()

    def animate_spoon_heat(self):
        if self.heat_step > 20:
            return  # stop after full conduction

        # Create a copy of the spoon for recoloring
        red_spoon = self.original_spoon.convert("RGBA")
        pixels = red_spoon.load()

        width, height = red_spoon.size
        progress = int(width * (self.heat_step / 20))  # how far heat has spread

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:  # Only tint visible pixels
                    if x <= progress:  # Heat only spreads up to 'progress'
                        intensity = int(255 * (x / width))  # weaker at tip, stronger at pot end
                        new_r = min(255, r + intensity)
                        new_g = max(0, g - intensity // 3)
                        new_b = max(0, b - intensity // 2)
                        pixels[x, y] = (new_r, new_g, new_b, a)

        # Update canvas with new tinted image
        spoon_img = ImageTk.PhotoImage(red_spoon)
        self.images['spoon'] = spoon_img  # prevent garbage collection
        self.canvas.itemconfig(self.spoon, image=spoon_img)

        self.heat_step += 1
        self.canvas.after(300, self.animate_spoon_heat)

    def show_convection(self):
        self.clear_canvas()
        self.info.config(text="Convection: Heat transfer by fluid movement (Boiling water currents).")

        # Load pot
        pot_img = self.load_image("images/pot_c.png", size=(200, 200))
        self.images['pot'] = pot_img
        self.canvas.create_image(350, 220, image=pot_img)

        # Load arrows
        up_arrow = self.load_image("images/arrow_up_red.png", size=(50, 80))
        down_arrow = self.load_image("images/arrow_down_blue.png", size=(50, 80))
        self.images['up_arrow'] = up_arrow
        self.images['down_arrow'] = down_arrow

        # Place arrows (store references so we can animate)
        self.up_arrows = [
            self.canvas.create_image(350, 270, image=up_arrow),  # middle bottom
            self.canvas.create_image(310, 270, image=up_arrow),  # left bottom
            self.canvas.create_image(390, 270, image=up_arrow)  # right bottom
        ]

        self.down_arrows = [
            self.canvas.create_image(350, 150, image=down_arrow),  # middle top
            self.canvas.create_image(310, 150, image=down_arrow),  # left top
            self.canvas.create_image(390, 150, image=down_arrow)  # right top
        ]

        # Start animation
        self.animate_convection()

    def animate_convection(self):
        # Move up arrows
        for arrow in self.up_arrows:
            self.canvas.move(arrow, 0, -10)  # move upward
            x, y = self.canvas.coords(arrow)
            if y < 100:  # reset to bottom
                self.canvas.coords(arrow, x, 270)

        # Move down arrows
        for arrow in self.down_arrows:
            self.canvas.move(arrow, 0, 10)  # move downward
            x, y = self.canvas.coords(arrow)
            if y > 270:  # reset to top
                self.canvas.coords(arrow, x, 150)

        # Loop again
        self.canvas.after(300, self.animate_convection)

    def show_radiation(self):
        self.clear_canvas()
        self.info.config(text="Radiation: Heat transfer by electromagnetic waves (Sun → Human).")

        # Reset heat progress every time we show radiation
        self.heat_step = 0

        # Setup radiation scene
        self.setup_radiation()

        # ✅ Initialize radiation rays list
        self.radiation_rays = []

        # Start the animation
        self.animate_radiation_rays()

    def setup_radiation(self):
        # Load sun image
        self.sun_img = Image.open("images/sun.png").resize((80, 80))
        self.sun_photo = ImageTk.PhotoImage(self.sun_img)
        self.sun = self.canvas.create_image(100, 100, image=self.sun_photo, anchor="center")

        # Always reload a fresh human image for tinting
        self.original_human = Image.open("images/human.png").resize((120, 120))
        self.human_photo = ImageTk.PhotoImage(self.original_human)
        self.human = self.canvas.create_image(500, 350, image=self.human_photo, anchor="center")

    def animate_radiation_rays(self):
        # to make sure list exists
        if not hasattr(self, "radiation_rays"):
            self.radiation_rays = []

        # to clear old rays
        for ray in self.radiation_rays:
            self.canvas.delete(ray)
        self.radiation_rays.clear()

        # to get positions of sun and human
        sun_coords = self.canvas.coords(self.sun)
        human_coords = self.canvas.coords(self.human)

        if not sun_coords or not human_coords:
            return

        sun_x, sun_y = sun_coords
        human_x, human_y = human_coords

        # to draw rays as a cone converging to the human for ultra violet rays from sun
        import random
        for i in range(12):  # number of rays
            offset_x = random.randint(-40, 40)
            offset_y = random.randint(-40, 40)

            ray = self.canvas.create_line(
                sun_x, sun_y,
                human_x + offset_x, human_y + offset_y,
                fill="yellow", width=2
            )
            self.radiation_rays.append(ray)

        # to animate heat tint on the human
        if not hasattr(self, "heat_step"):
            self.heat_step = 0
        self.animate_human_tint()

        # to continue animation
        self.canvas.after(300, self.animate_radiation_rays)

    def animate_human_tint(self):
        if self.heat_step > 20:
            return  # stop after full heating

        # Create a copy of the original human image for recoloring
        heated_human = self.original_human.convert("RGBA")
        pixels = heated_human.load()

        width, height = heated_human.size
        progress = int(height * (self.heat_step / 20))  # heat spreads from top down

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    if y <= progress:
                        intensity = int(255 * (y / height))
                        new_r = min(255, r + intensity)
                        new_g = max(0, g - intensity // 3)
                        new_b = max(0, b - intensity // 2)
                        pixels[x, y] = (new_r, new_g, new_b, a)

        human_img = ImageTk.PhotoImage(heated_human)
        self.images['human'] = human_img
        self.canvas.itemconfig(self.human, image=human_img)

        self.heat_step += 1
        self.canvas.after(300, self.animate_human_tint)


# ================================
# Tab 2–4: Particle Simulation (Solid, Liquid, Gas)
# ================================
class HeatSimulationTab:
    def __init__(self, parent, state="Solid"):
        self.state = state
        self.temperature = 20

        # Frame
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill="both", expand=True)

        # Title
        self.label = tk.Label(self.frame, text=f"{self.state} State Heat Simulation",
                              font=("Segoe UI", 16, "bold"),
                              fg="#ffffff", bg="#1e1e1e")
        self.label.pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(self.frame, width=700, height=400,
                                bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Temp label (define BEFORE slider to avoid error)
        self.temp_label = tk.Label(self.frame, text=f"Temperature: {self.temperature}°C",
                                   font=("Segoe UI", 12), fg="#ffffff", bg="#1e1e1e")
        self.temp_label.pack(pady=5)

        # Slider
        self.slider = ttk.Scale(self.frame, from_=0, to=100,
                                orient="horizontal",
                                command=self.update_temperature,
                                style="TScale")
        self.slider.set(self.temperature)
        self.slider.pack(pady=10, fill="x", padx=50)

        # Particles
        self.particles = []
        self.base_positions = []

        if self.state == "Solid":
            self.create_grid_particles(rows=5, cols=8, spacing=80)
        elif self.state == "Liquid":
            self.create_random_particles(count=40)
        elif self.state == "Gas":
            self.create_random_particles(count=25)

        # Animate
        self.animate()

    def create_grid_particles(self, rows, cols, spacing):
        for i in range(rows):
            for j in range(cols):
                x = 80 + j * spacing
                y = 80 + i * spacing
                particle = self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                                   fill="#44aaff", outline="")
                self.particles.append(particle)
                self.base_positions.append((x, y))

    def create_random_particles(self, count):
        for _ in range(count):
            x = random.randint(50, 650)
            y = random.randint(50, 350)
            particle = self.canvas.create_oval(x-8, y-8, x+8, y+8,
                                               fill="#44aaff", outline="")
            self.particles.append(particle)
            self.base_positions.append((x, y))

    def update_temperature(self, val):
        self.temperature = int(float(val))
        self.temp_label.config(text=f"Temperature: {self.temperature}°C")

    def animate(self):
        for idx, particle in enumerate(self.particles):
            base_x, base_y = self.base_positions[idx]

            if self.state == "Solid":
                amp = int(self.temperature / 5)
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)

            elif self.state == "Liquid":
                amp = int(self.temperature / 3)
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)

            elif self.state == "Gas":
                amp = int(self.temperature / 2 + 5)
                dx = random.randint(-amp, amp)
                dy = random.randint(-amp, amp)

            # Glow effect
            red = min(255, 50 + self.temperature * 2)
            blue = max(0, 255 - self.temperature * 2)
            color = f"#{red:02x}33{blue:02x}"

            self.canvas.move(particle, dx, dy)

            coords = self.canvas.coords(particle)
            if coords:
                x1, y1, x2, y2 = coords
                if x1 < 0 or x2 > 700 or y1 < 0 or y2 > 400:
                    self.canvas.move(particle, -dx, -dy)

            self.canvas.itemconfig(particle, fill=color)

        self.frame.after(100, self.animate)


# ================================
# Main App
# ================================
class HeatSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Heat Transfer Simulation Tool (VHTST)")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e1e1e")

        # Dark style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("Dark.TFrame", background="#1e1e1e")
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#333333", foreground="#ffffff",
                        padding=10, font=("Segoe UI", 11, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#555555")])

        style.configure("TScale",
                        background="#1e1e1e",
                        troughcolor="#333333",
                        sliderthickness=25,
                        sliderlength=25)
        style.map("TScale", background=[("active", "#444444")])

        # Notebook (tabs)
        notebook = ttk.Notebook(root, style="TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Tabs
        self.transfer_tab = HeatTransferTab(notebook)
        self.modes_tab = HeatModesTab(notebook)
        notebook.add(self.modes_tab.frame, text="Heat Transfer Modes")
        self.solid_tab = HeatSimulationTab(notebook, state="Solid")
        self.liquid_tab = HeatSimulationTab(notebook, state="Liquid")
        self.gas_tab = HeatSimulationTab(notebook, state="Gas")

        notebook.add(self.transfer_tab.frame, text="Heat Transfer (2 Objects)")
        notebook.add(self.solid_tab.frame, text="Solid")
        notebook.add(self.liquid_tab.frame, text="Liquid")
        notebook.add(self.gas_tab.frame, text="Gas")


if __name__ == "__main__":
    root = tk.Tk()
    app = HeatSimulationApp(root)
    root.mainloop()
