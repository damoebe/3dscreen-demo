import cv2
import time
from tkinter import *

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

capture = cv2.VideoCapture(0)


# this project was coded by a vibe coder any criticizers can go fuck themselves
# don't use shitty camera like me, or it will be laggy
class CubiWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("cubi")
        self.state("zoomed")
        self.after(0, )
        self.update()


root = CubiWindow()

w = root.winfo_width()
h = root.winfo_height()

canvas = Canvas(root, width=w, height=h)
canvas.config(background="gray")

cubi_size = 200


def get_square_for(x, y, size):
    return [x - size, y + size, x + size, y + size, x + size, y - size, x - size, y - size]


X_pos = 0
Y_pos = 0

X_pos_no_lim = 0
Y_pos_no_lim = 0

eclapsed_time_list = [1]

while True:
    # fps mesure
    start_time = time.time()

    ret, frame = capture.read()
    # face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 7)

    # for stats
    detected_faces = len(faces)

    # very important for anti shaking (to prevent neck detection)
    if len(faces) > 1:
        if faces[0][1] > faces[1][1]:
            faces = [faces[1]]
        else:
            faces = [faces[0]]

    for (x, y, width, height) in faces:
        anti_shaking_factor = 0.4

        X_pos = X_pos + anti_shaking_factor * (x - ((frame.shape[1]) / 2) - X_pos)
        Y_pos = Y_pos + anti_shaking_factor * (y - ((frame.shape[0]) / 2) - Y_pos)
        X_pos_no_lim = X_pos + anti_shaking_factor * (x - ((frame.shape[1]) / 2) - X_pos)
        Y_pos_no_lim = Y_pos + anti_shaking_factor * (y - ((frame.shape[0]) / 2) - Y_pos)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 1)
        cv2.putText(
            frame,
            "w=" + str(width) + " h=" + str(height),
            (x, y + height + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,  # font scale
            (255, 255, 255),  # color (BGR)
            1,  # thickness
            cv2.LINE_AA
        )

    cv2.imshow("test", frame)

    # 3d cube

    # limit
    X_limit = 120
    Y_limit = 120
    if X_pos > X_limit:
        X_pos = X_limit

    if X_pos < -X_limit:
        X_pos = -X_limit

    if Y_pos > Y_limit:
        Y_pos = Y_limit

    if Y_pos < -Y_limit:
        Y_pos = -Y_limit

    X_pos *= 0.5
    Y_pos *= 0.5

    # clear
    canvas.delete("all")

    back_size = cubi_size / 2 - 15

    # all points for cube
    down_points = [w / 2 + back_size - X_pos, h / 2 + back_size + Y_pos, w / 2 + 100, h / 2 + 100, w / 2 - 100,
                   h / 2 + 100,
                   w / 2 - back_size - X_pos, h / 2 + back_size + Y_pos]
    up_points = [w / 2 - back_size - X_pos, h / 2 - back_size + Y_pos, w / 2 - 100, h / 2 - 100, w / 2 + 100,
                 h / 2 - 100,
                 w / 2 + back_size - X_pos, h / 2 - back_size + Y_pos]
    left_points = [w / 2 - back_size - X_pos, h / 2 - back_size + Y_pos, w / 2 - 100, h / 2 - 100, w / 2 - 100,
                   h / 2 + 100,
                   w / 2 - back_size - X_pos, h / 2 + back_size + Y_pos]
    right_points = [w / 2 + back_size - X_pos, h / 2 + back_size + Y_pos, w / 2 + 100, h / 2 + 100, w / 2 + 100,
                    h / 2 - 100,
                    w / 2 + back_size - X_pos, h / 2 - back_size + Y_pos]

    canvas.create_polygon(down_points, fill="orange", outline="black")
    canvas.create_polygon(up_points, fill="orange", outline="black")

    # no overlapping
    if w / 2 - back_size - X_pos <= w / 2 - 100:
        canvas.create_polygon(left_points, fill="green", outline="black")

    if w / 2 + back_size - X_pos >= w / 2 + 100:
        canvas.create_polygon(right_points, fill="green", outline="black")

    # repaint
    canvas.create_polygon(get_square_for(w / 2, h / 2, cubi_size / 2), fill='blue', outline="black")

    wall_size = 300
    move_speed = 0.8

    # background effect
    canvas.create_polygon(
        get_square_for(w / 2 - (X_pos_no_lim * move_speed), h / 2 + (Y_pos_no_lim * move_speed), wall_size),
        outline="black", fill="")

    canvas.create_line(w / 2 - (X_pos_no_lim * move_speed) - wall_size, h / 2 + (Y_pos_no_lim * move_speed) - wall_size,
                       0, 0)
    canvas.create_line(w / 2 - (X_pos_no_lim * move_speed) - wall_size, h / 2 + (Y_pos_no_lim * move_speed) + wall_size,
                       0, h)
    canvas.create_line(w / 2 - (X_pos_no_lim * move_speed) + wall_size, h / 2 + (Y_pos_no_lim * move_speed) + wall_size,
                       w, h)
    canvas.create_line(w / 2 - (X_pos_no_lim * move_speed) + wall_size, h / 2 + (Y_pos_no_lim * move_speed) - wall_size,
                       w, 0)

    avg_eclapsed_time = 0
    for num in eclapsed_time_list:
        avg_eclapsed_time += num

    avg_eclapsed_time /= len(eclapsed_time_list)

    # hacker stats : )
    canvas.create_text(150, 80, text="detected faces: " + str(detected_faces) + "\n"
                                                        "X-Pos: " + str(X_pos) + "\n"
                                                        "Y-Pos: " + str(Y_pos) + "\n"
                                                        "x-no-lim: " + str(X_pos_no_lim) + "\n"
                                                        "y-no-lim: " + str(Y_pos_no_lim) + "\n"
                                                        "fps: " + str(int(1/avg_eclapsed_time)) + "\n"
                       , fill="red",
                       font='Helvetica 12 bold')

    canvas.pack()
    root.update()

    eclapsed_time_list.append(time.time() - start_time)

    if len(eclapsed_time_list) == 50:
        eclapsed_time_list.pop(0)

    # e is escape
    if cv2.waitKey(1) == ord("e"):
        break

capture.release()
