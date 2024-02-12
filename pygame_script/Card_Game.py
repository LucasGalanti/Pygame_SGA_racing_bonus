import pygame
import random
import json
import pandas as pd
import os
import time


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

def asset_path(relative_path):
    return os.path.join(script_dir,relative_path)

## Initialize the game
pygame.init()

## Start display
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('Acelerador de vendas')

##Set Game clock and FPS
FPS = 60
clock = pygame.time.Clock()

#region - Defining Classes
class Game():
    """A class to help control and update the gameplay"""

    def __init__(self, card_group, player_group, second_player_group, old_budget_group, new_budget_group, char_selection_group):
        "Initialize the game"
        self.card_group = card_group
        self.old_budget_group = old_budget_group
        self.player_group = player_group
        self.second_player = second_player_group
        self.new_budget_group = new_budget_group
        self.vendas = 0
        self.selected_cards = 0
        self.current_frame = 0
        self.frame_counter = 0
        self.FPS_timeout = 0
        self.vendas_gerais = 0
        self.char_selection_group = char_selection_group

        #region - Create map icon, which will be blinking
        self.map_image_list = []

        #fist possibilty - map icon appearing
        self.map_image_icon = pygame.image.load(asset_path('assets/map icon.png'))
        self.map_image_list.append(self.map_image_icon)
        self.map_image_rect = self.map_image_icon.get_rect()

        #second possibility - map icon not appearing (blank)
        self.map_blank = pygame.Surface(self.map_image_rect.size, pygame.SRCALPHA)
        self.map_image_list.append(self.map_blank)
        
        #endregion

    def update(self):
        """Update the game"""
        self.old_bonus()
        self.new_bonus()

        
        if clicking_enabled == True:
            self.check_for_round_completion()

    def draw(self):
        "Draw the HUD (probably depending on the menu)"

        #draw everything
        display_surface.blit(background_image,background_rect)
        display_surface.blit(scroll_image,scroll_rect)
        display_surface.blit(bonus_board_image,bonus_board_rect)
        display_surface.blit(bonus_novo_board_image, bonus_novo_board_rect)
        display_surface.blit(final_bonus_image, final_bonus_rect)

        #region - map icon position x_parameters, to be on top of the day depending on the current day
        self.dia_map_dict ={
            5 : 236,
            10 : 364,
            15 : 492,
            20 : 620,
            25 : 748,
            30 : 876
        }

        #Update the map_icon position with the day
        self.map_image_rect.center = (self.dia_map_dict[self.dia], 149)
        
        # Update sprite every 1/2 second (30 FRAMES) (empty or )
        if self.frame_counter % 10 == 0:
            if self.map_image_icon == self.map_image_list[0]:
                self.map_image_icon = self.map_image_list[1]
            else:
                self.map_image_icon = self.map_image_list[0]

        #Update the frame counter
        self.frame_counter += 1

        #blit the icon on the display
        display_surface.blit(self.map_image_icon, self.map_image_rect)
        #endregion

        
        #Draw the new and old bonus into the respective box

        self.bonus_font = pygame.font.Font(asset_path( 'assets/joystix.otf'), 35)

        #old_bonus
        self.bonus_antigo_text = self.bonus_font.render("{:.0%}".format(self.old_bonus()), True, (116, 63,57))
        self.bonus_antigo_rect = self.bonus_antigo_text.get_rect()
        self.bonus_antigo_rect.center = (1587, 656)
        display_surface.blit(self.bonus_antigo_text, self.bonus_antigo_rect)

        #new_bonus
        self.bonus_novo_text = self.bonus_font.render("{:.0%}".format(self.new_bonus()), True, (24, 20, 37))
        self.bonus_novo_rect = self.bonus_novo_text.get_rect()
        self.bonus_novo_rect.center = (1783, 656)
        display_surface.blit(self.bonus_novo_text, self.bonus_novo_rect)

    def bonus_ind_por_atingmento(self, atingimento):
        """Calculates the amount of bonus earned in each stage by the vendor"""
        """IMPORTANT: THIS VALUE DOES NOT REPRESENT THE REAL BONUS VALUES USED BY NORTON"""
        """AND WAS CHANGED IN CODE TO PRESERVE ITS STRATEGY COMPLIANCE"""

        if atingimento >= 1.2:
            return 1.2
        elif atingimento >= 1.0:
            return atingimento - 0.05
        elif atingimento >= 0.5:
            if atingimento < 0.60:
                return 0.20
            elif atingimento < 0.70:
                return 0.30
            elif atingimento < 0.80:
                return 0.50
            elif atingimento < 0.90:
                return 0.60
            elif atingimento < 0.95:
                return 0.70
            elif atingimento < 1:
                return 0.90
        else:
            return 0

    def old_bonus(self):
        #bonus individuais x pesos
        self.bonus_old_final = 0
        self.atingimento_geral = self.vendas_gerais/self.meta_total

        if self.atingimento_geral >=0.5:
            for linha in my_old_budget_group:
                bonus_ind = self.bonus_ind_por_atingmento(linha.atingimento_texto_atual)
                self.bonus_old_final += bonus_ind*linha.peso
    
            # if we reach 0.5, we can get the 5% of "motivo 1" and "motivo 2"
            self.bonus_old_final += 0.05
            # if we reach 0.5, we can get the 5% of "motivo 1" and "motivo 2"
            self.bonus_old_final += 0.05
        
        return self.bonus_old_final

    def new_bonus(self):
        #bonus individuais x pesos
        self.bonus_new_final = 0

        self.atingimento_geral = self.vendas_gerais/self.meta_total
        self.atingimento_acelerador = self.vendas_acelerador/self.meta_acelerador

        self.bonus_new_final += self.bonus_ind_por_atingmento(self.atingimento_geral)*self.peso_geral
        self.bonus_new_final += self.bonus_ind_por_atingmento(self.atingimento_acelerador)*self.peso_acelerador

        if self.atingimento_geral>=0.5:
            # if we reach 0.5, we can get the 5% of "motivo 1" and "motivo 2"
            self.bonus_new_final += 0.05
            # if we reach 0.5, we can get the 5% of "motivo 1" and "motivo 2"
            self.bonus_new_final += 0.05
        
        return self.bonus_new_final

    def check_for_round_completion(self):
        global clicking_enabled
        # the round lets the player choose 2 cards.
        if self.selected_cards >=2:
            clicking_enabled = False
            if self.FPS_timeout >=10:
                self.FPS_timeout = 0
                self.round +=1
                if self.round>6:
                    self.end_game()
                else:
                    self.next_round_dia(self.round)
                    clicking_enabled = True
            else:
                self.FPS_timeout +=1

    def load_card_game(self):

        # Specify the folder path where the JSON files are located
        folder_path = asset_path('Game_Setups')

        # Get a list of all JSON files in the folder
        json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

        # Select a random JSON file from the list
        self.json_file = random.choice(json_files)

        # Read the selected JSON file
        with open(os.path.join(folder_path, self.json_file), 'r') as f:
            self.data = json.load(f)

        #for the selected game, get the metas and pesos
        self.pesos_meta_dict = self.data['pesos_meta_dict']

        #now we get the weights of the general and acceleration group
        self.peso_geral =       self.data["peso_geral"]
        self.peso_acelerador =  self.data["peso_acelerador"]
        self.meta_acelerador =  self.data["meta_acelerador"]

        #meta total é a soma das metas individuais
        self.meta_total = sum(value[1] for value in self.pesos_meta_dict.values())

        #for the selected game, get the linhas_aceleradoras list
        self.linhas_aceleradoras = self.data['linhas_aceleradoras']

        # Convert each dictionary in baralho_dict back to a DataFrame
        possible_card_games = {k: pd.DataFrame(v) for k, v in self.data['baralho_dict'].items()}

        #select a random 'baralho' in the dict
        selected_card_game_number = random.choice(list(possible_card_games.keys()))

        self.card_game = possible_card_games[selected_card_game_number]

        #lista de dias no jogo [padrão será 5, 10, 15, 20, 25 e 30]
        self.lista_dias = self.card_game['Dia'].unique().tolist()

        #lista de cartas por dia [padrão será 1, 2, 3 e 4]
        self.lista_cartas = self.card_game['Carta'].unique().tolist()

    def enable_click(self):
        global player_1_running
        global player_2_running
        global bar_filling

        bar_fill_check = False

        #Check if any "linha" is currently growing
        for linha in self.old_budget_group:
            if linha.growing == True:
                bar_fill_check = True
        
        bar_filling = bar_fill_check
            
        if player_1_running or player_2_running or bar_filling:
            return False
        else:
            return True

    def define_budget_groups(self, peso_meta_dict):
        """Create and include in the peso_meta_class"""

        #Define old budget group
        for i, linha in enumerate(peso_meta_dict.keys()):
            peso = peso_meta_dict[linha][0]
            meta = peso_meta_dict[linha][1]
            old_budget_linha = Old_Budget(linha, peso, meta, i, 0)
            my_old_budget_group.add(old_budget_linha)

        #Define new Budget Group
        for player in self.player_group:
            new_budget_geral = New_Budget("Geral", self.peso_geral, self.meta_total, posicao=0, char_icon= player.gui_icon)
        
        for player2 in self.second_player:
            new_budget_acelerador = New_Budget("Aceleradog", self.peso_acelerador, self.meta_acelerador, posicao=1, char_icon= player2.gui_icon)
        
        my_new_budget_group.add(new_budget_geral)
        my_new_budget_group.add(new_budget_acelerador)

    def check_for_card_selection(self, mouse_x_pos, mouse_y_pos):
        "Check if a sales card has been selected"
        mouse_rect = pygame.Rect(mouse_x_pos,mouse_y_pos, 1, 1)
        for card in self.card_group:
            if card.rect.colliderect(mouse_rect):
                card.click_sound.play()
                self.vendas_gerais += card.valor
                valor_acelerador = 0
                if card.acelerador:
                    valor_acelerador = card.valor
                    self.vendas_acelerador += valor_acelerador

                for player in my_Main_Player:
                    player.vendas += card.valor
                
                for player2 in my_Second_Player:
                    player2.vendas += valor_acelerador

                for linha_old_budget in my_old_budget_group:
                    if linha_old_budget.linha == card.linha:
                        linha_old_budget.venda += card.valor
                
                for linha_new_budget in my_new_budget_group:
                    if linha_new_budget.linha == "Geral":
                        linha_new_budget.venda += card.valor
                    if linha_new_budget.linha == "Aceleradog":
                        linha_new_budget.venda += valor_acelerador

                card.kill()
                self.selected_cards +=1
                if self.selected_cards>=2:
                    self.card_group.empty()

    def next_round_dia(self, round_num):
        "Eliminate the cards from current round, load next day"
        #Create a linup of 4 cards

        #The list starts at 0, our "round" starts at 1
        self.dia = self.lista_dias[round_num-1] 

        #resetamos a nossa lista de cartas que será mostrada
        self.card_group.empty()
        self.selected_cards = 0
        #e colocamos as cartas relativas 
        
        shuffle_factor = random.randint(0, 2)
        for card_num in range(len(self.lista_cartas)):
            #we create a index in the style of "5-1", "10-3", "20-4"

            #we shuffle the cards within the day, to create the ilusion of different games being generated
            new_card_num = (card_num + shuffle_factor) % len(self.lista_cartas) + 1
            carta_dia_temp = str(self.dia) + '-' + str(new_card_num)

            #we search for the "linha", "valor" and "acelerador" for this index
            linha_temp = self.card_game.loc[carta_dia_temp]['Linha']
            valor_temp = self.card_game.loc[carta_dia_temp]['Valor']
            acc_temp = self.card_game.loc[carta_dia_temp]['Acelerador']
            
            #we create a Card class item, with the generated values from the self.lista_cartas, that is is the json file
            card = Card(self.dia, card_num+1, linha_temp, valor_temp, acc_temp)
            self.card_group.add(card)

    def restart_player(self):
        self.player_group.empty()
        player = Player(sex = self.sex_selected, skin = self.skin_selected, peso = self.peso_geral, meta = self.meta_total, init_x= 190)
        self.player_group.add(player)

        self.second_player.empty()
        second_player = Player_2(type = "Dog", peso = self.peso_acelerador, meta = self.meta_acelerador, init_x= 90)
        self.second_player.add(second_player)

    def new_game(self):
        random_music = random.randint(1,2)
        pygame.mixer.music.load(asset_path( 'assets/mixer/race_song_' + str(random_music) + '.mp3'))
        pygame.mixer.music.play(-1,0)
        self.vendas_gerais = 0
        self.vendas_acelerador = 0
        self.atingimento_geral = 0
        self.bonus_atual = 0
        self.bonus_novo = 0
        self.round = 1
        self.load_card_game()
        self.restart_player()
        my_old_budget_group.empty()
        my_new_budget_group.empty()
        self.define_budget_groups(self.pesos_meta_dict)
        self.next_round_dia(1)

    def end_game(self):
        global running
        pygame.mixer.music.load(asset_path( 'assets/mixer/end_level_sound.mp3'))
        pygame.mixer.music.set_volume(0.8)  # Increase the volume to 80%
        pygame.mixer.music.play()
        
        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pass

        game_paused = True
        while game_paused:
            for event in pygame.event.get():
                #Check if player wants out
                if event.type == pygame.QUIT:
                    running = False
                    game_paused = False

                if (event.type == pygame.MOUSEBUTTONDOWN):
                    game_paused = False
    
        self.start_menu()

    def char_selection_page(self):
        """
        This is the first page the game will open after the main menu
        The player will have the option to choose between 2 male and 2 female characters
        """

        global running
        pygame.mixer.music.load(asset_path( 'assets/mixer/instructions_music.mp3'))
        pygame.mixer.music.play(-1,0)

        self.char_selection_group.empty()
        playable_chars = ["M_1", "M_2", "F_1", "F_3"]

        char_background = pygame.image.load(asset_path( 'assets/char_selection/char_selection_page.png'))
        char_background_rect = char_background.get_rect()
        char_background_rect.topleft = (0,0)

        for i, char in enumerate(playable_chars):
            sex, skin = char.split("_")
            new_char = CharSelection(position = i, sex = sex, skin = skin, clothes = 1)
            self.char_selection_group.add(new_char)

        self.on_char_select = True
        while self.on_char_select:
            for event in pygame.event.get():
                #Check if player wants out
                if event.type == pygame.QUIT:
                    self.on_char_select = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_rect = pygame.Rect(event.pos[0],event.pos[1], 1, 1)

                    #We check if there was a click into any of the CharSelection class boxes
                    for char in self.char_selection_group:
                        if char.rect.colliderect(mouse_rect):

                            # We toggle the is_selected value to true, and the sex and skin is selected for our game
                            char.is_selected = True
                            self.sex_selected = char.sex
                            self.skin_selected = char.skin

                #if the selection animation ends, we leave the while loop
                for char in self.char_selection_group:
                    if char.end_selection == True:
                            self.on_char_select = False

            #update image
            display_surface.blit(char_background, char_background_rect)

            self.char_selection_group.update()
            self.char_selection_group.draw(display_surface)
            pygame.display.update()
        
        pygame.display.update()
        #after we leave the while loop, we can enter the instructions page
        self.instructions_page()

    def instructions_page(self):
        global running
        self.on_start_menu = False

        ##page 1
        page_1_img = pygame.image.load(asset_path( 'assets/instrucoes_background/page1.PNG'))
        page_1_rect = page_1_img.get_rect()
        page_1_rect.topleft = (0,0)

        page_2_img = pygame.image.load(asset_path( 'assets/instrucoes_background/page2.PNG'))
        page_2_rect = page_2_img.get_rect()
        page_2_rect.topleft = (0,0)

        page_3_img = pygame.image.load(asset_path( 'assets/instrucoes_background/page3.PNG'))
        page_3_rect = page_3_img.get_rect()
        page_3_rect.topleft = (0,0)

        page_4_img = pygame.image.load(asset_path( 'assets/instrucoes_background/page4.PNG'))
        page_4_rect = page_4_img.get_rect()
        page_4_rect.topleft = (0,0)

        player_float_pos = 1
        dog_idle_float_pos = 1

        player_scale = 7
        dog_scale = 4

        current_page = 1

        on_inst_page = True
        while on_inst_page:
            
            for event in pygame.event.get():
                #Check if player wants out
                if event.type == pygame.QUIT:
                    on_inst_page = False
                    running = False

                #Check if some button have been clicked to go to next page
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    #If clicked, we run the script (usually an animation and change the screen)
                    current_page += 1
                    #and end the start_menu loop

            if current_page == 1:
                #Blit the HUD to display

                ## loading player image
                if int(player_float_pos) > 7:
                    player_float_pos = 1

                player_pos = str("0"+str(int(player_float_pos)))
                
                if self.sex_selected == "M":
                    self.sex_spelled = "Male"
                else:
                    self.sex_spelled = "Female"

                folder_path = 'assets/Main_Chars/'+ self.sex_spelled + '/Character ' + str(self.skin_selected) + '/Clothes 1/'
                image_path = 'Character' + str(self.skin_selected) + str(self.sex_selected) + "_1_idle_"+str(player_pos)+'.png'

                original_player_image = pygame.image.load(asset_path( folder_path+image_path))
                player_image = pygame.transform.scale(
                    original_player_image, 
                    (original_player_image.get_width()*player_scale, original_player_image.get_height()*player_scale)
                )
                player_image_rect = player_image.get_rect()
                player_image_rect.center = (497,460)
                player_float_pos += 0.1


                ## loading dog image
                if int(dog_idle_float_pos) > 24:
                    dog_idle_float_pos = 1

                dog_idle_pos = int(dog_idle_float_pos)

                original_dog_image = pygame.image.load(asset_path( 'assets/Companion/Approved/Dog/instruction_sprites/idle_instruction'+str(dog_idle_pos)+'.png'))
                dog_idle_image = pygame.transform.scale(
                    original_dog_image, 
                    (original_dog_image.get_width()*dog_scale, original_dog_image.get_height()*dog_scale)
                )
                dog_idle_rect = dog_idle_image.get_rect()
                dog_idle_rect.center = (1513,460+20)
                dog_idle_float_pos += 0.1

                display_surface.blit(page_1_img,page_1_rect)
                display_surface.blit(player_image,player_image_rect)
                display_surface.blit(dog_idle_image,dog_idle_rect)

            elif current_page == 2:
                display_surface.blit(page_2_img,page_2_rect)

            elif current_page == 3:
                
                ## loading running image
                if int(player_float_pos) > 4:
                    player_float_pos = 1

                player_pos = str("0"+str(int(player_float_pos)))

                folder_path = 'assets/Main_Chars/'+ self.sex_spelled + '/Character ' + str(self.skin_selected) + '/Clothes 1/'
                image_path = 'Character' + str(self.skin_selected) + str(self.sex_selected) + "_1_car_running_"+str(player_pos)+'.png'

                original_player_image = pygame.image.load(asset_path( folder_path + image_path))
                player_image = pygame.transform.scale(
                    original_player_image, 
                    (original_player_image.get_width()*player_scale, original_player_image.get_height()*player_scale)
                )
                player_image_rect1 = player_image.get_rect()
                player_image_rect1.center = (1650-150,250)

                player_image_rect2 = player_image.get_rect()
    
                player_image_rect2.centerx = player_image_rect1.centerx+200
                player_image_rect2.centery = player_image_rect1.centery+466

                player_float_pos += 0.1

                ## loading dog image
                if int(dog_idle_float_pos) > 4:
                    dog_idle_float_pos = 1

                dog_idle_pos = int(dog_idle_float_pos)

                original_dog_image = pygame.image.load(asset_path( 'assets/Companion/Approved/Dog/instruction_sprites/dog_car_running'+str(dog_idle_pos)+'.png'))
                dog_idle_image = pygame.transform.scale(
                    original_dog_image, 
                    (original_dog_image.get_width()*dog_scale, original_dog_image.get_height()*dog_scale)
                )
                dog_idle_rect = dog_idle_image.get_rect()
                dog_idle_rect.bottom = player_image_rect2.bottom
                dog_idle_rect.right = player_image_rect2.left+20+138
                dog_idle_float_pos += 0.2


                ##blitting on the display

                display_surface.blit(page_3_img,page_3_rect)
                display_surface.blit(player_image,player_image_rect1)
                display_surface.blit(player_image,player_image_rect2)
                display_surface.blit(dog_idle_image,dog_idle_rect)


            elif current_page == 4:
                display_surface.blit(page_4_img,page_4_rect)

            else:
                on_inst_page = False
                self.new_game()
        
            pygame.display.update()

    def start_menu(self):
        global running
        pygame.mixer.music.load(asset_path( 'assets/mixer/start_menu_music.mp3'))
        pygame.mixer.music.play(-1,0)
        
        start_menu_button_group = pygame.sprite.Group()
        "Draw the HUD (probably depending on the menu)"
        #Set colors
        BACKGROUND = (255,255,255)

        #create buttons
        new_game_button = Travel_Button(self, 'char_selection_page', 'button_init_vendas', [1,2,3], (400,96), BACKGROUND)

        #position buttons
        new_game_button.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+120)

        start_menu_button_group.add(new_game_button)

        background_menu_image = pygame.image.load(asset_path( 'assets/menu_background.png'))
        background_menu_rect = background_menu_image.get_rect()
        background_menu_rect.topleft = (0,0)

        self.on_start_menu = True
        pistax = 0
        dog_initial_x = 351
        dog_final_x = 1000
        dog_x = dog_initial_x

        dog_stop_count = 0
        dog_initial_velocity = 5
        dog_velocity = -dog_initial_velocity
        dog_idle_float_pos = 1

        player_initial_x = 500
        player_final_x = 1300
        player_x = (player_initial_x+player_final_x)//2

        player_stop_count = 0
        player_initial_velocity = 3
        player_velocity = player_initial_velocity
        player_idle_float_pos = 1


        playable_chars = ["M_1", "M_2", "F_1", "F_3"]

        #get a random value in the playable_chars list
        menu_char = random.choice(playable_chars)

        sex_menu, skin_menu = menu_char.split("_")
        if sex_menu == "M":
            sex_spelled_menu = "Male"
        else:
            sex_spelled_menu = "Female"

        player_float_pos = 1

        while self.on_start_menu:

            #Blit the HUD to display
            display_surface.blit(background_menu_image,background_menu_rect)

            #Blit button
            for button in start_menu_button_group:
                display_surface.blit(button.image, button.rect)


            #load running pista
            pista_delta_x = 30
            
            if pistax <= -1920:
                pistax = 0
            else:
                pistax -= pista_delta_x

            pista_image = pygame.image.load(asset_path( 'assets/main_menu_racing_track.png'))
            pista_image_rect = pista_image.get_rect()
            pista_image_rect.bottom = WINDOW_HEIGHT
            pista_image_rect.left = pistax

            display_surface.blit(pista_image, pista_image_rect)


            #load running dog

            #updating sprite
            if int(dog_idle_float_pos) > 4:
                dog_idle_float_pos = 1

            dog_idle_pos = int(dog_idle_float_pos)

            original_dog_image = pygame.image.load(asset_path( 'assets/Companion/Approved/Dog/instruction_sprites/dog_car_running'+str(dog_idle_pos)+'.png'))
            dog_idle_image = pygame.transform.scale(
                original_dog_image, 
                (original_dog_image.get_width()*5, original_dog_image.get_height()*5)
            )
            dog_idle_rect = dog_idle_image.get_rect()
            dog_idle_float_pos += 1

            #updating dog velocity
            if dog_x <= dog_initial_x or dog_x >= dog_final_x:
                dog_velocity = 0

                if dog_stop_count >= 30:
                    dog_stop_count = 0
                    if dog_x <= dog_initial_x:
                        dog_velocity = dog_initial_velocity
                    elif dog_x >= dog_final_x:
                        dog_velocity = -dog_initial_velocity
                
                else:
                    dog_stop_count += 1


                
            #updating dog position
            dog_x += dog_velocity
            dog_idle_rect.bottom = 850
            dog_idle_rect.left = dog_x
            
            #displaying dog
            display_surface.blit(dog_idle_image, dog_idle_rect)





            ## loading player running image

            if int(player_float_pos) > 4:
                player_float_pos = 1

            player_pos = str("0"+str(int(player_float_pos)))

            folder_path = 'assets/Main_Chars/'+ sex_spelled_menu + '/Character ' + str(skin_menu) + '/Clothes 1/'
            image_path = 'Character' + str(skin_menu) + str(sex_menu) + "_1_car_running_"+str(player_pos)+'.png'

            original_player_image = pygame.image.load(asset_path( folder_path + image_path))
            player_image = pygame.transform.scale(
                original_player_image, 
                (original_player_image.get_width()*8, original_player_image.get_height()*8)
            )
            player_image_rect1 = player_image.get_rect()
            player_float_pos += 1

            #updating player velocity

            #updating player velocity
            if player_x <= player_initial_x or player_x >= player_final_x:
                player_velocity = 0

                if player_stop_count >= 30:
                    player_stop_count = 0
                    if player_x <= player_initial_x:
                        player_velocity = player_initial_velocity
                    elif player_x >= player_final_x:
                        player_velocity = -player_initial_velocity
                
                else:
                    player_stop_count += 1

            #updating player position
            player_x += player_velocity
            player_image_rect1.bottom = 1000
            player_image_rect1.left = player_x

            #displaying Player
            display_surface.blit(player_image, player_image_rect1)

            pygame.display.update()

        
            for event in pygame.event.get():
                #Check if player wants out
                if event.type == pygame.QUIT:
                    running = False
                    self.on_start_menu = False

                #Check if some button have been clicked
                for button in start_menu_button_group:
                    if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                        self.on_start_menu = False
                        #If clicked, we run the script (usually an animation and change the screen)
                        button.click_script()
                        #and end the start_menu loop

    def draw_buttons(self, button_group):
        for button in button_group:
            button.draw_button()

