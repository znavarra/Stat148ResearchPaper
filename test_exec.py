import pygame
import pandas as pd
from pygame.locals import *
import random
import math
import pandas as pd
import sys
import os

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, filename)

info_path = resource_path('info.csv')
score_path = resource_path('scores.csv')
time_path = resource_path('times.csv')

width, height = 1000, 650
screen = pygame.display.set_mode((width, height))
config_data = {}

def user_interface():
    global config_data
    pygame.init()

    base_font = pygame.font.Font(None, 35)
    label_font = pygame.font.Font(None, 50)
    sex_at_birth = pygame.font.Font(None, 40)
    corrective_lenses = pygame.font.Font(None, 30)
    done_font = pygame.font.Font(None, 100)

    color_active = (0, 128, 128)
    color_passive = (180, 200, 210)
    indigo = (2, 52, 63)
    skin = (240, 237, 204)

    screen.fill(skin)

    done = pygame.Rect(350, 400, 300, 100)
    done_text = done_font.render("Done", True, skin)

    input_fields = [
        {"label": "Name:", "rect": pygame.Rect(175, 50, 280, 50), "text": "", "active": False},
        {"label": "Year:", "rect": pygame.Rect(175, 125, 280, 50), "text": "", "active": False},
        {"label": "Course:", "rect": pygame.Rect(175, 200, 280, 50), "text": "", "active": False},
        {"label": "Email:", "rect": pygame.Rect(175, 275, 280, 50), "text": "", "active": False},
        {"label": "GCash:", "rect": pygame.Rect(650, 50, 280, 50), "text": "", "active": False},
        {"label": "Sex at Birth:", "rect": pygame.Rect(650, 125, 280, 50), "text": "", "active": False},
        {"label": "Age:", "rect": pygame.Rect(650, 200, 280, 50), "text": "", "active": False},
        {"label": "Wears Corrective Lenses:", "rect": pygame.Rect(650, 275, 280, 50), "text": "", "active": False}
    ]

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for field in input_fields:
                    if field["rect"].collidepoint(event.pos):
                        for f in input_fields:
                            f["active"] = False
                        field["active"] = True
                        break
                else:
                    for field in input_fields:
                        field["active"] = False

                if done.collidepoint(event.pos):
                    data = {}
                    file = pd.read_csv(info_path, header=0)
                    for fields in input_fields:
                        data[fields["label"]] = fields["text"]

                        if fields["label"] == "Name:":
                            name = fields["text"]
                        if fields["label"] == "Email:":
                            email = fields["text"]

                    unique_id = name + email
                    data["unique_id"] = unique_id
                    data["score"] = 0

                    config_data = {
                        "unique_id": unique_id
                    }

                    new_row = pd.DataFrame([data])
                    file = pd.concat([file, new_row], ignore_index=True)
                    file.to_csv(info_path, index=False)

                    return landing_page()  # Transition to landing_page
            
            if event.type == pygame.KEYDOWN:
                for field in input_fields:
                    if field["active"]:
                        if event.key == pygame.K_BACKSPACE:
                            field["text"] = field["text"][:-1]
                        else:
                            field["text"] += event.unicode
        
        pygame.draw.rect(screen, indigo, done)
        screen.blit(done_text, (done.x + 60, done.y + 17))

        for field in input_fields:
            pygame.draw.rect(screen, color_active if field["active"] else color_passive, field["rect"])

            if field["label"] == "Sex at Birth:":
                label_width, _ = sex_at_birth.size(field["label"])
                label_x = field["rect"].x - (label_width + 10)

                label_surface = sex_at_birth.render(field["label"], False, indigo)
                screen.blit(label_surface, (label_x, field["rect"].y + 10))

                input_surface = base_font.render(field["text"], True, (255, 255, 255))
                screen.blit(input_surface, (field["rect"].x + 5, field["rect"].y + 10))

                field["rect"].w = max(280, input_surface.get_width() + 10)

            elif field["label"] == "Wears Corrective Lenses:":
                label_width1, _ = corrective_lenses.size("Wears Corrective:")
                label_width2, _ = corrective_lenses.size("Lenses:")
                label_x1 = field["rect"].x - (label_width1 + 5)
                label_x2 = field["rect"].x - (label_width2 + 5)

                label_surface1 = corrective_lenses.render("Wears Corrective", False, indigo)
                label_surface2 = corrective_lenses.render("Lenses:", False, indigo)

                screen.blit(label_surface1, (field["rect"].x - (label_width1 + 5), field["rect"].y + 5))
                screen.blit(label_surface2, (field["rect"].x - (label_width2 + 10), field["rect"].y + 25))

                input_surface = base_font.render(field["text"], True, (255, 255, 255))
                screen.blit(input_surface, (field["rect"].x + 5, field["rect"].y + 10))

                field["rect"].w = max(280, input_surface.get_width() + 10)

            elif field["label"] not in ["Wears Corrective Lenses:", "Sex at Birth:"]:
                label_width, _ = label_font.size(field["label"])
                label_x = field["rect"].x - (label_width + 10)
                label_surface = label_font.render(field["label"], False, indigo)
                screen.blit(label_surface, (label_x, field["rect"].y + 5))
                
                input_surface = base_font.render(field["text"], True, (255, 255, 255))
                screen.blit(input_surface, (field["rect"].x + 5, field["rect"].y + 12.5))

                field["rect"].w = max(280, input_surface.get_width() + 10)

        for field in input_fields:
            guide = {
                "Year:": "e.g. 1st, 2nd, etc.",
                "Course:": "e.g. BS Statistics",
                "GCash:": "Optional",
                "Sex at Birth:": "Male or Female",
                "Wears Corrective Lenses:": "Yes or No"
            }
            if field["text"] == '' and field["label"] in ('Year:', 'Course:', 'GCash:', 'Sex at Birth:', 'Wears Corrective Lenses:'):
                input_surface = base_font.render(guide[field["label"]], True, skin)
                screen.blit(input_surface, (field["rect"].x + 5, field["rect"].y + 12.5))

        pygame.display.flip()

    pygame.quit()
    return None

def landing_page():
    font = pygame.font.SysFont(None, 70)
    blue = (0, 0, 255)
    white = (250, 250, 250)
    indigo = (2, 52, 63)
    skin = (240, 237, 204)

    screen.fill(skin)

    choice1_rect = Rect(200, 50, 200, 100)
    pygame.draw.rect(screen, indigo, choice1_rect)
    choice1_text = "1"
    choice1_img = font.render(choice1_text, True, skin)
    screen.blit(choice1_img, (285, 75))

    choice2_rect = Rect(600, 50, 200, 100)
    pygame.draw.rect(screen, indigo, choice2_rect)
    choice2_text = "2"
    choice2_img = font.render(choice2_text, True, skin)
    screen.blit(choice2_img, (685, 75))

    choice3_rect = Rect(200, 200, 200, 100)
    pygame.draw.rect(screen, indigo, choice3_rect)
    choice3_text = "3"
    choice3_img = font.render(choice3_text, True, skin)
    screen.blit(choice3_img, (285, 225))

    choice4_rect = Rect(600, 200, 200, 100)
    pygame.draw.rect(screen, indigo, choice4_rect)
    choice4_text = "4"
    choice4_img = font.render(choice4_text, True, skin)
    screen.blit(choice4_img, (685, 225))

    choice5_rect = Rect(200, 350, 200, 100)
    pygame.draw.rect(screen, indigo, choice5_rect)
    choice5_text = "5"
    choice5_img = font.render(choice5_text, True, skin)
    screen.blit(choice5_img, (285, 375))

    choice6_rect = Rect(600, 350, 200, 100)
    pygame.draw.rect(screen, indigo, choice6_rect)
    choice6_text = "6"
    choice6_img = font.render(choice6_text, True, skin)
    screen.blit(choice6_img, (685, 375))

    choice7_rect = Rect(200, 500, 200, 100)
    pygame.draw.rect(screen, indigo, choice7_rect)
    choice7_text = "7"
    choice7_img = font.render(choice7_text, True, skin)
    screen.blit(choice7_img, (285, 525))

    choice8_rect = Rect(600, 500, 200, 100)
    pygame.draw.rect(screen, indigo, choice8_rect)
    choice8_text = "8"
    choice8_img = font.render(choice8_text, True, skin)
    screen.blit(choice8_img, (685, 525))

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if choice1_rect.collidepoint(pos):
                    config_data["treatment"] = 1
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 1:
                        return hexes()

                if choice2_rect.collidepoint(pos):
                    config_data["treatment"] = 2
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 2:
                        return rectangles() 
                
                if choice3_rect.collidepoint(pos):
                    config_data["treatment"] = 3
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 3:
                        return larger_hexes() 
                
                if choice4_rect.collidepoint(pos):
                    config_data["treatment"] = 4
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 4:
                        return larger_rectangles() 
                    
                if choice5_rect.collidepoint(pos):
                    config_data["treatment"] = 5
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 5:
                        return hexes_varying_colors()
                    
                if choice6_rect.collidepoint(pos):
                    config_data["treatment"] = 6
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 6:
                        return rectangles_varying_colors()

                if choice7_rect.collidepoint(pos):
                    config_data["treatment"] = 7
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 7:
                        return larger_hexes_varying_colors()
                    
                if choice8_rect.collidepoint(pos):
                    config_data["treatment"] = 8
                    #result = hexes()
                    result = config_data["treatment"]
                    if result == 8:
                        return larger_rectangles_varying_colors()

        pygame.display.update()

    pygame.quit()
    return None

def hexes():

    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (250,250,250)#(0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    hexes = {}
    clicked = {}
    sample = []
    r = 50
    count = 0
    game_over = False
    scored = 0
    order = {}
    clicks = 0
    correct = 0
    strike = 0
    ready_click = False
    next_round_state = False

    for k in range(5):
        
        if k%2 == 1:
            x = 187.5
            z = 8
        else:
            x = 142.5
            z = 9
        
        for j in range(z):
            array = [
                (
                    round(x + 90*j + r * math.cos(math.pi / 3 * i - math.pi / 2),1),
                    round(100 + 77 * k + r * math.sin(math.pi / 3 * i - math.pi / 2),1)
                )
                for i in range(6)
            ]

            hexes[count] = array
            clicked[count] = False
            count += 1



    def generate_polygons(num): 
        
        nonlocal sample, order, clicks, correct

        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,43), num)

        label = 1
        for samp in sample: 
            pygame.draw.polygon(screen, blue, hexes[samp]) #producing tiles
            
            order[samp] = label #producing tile numbers
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in hexes[samp]]) / len(hexes[samp])
            shape_y = sum([point[1] for point in hexes[samp]]) / len(hexes[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, green)
            screen.blit(label_img, (label_x, label_y+2))
            clicked[samp] = False
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, green)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        print(duration)
        time.append(duration)
        
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                #run = False
                number = 16
                #runpy.run_path("user interface.py")
                #run = False

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,blue,hexes[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, hexes[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,hexes[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,hexes[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, green)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
        
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def rectangles():

    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (250,250,250)#(0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    hexes = {}
    clicked = {}
    order = {}
    sample = []
    scored = 0

    start_x = 99.5
    start_y = 53.5
    length = 75
    gap = 81.2

    rectangles = {}

    j = 0
    for k in range(5):
        for i in range(10):
            array = [
                (start_x + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + length + gap*k),
                (start_x + gap*i, start_y + length + gap*k)
            ]

            rectangles[j] = array
            j += 1



    def generate_polygons(number):
        nonlocal sample, order, clicks, correct
        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,50), number)

        label = 1
        for samp in sample:
            pygame.draw.polygon(screen,blue,rectangles[samp])
            order[samp] = label
            clicked[samp] = False
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in rectangles[samp]]) / len(rectangles[samp])
            shape_y = sum([point[1] for point in rectangles[samp]]) / len(rectangles[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, green)
            screen.blit(label_img, (label_x, label_y+2))
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, green)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        print(duration)
        time.append(duration)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,blue,rectangles[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, rectangles[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,rectangles[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,rectangles[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, green)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):

                    return user_interface()

        pygame.display.update()

    return user_interface()

def larger_hexes():
    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (250,250,250)#(0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)


    hexes = {}
    clicked = {}
    order = {}
    sample = []
    scored = 0
    r = 60
    count = 0

    for k in range(4):
        
        if k%2 == 1:
            x = 172.5 * 1.2
            z = 7
        else:
            x = 127.5 * 1.2
            z = 7
        
        for j in range(z):
            array = [
                (
                    round(x + 108*j + r * math.cos(math.pi / 3 * i - math.pi / 2),1),
                    round(113.5 + 92.4 * k + r * math.sin(math.pi / 3 * i - math.pi / 2),1)
                )
                for i in range(6)
            ]

            hexes[count] = array
            clicked[count] = False
            count += 1


    def generate_polygons(num): 
        
        nonlocal sample, order, clicks, correct

        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,28), num)

        label = 1
        for samp in sample: 
            pygame.draw.polygon(screen, blue, hexes[samp]) #producing tiles
            
            order[samp] = label #producing tile numbers
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in hexes[samp]]) / len(hexes[samp])
            shape_y = sum([point[1] for point in hexes[samp]]) / len(hexes[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, green)
            screen.blit(label_img, (label_x, label_y+2))
            clicked[samp] = False
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, green)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,blue,hexes[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, hexes[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,hexes[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,hexes[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, green)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def larger_rectangles():
    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (250,250,250)#(0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    hexes = {}
    clicked = {}
    order = {}
    sample = []
    scored = 0

    start_x = 100
    start_y = 55.5
    length = 75*1.25
    gap = 81.2*1.25

    rectangles = {}

    j = 0
    for k in range(4):
        for i in range(8):
            array = [
                (start_x + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + length + gap*k),
                (start_x + gap*i, start_y + length + gap*k)
            ]

            rectangles[j] = array
            j += 1



    def generate_polygons(number):
        nonlocal sample, order, clicks, correct
        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,32), number)

        label = 1
        for samp in sample:
            pygame.draw.polygon(screen,blue,rectangles[samp])
            order[samp] = label
            clicked[samp] = False
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in rectangles[samp]]) / len(rectangles[samp])
            shape_y = sum([point[1] for point in rectangles[samp]]) / len(rectangles[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, green)
            screen.blit(label_img, (label_x, label_y+2))
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, green)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,blue,rectangles[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, rectangles[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,rectangles[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,rectangles[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()
                            print(clicks)

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, green)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def hexes_varying_colors():
    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    color_dict = {
        0: (204, 0, 102),   # Raspberry
        1: (255, 0, 0),     # Red
        2: (0, 128, 0),     # Dark Green
        3: (0, 0, 255),     # Blue
        4: (255, 223, 0),  # Golden Yellow
        5: (255, 165, 0),   # Orange
        6: (128, 0, 128),   # Purple
        7: (160, 82, 45),  # Saddle Brown
        8: (255, 0, 255),   # Magenta
        9: (0, 128, 0),     # Dark Green
        10: (128, 0, 0),    # Dark Red
        11: (0, 0, 128),    # Dark Blue
        12: (255, 69, 0),   # Red-Orange
        13: (75, 0, 130),   # Indigo
        14: (139, 0, 0),    # Deep Red
        15: (0, 139, 0),    # Deep Green
        16: (0, 0, 139),    # Deep Blue
        17: (255, 223, 0),  # Golden Yellow
        18: (128, 128, 0),  # Olive
        19: (139, 69, 19),  # Brown
        20: (0, 255, 127),  # Spring Green
        21: (220, 20, 60),  # Crimson
        22: (154, 205, 50), # Yellow Green
        23: (255, 140, 0),  # Dark Orange
        24: (46, 139, 87),  # Sea Green
        25: (160, 82, 45),  # Saddle Brown
        26: (255, 20, 147), # Deep Pink
        27: (34, 139, 34),  # Forest Green
        28: (165, 42, 42),  # Dark Brown
        29: (0, 191, 255),  # Deep Sky Blue
        30: (147, 112, 219),# Medium Purple
        31: (255, 99, 71),  # Tomato Red
        32: (144, 238, 144),# Light Green
        33: (0, 206, 209),  # Turquoise
        34: (255, 105, 180),# Hot Pink
        35: (176, 224, 230),# Light Blue
        36: (72, 61, 139),  # Dark Slate Blue
        37: (50, 205, 50),  # Lime Green
        38: (0, 128, 128),  # Teal
        39: (210, 105, 30), # Chocolate
        40: (255, 0, 127),  # Rose
        41: (128, 128, 128),# Gray
        42: (105, 105, 105),# Dark Gray
        43: (192, 192, 192),# Silver
        44: (0, 0, 128),    # Dark Blue
        45: (255, 153, 51), # Saffron
        46: (153, 50, 204), # Dark Orchid
        47: (0, 153, 153),  # Deep Teal
        48: (178, 34, 34),  # Firebrick
        49: (102, 51, 153), # Dark Violet
    }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    hexes = {}
    clicked = {}
    order = {}
    sample = []
    scored = 0
    r = 50
    count = 0



    for k in range(5):
        
        if k%2 == 1:
            x = 187.5
            z = 8
        else:
            x = 142.5
            z = 9
        
        for j in range(z):
            array = [
                (
                    round(x + 90*j + r * math.cos(math.pi / 3 * i - math.pi / 2),1),
                    round(100 + 77 * k + r * math.sin(math.pi / 3 * i - math.pi / 2),1)
                )
                for i in range(6)
            ]

            hexes[count] = array
            clicked[count] = False
            count += 1

    def generate_polygons(num): 
        
        nonlocal sample, order, clicks, correct

        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,43), num)

        label = 1
        for samp in sample: 
            pygame.draw.polygon(screen, color_dict[samp], hexes[samp]) #producing tiles
            
            order[samp] = label #producing tile numbers
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in hexes[samp]]) / len(hexes[samp])
            shape_y = sum([point[1] for point in hexes[samp]]) / len(hexes[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, white)
            screen.blit(label_img, (label_x, label_y+2))
            clicked[samp] = False
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, white)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,color_dict[hex],hexes[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, hexes[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,hexes[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,hexes[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, white)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def rectangles_varying_colors():
    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    pygame.init()

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    color_dict = {
        0: (204, 0, 102),   # Raspberry
        1: (255, 0, 0),     # Red
        2: (0, 128, 0),     # Dark Green
        3: (0, 0, 255),     # Blue
        4: (255, 223, 0),  # Golden Yellow
        5: (255, 165, 0),   # Orange
        6: (128, 0, 128),   # Purple
        7: (160, 82, 45),  # Saddle Brown
        8: (255, 0, 255),   # Magenta
        9: (0, 128, 0),     # Dark Green
        10: (128, 0, 0),    # Dark Red
        11: (0, 0, 128),    # Dark Blue
        12: (255, 69, 0),   # Red-Orange
        13: (75, 0, 130),   # Indigo
        14: (139, 0, 0),    # Deep Red
        15: (0, 139, 0),    # Deep Green
        16: (0, 0, 139),    # Deep Blue
        17: (255, 223, 0),  # Golden Yellow
        18: (128, 128, 0),  # Olive
        19: (139, 69, 19),  # Brown
        20: (0, 255, 127),  # Spring Green
        21: (220, 20, 60),  # Crimson
        22: (154, 205, 50), # Yellow Green
        23: (255, 140, 0),  # Dark Orange
        24: (46, 139, 87),  # Sea Green
        25: (160, 82, 45),  # Saddle Brown
        26: (255, 20, 147), # Deep Pink
        27: (34, 139, 34),  # Forest Green
        28: (165, 42, 42),  # Dark Brown
        29: (0, 191, 255),  # Deep Sky Blue
        30: (147, 112, 219),# Medium Purple
        31: (255, 99, 71),  # Tomato Red
        32: (144, 238, 144),# Light Green
        33: (0, 206, 209),  # Turquoise
        34: (255, 105, 180),# Hot Pink
        35: (176, 224, 230),# Light Blue
        36: (72, 61, 139),  # Dark Slate Blue
        37: (50, 205, 50),  # Lime Green
        38: (0, 128, 128),  # Teal
        39: (210, 105, 30), # Chocolate
        40: (255, 0, 127),  # Rose
        41: (128, 128, 128),# Gray
        42: (105, 105, 105),# Dark Gray
        43: (192, 192, 192),# Silver
        44: (0, 0, 128),    # Dark Blue
        45: (255, 153, 51), # Saffron
        46: (153, 50, 204), # Dark Orchid
        47: (0, 153, 153),  # Deep Teal
        48: (178, 34, 34),  # Firebrick
        49: (102, 51, 153), # Dark Violet
    }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    clicked = {}
    order = {}
    sample = []
    scored = 0

    start_x = 99.5
    start_y = 53.5
    length = 75
    gap = 81.2

    rectangles = {}

    j = 0
    for k in range(5):
        for i in range(10):
            array = [
                (start_x + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + length + gap*k),
                (start_x + gap*i, start_y + length + gap*k)
            ]

            rectangles[j] = array
            j += 1



    def generate_polygons(number):
        nonlocal sample, order, clicks, correct
        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,50), number)

        label = 1
        for samp in sample:
            pygame.draw.polygon(screen,color_dict[samp],rectangles[samp])
            order[samp] = label
            clicked[samp] = False
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in rectangles[samp]]) / len(rectangles[samp])
            shape_y = sum([point[1] for point in rectangles[samp]]) / len(rectangles[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, white)
            screen.blit(label_img, (label_x, label_y+2))
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, white)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,color_dict[hex],rectangles[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, rectangles[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,rectangles[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,rectangles[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, white)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def larger_rectangles_varying_colors():

    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    color_dict = {
        0: (204, 0, 102),   # Raspberry
        1: (255, 0, 0),     # Red
        2: (0, 128, 0),     # Dark Green
        3: (0, 0, 255),     # Blue
        4: (255, 223, 0),  # Golden Yellow
        5: (255, 165, 0),   # Orange
        6: (128, 0, 128),   # Purple
        7: (160, 82, 45),  # Saddle Brown
        8: (255, 0, 255),   # Magenta
        9: (0, 128, 0),     # Dark Green
        10: (128, 0, 0),    # Dark Red
        11: (0, 0, 128),    # Dark Blue
        12: (255, 69, 0),   # Red-Orange
        13: (75, 0, 130),   # Indigo
        14: (139, 0, 0),    # Deep Red
        15: (0, 139, 0),    # Deep Green
        16: (0, 0, 139),    # Deep Blue
        17: (255, 223, 0),  # Golden Yellow
        18: (128, 128, 0),  # Olive
        19: (139, 69, 19),  # Brown
        20: (0, 255, 127),  # Spring Green
        21: (220, 20, 60),  # Crimson
        22: (154, 205, 50), # Yellow Green
        23: (255, 140, 0),  # Dark Orange
        24: (46, 139, 87),  # Sea Green
        25: (160, 82, 45),  # Saddle Brown
        26: (255, 20, 147), # Deep Pink
        27: (34, 139, 34),  # Forest Green
        28: (165, 42, 42),  # Dark Brown
        29: (0, 191, 255),  # Deep Sky Blue
        30: (147, 112, 219),# Medium Purple
        31: (255, 99, 71),  # Tomato Red
        32: (144, 238, 144),# Light Green
        33: (0, 206, 209),  # Turquoise
        34: (255, 105, 180),# Hot Pink
        35: (176, 224, 230),# Light Blue
        36: (72, 61, 139),  # Dark Slate Blue
        37: (50, 205, 50),  # Lime Green
        38: (0, 128, 128),  # Teal
        39: (210, 105, 30), # Chocolate
        40: (255, 0, 127),  # Rose
        41: (128, 128, 128),# Gray
        42: (105, 105, 105),# Dark Gray
        43: (192, 192, 192),# Silver
        44: (0, 0, 128),    # Dark Blue
        45: (255, 153, 51), # Saffron
        46: (153, 50, 204), # Dark Orchid
        47: (0, 153, 153),  # Deep Teal
        48: (178, 34, 34),  # Firebrick
        49: (102, 51, 153), # Dark Violet
    }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    clicked = {}
    order = {}
    sample = []
    scored = 0

    start_x = 100
    start_y = 55.5
    length = 75*1.25
    gap = 81.2*1.25

    rectangles = {}

    j = 0
    for k in range(4):
        for i in range(8):
            array = [
                (start_x + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + gap*k),
                (start_x + length + gap*i, start_y + length + gap*k),
                (start_x + gap*i, start_y + length + gap*k)
            ]

            rectangles[j] = array
            j += 1



    def generate_polygons(number):
        nonlocal sample, order, clicks, correct
        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,32), number)

        label = 1
        for samp in sample:
            pygame.draw.polygon(screen,color_dict[samp],rectangles[samp])
            order[samp] = label
            clicked[samp] = False
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in rectangles[samp]]) / len(rectangles[samp])
            shape_y = sum([point[1] for point in rectangles[samp]]) / len(rectangles[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, white)
            screen.blit(label_img, (label_x, label_y+2))
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, white)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,color_dict[hex],rectangles[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, rectangles[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,rectangles[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,rectangles[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, white)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()

def larger_hexes_varying_colors():
    scores = pd.read_csv(score_path, header = 0)
    times = pd.read_csv(time_path, header = 0)
    round_score = [config_data["unique_id"], config_data["treatment"]]
    time = [config_data["unique_id"], config_data["treatment"]]

    width = 1000
    height = 650
    screen = pygame.display.set_mode((width,height))

    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0 , 0)
    pink = (255, 16, 240)
    white = (250,250,250)

    screen.fill(black)

    color_dict = {
        0: (204, 0, 102),   # Raspberry
        1: (255, 0, 0),     # Red
        2: (0, 128, 0),     # Dark Green
        3: (0, 0, 255),     # Blue
        4: (255, 223, 0),  # Golden Yellow
        5: (255, 165, 0),   # Orange
        6: (128, 0, 128),   # Purple
        7: (160, 82, 45),  # Saddle Brown
        8: (255, 0, 255),   # Magenta
        9: (0, 128, 0),     # Dark Green
        10: (128, 0, 0),    # Dark Red
        11: (0, 0, 128),    # Dark Blue
        12: (255, 69, 0),   # Red-Orange
        13: (75, 0, 130),   # Indigo
        14: (139, 0, 0),    # Deep Red
        15: (0, 139, 0),    # Deep Green
        16: (0, 0, 139),    # Deep Blue
        17: (255, 223, 0),  # Golden Yellow
        18: (128, 128, 0),  # Olive
        19: (139, 69, 19),  # Brown
        20: (0, 255, 127),  # Spring Green
        21: (220, 20, 60),  # Crimson
        22: (154, 205, 50), # Yellow Green
        23: (255, 140, 0),  # Dark Orange
        24: (46, 139, 87),  # Sea Green
        25: (160, 82, 45),  # Saddle Brown
        26: (255, 20, 147), # Deep Pink
        27: (34, 139, 34),  # Forest Green
        28: (165, 42, 42),  # Dark Brown
        29: (0, 191, 255),  # Deep Sky Blue
        30: (147, 112, 219),# Medium Purple
        31: (255, 99, 71),  # Tomato Red
        32: (144, 238, 144),# Light Green
        33: (0, 206, 209),  # Turquoise
        34: (255, 105, 180),# Hot Pink
        35: (176, 224, 230),# Light Blue
        36: (72, 61, 139),  # Dark Slate Blue
        37: (50, 205, 50),  # Lime Green
        38: (0, 128, 128),  # Teal
        39: (210, 105, 30), # Chocolate
        40: (255, 0, 127),  # Rose
        41: (128, 128, 128),# Gray
        42: (105, 105, 105),# Dark Gray
        43: (192, 192, 192),# Silver
        44: (0, 0, 128),    # Dark Blue
        45: (255, 153, 51), # Saffron
        46: (153, 50, 204), # Dark Orchid
        47: (0, 153, 153),  # Deep Teal
        48: (178, 34, 34),  # Firebrick
        49: (102, 51, 153), # Dark Violet
    }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 60)
    game_over_font = pygame.font.SysFont(None, 100)
    play_again_font = pygame.font.SysFont(None, 60)
    #play_again_rect = Rect(300, 400, 300, 100) old play again rectangle
    play_again_rect = Rect(350, 500, 300, 100)
    game_screen_rect = Rect(95,47.5,815,415)
    ready_rect = Rect(350, 500, 300, 100)
    score_rect = Rect(50,525,300,100)

    pygame.draw.rect(screen,white,game_screen_rect)

    hexes = {}
    clicked = {}
    order = {}
    sample = []
    scored = 0
    r = 60
    count = 0

    for k in range(4):
        
        if k%2 == 1:
            x = 172.5 * 1.2
            z = 7
        else:
            x = 127.5 * 1.2
            z = 7
        
        for j in range(z):
            array = [
                (
                    round(x + 108*j + r * math.cos(math.pi / 3 * i - math.pi / 2),1),
                    round(113.5 + 92.4 * k + r * math.sin(math.pi / 3 * i - math.pi / 2),1)
                )
                for i in range(6)
            ]

            hexes[count] = array
            clicked[count] = False
            count += 1


    def generate_polygons(num): 
        
        nonlocal sample, order, clicks, correct

        clicks = 0
        correct = 0
        order = {}
        sample = []
        random.seed(number)
        sample = random.sample(range(0,28), num)

        label = 1
        for samp in sample: 
            pygame.draw.polygon(screen, color_dict[samp], hexes[samp]) #producing tiles
            
            order[samp] = label #producing tile numbers
            label_text = f"{label}"
            label_width, label_height = font.size(label_text)

            # Compute the center of the shape
            shape_x = sum([point[0] for point in hexes[samp]]) / len(hexes[samp])
            shape_y = sum([point[1] for point in hexes[samp]]) / len(hexes[samp])

            # Adjust the label position to center it
            label_x = shape_x - (label_width / 2)
            label_y = shape_y - (label_height / 2)

            label_img = font.render(label_text, True, white)
            screen.blit(label_img, (label_x, label_y+2))
            clicked[samp] = False
            label += 1

    def play_again():
        nonlocal game_over
        screen.fill(black)
        game_over_text = "Game Over"
        game_width, _ = game_over_font.size(game_over_text)
        game_over_img = game_over_font.render(game_over_text, True, red)
        screen.blit(game_over_img, ((1000-game_width)/2,150))

        final_score_text = f"Final Score: {scored}"
        final_width, _ = game_over_font.size(final_score_text)
        final_score_img = game_over_font.render(final_score_text, True, red)
        screen.blit(final_score_img, ((1000-final_width)/2,225))


        pygame.draw.rect(screen,red,play_again_rect)
        play_again_text = "Exit"
        play_again_img = play_again_font.render(play_again_text, True, black)
        text_width, text_height = play_again_font.size(play_again_text)

        text_x = play_again_rect.x + (play_again_rect.width - text_width) / 2
        text_y = play_again_rect.y + (play_again_rect.height - text_height) / 2

        screen.blit(play_again_img, (text_x, text_y))
        game_over = True
        

    def is_point_in_polygon(point, polygon):
        x, y = point
        inside = False
        px, py = polygon[-1]  # Last vertex
        for nx, ny in polygon:
            if (ny > y) != (py > y):  # Check if point is between y-bounds
                if x < (nx - px) * (y - py) / (ny - py + 1e-10) + px:
                    inside = not inside
            px, py = nx, ny
        return inside

    def ready():
        pygame.draw.rect(screen,blue,ready_rect)
        ready_text = "Ready"
        ready_img = play_again_font.render(ready_text, True, white)
        screen.blit(ready_img, (435,530))

    def score(clicks):
        nonlocal scored
        scored = clicks
        pygame.draw.rect(screen,black,score_rect)
        score_text = f"Score: {clicks}"
        score_img = score_font.render(score_text, True, blue)
        screen.blit(score_img, (50,525))

    def next_round():
        nonlocal strike, ready_click, scored, next_round_state
        next_round_state = True
        screen.fill(black)

        strike_text = f"Correct: {correct}"
        strike_width, _ = game_over_font.size(strike_text)
        strike_img = game_over_font.render(strike_text, True, blue)
        screen.blit(strike_img, ((1000-strike_width)/2,200))

    def timer():
        current_time = pygame.time.get_ticks()
        duration = current_time - start_time
        ready_time = duration
        time.append(ready_time)
        
    clicks = 0
    start_time = pygame.time.get_ticks()
    current_time = 0
    run = True
    number = 4
    correct = 0
    game_over = False
    ready_click = False
    strike = 0
    next_round_state = False

    generate_polygons(number)
    score(0)
    ready()

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                number = 16

            #if event.type == pygame.mouse.get_pressed()[0] == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()
                #print(pos)

                if ready_rect.collidepoint(pos) and ready_click == False:

                    timer()
                    
                    for hex in sample:

                        pygame.draw.polygon(screen,color_dict[hex],hexes[hex])
                    
                    ready_click = True
                    pygame.draw.rect(screen,black,ready_rect)

                if ready_click == True:

                    for hex in sample:

                        if is_point_in_polygon(pos, hexes[hex]) == True and clicked[hex] == False:
                            
                            clicks += 1
                            if clicks == order[hex]:
                                pygame.draw.polygon(screen,white,hexes[hex])
                                clicked[hex] = True
                                correct += 1
                            
                            if clicks != order[hex]:
                                clicked[hex] = True
                                pygame.draw.polygon(screen,white,hexes[hex])

                            if clicks == number:
                                if correct == clicks:
                                    score(correct)
                                number += 1
                                start_time = pygame.time.get_ticks()
                                print(correct)
                                round_score.append(correct)
                                next_round()

            if next_round_state == True:

                pygame.draw.rect(screen,blue,ready_rect)
                continue_text = "Continue"
                continue_img = play_again_font.render(continue_text, True, white)
                screen.blit(continue_img, (407.5,530))

                if ready_rect.collidepoint(pos):
                    start_time = pygame.time.get_ticks()
                    next_round_state = False
                    ready_click = False
                    screen.fill(black)
                    pygame.draw.rect(screen,white,game_screen_rect)
                    score(scored)
                    generate_polygons(number)
                    ready()

            if number == 16:
                missing = 14 - len(round_score)
                for i in range(missing):
                    round_score.append('')
                new_row = pd.DataFrame([round_score], columns = scores.columns)
                file = pd.concat([scores,new_row], ignore_index = True)
                file.to_csv(score_path, index = False)

                missing = 14 - len(time)
                print(missing)
                for i in range(missing):
                    time.append('')
                new_time = pd.DataFrame([time], columns = times.columns)
                file_time = pd.concat([times,new_time], ignore_index = True)
                file_time.to_csv(time_path, index = False)

                info = pd.read_csv(info_path, header = 0)
                info.loc[info["unique_id"] == config_data["unique_id"], "score"] = scored
                info.to_csv(info_path, index = False)
                play_again()
                next_round_state = False
                number +=1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over is True:
                
                pos = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(pos):
                    return user_interface()
        

        pygame.display.update()

    return user_interface()


user_interface()