import os
import base64

os.makedirs('assets', exist_ok=True)

# Black & brown dog image (placeholder)
dog_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAgCAYAAABLFQIFAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
0klEQVRIie3XwU3DMBAF0Dc5Ab0IC9hIFuxCXa/09E/knKpJ8CM+L6s4z8Vq0A0IKh1RMdMZJX4M
BYfPXAqAQUUAu49BdE+1UX47E+xgDzYDz6jPNzGLK2Af/JIVUuCN9Ldl/LdxLX07NED5c6Dp0ESu
FOVVqVOuUB9EDrN0h9QrH0a5EszUr5cbJTVQm+7F5LgkR2IqP9xlF3IUQkRwjEFkZDaPjNCSINJu
Fo6GOjvD1hUw8Nz1S+FfAjp9RKLeyKk+1Kk7Ml3yzsRdWLJIVJKVuQuCFq2lVvLJBuKgo70Rsmrg
Xt7Wyd5e51Ed7vyMYxiO/AFbDnnDwEKegE7u6CuEmqz7bD7ntF3NcTiO9lGG7X0nLIP1XmG32+3S
7ATpGnSftjUAsH8ApssSk93r7GjOiyTSoUxS1Gk2GUXzOvt6wIuElJcQBAhvxHNK6J8BRBvYbQvo
8J3IgAAAABJRU5ErkJggg==
"""

# Black & white cow image (placeholder)
cow_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAgCAYAAABLFQIFAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
Z0lEQVRIie2UsW7DMBBFf9QBdQAdQAdMAdMB9QAdEAdgAc6I7AlIBHwjcMk3Hmc5LEiofY4RQxDa
nPr5U9dyx52NgDnYcI3cd9V8hD9HO5R6DCKN2A1W6rC9F4Snw7/T0Xn/G3v3Tx3Tb81pjL2CMixq
TRMN0wGgI30Af4tPT6oA5W5QZ6m+Ftwg5gCYawXwCvlb2HzQP2D/BiT5bRUnWlFd0H2AaoV3FqJu
UYO+4Amvxtc5wBpw5+XT+vv+AIb+EOn22+rplK8WlqCMk4m8VGpkxICUmW7yC36h6lT0BnnDAacH
QP3y2BwGM1Q5tgD0JJhAOcTYiZkA50+iCQTq0Au1IvluA2QrClAgD9fCG1Lt4A+wAAAABJRU5Erk
Jggg==
"""

# Mad cow image (placeholder)
cow_mad_data = b"""
iVBORw0KGgoAAAANSUhEUgAAACgAAAAgCAYAAABLFQIFAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
i0lEQVRIie2UQQ6DIBBFX9gCd4AduAC3IA3cAJ3A1OAQyUEFgLCULQZLfGiL4gM63RjoWIY5K+jC
0bhP7/47G4pXgNWW/wCu+O/Xjwp4HIh1WBQ+AXAOLkyoMLAlTkyg6yRhxaPgC4EZw1XmXtRhC2uc
3Urb6NiqJ48kMrzOa5zqDWQyKZ7H9IBcivg9XpZjEwCf0Q1oW6UCd4LVeKr5LsV7sQ+/QpeOPz1S
VTtL19vqwBx1mcvlXrQETgu2ecFvHRA0MjiUZxGBZpE1UlLqm/Qgg13N4ogM5sV93Pt3iq03R+MW
3SZoAvEZV7clLXCco8OoAzr+o+zJp8zRqz20cgOYXvTFYASu2+0IazdkFpAvrhU5R7Z8u/DX+sNX
EtIb8b8/nUQAAAABJRU5ErkJggg==
"""

# Horseshoe image (placeholder)
horseshoe_data = b"""
iVBORw0KGgoAAAANSUhEUgAAABoAAAAgCAYAAAB4J+PeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAV
0lEQVQ4y2NgGAWjYBSMglEwCjPQ9kAbMQG2KYSGBkL6AIr6Aov6Bihgq6F0hqhNRVHRQc0E1E4pa
VYIkk9KBhcKEDGAsDAdDYo+wHwDKSiQUHYABG7QxcZoFqClEgJ8rW7AewF1HKA9NCUO5gAAAABJR
U5ErkJggg==
"""

# Jump sound (placeholder WAV base64)
jump_sound_data = b"""
UklGRigAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YYAAAAD///8=
"""

# Kick sound (placeholder WAV base64)
kick_sound_data = b"""
UklGRigAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YYAAAAD///8=
"""

def save_asset(filename, b64data):
    with open(os.path.join('assets', filename), 'wb') as f:
        f.write(base64.b64decode(b64data))

save_asset('dog.png', dog_data)
save_asset('cow.png', cow_data)
save_asset('cow_mad.png', cow_mad_data)
save_asset('horseshoe.png', horseshoe_data)
save_asset('jump.wav', jump_sound_data)
save_asset('kick.wav', kick_sound_data)

print("✅ All assets saved to 'assets/' folder.")
