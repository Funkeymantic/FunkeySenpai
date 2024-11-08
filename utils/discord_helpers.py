from datetime import datetime

# Helper function to print messages with a timestamp
def timestamp(message):
    timestamps = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamps}] {message}')

# Fancy font dictionary
fancy_font = {
    'A': '𝙰', 'a': '𝚊', 'B': '𝙱', 'b': '𝚋', 'C': '𝙲', 'c': '𝚌',
    'D': '𝙳', 'd': '𝚍', 'E': '𝙴', 'e': '𝚎', 'F': '𝙵', 'f': '𝚏',
    'G': '𝙶', 'g': '𝚐', 'H': '𝙷', 'h': '𝚑', 'I': '𝙸', 'i': '𝚒',
    'J': '𝙹', 'j': '𝚓', 'K': '𝙺', 'k': '𝚔', 'L': '𝙻', 'l': '𝚕',
    'M': '𝙼', 'm': '𝚖', 'N': '𝙽', 'n': '𝚗', 'O': '𝙾', 'o': '𝚘',
    'P': '𝙿', 'p': '𝚙', 'Q': '𝚀', 'q': '𝚚', 'R': '𝚁', 'r': '𝚛',
    'S': '𝚂', 's': '𝚜', 'T': '𝚃', 't': '𝚝', 'U': '𝚄', 'u': '𝚞',
    'V': '𝚅', 'v': '𝚟', 'W': '𝚆', 'w': '𝚠', 'X': '𝚇', 'x': '𝚡',
    'Y': '𝚈', 'y': '𝚢', 'Z': '𝚉', 'z': '𝚣'
}

# Function to convert a string to fancy font
def to_fancy_font(text):
    return ''.join(fancy_font.get(char, char) for char in text)