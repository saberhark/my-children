import time
import mouse

while True:
    time.sleep(0.3)
    print(mouse.get_position())

    if mouse.is_pressed("left"):
        break