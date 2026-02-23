import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import RotaryEncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.display import Display, SSD1306

keyboard = KMKKeyboard()

# 1. SETUP DES EXTENSIONS
keyboard.extensions.append(MediaKeys())

# 2. CONFIGURATION DE LA MATRICE (2 Lignes x 4 Colonnes)
# Lignes : Pin 1 (D0), Pin 2 (D1)
# Colonnes : Pin 3 (D2), Pin 4 (D3), Pin 7 (D6), Pin 11 (D10)
keyboard.row_pins = (board.D0, board.D1)
keyboard.col_pins = (board.D2, board.D3, board.D6, board.D10)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# 3. CONFIGURATION DES ENCODEURS (Rotation)
# On utilise la Pin 11 (D10) pour le signal B commun
encoder_handler = RotaryEncoderHandler()
encoder_handler.pins = (
    (board.D8, board.D10, None, False), # Encodeur 1 (Pin 9, Pin 11)
    (board.D9, board.D10, None, False), # Encodeur 2 (Pin 10, Pin 11)
)
keyboard.modules.append(encoder_handler)

# 4. CONFIGURATION DES LEDS (Pin 8 / D7)
rgb = RGB(pixel_pin=board.D7, num_pixels=2)
keyboard.extensions.append(rgb)

# 5. CONFIGURATION DE L'ÉCRAN OLED (Pins 5 & 6)
# KMK détecte automatiquement SDA/SCL sur le XIAO
display_driver = SSD1306(
    i2c=board.I2C(),
    device_address=0x3C,
)
display = Display(display_driver)
keyboard.extensions.append(display)

# 6. MAPPAGE DES TOUCHES (Keymap)
# Ligne 1 : MX1, MX2, MX3, Clic_Volume
# Ligne 2 : MX4, MX5, MX6, Clic_Micro
keyboard.keymap = [
    [
        KC.A,    KC.B,    KC.C,    KC.MUTE,        
        KC.D,    KC.E,    KC.F,    KC.AUDIO_MUTE,  
    ]
]

# Mapping des rotations
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD),), # Encodeur 1 : Volume haut/bas
    ((KC.UP, KC.DOWN),),   # Encodeur 2 : Flèches (ou ce que tu veux)
]

if __name__ == '__main__':
    keyboard.go()