from pygame import Surface
from pygame.transform import smoothscale

def gaussian_blur(surface: Surface, radius: float):
    scaled_surface = smoothscale(surface.convert_alpha(), (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface
