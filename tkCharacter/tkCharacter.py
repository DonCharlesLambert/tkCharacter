from tkinter import PhotoImage
import time

'''TODO
- Split up animation speed and movement speed
- Split self.direction into facing and current animation
- stop will stop depending on facing
- set stop animation with kwargs?
- animate will know nothing about facing
- future future: jumping
'''


class TkCharacter:
    animation_list = {
        "up"    : ["9", "10", "11"],
        "down"  : ["0", "1", "2"],
        "right" : ["6", "7", "8"],
        "left"  : ["3", "4", "5"],

        "left stance"  : ["0"],
        "right stance" : ["1"],
    }
    animation_number = 0

    def __init__(self, canvas, x, y, directory, **kwargs):
        self.sprite = PhotoImage(file=directory + r"\0.png")
        self.canvas_sprite = canvas.create_image(x, y, image=self.sprite)
        self.canvas = canvas
        self.image_dir = directory
        self.speed = 10
        self.move_interval = time.time()
        self.action_interval = time.time()
        self.direction = "stance"

        for key in kwargs.keys():
            if key == "speed":
                self.speed = kwargs[key]
            else:
                self.animation_list[key] = kwargs[key]

    def move(self, direction):
        self.direction = direction
        if direction == "left":
            self.canvas.move(self.canvas_sprite, -self.speed, 0)
        elif direction == "right":
            self.canvas.move(self.canvas_sprite, self.speed, 0)
        elif direction == "up":
            self.canvas.move(self.canvas_sprite, 0, -self.speed)
        elif direction == "down":
            self.canvas.move(self.canvas_sprite, 0, self.speed)

        if time.time() - self.move_interval > 0.1:
            self.move_interval = time.time()
            self.animate()

    def action(self, action):
        if time.time() - self.action_interval > 1:
            if self.direction != action:
                self.direction = action
                self.animation_number = 0
            if time.time() - self.move_interval > 0.1:
                self.move_interval = time.time()
                self.animate()
        else:
            if time.time() - self.move_interval > 0.3:
                self.stop()

    def pos(self):
        return self.canvas.coords(self.canvas_sprite)

    def stop(self):
        self.direction = "stance"
        self.animation_number = 0
        self.animate()

    def animate(self):
        current_animation = self.animation_list[self.direction]
        self.sprite = PhotoImage(file=self.image_dir + r'\\' + current_animation[self.animation_number] + ".png")
        self.end_of_animation(current_animation)
        self.animation_number = (self.animation_number + 1) % len(current_animation)
        self.canvas.itemconfig(self.canvas_sprite, image=self.sprite)

    def end_of_animation(self, current_animation):
        if self.animation_number == len(current_animation) - 1:
            self.action_interval = time.time()
