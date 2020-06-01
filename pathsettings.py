class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200 
        self.screen_height = 800 
        self.bg_color = (0,115,0)
        self.line_color=(115,0,0)
        self.paths=(178,34,34)
        self.pressed_square_color=(0,0,115)
        self.start_square_color=(0,255,255)
        self.finish_square_color=(173,255,47)
        self.solution_color=(1,0,0)
        self.solution_path_newer=(173,255,47)
        self.square_size=20
