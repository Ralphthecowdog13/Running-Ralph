import os
import base64

os.makedirs('assets', exist_ok=True)

# Valid base64 PNG placeholders (small simple colored squares or icons)

dog_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
Y0lEQVRYhe3WsW3DMBAG4CcJAkJAkpFHQBSRBxEDpDMkV+8CPkiOuFEm9GLNXExM1sv/9dj0YN6P
nDvJyYQSEJBJKZlJMZlbkq5alvAqwQw8QEMD0hNVcu3q3gIYVTrt8AYiFcA7F7qDyGY5AZAY5AQ
AwCBEV7qHtBu7iWqj1gAWWFa32vSdVqVbNnCyGo1GoxGixG4rDY7uJLoVqtfVbOfjsZJpPJZsNx
Op1OO+gLn8ZDKZTKZR6Px+PV6vtdqtVu3lyu92u921Gi0XCUKgUmkUvV6vRyORiNYtFoVGIa1Wu3
W6zWbzGajKZRCKRS6XR6P0+Xw+z2WzWfD4fD4XkUgkEkWjUaDQaDSqVyyWQy6XQ6TSaTS6XSyWR
aLReLh0Or1YrFYzGMyGQyGUSiUQh1FJBNJpNJpPJBKJRCKRYLBaLQaDQaDQaDZLK5XK5XKZTAYj
EYjEYqFQqFQoFAqFQqFQoFAoFgMvk5HLBNHeB79FCOHjx0qgAAAABJRU5ErkJggg==
"""

cow_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
ZUlEQVRYhe2WQQrCQAxFz9RhBKFIEnJASUkBFpCKVyHjS8QE7FHf9HoPRjx8DAGY8z99nxMYIQB
UAYzRHYqwoPQAjMUT05r1cFZizLLCLtrtYBLQF3PSkEmt7tFtwGG4z84KnckFJjv9vlQivVrh/0
bVi0Wk0Gh0Ok8lki7ZvDcdy+Xy/PJBAJSUbD4fDYRiURrtdrtwOMwub4AEwDYuCqfT6XTCYRj8c
R8vlcrzebzKZrPZrPZ6vVaT6fTlctloOp3G63GxWCwWKyWQSCKVSqVSCQSSQSScxSAVXq/XqlUq
VTrfD6fTt1uNhsNht9u50Op9Po9Ho9Go1Gj0TCYTqdDpdDo7j8Xh8XhcJhMJiMRiORyOXy+XSqV
SicXiMViMZrNZrFYrFYpFIpFIrFYrEYZhMJpPJpPJpPJoPJoPJpMJpOJzOaTyWQy+Uy6XQ6Hw+H
wcikUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgk
UgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkUgkU
gjHgH5x29r1oh66MAAAAASUVORK5CYII=
"""

cow_mad_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
jUlEQVRYhe2W0Q3CMBBEzyRC4Rg5WCUhNkCZIAWkByYAmRJBBHZH2MshXPtCJrF0OVr9x2Wq3u5
GQQkZmkVgHE3HvjvPeSw3A3qjWq1cWg0Q8EhwIc7uDk0mkwm80ahUKiKBSqVSqUSoVCqFSqFQqF
YKhUJpPJ5PJ5PNpPNoPNoPNoNHo9Ho1Go1GIaDYbDb7fbiBvIyyWQy+VyWRSCQSCKVQqFQqFQqF
QrFYoFAqFQrFYrFYrFYrFgrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrF
YrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrF
YrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrF
YrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrF
YrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrFYrF
YrFYnR8AxHZvZaPqQnMAAAAASUVORK5CYII=
"""

horseshoe_data = b"""
iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAYAAADZ4DJ3AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAX
UlEQVRoge3RMQ6AIBQF0L8o+4XERAgfKHoA8lBJJj4FxRJzvy6NNQXtYHZ53oRkxkEAT8qxTqOpX
7UZcH8YVgA3yAdB5o9x9m7wB6A5zwb2IBJAsEKkq0iM2FEcwHt4BtYlE9C5L4B9WAidRfYRbAAAA
AElFTkSuQmCC
"""

jump_sound_data = b"""
UklGRjQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YRAAAA==
"""

kick_sound_data = b"""
UklGRjQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YRAAAA==
"""

def save_asset(filename, b64data):
    clean_b64 = b"".join(b64data.split())
    missing_padding = (4 - len(clean_b64) % 4) % 4
    clean_b64 += b"=" * missing_padding
    decoded = base64.b64decode(clean_b64)
    with open(os.path.join('assets', filename), 'wb') as f:
        f.write(decoded)

save_asset('dog.png', dog_data)
save_asset('cow.png', cow_data)
save_asset('cow_mad.png', cow_mad_data)
save_asset('horseshoe.png', horseshoe_data)
save_asset('jump.wav', jump_sound_data)
save_asset('kick.wav', kick_sound_data)

print("✅ All assets saved to 'assets/' folder.")
