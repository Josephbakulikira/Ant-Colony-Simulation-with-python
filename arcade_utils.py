import arcade
import PIL.Image
import PIL.ImageDraw

def create_triangular_texture(size, color):
    """Create a triangular texture with the specified size and color."""
    # Convert color to RGBA tuple
    if isinstance(color, tuple):
        if len(color) == 3:
            color = (*color, 255)  # Add alpha channel if missing
    else:
        # Assume it's an arcade color
        color = (255, 255, 255, 255)  # Default to white if color type is unknown
    
    # Create transparent image
    image = PIL.Image.new('RGBA', (int(size), int(size)), (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)
    
    # Draw triangle
    points = [(size/2, 0),           # top
             (0, size),              # bottom left
             (size, size)]          # bottom right
    
    draw.polygon(points, fill=color)
    
    # Convert PIL image to Arcade texture
    texture_name = f"triangle_{size}"
    arcade_texture = arcade.Texture(texture_name, image)
    return arcade_texture