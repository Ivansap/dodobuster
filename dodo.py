from PIL import ImageGrab, Image
from pynput import keyboard

import pyautogui
import threading
import time
import copy

x1, y1 = 738, 374
x2, y2 = 1329, 966

d = 90
space = 10

class Status:
    _exit = False
    active = False




def get_field(im):
    field_img = []
    whites = 0
    pix = im.load()   
    for i in range(6):
        row = []
        for j in range(6):
            x1 = (space+d)*j
            y1 = (space+d)*i
            color = pix[x1+d/2, y1+5]
            if color == (255, 255, 255):
                whites += 1
            row.append(color)
        field_img.append(row)
    if whites > 5:
        raise Exception
    return field_img



def game_field(img_field):
    s = []
    field = []
    for line in img_field:
        row = []
        for pixel in line:
            if pixel not in s:
                s.append(pixel)
            row.append(s.index(pixel))

        field.append(row)
    return field


def show_field(field):
    img = Image.new('RGB', (90*6, 90*6))
    ofx = 90
    ofy = 90
    for i in range(6):
        ofy = 90*i
        ofx = 0
    for j in range(6):
        ofx = 90*j
        img.paste(field[i][j], (ofx, ofy))
    img.show()



def change(item1, item2):
    x = (space+d)*item1[1]+x1+45
    y = (space+d)*item1[0]+y1+45
    pyautogui.click(x, y)
    # time.sleep(0.1)

    x = (space+d)*item2[1]+x1+45
    y = (space+d)*item2[0]+y1+45
    pyautogui.click(x, y)
    # time.sleep(0.3)


def game(field):
    def change_places(tmp_field, item1, item2):
        try:
            if tmp_field[item1[0]][item1[1]] == tmp_field[item2[0]][item2[1]]:
                return False
            tmp_field[item1[0]][item1[1]], tmp_field[item2[0]][item2[1]] = tmp_field[item2[0]][item2[1]], tmp_field[item1[0]][item1[1]]
        except:
            return False
        return True

    def get_points(tmp_field):
        arr = tmp_field
        max_lines = []

        for i in range(6):
            line_length = 1
            line_length2 = 1
            tmp = None
            tmp2 = None

            for j in range(6):
                if tmp is None:
                    tmp = arr[i][j]
                    line_length = 1
                else:
                    if arr[i][j] == tmp:
                        line_length += 1
                    else:
                        tmp = arr[i][j]
                        if line_length > 2:
                            max_lines.append(line_length)
                        line_length = 1

                if tmp2 is None:
                    tmp2 = arr[j][i]
                    line_length2 = 1
                else:
                    if arr[j][i] == tmp2:
                        line_length2 += 1
                    else:
                        tmp2 = arr[j][i]
                        if line_length2 > 2:
                            max_lines.append(line_length2)
                        line_length2 = 1

            if line_length2 > 2:
                max_lines.append(line_length2)
            if line_length > 2:
                max_lines.append(line_length)

        points = sum([p*10 for p in max_lines])

        if points:
            return points
        return 0
         
    step = 0, 0
    change_step = 0, 0
    max_points = 0

    for i in range(6):
        for j in range(6):
            
            for y_add in range(2):
                for x_add in range(2):
                    if x_add == y_add or (i+y_add > 6) or (j+x_add > 6):
                        continue
                    tmp_field = copy.deepcopy(field)
                    if change_places(tmp_field, (i, j), (i+y_add, j+x_add)):
                        points = get_points(tmp_field)
                        if max_points <= points:
                            max_points = points
                            step = i,j
                            change_step = i+y_add, j+x_add
                            # change(step, change_step)
 
    if max_points:
        change(step, change_step)

def onKeyPress(key):
    try:
        k = key.char
    except Exception:
        k = key.name

    if (k == "z"):
        if Status.active:
            print('Go go go...')
        Status.active = not Status.active

    elif (k == "x"):
        Status._exit = not Status._exit

#show_field(field)
def main():
    listenerThread = keyboard.Listener(on_press = onKeyPress)
    listenerThread.start()

    while(not Status._exit):
        if (not Status.active):
            continue


        if (not Status.active or Status._exit):
            break
        pyautogui.move(0, 0)

        im = ImageGrab.grab()
        im = im.crop((x1, y1, x2, y2))
        try:
            field = get_field(im)
            f = game_field(field)
            game(f)
        except:
            print('Found Whites!')
            Status.active = not Status.active

    keyboard.Listener.stop(listenerThread)
    print("Stopped listerning")


main()