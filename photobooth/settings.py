class Settings:
    """A class to store all settings for the photobooth"""

    def __init__(self):
        """Initialie the photobooth's settings."""

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080

        # Photo settings
        self.photo_width = 1920
        self.photo_height = 1080

        # Taking picture related settings
        self.camera_start_delay = 5
        self.pic_storage = 'photobooth_pics/'
        self.backup_pics = True # Set to true if you want to backup the pics
        self.pic_backup = '/media/derek/Samsung USB2/pics' # Optional
        self.pic_path_base = "Carnival_Photobooth"

        # Camera Settings
        self.camera_rotation = 0
        self.camera_horizontal_flip = True

        # Button settings
        self.camera_gpio_pin = 21
        self.exit_gpio_pin = 23 # Optional

        # Canned screen images
        resource_folder = './photobooth/resources/carnival'
        self.intro_screen = f'{resource_folder}/intro.JPG'
        self.prep_1_screen = f'{resource_folder}/prep_1.JPG'
        self.prep_2_screen = f'{resource_folder}/prep_2.JPG'
        self.prep_3_screen = f'{resource_folder}/prep_3.JPG'
        self.prep_4_screen = f'{resource_folder}/prep_4.JPG'
        self.countdown_1_screen = f'{resource_folder}/countdown_1.JPG'
        self.countdown_2_screen = f'{resource_folder}/countdown_2.JPG'
        self.countdown_3_screen = f'{resource_folder}/countdown_3.JPG'
        self.processing_screen = f'{resource_folder}/processing.JPG'
        self.finalizing_screen = f'{resource_folder}/finalizing.JPG'
        self.photo_grid_screen = f'{resource_folder}/photo_grid.JPG'
        #self.photo_last_screen = f'{resource_folder}/last.JPG'
        #self.photo_test = f'{resource_folder}/test.jpg'
