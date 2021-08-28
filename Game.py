from tkinter import *
import random
import logging
import time

INITIAL_COORDS_XY_1 = [(140, 100), (120, 100), (100, 100)]
INITIAL_COORDS_XY_2 = [(160, 120), (140, 120), (120, 120)]
SPEED = 100


class Snake:
    def __init__(self):
        self.segments = []
        self.initialize_snake()
        self.head = self.segments[0]
        self.current_direction = "right"
        self.direction = "None"

    def __del__(self):
        class_name = self.__class__.__name__
        print(f"{class_name} Deleted ! ")

    def initialize_snake(self):
        for i in range(0, 3):
            rect = canvas.create_rectangle(INITIAL_COORDS_XY_1[i], INITIAL_COORDS_XY_2[i], width=2, fill="GREEN")
            self.segments.append(rect)

    def left_direction(self, event):
        head_coords = canvas.coords(self.segments[0])
        if self.current_direction != "right":
            head_coords[0] -= 20
            head_coords[2] -= 20
            canvas.after_cancel(self.direction)
            self.update_move()
            canvas.coords(self.segments[0], head_coords[0], head_coords[1], head_coords[2], head_coords[3])
            self.direction = canvas.after(SPEED, lambda: self.left_direction(event))
            self.current_direction = "left"

    def right_direction(self, event):
        head_coords = canvas.coords(self.segments[0])
        if self.current_direction != "left":
            head_coords[0] += 20
            head_coords[2] += 20
            canvas.after_cancel(self.direction)
            self.update_move()
            canvas.coords(self.segments[0], head_coords[0], head_coords[1], head_coords[2], head_coords[3])
            self.direction = canvas.after(SPEED, lambda: self.right_direction(event))
            self.current_direction = "right"

    def up_direction(self, event):
        head_coords = canvas.coords(self.segments[0])
        if self.current_direction != "down":
            head_coords[1] -= 20
            head_coords[3] -= 20
            canvas.after_cancel(self.direction)
            self.update_move()
            canvas.coords(self.segments[0], head_coords[0], head_coords[1], head_coords[2], head_coords[3])
            self.direction = canvas.after(SPEED, lambda: self.up_direction(event))
            self.current_direction = "up"

    def down_direction(self, event):
        head_coords = canvas.coords(self.segments[0])
        if self.current_direction != "up":
            head_coords[1] += 20
            head_coords[3] += 20
            canvas.after_cancel(self.direction)
            self.update_move()
            canvas.coords(self.segments[0], head_coords[0], head_coords[1], head_coords[2], head_coords[3])
            self.direction = canvas.after(SPEED, lambda: self.down_direction(event))
            self.current_direction = "down"

    def update_move(self):
        # self.snake_collision()
        self.outside_borders()
        self.apple_collision()
        for i in range(len(self.segments) - 1, 0, -1):
            new_coords = canvas.coords(self.segments[i - 1])
            canvas.coords(self.segments[i], new_coords[0], new_coords[1], new_coords[2], new_coords[3])

    def outside_borders(self):
        head_coords = canvas.coords(self.segments[0])
        if head_coords[0] > 600 or head_coords[0] < 0:
            root.quit()
        elif head_coords[1] > 600 or head_coords[1] < 100:
            root.quit()
        elif head_coords[2] > 600 or head_coords[2] < 0:
            root.quit()
        elif head_coords[3] > 600 or head_coords[3] < 100:
            root.quit()
        else:
            print(head_coords)
            self.snake_collision()

    def new_segment(self):
        new_xy = canvas.coords(self.segments[-1])
        rect = canvas.create_rectangle(new_xy[0], new_xy[1]+20, new_xy[2], new_xy[3]+20, width=2, fill="GREEN")
        self.segments.append(rect)

    def apple_collision(self):
        head_coords = canvas.coords(self.segments[0])

        if (apple.xy1[0] <= head_coords[0] <= apple.xy2[0]) and \
                (apple.xy1[1] <= head_coords[1] <= apple.xy2[1]) \
                or (apple.xy1[0] <= head_coords[2] <= apple.xy2[0]) and \
                (apple.xy1[1] <= head_coords[3] <= apple.xy2[1]):
            print(f"Apple Collision \nHEAD : {head_coords}\nAPPLE{apple.xy1, apple.xy2}")
            self.new_segment()
            apple.random_spawn()
            score.update_score()

    def snake_collision(self):
        head_coords = canvas.coords(self.segments[0])
        for segment in self.segments[1:]:
            segment_coords = canvas.coords(segment)
            print(f"{segment}\nCOORDS : {segment_coords}\nHEAD : {head_coords}")
            if ((segment_coords[0] == head_coords[0]) and (segment_coords[1] == head_coords[1])) \
                    or ((segment_coords[2] == head_coords[2]) and (segment_coords[3] == head_coords[3])):
                print("Snake Self Collision")
                root.quit()
                break


class Apple:

    def __init__(self):
        self.xy1 = [0, 0]
        self.xy2 = [0, 0]
        self.apple = 'None'
        self.initialize_apple()

    def initialize_apple(self):
        self.apple = canvas.create_rectangle(self.xy1[0], self.xy1[1], self.xy2[0], self.xy2[1], width=2, fill="RED")
        self.random_spawn()

    def random_spawn(self):
        random_x = random.randint(20, 116) * 5
        random_y = random.randint(20, 96) * 5
        self.xy1 = [random_x, random_y]
        self.xy2 = [random_x + 20, random_y + 20]
        canvas.coords(self.apple, self.xy1[0], self.xy1[1], self.xy2[0], self.xy2[1])


class Score:

    def __init__(self):
        self.score = 0
        self.score_text = 'None'
        self.initialize_score()

    def initialize_score(self):
        self.score_text = canvas.create_text(149, 49, fill="WHITE", text=f"Score : {self.score}", font=("Courier", 20))
        canvas.create_line(0, 98, 600, 98, width=2, fill="WHITE")

    def update_score(self):
        self.score += 1
        canvas.itemconfig(self.score_text, text=f"Score : {self.score}")


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x600")
    root.title("Snake Game")
    root.resizable(width=False, height=False)

    canvas = Canvas(root, width=600, height=600, bg="black")
    canvas.pack(fill="both", expand=True)

    score = Score()
    snake = Snake()
    apple = Apple()

    canvas.focus_set()
    canvas.bind('q', snake.left_direction)
    canvas.bind('d', snake.right_direction)
    canvas.bind('z', snake.up_direction)
    canvas.bind('s', snake.down_direction)

    root.mainloop()
