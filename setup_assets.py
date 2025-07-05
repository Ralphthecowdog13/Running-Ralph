import os
import base64

os.makedirs('assets', exist_ok=True)

def save_asset(filename, b64data):
    # Remove whitespace and pad correctly
    b64_clean = b64data.replace(b'\n', b'').replace(b' ', b'')
    missing_padding = len(b64_clean) % 4
    if missing_padding:
        b64_clean += b'=' * (4 - missing_padding)
    with open(os.path.join('assets', filename), 'wb') as f:
        f.write(base64.b64decode(b64_clean))

# Tiny 16x16 PNGs
dog_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAADUlEQVR42mNgYGBgAAAABAABJzQnCgAAAABJRU5ErkJggg=='
cow_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAGUlEQVR42mNgGAXUBwAD+QAEFgHCjoAxG2GAAAD1HGL9sF9bdwAAAABJRU5ErkJggg=='
cow_mad_data = cow_data
horseshoe_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAALUlEQVR42mNgGAWjYBSMglEwCjPQ9kAbMQG2KYSAEM5AcDxHDAUYxG3wAAgAikEDHvH0SgAAAABJRU5ErkJggg=='

# Silent WAVs with correct padding
jump_sound_data = b'UklGRlIAAABXQVZFZm10IBAAAAABAAEAESsAAABAAgAZGF0YQAAAAA='
kick_sound_data = jump_sound_data

# Save all
save_asset('dog.png', dog_data)
save_asset('cow.png', cow_data)
save_asset('cow_mad.png', cow_mad_data)
save_asset('horseshoe.png', horseshoe_data)
save_asset('jump.wav', jump_sound_data)
save_asset('kick.wav', kick_sound_data)

print("✅ All assets saved successfully into the 'assets' folder.")
