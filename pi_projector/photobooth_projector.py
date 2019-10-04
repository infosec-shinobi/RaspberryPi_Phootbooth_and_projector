import os
import stat
import sys
import time
import pygame
from shutil import copy2

# Storage related settings
pic_storage = 'grid_pics_projector/'

# Button settings
exit_gpio_pin = 23 # Optional

# Canned screen images
intro_screen = 'resources/intro.png'
find_pics_later = 'resources/find_pics_later.png'
final_image = 'resources/final.png'

#Samba share info
samba_user = 'pi'
samba_pass = 'raspberry'
samba_share = '//192.168.5.1/pishare/'
client_mnt_location = '/mnt/pishare/'
#samba_share = 'test_pics'

def mount_pics():
    """Mount the samaba share from the other pi"""
    
    print('Launching in 5 minutes...')
    time.sleep(300)
    try:
        # mount the drive
        cmd = "sudo mount -t cifs "+samba_share+" "+client_mnt_location+" -o user="+samba_user+",pass="+samba_pass
        os.system(cmd)
    except:
        print('Error mounting shared drive')

def get_photo_list():
    """Create a list of photos to display"""

    # create list
    photo_dir = os.listdir(client_mnt_location)

    return photo_dir

def check_for_input():
    """A function to handle keyboard/mouse/device input events. """
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    pygame.quit()
            else:
                continue

def display_pic(display, pic):

        current_pic = pygame.image.load(pic)
        current_pic = pygame.transform.scale(current_pic, (screenw, screenh))
        pygame.display.flip()
        display.blit(current_pic, (0, 0))
        pygame.display.update()
        pygame.display.set_caption("Photobooth Projector!")

def exit_program():
    sys.exit()

def run_projector():

    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
    global screenw
    screenw = screen.get_rect().width
    global screenh
    screenh = screen.get_rect().height
    #pygame.mouse.set_visible(False)  # hide the mouse cursor

    while True:
        
        check_for_input()
        current_pic_list = []

        #display intro
        display_pic(screen, intro_screen)
        time.sleep(3)
        # display where to find pics later at
        display_pic(screen, find_pics_later)
        time.sleep(3)

        #get current listing of photos in samba share
        current_pic_list = get_photo_list()
		
        #cylce through and display each photo
        for photo in current_pic_list:
            check_for_input()
            current_grid_pic = client_mnt_location+photo
            display_pic(screen, current_grid_pic)
            time.sleep(3)

        # display thank you screen
        display_pic(screen, final_image)
        time.sleep(3)
        
        check_for_input()
        copyFiles()
        #check_for_input()
        #exit_program()

def copyFiles():
	
	sourced_list = (file for file in os.listdir(client_mnt_location))
	
	for file in sourced_list:
		if not os.path.exists(os.path.join(pic_storage, file)):
			file2copy = client_mnt_location + file
			copy2(file2copy, pic_storage)
	

if __name__ == '__main__':
    # Make a game instance, and run the game.

    mount_pics()
    run_projector()
