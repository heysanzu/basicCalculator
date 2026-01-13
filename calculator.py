import turtle
import tkinter as tk

# Configuration
FONT = ("Comic Sans MS", 18, "normal")
DISPLAY_FONT = ("Comic Sans MS", 25, "bold")
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Screen
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("#f0f0f0")  
screen.title("Calculator")
screen.tracer(0)

# Icon
try:
    root = screen.getcanvas().winfo_toplevel()
    img = tk.PhotoImage(file="icon.png")
    root.iconphoto(True, img)
except:
    pass

# Turtles
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()

display_pen = turtle.Turtle()
display_pen.hideturtle()
display_pen.penup()

# State & Data
calc_input = ""
buttons = []
labels = [
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "DEL", "="]
]

def draw_rect(x, y, w, h, color="white"):
    drawer.goto(x - w/2, y - h/2)
    drawer.fillcolor(color)
    drawer.begin_fill()
    drawer.pendown()
    for _ in range(2):
        drawer.forward(w)
        drawer.left(90)
        drawer.forward(h)
        drawer.left(90)
    drawer.penup()
    drawer.end_fill()

def build_ui():
    drawer.clear()
    buttons.clear()
    
    # Draw Display Box
    draw_rect(0, 200, 320, 70, "white")
    
    # Draw Grid
    start_x, start_y = -120, 100
    for r, row in enumerate(labels):
        for c, label in enumerate(row):
            x = start_x + (c * 80)
            y = start_y - (r * 70)
            
            # Color coding for operators
            btn_color = "#ffffff" if label.isdigit() or label == "." else "#ff00dd" if label == "=" else "#73ff01"
            
            draw_rect(x, y, 70, 60, btn_color)
            drawer.goto(x, y - 15)
            drawer.color("black")
            drawer.write(label, align="center", font=FONT)
            
            # Store hitboxes: (xmin, xmax, ymin, ymax, label)
            buttons.append((x-35, x+35, y-30, y+30, label))
    screen.update()

def update_display():
    display_pen.clear()
    display_pen.goto(150, 182) # Right-aligned in the box
    
    text_to_show = calc_input if calc_input != "" else "0"
    
    if len(text_to_show) > 15:
        text_to_show = "..." + text_to_show[-12:]
        
    display_pen.write(text_to_show, align="right", font=DISPLAY_FONT)
    screen.update()

def handle_click(x, y):
    global calc_input
    
    for x_min, x_max, y_min, y_max, label in buttons:
        if x_min < x < x_max and y_min < y < y_max:
            if label == "C":
                calc_input = ""
            elif label == "DEL":
                calc_input = calc_input[:-1]
            elif label == "=":
                try:
                    # eval() handles the math
                    result = eval(calc_input)
                    if isinstance(result, float):
                        calc_input = format(result, '.10g')
                    else:
                        calc_input = str(result)
                except Exception:
                    calc_input = "Error"
            else:
                if len(calc_input) < 20:
                    calc_input += label
            
            update_display()
            break

# Initialization
build_ui()
update_display()

screen.onclick(handle_click)
screen.listen()
screen.mainloop()
