import sys
import pygame
import time
import os
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
from shutil import copy2
from settings import Settings

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class wedding_photobooth:
    """Overall class to manage the wedding photobooth"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        global screenw
        screenw = self.screen.get_rect().width
        global  screenh
        screenh = self.screen.get_rect().height
        
    def display_start_screen(self):
        background = pygame.image.load(self.settings.intro_screen)
        background = pygame.transform.scale(background, (screenw, screenh))
        pygame.display.flip()
        self.screen.blit(background, (0, 0))
        pygame.display.update()
        pygame.display.set_caption("Wedding Photobooth!")

    def pic_countdown(self, pic_num, total_pics, timestamp):
        
        white = [255, 255, 255]
        total_pics_to_take = total_pics
        if pic_num == 0:
            prep_screen = pygame.image.load(self.settings.prep_1_screen)
            prep_screen = pygame.transform.scale(prep_screen, (screenw, screenh))
        elif pic_num == 1:
            prep_screen = pygame.image.load(self.settings.prep_2_screen)
            prep_screen = pygame.transform.scale(prep_screen, (screenw, screenh))
        elif pic_num == 2:
            prep_screen = pygame.image.load(self.settings.prep_3_screen)
            prep_screen = pygame.transform.scale(prep_screen, (screenw, screenh))
        elif pic_num == 3:
            prep_screen = pygame.image.load(self.settings.prep_4_screen)
            prep_screen = pygame.transform.scale(prep_screen, (screenw, screenh))
        else:
            #Potentially write this error out to an error file...
            print("Add additional logic for additional prep screens")

        self.screen.blit(prep_screen, (0, 0))
        pygame.display.update()
        time.sleep(.5)

        count3 = pygame.image.load(self.settings.countdown_3_screen)
        count3 = pygame.transform.scale(count3, (screenw, screenh))
        self.screen.blit(count3, (0, 0))
        pygame.display.update()
        time.sleep(.5)
        count2 = pygame.image.load(self.settings.countdown_2_screen)
        count2 = pygame.transform.scale(count2, (screenw, screenh))
        self.screen.blit(count2, (0, 0))
        pygame.display.update()
        time.sleep(.5)
        count1 = pygame.image.load(self.settings.countdown_1_screen)
        count1 = pygame.transform.scale(count1, (screenw, screenh))
        self.screen.blit(count1, (0, 0))
        pygame.display.update()
        time.sleep(.5)
        
        self.screen.fill(white)
        pygame.display.update()

        taken_pic = self.take_photo(pic_num, total_pics_to_take, timestamp)
        display_pic = pygame.image.load(taken_pic)
        self.screen.blit(display_pic, (0, 0))
        pygame.display.update()
        time.sleep(3)

        return(taken_pic)

    def exit_program(self):
        sys.exit()

    def _check_events(self):
        # Watch for keyboard and mouse events.
        #https://www.digikey.com/en/maker/projects/how-to-build-interactive-graphics-controllers-for-a-raspberry-pi/00086fd384094e27b7d88e835b800d0f
        #https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs
        
        button = self.settings.camera_gpio_pin
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
        buttonpress = 'Notpushed'
        input_state = GPIO.input(button) # Sense the button
               
        print('checking events')
        print(input_state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    pygame.quit()
            else:
                continue
        if input_state == 0:
            buttonpress = 'Pushed'
            print('Button push')
            return buttonpress

    def take_photo(self, photo_in_series, pic_count, timestamp):
        #https://picamera.readthedocs.io/en/release-1.13/recipes1.html

        camera.rotation = self.settings.camera_rotation
        #camera.resolution = (1920, 1080)
        camera.resolution = (1600, 900)
        # Set ISO to the desired value
        camera.iso = 600
        # Wait for the automatic gain control to settle
        time.sleep(1)
        # Now fix the values
        #camera.shutter_speed = 800

        total_pic_count = pic_count
        temp_file_name = "temp_file.jpg"
        #pygame.display.quit()
        #camera.start_preview()
        time.sleep(1)
        camera.capture(temp_file_name, use_video_port=False)
        final_pic = self.save_pics(temp_file_name, photo_in_series, total_pic_count, timestamp)

        return(final_pic)

    def get_timestamp(self):
        now = datetime.now()
        currenttime = now.strftime("%m_%d_%Y_%H_%M_%S")
        return(currenttime)

    def save_pics(self, pic_taken, pic_num, total_pics_taken,timestamp):
        """Save the taken picture"""

        photo_series = total_pics_taken
        series_sub_photo = pic_num + 1
        prim_storage = self.settings.pic_storage
        name_base = self.settings.pic_path_base
        timestampOfSeries = timestamp

        filename = prim_storage + name_base + "_" + str(timestampOfSeries) + "_" + str(series_sub_photo) + "_of_" + str(photo_series) + ".jpg"

        copy2(pic_taken, filename)
        print(filename)

        if self.settings.backup_pics == True:
            print("Backup enabled")
            backup_stroage = self.settings.pic_backup
            bkup_file = backup_stroage + name_base + "_" + str(timestampOfSeries) + "_" + str(series_sub_photo) + "_of_" + str(photo_series) + ".jpg"
            copy2(filename, bkup_file)

        return(filename)
        
    def save_gridPics(self,timestamp):
        """Save the grid picture"""

        prim_storage = self.settings.pic_storage
        name_base = self.settings.pic_path_base
        timestampOfSeries = timestamp
        gridFolder ='gridPics/'

        gridPicLocation = prim_storage + gridFolder + name_base + str(timestampOfSeries) + ".jpg"

        copy2('grid.jpeg', gridPicLocation)
        print(gridPicLocation)

        if self.settings.backup_pics == True:
            print("Backup enabled")
            backup_stroage = self.settings.pic_backup
            bkup_file = backup_stroage + gridFolder + name_base + "_" + str(timestampOfSeries) + ".jpg"
            copy2(gridPicLocation, bkup_file)

    def grid_display(self,files):
        """Display all 4 pictures to a grid"""

        grid = pygame.image.load(self.settings.photo_grid_screen)
        grid = pygame.transform.scale(grid, (screenw, screenh))
        self.screen.blit(grid, (0, 0))

        pic1, pic2, pic3, pic4 = [files[i] for i in (0, 1, 2, 3)]


        photo1 = pygame.image.load(pic1)
        photo2 = pygame.image.load(pic2)
        photo3 = pygame.image.load(pic3)
        photo4 = pygame.image.load(pic4)

        pic_1_x = ((screenw / 2) * 0.94)
        pic_1_y = ((screenh / 2) * 0.91)

        pic_1_x = int(pic_1_x)
        pic_1_y = int(pic_1_y)

        pic_2_4_x_start = int(pic_1_x * 1.13)
        pic_3_4_y_start = int(pic_1_y * 1.21)
        photo1 = pygame.transform.scale(photo1, (pic_1_x, pic_1_y))
        photo2 = pygame.transform.scale(photo2, (pic_1_x, pic_1_y))
        photo3 = pygame.transform.scale(photo3, (pic_1_x, pic_1_y))
        photo4 = pygame.transform.scale(photo4, (pic_1_x, pic_1_y))

        #   Photo grid
        #   1 | 2
        #   -----
        #   3 | 4

        self.screen.blit(photo1, (0, 0))  # photo 1
        self.screen.blit(photo2, (0, pic_3_4_y_start))  # photo 3
        self.screen.blit(photo3, (pic_2_4_x_start, pic_3_4_y_start))  # photo 4
        self.screen.blit(photo4, (pic_2_4_x_start, 0))  # photo 2
        pygame.display.update()
        pygame.image.save(self.screen, "grid.jpeg")
        time.sleep(10)


    def run_photobooth(self):
        """Start the main loop for the photobooth."""
        pics_to_take = 4
        
        while True:
            self.display_start_screen()
            #time.sleep(1)
            buttonStatus = 'Notpushed'
            buttonStatus = self._check_events()
            if buttonStatus == 'Pushed':
            
                current_pics =[]
                timestamp = self.get_timestamp()
                for i in range(pics_to_take):
                    pic_name = self.pic_countdown(i, pics_to_take,timestamp)
                    current_pics.append(pic_name)

                self.grid_display(current_pics)
                self.save_gridPics(timestamp)
                
            else:
                continue
            #self.exit_program()
#    def display_final(self):

if __name__ == '__main__':
    # Make a game instance, and run the game.
    booth = wedding_photobooth()
    booth.run_photobooth()
