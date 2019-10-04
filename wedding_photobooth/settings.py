class Settings:
    """A class to store all settings for the photobooth"""

    def __init__(self):
        """Initialie the photobooth's settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # Photo settings
        self.photo_width = 1200
        self.photo_height = 800

        # Taking picture related settings
        self.camera_start_delay = 5
        self.pic_storage = 'booth_pics/'
        self.backup_pics = False # Set to true if you want to backup the pics
        self.pic_backup = '/mnt/usb/' # Optional
        self.pic_path_base = "Volmering_Photobooth"

        # Camera Settings
        self.camera_rotation = 0
        self.camera_horizontal_flip = True

        # Button settings
        self.camera_gpio_pin = 21
        self.exit_gpio_pin = 23 # Optional

        # Canned screen images
        self.intro_screen = 'resources/intro.png'
        self.prep_1_screen = 'resources/prep_1.png'
        self.prep_2_screen = 'resources/prep_2.png'
        self.prep_3_screen = 'resources/prep_3.png'
        self.prep_4_screen = 'resources/prep_4.png'
        self.countdown_1_screen = 'resources/countdown_1.png'
        self.countdown_2_screen = 'resources/countdown_2.png'
        self.countdown_3_screen = 'resources/countdown_3.png'
        self.processing_screen = 'resources/processing.png'
        self.finalizing_screen = 'resources/finalizing.png'
        self.photo_grid_screen = 'resources/photo_grid.png'
        self.photo_last_screen = 'resources/last.png'
        self.photo_test = 'resources/test.jpg'
