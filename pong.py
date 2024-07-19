from tkinter import Tk, Canvas, PhotoImage, Label, Frame, Button, Entry, StringVar, messagebox, Event, IntVar
from random import random, randint, choice
import time
global player_score, player_lives, WIDTH, HEIGHT, paddle_left_pos, paddle_right_pos
global ball_speed_x, ball_speed_y
from PIL import Image, ImageTk

class Frames():
    def __init__(self, window):
        
        
        self.window = window
        self.window.title("P I N G   P O N G")
        self.window.geometry("1200x720")
        self.window.resizable(False,False)
        self.WIDTH = 1200
        self.HEIGHT = 720
         
        
        # Player Name
        self.player_name = StringVar()
        self.x = self.WIDTH//2
        self.y = self.HEIGHT//2
         
        # Player Score 
        self.player_score = 0
         
        # Player Lives
        self.player_lives = 5
        self.player_info = [self.player_name, self.player_score, self.player_lives]
        
        self.count = 0
        # Initial Ball Speed
        self.ball_speed_x = 3
        self.ball_speed_y = 3
        
        self.time_left = 180
        self.minute = self.time_left//60
        self.second = self.time_left%60
        
        self.hit_paddle = False
        self.ball_dead = False
        self.balls = []
        self.time_delay = 6000
        
        # Landing Frame
        self.Landing_Frame = Canvas(window, width=self.WIDTH, height=self.HEIGHT, background='#040348')
        self.Landing_Frame.pack(expand=True, fill='both')
        self.title = Label(self.Landing_Frame, text ='TechSpin Ping Pong', font = ('Helvetica', 60),width=50,background='#040348',fg='#FFFFFF')
        self.title.grid(column = 0, row = 0, padx=20, pady=20)
        
        # Landing Frame Buttons
        self.Landing_Frame.grid_columnconfigure(0, weight=1)
        self.btn1 = Button(self.Landing_Frame, text='Start Game', font=('Arial Bold', 18),relief='raised', borderwidth=7,width=15, height=2, command=self.landing_to_name)
        self.btn1.grid(column=0, row=1, pady=15)
    
        self.btn2 = Button(self.Landing_Frame, text='Instructions', font=('Arial Bold', 18), relief='raised', borderwidth=7,width=15, height=2, command=self.Execute_Instructions)
        self.btn2.grid(column=0, row=2, pady=15)

        self.btn3 = Button(self.Landing_Frame, text='Leaderboard', font=('Arial Bold', 18),relief='raised', borderwidth=7, width=15, height=2, command=self.Execute_Leaderboard)
        self.btn3.grid(column=0, row=3, pady=15)
        
        
        
        
        
        # Instructions Frame
        self.Instruction_Frame = Canvas(window, width=self.WIDTH, height=self.HEIGHT, background='#040348')
        
        # Creating an Instruction Label
        self.Label_instruction1 = Label(self.Instruction_Frame, text='Instructions', font = ('Helvetica', 60),width=50,background='#040348',fg='#FFFFFF')
        self.Label_instruction1.pack(pady=12.5)
        self.instruction1 = Label(
        self.Instruction_Frame,
        text='Welcome to TechSpin Pong!\n\nTASK:\n1. Get 10 point for turning every \nping pong ball you hit with your paddle \nfrom white to blue.\n2. You have 5 lives and 3 minutes.\n3. Every time you miss the ball,\n you lose a lives.\n4. Game ends when you lose all your lives\nCHEATS:\n1. Press <i> to increase paddle size\n2. Press <d> to decrease ball speed\n3. Press <s> to add a Live\n4. Hit <q> followed by <c>,\n and see what it does!', 
        font=('Arial Bol',18),
        relief='sunken',
        justify='center',
        width=35, 
        height=18)
        self.instruction1.pack(pady=12.5)

        # Instruction Buttons
        self.buttonFrame1 = Frame(self.Instruction_Frame, background='#040348')
        self.buttonFrame1.columnconfigure(0, weight=1)
        self.buttonFrame1.columnconfigure(1, weight=1)
        self.buttonFrame1.pack(fill='x')

        self.Back_Button1 = Button(self.buttonFrame1, text='Back', font = ('Arial Bold', 18),  relief='raised', borderwidth=7, width=1, command=self.instruction_to_landing)
        self.Back_Button1.grid(column=0, row=0, sticky='WE', padx=20)

        self.Start_Button = Button(self.buttonFrame1, text='Start Game', font = ('Arial Bold', 18),  relief='raised', borderwidth=7, width=1,command=self.instructions_to_name )
        self.Start_Button.grid(column=1, row=0, sticky='WE', padx=20)

        

        # LeaderBoard Frame
        self.Leaderboard_frame = Canvas(window, width=self.WIDTH, height=self.HEIGHT, background='#040348')

        # Leadership Label
        self.Label_leaderboard = Label(self.Leaderboard_frame, text='LeaderBoard', font = ('Helvetica', 60),width=50,background='#040348',fg='#FFFFFF')
        self.Label_leaderboard.pack(pady=10)
        self.lead = ''
        self.leaderboard_data = self.read_data()
        for i,entry in enumerate(self.leaderboard_data):
            self.lead = self.label + f'#{i + 1}: {entry[0]}  - Score: {entry[1]}'
        self.leaderboard = Label(
            self.Leaderboard_frame,
            text=self.lead, 
            font=('Arial Bol',18),
                  relief='sunken',
            justify='center',
            width=35, 
            height=10
            )
        self.leaderboard.pack(pady=10)

        # Button for Leadership Page
        self.Back_Button2 = Button(self.Leaderboard_frame, text='Back', font = ('Arial Bold', 18),  relief='raised', borderwidth=7, command=self.leaderboard_to_landing)
        self.Back_Button2.pack(pady=10)


        
        # Name Page
        self.Asking_name = Canvas(window, width=self.WIDTH, height=self.HEIGHT, background='#040348')
        
        # Asking Name Label
        self.Ask_name_label = Label(self.Asking_name, text='Ready!', font = ('Helvetica', 60),width=50,background='#040348',fg='#FFFFFF')
        self.Ask_name_label.pack(pady=10)
        
        # Organizing Labels, Entry, and Button
        self.Name_frame = Frame(self.Asking_name, background='#040348')
        self.Name_frame.columnconfigure(0,weight=1)
        self.Name_frame.columnconfigure(1, weight=1)
        self.Name_frame.pack(fill='x', pady=70)

        self.Ask_name_label = Label(self.Name_frame, text='Enter Your name: ', font=('Arial Bold', 20), background='#040348', fg='#FFFFFF')
        self.Ask_name_label.grid(column=0, row=0)

        self.Name_Entry = Entry(self.Name_frame, textvariable=self.player_name,font=('calibre',20,'normal'), justify='center', width=20)
        self.Name_Entry.grid(column=1, row=0)


        self.Begin_button = Button(self.Asking_name,  text='BEGIN', font = ('Arial Bold', 18),  relief='raised', borderwidth=7, command=self.name_to_game)
        self.Begin_button.pack(pady=5)
        
        # Game Screen        
        self.pong_image = PhotoImage(file='images/madar.png')
        self.boss_image = PhotoImage(file='images/boss1.png')
        self.Game_screen = Canvas(self.window,width=self.WIDTH, height=self.HEIGHT )
        self.Game_screen.create_image(0, 0, image = self.pong_image, anchor='nw')

             
        self.Score_text = self.Game_screen.create_text((self.WIDTH/6), 20, text='Score: ' + str(self.player_score),font=('Arial Bold', 20), fill='White' )
       
        self.player_lives_text = self.Game_screen.create_text((self.WIDTH/6) * 4, 20, text='Lives: ' + str(self.player_lives),font=('Arial Bold', 20), fill='White' )
        
        self.time_text = self.Game_screen.create_text((self.WIDTH/6) * 5, 20, text=f'{self.minute}:{self.second} ',font=('Arial Bold', 20), fill='Green' )
        
        self.right_paddle = self.Game_screen.create_rectangle(self.WIDTH - 30, self.HEIGHT/2 - 130/2, self.WIDTH -10, self.HEIGHT/2 + 130/2, fill='White',tags= "right_paddle")
        
        self.boss_screen = Canvas(window, width=self.WIDTH, height=self.HEIGHT)
        self.boss_screen.create_image(0,0,image = self.boss_image, anchor = 'nw')
        
        
        
        
        # Label that asks to start
        self.ask_to_start = self.Game_screen.create_text(600, 360, text='Get Ready!',font=('Arial Bold', 50), fill='Blue' )
        # Creating the Binding Functions
        self.window.bind('<Up>', self.move_right_paddle_up)
        self.window.bind('<Down>', self.move_right_paddle_down)
        self.window.bind('<Key>',self.boss)
        
        
    
    def landing_to_name(self):
        # Loading the Name Page from the Landing Page
        self.Landing_Frame.pack_forget()
        self.Asking_name.pack(expand=True,fill='both')
    
        
    def Execute_Instructions(self):
        # Loading a Instructions Page from the Landing Page
        self.Landing_Frame.pack_forget()
        self.Instruction_Frame.pack(fill='both', expand=True)   
       
       
    def Execute_Leaderboard(self):
        # Loading the leaderboard page from the Landing Page
        self.Landing_Frame.pack_forget()
        self.Leaderboard_frame.pack(fill='both', expand=True)
    
    
    
    def instruction_to_landing(self):
        # Instruction back to the Landing Page
        self.Instruction_Frame.pack_forget()
        self.Landing_Frame.pack(expand=True, fill='both')
    

    def instructions_to_name(self):
        # Instruction to Name Page
        self.Instruction_Frame.pack_forget()
        self.Asking_name.pack(expand=True,fill='both')       


    def leaderboard_to_landing(self):
        # Leaderboard to the landing page
        self.Leaderboard_frame.pack_forget()
        self.Landing_Frame.pack(expand=True, fill='both')
    
    def delete_ask_to_start(self):
        self.Game_screen.delete(self.ask_to_start)
    
    def name_to_game(self):
        # Moving From the Name to the Game (Remember to Change the Class of the Game call function)
        if self.player_name.get() != '':
            self.Asking_name.pack_forget()
            self.Game_screen.pack(expand=True, fill='both')
            self.start_game()    
        
    def move_ball_now(self, id):
        self.Game_screen.move(id[0], id[1], id[2])
        if id[3]:
            coords = self.Game_screen.coords(id[0])

        # Bounce off when hitting the top or bottom boundaries after hitting the paddle
            if coords[1] >= self.HEIGHT or coords[3] <= 0:
                id[1], id[2] = id[1], id[2]
                self.Game_screen.move(id[0], id[1], id[2])
                self.Game_screen.delete(id[0])

            # Bounce off when hitting the left boundary after hitting the paddle
            if coords[0] <= 0:
                id[1], id[2] = id[1], id[2]
                self.Game_screen.move(id[0], id[1], id[2])
                self.Game_screen.delete(id[0])

            
        elif id[4]:
            # Deleting that particular ball
            self.player_lives -= 1
            self.update_player_lives()
            self.Game_screen.delete(id[0])
            
        else:
            # if (self.hit_paddle is not True) and (self.ball_dead is not True):
            coords = self.Game_screen.coords(id[0])

        # Bounce off when hitting the top or bottom boundaries
            if coords[1] >= self.HEIGHT or coords[3] <= 0:
                id[2] = -id[2]

            overlapping_items = self.Game_screen.find_overlapping(*self.Game_screen.bbox(id[0]))
            for item in overlapping_items:
                if 'right_paddle' in self.Game_screen.gettags(item):
                    # Bounce off when hitting the paddle
                    id[1] *= -1
                    id[3] = True
                    if self.time_delay >= 1800:
                        self.time_delay -= 200
                    
                    if (self.player_score > 0) and (self.player_score % 30 == 0) and (self.ball_speed_x < 18):
                        self.ball_speed_x += 0.3
                        self.ball_speed_y += 0.3
                       
                    self.player_score += 10
                    self.update_score()
                    self.Game_screen.itemconfig(id[0], fill = 'blue')
                    break
                
            if coords[2] >= self.WIDTH:
                id[4] = True
                id[1], id[2] = id[1], id[2]
                self.Game_screen.move(id[0], id[1], id[2])
                

    def update_time(self):
        # Feature the displays the time and changes it
        if self.time_left > 0 and self.player_lives>0:
            self.time_left -= 1
            self.minute = self.time_left//60
            self.second = self.time_left%60
            self.Game_screen.itemconfig(self.time_text, text = f'{self.minute}:{self.second}')
            self.Game_screen.after(1000, self.update_time)
        else:
            pass

    def generate_ball(self):
        # Generates a ball whenever called periodically
        height = randint(0, self.HEIGHT)
        self.count += 1
        speed_x, speed_y = self.ball_speed_x, choice([-self.ball_speed_y, -self.ball_speed_y +1,0,self.ball_speed_y-1,self.ball_speed_y])
        hit_paddle, ball_dead = self.hit_paddle, self.ball_dead
        id = ['ball' + str(self.count),speed_x, speed_y,hit_paddle,ball_dead ]
        self.Game_screen.create_oval(-10, height - 10, 15, height - 35, fill='White', tags=id[0])
        self.Game_screen.after(1000, lambda: self.update_time_ball(1000, id))

    def update_time_ball(self,t, id):
        # Function that moves a single ball whenever called
        if not self.pause:
            if self.time_left > 0 and len(self.Game_screen.coords(id[0])) < 4:
                None
            elif self.time_left > 0 and self.player_lives>0:
                self.move_ball_now(id)
                self.Game_screen.after(20, lambda: self.update_time_ball(20, id))
            else:
                dead = self.Game_screen.create_text(600, 360, text='GAME OVER!\nPlease Check Leaderboard',font=('Arial Bold', 50), fill='Blue' )
            
    def update_ball(self):
        # Function that generates a ball after a certain time delay
        if not self.pause:
            if self.time_left > 0 and self.player_lives>0:
        
                self.generate_ball()
                self.Game_screen.after(self.time_delay, lambda: self.update_ball())
            else:
                dead = self.Game_screen.create_text(600, 360, text='GAME OVER!',font=('Arial Bold', 50), fill='Blue' )
                self.end_game()
    
    
        
    
    def end_game(self):
        # Function that deletes the Game_screen Frame and allows player to play again
        
        self.update_data()  
        self.Game_screen.destroy()
        self.player_lives = 5
        self.player_score = 0
        self.time_left = 180
        self.ball_speed_x = 3
        self.ball_speed_y = 3
        self.hit_paddle = False
        self.ball_dead = False
        self.balls = []
        self.time_delay = 6000
        self.count = 0
        
        self.Game_screen = Canvas(self.window,width=self.WIDTH, height=self.HEIGHT )
        self.Game_screen.create_image(0, 0, image = self.pong_image, anchor='nw')

             
        self.Score_text = self.Game_screen.create_text((self.WIDTH/6), 20, text='Score: ' + str(self.player_score),font=('Arial Bold', 20), fill='White' )
       
        self.player_lives_text = self.Game_screen.create_text((self.WIDTH/6) * 4, 20, text='Lives: ' + str(self.player_lives),font=('Arial Bold', 20), fill='White' )
        
        self.time_text = self.Game_screen.create_text((self.WIDTH/6) * 5, 20, text=f'{self.minute}:{self.second} ',font=('Arial Bold', 20), fill='Green' )
        
        self.right_paddle = self.Game_screen.create_rectangle(self.WIDTH - 30, self.HEIGHT/2 - 130/2, self.WIDTH -10, self.HEIGHT/2 + 130/2, fill='White',tags= "right_paddle")
        
        self.boss_screen = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.boss_screen.create_image(0,0,image = self.boss_image, anchor = 'nw')  
        
        self.ask_to_start = self.Game_screen.create_text(600, 360, text='Get Ready!',font=('Arial Bold', 50), fill='Blue' )
        self.Landing_Frame.pack(expand=True,fill='both')
    
    
            
    
    def start_game(self):
        # Function call to start the game
        self.Game_screen.after(2000, self.delete_ask_to_start)  # Removes the ready button
        
        self.pause = False
        self.update_score()
        self.update_player_lives()
        self.Game_screen.after(1000,self.update_time)
        self.Game_screen.after(1000, lambda: self.update_ball())

    def update_score(self):
        # To update the Score_text Label
        self.Game_screen.itemconfig(self.Score_text, text='Score: ' + str(self.player_score))

    def update_player_lives(self):
        # To update the player lives
        self.Game_screen.itemconfig(self.player_lives_text, text='Lives: ' + str(self.player_lives))

      
    def display_data(self):
        # Displaying data when called
        self.leaderboard_data = self.read_data()
        for i,entry in enumerate(self.leaderboard_data):
            self.lead = self.label + f'#{i + 1}: {entry[0]}  - Score: {entry[1]}'
        self.Leaderboard_frame.itemconfig(self.leaderboard,text =self.lead)
    
    def read_data(self):
        # Reading the data
        try:
            with open("leader.txt", "r") as file:
                self.leaderboard_data = []
                data = file.readlines
                for line in data:
                    x = line.split(':')
                    self.leaderboard_data.append(x)
        except FileNotFoundError:
            self.leaderboard_data = []
        return self.leaderboard_data
            
    def update_data(self):
        self.leaderboard_data = self.read_data()

        for data in self.leaderboard_data:
            if self.player_name.get() == data[0]:
                # Player is already in the leaderboard
                if int(self.player_score) > int(data[1]):
                    # Update score if the current score is higher
                    data[1] = self.player_score
                break
        else:# Player is not in the leaderboard; add a new ent
            self.leaderboard_data.append([self.player_name.get(), self.player_score])

        # Sort the leaderboard based on the scores in descending order
        self.leaderboard_data.sort(key=lambda x: int(x[1]), reverse=True)

        # Write the updated leaderboard data back to the file
        with open("leaderboard.txt", "w") as file:
            for entry in self.leaderboard_data:
                file.write(f'{entry[0]}:{entry[1]}\n')    
        
    

    
    
            
    
            
    def move_right_paddle_up(self, event):
        # Bind function that allows the movement of the paddle
        x = 0
        y = -20
        coord = self.Game_screen.coords(self.right_paddle)
        if  coord[1] <= 15:
            self.Game_screen.move(self.right_paddle,x,0)
        else:
            self.Game_screen.move(self.right_paddle,x,y)
    
    def move_right_paddle_down(self,event):
        # Bind function that allows the movement of the paddle
        x = 0
        y = 20
        coord = self.Game_screen.coords(self.right_paddle)
        # print(coord)
        if coord[3] >= self.HEIGHT - 15:
            self.Game_screen.move(self.right_paddle,x,0)
        else:
            self.Game_screen.move(self.right_paddle,x,y)
        
    def boss(self, event):
        # All the boss keys
        key = event.char
        if key == 'q':
            print('Hello')
            self.Game_screen.pack_forget()
            self.boss_screen.pack(expand = True, fill = 'both')
            
        if key == 'c':
            self.boss_screen.pack_forget()
            self.Game_screen.pack(expand=True, fill='both')
        
        
        if key == 'i':
            coords = self.Game_screen.coords(self.right_paddle)
            if coords[3] - coords[1] < 250:
                self.Game_screen.coords(self.right_paddle,coords[0],coords[1] - 5 ,coords[2],coords[3] + 5)
                
                
        if key == 'o':
            coords = self.Game_screen.coords(self.right_paddle)
            if coords[3] - coords[1] > 120:
                self.Game_screen.coords(self.right_paddle,coords[0],coords[1] + 5 ,coords[2],coords[3] - 5)
         
        if key == 's':
            if self.player_lives<  15:
                self.player_lives += 1
                self.Game_screen.itemconfig(self.player_lives_text, text='Lives: ' + str(self.player_lives))

         
       