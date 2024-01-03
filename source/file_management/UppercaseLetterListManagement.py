import os
from .FileUtilities import compute_output_directory, write_text_to_file_if_uninitialized
from talon import app

def guarantee_uppercase_letters_list_initialized():
    '''If the uppercase letters list does not exist, this initializes it with defaults'''
    path = os.path.join(compute_output_directory(), "uppercase_letters.talon-list")
    write_text_to_file_if_uninitialized(path, r"""list: user.mouse_control_chicken_uppercase_letter
-
arch:   A
barn:   B
cow:    C
dune:   D
earth:  E
faint:  F
gnome:  G
ham:    H
knight: I
jane:   J
keen:   K
lime:   L
moon:   M
nice:   N
old:    O
peach:  P
quip:   Q
rhyme:  R
sand:   S
treat:  T
um:     U
veil:   V
whip:   W
sphinx: X
year:   Y
cheese: Z
"""         
            )

app.register('ready', guarantee_uppercase_letters_list_initialized)