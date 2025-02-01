import os

# Directory configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
FONT_DIR = os.path.join(ASSETS_DIR, 'fonts')

# API configurations
STARRY_API_KEY = "BlodgkIBFkqlY4k964rVFcuGomVzRg"
GOOGLE_API_KEY = "AIzaSyCPyLDUR6YE-ikbPognywlD7SsHptaAvsU"
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Processing parameters
DEFAULT_PARAMS = {
    'languages': ['english', 'hindi', 'gujarati'],
    'audio_speed': 1.4,
    'font_size': 60,
    'sections_per_part': 3,
    'font_map': {
        'hindi': 'NotoSansDevanagari-Regular.ttf',
        'gujarati': 'NotoSansGujarati-Regular.ttf',
        'english': 'arial.ttf'
    }
}

# Create directories if they don't exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)