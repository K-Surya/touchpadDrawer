import threading
import queue
import turtle
from evdev import InputDevice, ecodes

#Touch pad device..
TOUCHPAD_PATH = "/dev/input/event" + input("Enter the touchpad IO number : ")

event_queue = queue.Queue()
drawing = False  # whether we are currently drawing (finger down)

# --- Step 1: Get touchpad coordinate ranges ---
def get_abs_ranges(dev):
    absinfo = dev.capabilities().get(ecodes.EV_ABS, [])
    ranges = {}
    for code, absinfo_data in absinfo:
        ranges[code] = (absinfo_data.min, absinfo_data.max)
    return ranges

def touchpad_listener(path, q):
    dev = InputDevice(path)
    print(f"Listening on {path} ({dev.name}) ...")

    ranges = get_abs_ranges(dev)
    print("Touchpad ranges:", ranges)

    x_range = ranges.get(ecodes.ABS_X, (0, 4000))
    y_range = ranges.get(ecodes.ABS_Y, (0, 3000))

    x, y = None, None
    finger_down = False

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
            # Finger touches down
            if event.value == 1:
                finger_down = True
                q.put(("TOUCH_DOWN",))
            # Finger lifts up
            elif event.value == 0:
                finger_down = False
                q.put(("TOUCH_UP",))

        elif event.type == ecodes.EV_ABS:
            if event.code in [ecodes.ABS_MT_POSITION_X, ecodes.ABS_X]:
                x = event.value
            elif event.code in [ecodes.ABS_MT_POSITION_Y, ecodes.ABS_Y]:
                y = event.value

            if x is not None and y is not None and finger_down:
                q.put(("MOVE", x, y, x_range, y_range))
                x, y = None, None

def update_turtle():
    global drawing
    try:
        while True:
            event = event_queue.get_nowait()

            if event[0] == "TOUCH_DOWN":
                drawing = False  # reset stroke state

            elif event[0] == "TOUCH_UP":
                drawing = False
                t.penup()

            elif event[0] == "MOVE":
                _, x, y, x_range, y_range = event

                draw_x = int((x - x_range[0]) / (x_range[1] - x_range[0]) * screen.window_width()) - screen.window_width() // 2
                draw_y = screen.window_height() // 2 - int((y - y_range[0]) / (y_range[1] - y_range[0]) * screen.window_height())

                if not drawing:
                    # First point → move without drawing
                    t.penup()
                    t.goto(draw_x, draw_y)
                    drawing = True
                else:
                    # Subsequent points → draw
                    t.pendown()
                    t.goto(draw_x, draw_y)

    except queue.Empty:
        pass

    screen.ontimer(update_turtle, 10)

# --- Step 2: Setup turtle ---
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)  # fullscreen
screen.title("Touchpad Drawing Tablet")

# Hide system mouse pointer
canvas = screen.getcanvas()
canvas.config(cursor="none")

t = turtle.Turtle()
t.speed(0)
t.pensize(2)
t.hideturtle()   # 🔥 hide the turtle arrow
t.penup()

# --- Step 3: Key controls ---
def clear_screen():
    t.clear()
    t.penup()
    print("Screen cleared")

def quit_app():
    print("Exiting...")
    screen.bye()

screen.listen()
screen.onkey(clear_screen, "c")  # press 'c' to clear
screen.onkey(quit_app, "q")      # press 'q' to quit

# --- Step 4: Start background listener ---
listener_thread = threading.Thread(
    target=touchpad_listener, args=(TOUCHPAD_PATH, event_queue), daemon=True
)
listener_thread.start()

update_turtle()
screen.mainloop()

