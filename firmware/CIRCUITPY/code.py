import board
import displayio
import busio
import digitalio
from adafruit_st7735r import ST7735R
from fourwire import FourWire
from adafruit_display_text import label
import terminalio

print("Running!")

# --- Setup Display ---
displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
tft_cs = board.GP20
dc = board.GP22
reset = board.GP26
display_bus = FourWire(spi, command=dc, chip_select=tft_cs, reset=reset)
display = ST7735R(display_bus, width=128, height=160, colstart=0, rowstart=0, bgr=True)
display.rotation = 270
splash = displayio.Group()
display.root_group = splash

# --- Background ---
color_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black background
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# --- Text Label ---
text_area = label.Label(terminalio.FONT, text="Waiting for press...", color=0xFFFFFF)
text_area.x = 10
text_area.y = 60


# --- Setup Buttons ---
button_up = digitalio.DigitalInOut(board.GP12)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP  # Use internal pull-up

button_left = digitalio.DigitalInOut(board.GP13)
button_left.direction = digitalio.Direction.INPUT
button_left.pull = digitalio.Pull.UP  # Use internal pull-up

button_down = digitalio.DigitalInOut(board.GP14)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP  # Use internal pull-up

button_right = digitalio.DigitalInOut(board.GP15)
button_right.direction = digitalio.Direction.INPUT
button_right.pull = digitalio.Pull.UP  # Use internal pull-up

button_a = digitalio.DigitalInOut(board.GP5)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP  # Use internal pull-up

button_b = digitalio.DigitalInOut(board.GP6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP  # Use internal pull-up

desk_background = displayio.OnDiskBitmap("assets/Desk-BG.bmp")
desk_bg_sprite = displayio.TileGrid(desk_background, pixel_shader=desk_background.pixel_shader)

splash.append(desk_bg_sprite)
splash.append(text_area)

# --- Main Loop ---
while True:
    if not button_up.value:  # Button is pressed (active low)
        text_area.text = "Up button pressed!"
    elif not button_left.value:
        text_area.text = "Left button pressed!"
    elif not button_down.value:
        text_area.text = "Down button pressed!"
    elif not button_right.value:
        text_area.text = "Right button pressed!"
    elif not button_a.value:
        text_area.text = "Button A pressed!"
    elif not button_b.value:
        text_area.text = "Button B pressed!"
    else:
        text_area.text = "Waiting for press..."