class CharSelection(pygame.sprite.Sprite):

    """ A class to model a selectable player in the char selection page"""
    def __init__(self, position, sex, skin, clothes = 1):
        super().__init__()
        self.sex = sex #M or F
        self.skin = skin #1, 2 or 3
        self.clothes = clothes #por enquanto só 1
        self.action = 'idle'
        self.action_sprites = ['idle', 'select']
        self.position = position # between 0 and 4 for now
        self.float_sprite_pos = 0
        self.float_delta = 0.5
        self.frame_float_delta = 0.25
        self.is_selected = False
        self.frame_sprite_float_pos = 0
        self.sprite_float_position = 0
        self.end_selection = False

        #region Create sprite action dictionary self.image_dict{}
        self.folder = 'assets/char_selection/'
        self.char_key_name = "Character" + str(self.skin) + self.sex + "_" + str(self.clothes) + "_"

        self.image_dict = {}
        for action in self.action_sprites:
            initial_sprite_name = self.char_key_name + action + "_"
            # for example, it could be "/assets/Main_Chars/Female/Character 2/Clothes 1/Character2F_1_idle_"

            # Get a list of all files in the self.folder directory
            files = os.listdir(asset_path(self.folder))

            # Filter the list to include only PNG files that start with initial_sprite_name
            png_files = [file for file in files if file.startswith(initial_sprite_name) and file.endswith(".png")]

            # Load and transform the images
            for i, png_image in enumerate(png_files):
                full_path = os.path.join(asset_path(self.folder), png_image)
                loaded_image = pygame.image.load(full_path)
                key = f"{action}_{i}"
                self.image_dict[key] = loaded_image
        #endregion


        #use the unselected frame image to compose our image rect
        self.unselected_frame_image = pygame.image.load(asset_path( 'assets/char_selection/not_selected_frame.png'))

        self.image = pygame.Surface(self.unselected_frame_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.frame_rect = self.unselected_frame_image.get_rect()
        self.frame_rect.topleft = (0,0)

        #positioning the rect based on the position
        self.INICIO_FRAMES_LEFT = 93#93
        self.INICIO_FRAMES_TOP = 411
        self.DIST_BETWEEN_FRAMES = 58
        self.rect.topleft = (self.INICIO_FRAMES_LEFT + (self.position)*(self.rect.width+self.DIST_BETWEEN_FRAMES), self.INICIO_FRAMES_TOP)  # Set the position of the image rectangle to match the frame rectangle
        
        self.selected_frame_image_list = [
            pygame.image.load(asset_path( 'assets/char_selection/char_selected_01.png')),
            pygame.image.load(asset_path( 'assets/char_selection/char_selected_02.png')),
            pygame.image.load(asset_path( 'assets/char_selection/char_selected_03.png')),
        ]

        self.char_sprite = self.image_dict['idle_0']
        self.char_rect = self.char_sprite.get_rect()
        self.char_rect.center = (self.rect.width//2, self.rect.height//2)

        self.image.blit(self.unselected_frame_image, self.frame_rect)
        self.image.blit(self.char_sprite, self.char_rect)

    def update(self):

        #creation of a dict with the current action

        #check if character was selected the last frame
        if self.action == 'idle' and self.is_selected == True:
            self.action = 'select'
            self.sprite_float_position = 0
        
        #choose the current sprite for the char
        self.sprite_filtered_dict = {k: v for k, v in self.image_dict.items() if k.startswith(self.action)}

        self.char_sprite = self.sprite_filtered_dict[self.action + "_" + str(int(self.sprite_float_position))]

        self.char_rect = self.char_sprite.get_rect()

        self.char_rect.center = (self.rect.width//2, self.rect.height//2)

        if self.action == 'idle' and int(self.sprite_float_position) >= len(self.sprite_filtered_dict)-1:
            self.sprite_float_position = 0
        else:
            self.sprite_float_position += self.float_delta

        ## when the animation for the select sprite is over, finish the select screen
        if self.action == 'select' and  int(self.sprite_float_position) >= len(self.sprite_filtered_dict)-1:
            self.sprite_float_position = 0
            self.end_selection = True

        #choose the current sprite for the frame
        if self.action == 'idle':
            self.frame_sprite = pygame.image.load(asset_path( 'assets/char_selection/not_selected_frame.png'))

        else:
            self.frame_sprite = self.selected_frame_image_list[int(self.frame_sprite_float_pos)]

        #update the position of the selected frame sprite position
        if self.action == 'select' and int(self.frame_sprite_float_pos) < len(self.selected_frame_image_list)-2:
            self.frame_sprite_float_pos += self.frame_float_delta
            
        
        #draw the self.image surface
        self.image = pygame.Surface(self.unselected_frame_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.INICIO_FRAMES_LEFT + (self.position)*(self.rect.width+self.DIST_BETWEEN_FRAMES), self.INICIO_FRAMES_TOP) 

        self.image.blit(self.frame_sprite, self.frame_rect)
        self.image.blit(self.char_sprite, self.char_rect)

class Card(pygame.sprite.Sprite):
    """A class to model a selectable card"""

    def __init__(self, dia, carta, linha, valor, acelerador):
        """Initizalize the card"""
        super().__init__()
        self.dia = dia
        self.carta = carta
        self.acelerador = acelerador
        self.dia_carta = str(self.dia) + "-" + str(self.carta)
        self.linha = linha
        self.valor = valor

        # Imagem depende se o item é acelerador ou não

        if self.acelerador == True:
            self.image = pygame.image.load(asset_path( 'assets/card_acel_small_frame_2.png'))
            # self.image = pygame.transform.scale(self.image, (245*scale_card, 300*scale_card))
            self.color = (239, 168, 80)
            self.click_sound = pygame.mixer.Sound(asset_path( 'assets/mixer/card_choice.wav'))
        else:
            self.image = pygame.image.load(asset_path( 'assets/card_geral_small_frame_2.png'))
            # self.image = pygame.transform.scale(self.image, (245*scale_card, 300*scale_card))
            self.color = (21, 122, 171)
            self.click_sound = pygame.mixer.Sound(asset_path( 'assets/mixer/card_choice.wav'))

        self.rect = self.image.get_rect()

        CARD_TOP = 325
        CARD_LEFT = 75
        CARD_SPACING = 10

        self.rect.top = CARD_TOP
        self.rect.left = CARD_LEFT + (self.carta - 1) * (self.rect.width + CARD_SPACING)

        self.linha_font = pygame.font.SysFont('calibri', 42, bold=True)
        self.wrapped_text = self.wrap_text(str(linha), self.linha_font, max_width=(self.rect.width - 45))
        self.linha_text = [self.linha_font.render(line, True, self.color) for line in self.wrapped_text]

        self.value_font = pygame.font.SysFont('calibri', 32)
        self.value_text = self.value_font.render(str(valor) + ".000R$", True, self.color)

        # Calculate the center position of the card
        center_x = self.rect.width // 2
        center_y = self.rect.height // 2

        # Calculate the total height of the text surfaces
        total_text_height = sum(line.get_height() for line in self.linha_text)

        # Calculate the starting y position for the first line
        start_y = center_y - total_text_height // 2

        # Draw the value_text 10 pixels above the center of the card
        value_pos = ((self.rect.width - self.value_text.get_width()) // 2, center_y - self.value_text.get_height() // 2 + 15)
        self.image.blit(self.value_text, value_pos)

        #Draw the product name on top of the value. The product name should not have more than 3 lines.
        #this part of the code is designed so the center of the texts are aligned vertically

        altura_inicial = 20
        n_linhas = len(self.linha_text)
        h_add = 0.5*(3-n_linhas)

        for i, line in enumerate(self.linha_text):
            linha_pos = ((self.rect.width - line.get_width()) // 2, altura_inicial + h_add*line.get_height() + i * line.get_height())
            self.image.blit(line, linha_pos)


    def update(self):
        pass

    def wrap_text(self, text, font, max_width):
        """
        A simple way to wrap text in Pygame. Splits the text into words, then adds one word at a time to the
        lines until the width of the next word would make the line too long.
        """
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_line_width = font.size(test_line)[0]
            if test_line_width < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines

class Travel_Button(pygame.sprite.Sprite):
    """A class to model a selectable card"""

    def __init__(self, game, action_name, sprite_name, positions_list, button_size, background_color):
        """Initizalize the card"""
        self.folder = 'assets/UI/'
        self.i = 0
        self.background_color = background_color
        self.sprite_name = sprite_name
        self.button_size = button_size
        self.positions_list = positions_list
        self.position = positions_list[self.i]
        self.image = pygame.image.load(asset_path( self.folder + sprite_name +"_" + str(self.position) + ".png"))
        self.image = pygame.transform.scale(self.image, button_size)
        self.game = game
        self.action = action_name
        super().__init__()
        self.rect = self.image.get_rect()

    def draw_button(self):
        display_surface.blit(self.image, self.rect)

    def animate(self):
        for pos in (self.positions_list+self.positions_list[-2::-1]):
            self.image = pygame.image.load(asset_path( self.folder + self.sprite_name +"_" + str(pos) + ".png"))
            self.image = pygame.transform.scale(self.image, self.button_size)
            pygame.draw.rect(display_surface, self.background_color, self.rect)
            display_surface.blit(self.image, self.rect)
            pygame.display.update()
            time.sleep(0.02)

    def run_action(self):
        getattr(self.game, self.action)()

    def click_script(self):
        self.animate()
        pygame.mixer.Sound(asset_path('assets/mixer/button_click.wav')).play()
        time.sleep(2)  # Insert a 2-second delay
        self.run_action()

class Old_Budget(pygame.sprite.Sprite):
    """Uma Classe para colocarmos nossas barras de atingimento individual"""
    def __init__(self, linha, peso, meta, posicao,venda):
        """Inicir meta"""
        global bonus_board_rect
        super().__init__()
        self.linha = linha
        self.peso = peso
        self.meta = meta
        self.venda = 0
        self.posicao = posicao
        self.atingimento = self.venda/self.meta
        self.barra_atual = 0
        self.valor_texto_atual = 0
        self.atingimento_texto_atual = 0
        self.growing = False
        #self.draw_self()
        self.velocity = 5

        self.update_main_rect()

    def update_main_rect(self):
        # Create a transparent surface
        self.image = pygame.Surface((330, 52), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        #Position the rect based on the position of the product line (currently goes from haviest to lightest)
        self.rect.topleft = (bonus_board_rect.left + 60, bonus_board_rect.top + 80 + self.posicao * (self.rect.height))

        #exp bar frame goes on the bottom left of the rect
        self.exp_bar_frame = pygame.image.load(asset_path( 'assets/exp_bar.png'))
        self.exp_bar_frame_rect = self.exp_bar_frame.get_rect()
        self.exp_bar_frame_rect.bottomleft = (0, self.rect.height)

        #peso bar frame goes right beside the exp bar
        self.peso_bar_frame = pygame.image.load(asset_path( 'assets/peso_bar.png'))
        self.peso_bar_frame_rect = self.peso_bar_frame.get_rect()
        self.peso_bar_frame_rect.bottomleft = (self.exp_bar_frame_rect.right + 7, self.exp_bar_frame_rect.bottom)


    def draw_growth_bar(self):
        pygame.draw.rect(
            self.image, 
            (255,150,64),                          #Color
            rect = (
                self.exp_bar_frame_rect.left,                  #top-left x
                self.exp_bar_frame_rect.top,                  #top-left y
                self.barra_atual,  #width
                self.exp_bar_frame_rect.height #height
            )
        )

    def update_exp_bar_old(self):
        #Update the growing values in the bars
        if self.valor_texto_atual < self.venda and (player_1_running == False and player_2_running == False):
            self.valor_texto_atual += 2

        if self.valor_texto_atual > self.venda and (player_1_running == False and player_2_running == False):
            self.valor_texto_atual -= 1
        
        self.atingimento_texto_atual = self.valor_texto_atual/self.meta

        #We check where should be positioned to see if our bar should grow. The limit is 120% of atingimento
        #Which will be at the limit of our exp_bar_frame width
        if self.atingimento >= 1.2:
            self.posicao_devida = 1.2*(self.exp_bar_frame_rect.width/1.2)
        else:
            self.posicao_devida = self.atingimento*(self.exp_bar_frame_rect.width/1.2)

        ##finally, we grow the value of the barra_atual
        if self.barra_atual < self.posicao_devida and (player_1_running == False and player_2_running == False):
            self.barra_atual += self.velocity
            if self.growing == False:
                    self.growing = True
        else:
            self.growing = False

        if self.barra_atual > self.posicao_devida:
            self.barra_atual = self.posicao_devida

    def update_texts(self):
        global bonus_board_rect

        """
        For each product line, we will create a template that will go as follows:

        Name of the line                                       Peso
         _____________________________________________    _____________
        |current sales / target sales  ->   % reached |  | weight in % |
         ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞    ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞
        """

        WRITING_OLD_BONUS_COLOR = (62, 40, 50)
        # Update the text font
        self.font = pygame.font.Font(asset_path('assets/joystix.otf'), 18)
        self.linha_text = self.font.render(str(self.linha), True, WRITING_OLD_BONUS_COLOR)
        self.linha_rect = self.linha_text.get_rect()
        self.linha_rect.bottomleft = (self.exp_bar_frame_rect.left, self.exp_bar_frame_rect.top+3)

        #We will start from the right to the left, to acomodate 0, 10s and 100s in the values
        self.perc_text = self.font.render("{:.0%}".format(self.atingimento_texto_atual), True, WRITING_OLD_BONUS_COLOR)
        self.perc_rect = self.perc_text.get_rect()
        self.perc_rect.centery = self.exp_bar_frame_rect.centery
        self.perc_rect.right = self.exp_bar_frame_rect.right-13

        self.meta_text = self.font.render(str(self.meta) + " ->", True, WRITING_OLD_BONUS_COLOR)
        self.meta_rect = self.meta_text.get_rect()
        self.meta_rect.centery = self.exp_bar_frame_rect.centery
        self.meta_rect.right = self.exp_bar_frame_rect.right-81

        self.venda_text = self.font.render(str(self.valor_texto_atual) + "/", True, WRITING_OLD_BONUS_COLOR)
        self.venda_rect = self.venda_text.get_rect()
        self.venda_rect.centery = self.exp_bar_frame_rect.centery
        self.venda_rect.right = self.exp_bar_frame_rect.right-170

        self.peso_text = self.font.render("{:.0%}".format(self.peso), True, WRITING_OLD_BONUS_COLOR)
        self.peso_rect = self.peso_text.get_rect()
        self.peso_rect.center = self.peso_bar_frame_rect.center

    def update(self):
        #Create green bar on image
        global player_1_running
        global player_2_running

        self.atingimento = self.venda/self.meta

        self.update_main_rect()
        self.update_exp_bar_old()
        self.update_texts()

        # Draw the text on the image
        self.draw_growth_bar()
        self.image.blit(self.linha_text, self.linha_rect)
        self.image.blit(self.perc_text, self.perc_rect)
        self.image.blit(self.meta_text, self.meta_rect)
        self.image.blit(self.venda_text, self.venda_rect)
        self.image.blit(self.exp_bar_frame, self.exp_bar_frame_rect)
        self.image.blit(self.peso_bar_frame, self.peso_bar_frame_rect)
        self.image.blit(self.peso_text, self.peso_rect)

        # Blit the image onto the display surface
        # display_surface.blit(self.image, self.rect)

class New_Budget(pygame.sprite.Sprite):
    """Uma Classe para colocarmos as barras de atingimento de acelerador e Geral"""
    def __init__(self, Acelerador_ou_Geral, peso, meta, posicao, char_icon):
        """Inicir meta"""
        global bonus_novo_board_rect
        super().__init__()
        self.linha = Acelerador_ou_Geral
        self.peso = peso
        self.meta = meta
        self.venda = 0
        self.posicao = posicao
        self.atingimento = self.venda/self.meta
        self.barra_atual = 0
        self.valor_texto_atual = 0
        self.atingimento_texto_atual = 0
        self.growing = False
        self.velocity = 5
        self.char_icon = char_icon
        self.update_main_rect()

    def update_main_rect(self):
        # Create a transparent surface
        self.image = pygame.Surface((316, 120), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        #Position the rect based on the position of the product line (currently goes from haviest to lightest)
        self.rect.topleft = (bonus_novo_board_rect.left + 39, bonus_novo_board_rect.top + 75 + self.posicao * (self.rect.height))

        #exp bar frame goes on the bottom left of the rect
        self.exp_bar_frame = pygame.image.load(asset_path('assets/exp_bar_new_model.png'))
        self.exp_bar_frame_rect = self.exp_bar_frame.get_rect()
        self.exp_bar_frame_rect.bottomleft = (0, self.rect.height)

        self.peso_bar_frame = pygame.image.load(asset_path('assets/peso_new_model.png'))
        self.peso_bar_frame_rect = self.peso_bar_frame.get_rect()
        self.peso_bar_frame_rect.bottomleft = (self.exp_bar_frame_rect.right + 8, self.exp_bar_frame_rect.bottom)

        self.player_icon = self.char_icon
        self.player_icon_rect = self.player_icon.get_rect()
        self.player_icon_rect.bottomleft = (self.exp_bar_frame_rect.left, self.exp_bar_frame_rect.top)

    def draw_growth_bar(self):
        pygame.draw.rect(
            self.image, 
            (255,150,64),                          #Color
            rect = (
                self.exp_bar_frame_rect.left,                  #top-left x
                self.exp_bar_frame_rect.top,                  #top-left y
                self.barra_atual,  #width
                self.exp_bar_frame_rect.height #height
            )
        )

    def update_exp_bar_old(self):
        
        #Update the growing values in the bars
        if self.valor_texto_atual < self.venda and (player_1_running == False and player_2_running == False):
            self.valor_texto_atual += 2

        if self.valor_texto_atual > self.venda and (player_1_running == False and player_2_running == False):
            self.valor_texto_atual -= 1
        
        self.atingimento_texto_atual = self.valor_texto_atual/self.meta

        #We check where should be positioned to see if our bar should grow. The limit is 120% of atingimento
        #Which will be at the limit of our exp_bar_frame width
        if self.atingimento >= 1.2:
            self.posicao_devida = 1.2*(self.exp_bar_frame_rect.width/1.2)
        else:
            self.posicao_devida = self.atingimento*(self.exp_bar_frame_rect.width/1.2)

        ##finally, we grow the value of the barra_atual
        if self.barra_atual < self.posicao_devida and (player_1_running == False and player_2_running == False):
            self.barra_atual += self.velocity
            if self.growing == False:
                    self.growing = True
        else:
            self.growing = False

        if self.barra_atual > self.posicao_devida:
            self.barra_atual = self.posicao_devida

    def update_texts(self):
        global bonus_board_rect

        """
        For each product line, we will create a template that will go as follows:

        Name of the line                                       Peso
         _____________________________________________    _____________
        |current sales / target sales  ->   % reached |  | weight in % |
         ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞    ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞ ͞
        """

        WRITING_NEW_BONUS_COLOR = (58, 68, 102)
        # Update the text font
        self.font = pygame.font.Font(asset_path('assets/joystix.otf'), 18)
        self.title_font = pygame.font.Font(asset_path('assets/joystix.otf'), 30)
        #Nesse caso, a "linha" vai se chamar ACELERADOR ou GERAL
        self.linha_text = self.title_font.render(str(self.linha), True, WRITING_NEW_BONUS_COLOR)
        self.linha_rect = self.linha_text.get_rect()
        self.linha_rect.bottomleft = (self.exp_bar_frame_rect.left+68, self.exp_bar_frame_rect.top-3)

        #We will start from the right to the left, to acomodate 0, 10s and 100s in the values
        self.perc_text = self.font.render("{:.0%}".format(self.atingimento_texto_atual), True, WRITING_NEW_BONUS_COLOR)
        self.perc_rect = self.perc_text.get_rect()
        self.perc_rect.centery = self.exp_bar_frame_rect.centery
        self.perc_rect.right = self.exp_bar_frame_rect.right-15

        self.meta_text = self.font.render(str(self.meta) + ">", True, WRITING_NEW_BONUS_COLOR)
        self.meta_rect = self.meta_text.get_rect()
        self.meta_rect.centery = self.exp_bar_frame_rect.centery
        self.meta_rect.right = self.exp_bar_frame_rect.right-73

        self.venda_text = self.font.render(str(self.valor_texto_atual) + "|", True, WRITING_NEW_BONUS_COLOR)
        self.venda_rect = self.venda_text.get_rect()
        self.venda_rect.centery = self.exp_bar_frame_rect.centery
        self.venda_rect.right = self.exp_bar_frame_rect.right-145

        self.peso_text = self.font.render("{:.0%}".format(self.peso), True, WRITING_NEW_BONUS_COLOR)
        self.peso_rect = self.peso_text.get_rect()
        self.peso_rect.center = self.peso_bar_frame_rect.center

    def update(self):
        #Create green bar on image
        global player_1_running
        global player_2_running

        self.atingimento = self.venda/self.meta

        self.update_main_rect()
        self.update_exp_bar_old()
        self.update_texts()

        # Draw the text on the image
        self.draw_growth_bar()
        self.image.blit(self.linha_text, self.linha_rect)
        self.image.blit(self.perc_text, self.perc_rect)
        self.image.blit(self.meta_text, self.meta_rect)
        self.image.blit(self.venda_text, self.venda_rect)
        self.image.blit(self.exp_bar_frame, self.exp_bar_frame_rect)
        self.image.blit(self.player_icon, self.player_icon_rect)
        self.image.blit(self.peso_bar_frame, self.peso_bar_frame_rect)
        self.image.blit(self.peso_text, self.peso_rect)

        # Blit the image onto the display surface
        # display_surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    """Uma Classe para colocarmos o jogador principal"""
    def __init__(self, sex, skin, peso, meta, init_x):
        """Inicir meta"""
        super().__init__()

        self.sex_sigla = sex

        if self.sex_sigla == "M":
            self.sex = "Male"
        else:
            self.sex = "Female"
        
        self.skin = skin #"Skin 1, 2 ou 3"
        self.clothes = 1 #Por enquanto vamos deixar a opção de Clothes como 1 apenas"
        self.peso = peso
        self.meta = meta
        self.vendas = 0
        #self.vendas = 800 ##para testes
        self.atingimento = self.vendas/self.meta
        self.sprite_position = 1
        self.velocity = 0
        self.start_y_pos = 1000
        self.sprite_float_delta = 1

        """This dictonary has the possible medals as keys
        
        the first value is the percentage of target necessary to achieve the medal
        the second value is wether or not the player already have the medal
        """
        self.medal_dict={
            "silver":   [0.5, False, False],
            "gold":     [1.0, False, False],
            "diamond":  [1.2, False, False]
        }

        #region Create sprite action dictionary self.image_dict{}
        """Here we will look into the folder with the character sprites
        all the sprites are named as exampled:
        Character2F_1_idle_0
        Character2F_2_idle_1
        Character3M_1_run_0

        so we will create a dictionary that will have the keys as the sprite action, and the values will be the image itself
        self.image_dict{
            "idle_0": image,
            "run_1": image,
            ...
        }
        """
        self.folder = asset_path('assets/Main_chars/'+self.sex+"/Character "+str(skin)+"/Clothes "+str(self.clothes)+"/")
        self.char_key_name = "Character" + str(self.skin) + self.sex_sigla + "_" + str(self.clothes) + "_"
        self.upscale = 5
        self.action_sprites = [
            "idle", "walk", "talk", "run", 
            "car_idle", "car_running", 
            "silver_medal_get", "gold_medal_get", "diamond_medal_get",
            "silver_medal_hold", "gold_medal_hold", "diamond_medal_hold"
            ]
        self.gui_icon = pygame.image.load(asset_path('assets/Main_chars/'+self.sex+"/Character "+str(skin)+"/Clothes "+str(self.clothes)+"/"+"Icon.png"))
        self.image_dict = {}
        for action in self.action_sprites:
            initial_sprite_name = self.char_key_name + action + "_"
            # for example, it could be "/assets/Main_Chars/Female/Character 2/Clothes 1/Character2F_1_idle_"

            # Get a list of all files in the self.folder directory
            files = os.listdir(self.folder)

            # Filter the list to include only PNG files that start with initial_sprite_name
            png_files = [file for file in files if file.startswith(initial_sprite_name) and file.endswith(".png")]

            # Load and transform the images
            for i, png_image in enumerate(png_files):
                loaded_image = pygame.image.load(os.path.join(self.folder, png_image))
                transformed_image = pygame.transform.scale(
                    loaded_image, 
                    (loaded_image.get_width()*self.upscale, loaded_image.get_height()*self.upscale)
                )
                key = f"{action}_{i}"
                self.image_dict[key] = transformed_image
        #endregion

        ## Change 30/01 - new animation sprite is "car_idle"
        self.action = "car_idle"
        self.sprite_position = 0
        self.image = self.image_dict[self.action+"_" +str(self.sprite_position)]
        self.rect = self.image.get_rect()
        self.rect.bottom = self.start_y_pos
        self.rect.centerx = init_x
        self.sprite_float_position = 0
        self.atingimento = self.vendas / self.meta
        self.medal_winning = False

    def animation_loop(self):
        """loop between the sprites of the current animation"""
        # We count how many sprites we have for the current animation
        # For example, the idle animation goes from idle_0 till idle_7
        # while the run animation goes from run_0 till run_9

        # So first we need to filter the dict with only the keys that start with the current animation name
        self.sprite_filtered_dict = {k: v for k, v in self.image_dict.items() if k.startswith(self.action)}
        
        # If we are in the last sprite position, return to sprite_0
        if int(self.sprite_float_position) >= len(self.sprite_filtered_dict)-1:
            self.sprite_float_position = 0
        else:
            self.sprite_float_position += self.sprite_float_delta

        self.sprite_position = int(self.sprite_float_position)
                
        self.image = self.image_dict[self.action + "_" + str(self.sprite_position)]
        #self.rect = self.image.get_rect()
        #self.rect.bottom = self.start_y_pos

    def update(self):
        """Player_Position"""
        global player_1_running
        global player_2_running
        global bar_filling
        
        position_zero_x = 298
        position_100_x = 1555
        position_120_x = 1879
        PLAYER_VELOCITY = 10
        x_por_porcentagem = (position_100_x - position_zero_x)

        self.atingimento = self.vendas / self.meta

        #Checking where we should be right now
        if self.atingimento > 1.2:
            self.posicao_devida = position_120_x
        else:
            self.posicao_devida = int(position_zero_x + self.atingimento * x_por_porcentagem)

        #checking where we are
        #18pixels é o espaço entre o limite direito do sprite e a ponta do carro
        self.posicao_atual = (self.rect.right-18*self.upscale)

        #Prioridade de animações
        #1 - O player atingiu 50% ou 100% ou 120% e vai ganhar uma medalha
        ## ESSES VALORES FORAM ALTERADOS PARA PRESERVAR A ESTRATÉGIA DA SGA
        for medal, value in self.medal_dict.items():
            percentage = value[0]
            is_achieved = value[1]
            board_shown = value[2]
            min_position_to_medal = int(position_zero_x + x_por_porcentagem*percentage)

            #Condições para ganhar a medalha
            # 1)o player não ganhou ainda a medalha 
            # 2)E sua posição no jogo atual é maior ou igual ao mínimo necessário para o ganho
            if is_achieved == False and self.posicao_atual >= min_position_to_medal:

                #start the animation
                if self.medal_winning == False:
                    self.medal_winning = True
                    self.board_shown = False
                    self.sprite_position = 0  # Set to 0.0 instead of 1.0
                    self.sprite_float_position = 0  # Set to 0.0 instead of 1.0
                    self.sprite_float_delta = 1
                    self.velocity = 0
                    self.action = str(medal) + "_medal_get"
                
                ##position to show the medal board
                elif (self.medal_winning == True) and (self.sprite_float_position >= 6) and board_shown == False:
                    
                    self.medal_dict[medal][2] = True #So that we do not enter in the same board twice

                    #Load the board image
                    board_image = pygame.image.load(asset_path('assets/placa_atingimento_'+ medal + ".png"))
                    board_rect = board_image.get_rect()
                    board_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

                    #Load the player action
                    board_player_action = medal + "_medal_hold"

                    #filtered dict with medal hold action
                    board_sprite_filtered_dict = {k: v for k, v in self.image_dict.items() if k.startswith(board_player_action)}
                    
                    #start sprite frame position and speed of change
                    board_sprite_float_position = 0
                    board_sprite_float_delta = 0.1
                    self.medal_sound = pygame.mixer.Sound(asset_path('assets/mixer/medal_get.wav'))
                    self.medal_sound.play()
                    in_medal_board = True
                    while in_medal_board:
                        #check for board_quit:
                        for event in pygame.event.get():
                            if (event.type == pygame.MOUSEBUTTONDOWN):
                                in_medal_board = False #quit the board and continue the game
                                break  # break out of the while loop
                                
                        #if stays in board, update the display
                        #updating the player board sprite
                        if int(board_sprite_float_position) >= len(board_sprite_filtered_dict)-1:
                            board_sprite_float_position = 0
                        else:
                            board_sprite_float_position += board_sprite_float_delta

                        board_sprite_position = int(board_sprite_float_position)
                        board_player_image = board_sprite_filtered_dict[board_player_action + "_" + str(board_sprite_position)]
                        board_player_rect = board_player_image.get_rect()
                        board_player_rect.centery = board_rect.centery
                        board_player_rect.left = board_rect.left + 46

                        #blit the board and the player image


                        my_Main_Player.draw(display_surface)
                        my_card_group.draw(display_surface)
                        my_Second_Player.draw(display_surface)
                        my_old_budget_group.draw(display_surface)
                        my_new_budget_group.draw(display_surface)
                        display_surface.blit(board_image, board_rect)
                        display_surface.blit(board_player_image, board_player_rect)
                        pygame.display.update()
                        clock.tick(FPS)

                elif self.medal_winning == True and self.sprite_float_position == 0:
                    self.medal_dict[medal][1] = True
                    self.medal_winning = False
                    self.action = "car_idle"
                    self.sprite_float_position = 0  # Set to 0.0 instead of 1.0

        #2 - Checar se o player deve andar ou ficar parado se não estivermos ganhando medalha
        if self.medal_winning == False:
            #Checar se devemos andar
            if self.vendas > 0 and  self.posicao_atual < self.posicao_devida:
                #se o carro ainda não estiver andando, vamos para o sprite position 1
                if self.action != "car_running":
                    self.sprite_float_position = 1
                    self.sprite_float_delta = 1
                
                #se o carro já estiver andando, mantemos o sprite position
                self.action ="car_running"
                self.sprite_float_delta = 1
                self.velocity = PLAYER_VELOCITY
                player_1_running = True
            
            else:
                if self.action != "car_idle":
                    self.sprite_float_position = 1 

                self.action = "car_idle"
                self.sprite_float_delta = 1
                self.velocity = 0
                player_1_running = False

        #rodar o loop 
        self.animation_loop()
        self.rect.left += self.velocity

class Player_2(pygame.sprite.Sprite):
    """Uma Classe para colocarmos o jogador principal"""
    def __init__(self, type, peso, meta, init_x):
        """Inicir meta"""
        super().__init__()
        self.type = type #"Dog" ou "Cat"

        self.peso = peso
        self.meta = meta
        self.vendas = 0
        self.atingimento = self.vendas/self.meta
        self.velocity = 0
        self.start_y_pos = 841
        self.folder = 'assets/Companion/Approved/' + self.type + "/"
        self.image_dict = {}

        self.gui_icon = pygame.image.load(asset_path( self.folder+"Icon.png"))

        self.action_sprites_frames = {"car_idle":24,"car_running":4}
        self.upscale = 4
        for action, frames in self.action_sprites_frames.items():
            self.get_image_into_dictionary(action, frames)

        self.action = "car_idle"
        self.sprite_position = 1
        self.image = self.image_dict[self.action+"_" +str(self.sprite_position)]

        self.rect = self.image.get_rect()
        self.rect.bottom = self.start_y_pos
        self.rect.centerx = init_x
        
        self.frame_counter = 0
        self.atingimento = self.vendas / self.meta

    def get_image_into_dictionary(self, action, n_frames):
        """
        This is similar to the main player case, but here the player 2 have sprite_sheets instead of individual sprites
    
        """
        #load the horizontal image sheet
        self.sprite_sheet = pygame.image.load(asset_path( self.folder + action +".png")).convert_alpha()

        #Define the sizes of each sprite
        self.sprite_width = self.sprite_sheet.get_width()/n_frames
        self.sprite_height = self.sprite_sheet.get_height()
        
        for frame in range(n_frames):
            #if there are 4 frames, we will create the action_0, action_1, action_2 and action_3 frame
            #Create a transparent background the size of the desired sprite
            sprite_background = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)

            #blit the portion of the spritesheet
            sprite_background.blit(
                self.sprite_sheet, 
                (0,0), 
                ((frame * self.sprite_width, 0, self.sprite_width, self.sprite_height))#here if frame = 0, we start at width 0, if frame =1, we start at the second sprite
            )

            #now we scale the image if needed
            transformed_image = pygame.transform.scale(
                sprite_background,
                (self.sprite_width*self.upscale, self.sprite_height*self.upscale)
            )

            #finally we add the sprite to our animation dictionary
            key = f"{action}_{frame}"
            self.image_dict[key] = transformed_image

    def animation_loop(self):
        """loop between the sprites of the current animation"""
        # We count how many sprites we have for the current animation
        # For example, the idle animation goes from idle_0 till idle_7
        # while the run animation goes from run_0 till run_9
        # So first we need to filter the dict with only the keys that start with the current animation name
        self.sprite_filtered_dict = {k: v for k, v in self.image_dict.items() if k.startswith(self.action)}
        # If we are in the last sprite position, return to sprite_0
        if self.sprite_position >= len(self.sprite_filtered_dict)-1:
            self.sprite_position = 1
        else:
            self.sprite_position += 1
                
        self.image = self.image_dict[self.action + "_" + str(self.sprite_position)]
        #self.rect = self.image.get_rect()
        #self.rect.bottom = self.start_y_pos

    def update(self):
        """Player_Position"""
        global player_1_running
        global player_2_running
        global bar_filling

        position_zero_x = 145
        position_100_x = 1408
        position_120_x = 1732
        self.init_PLAYER_VELOCITY = 10
        x_por_porcentagem = (position_100_x - position_zero_x)
        self.atingimento = self.vendas / self.meta
        self.posicao_devida = int(position_zero_x + self.atingimento * x_por_porcentagem)

        #Checar se devemos andar
        if player_1_running == False and self.vendas > 0 and (self.rect.right-18*self.upscale) < self.posicao_devida and (self.rect.right-18*self.upscale) < position_120_x:
            player_2_running = True
            self.action ="car_running"
            self.velocity = self.init_PLAYER_VELOCITY
        else:
            player_2_running = False
            self.action = "car_idle"
            self.velocity = 0

        if self.action == 'car_running':
            self.fps_round_num = 1
        else:
            self.fps_round_num = 1

        # Update sprite every 1 frames
        if self.frame_counter % self.fps_round_num == 0:
            self.animation_loop()
            # Update position
            self.rect.left += self.velocity
        self.frame_counter += 1

#endregion

#starting game parameters
player_1_running = False
player_2_running = False
bar_filling = False
clicking_enabled = True

#creating sprite groups
my_Main_Player = pygame.sprite.Group()
my_Second_Player = pygame.sprite.Group()
my_card_group = pygame.sprite.Group()
my_old_budget_group = pygame.sprite.Group()
my_new_budget_group = pygame.sprite.Group()
my_char_selection_group = pygame.sprite.Group()

#including all the sprite groups in the game class
my_game = Game(my_card_group, my_Main_Player, my_Second_Player, my_old_budget_group, my_new_budget_group, my_char_selection_group)

#region Define images

background_image = pygame.image.load(asset_path( 'assets/racing_background.png'))
background_image = pygame.transform.scale(background_image, (1920,1080))
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

scroll_image = pygame.image.load(asset_path( 'assets/game_board.png'))
scroll_rect = scroll_image.get_rect()
scroll_rect.topleft = (25,25)

#Bonus board old model
bonus_board_image = pygame.image.load(asset_path( 'assets/modelo_antigo.png'))
bonus_board_rect = bonus_board_image.get_rect()
bonus_board_rect.top = scroll_rect.top
bonus_board_rect.left = scroll_rect.right + 10

#Bonus board mnew model
bonus_novo_board_image = pygame.image.load(asset_path( 'assets/modelos_bonus_novo.png'))
bonus_novo_board_rect = bonus_novo_board_image.get_rect()
bonus_novo_board_rect.topleft = (bonus_board_rect.right + 10, bonus_board_rect.top)

final_bonus_image = pygame.image.load(asset_path( 'assets/bonus_board.png'))
final_bonus_rect = final_bonus_image.get_rect()
final_bonus_rect.top = bonus_novo_board_rect.bottom-41
final_bonus_rect.left = bonus_board_rect.right-51

#endregion

#region - Game start and loop
my_game.start_menu()

## Main Game Loop
running = True
while running:
    #check for game events (clicks):
    for event in pygame.event.get():
        #Check if player wants out
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN) and clicking_enabled:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            my_game.check_for_card_selection(mouse_x, mouse_y)

    clicking_enabled = my_game.enable_click()

    #Update and draw game object
    my_game.update()
    my_game.draw()

    #Update and display all sprite groups
    my_card_group.update()
    my_card_group.draw(display_surface)

    my_Main_Player.update()
    my_Main_Player.draw(display_surface)

    my_Second_Player.update()
    my_Second_Player.draw(display_surface)

    my_old_budget_group.update()
    my_old_budget_group.draw(display_surface)

    my_new_budget_group.update()
    my_new_budget_group.draw(display_surface)

    #Update display
    pygame.display.update()
    clock.tick(FPS)

#endregion

#Quit Game
pygame.quit()
