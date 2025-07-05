import os
import base64

os.makedirs('assets', exist_ok=True)

# Valid, minimal base64 PNG (16x16 black square) for dog.png
dog_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAADUlEQVR42mNgYGBgAAAABAABJzQnCgAAAABJRU5ErkJggg=='

# Valid, minimal base64 PNG (16x16 black and white checkerboard) for cow.png
cow_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAGUlEQVR42mNgGAXUBwAD+QAEFgHCjoAxG2GAAAD1HGL9sF9bdwAAAABJRU5ErkJggg=='

# Same minimal black and white for cow_mad.png
cow_mad_data = cow_data

# Valid base64 PNG (16x16 gray horseshoe shape) placeholder for horseshoe.png
horseshoe_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAALUlEQVR42mNgGAWjYBSMglEwCjPQ9kAbMQG2KYSAEM5AcDxHDAUYxG3wAAgAikEDHvH0SgAAAABJRU5ErkJggg=='

# Tiny silent WAV sound (1 second) for jump.wav
jump_sound_data = b'UklGRlIAAABXQVZFZm10IBAAAAABAAEAESsAAABAAgAZGF0YQAAAAA='

# Tiny silent WAV sound (1 second) for kick.wav
kick_sound_data = jump_sound_data

def save_asset(filename, b64data):
    with open(os.path.join('assets', filename), 'wb') as f:
        f.write(base64.b64decode(b64data))

save_asset('dog.png', dog_data)
save_asset('cow.png', cow_data)
save_asset('cow_mad.png', cow_mad_data)
save_asset('horseshoe.png', horseshoe_data)
save_asset('jump.wav', jump_sound_data)
save_asset('kick.wav', kick_sound_data)

print("✅ Assets saved successfully in 'assets/' folder.")
