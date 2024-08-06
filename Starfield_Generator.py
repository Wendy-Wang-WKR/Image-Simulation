#Starfield generator, creates an array of tuples (RA, Dec, Mag).
import numpy as np

class Star_Generator:
    def __init__(self, RA, DEC, magnitude, number_of_stars, number_of_images):
        self.Ra = RA
        self.Dec = DEC
        self.n = number_of_stars
        self.m = magnitude
        self.x = number_of_images
        
    def generate_single_image(self, previous_stars = None):
        # Initialize an array to store star data
        points = []
        RA_width = 0.3
        Dec_width = 0.2
        mag_width = 7

        mag_mod = 0
        
        if previous_stars is None:
            for i in range(self.n):
                random_RA = np.random.uniform(self.Ra - RA_width, self.Ra + RA_width)
                random_Dec = np.random.uniform(self.Dec - Dec_width, self.Dec + Dec_width)
                random_mag = np.random.uniform(self.m - mag_width, self.m + mag_width)
                points.append((random_RA, random_Dec, random_mag))
        else:
            for star in previous_stars:
                random_RA = star[0]
                random_Dec = star[1]
                random_mag = np.random.uniform(star[2] - mag_mod, star[2] + mag_mod)
                points.append((random_RA, random_Dec, random_mag))
        return np.array(points)
    
    def generate_images(self):
        images = []
        previous_stars = None
        
        for i in range(self.x):
            current_stars = self.generate_single_image(previous_stars)
            images.append(current_stars)
            previous_stars = current_stars
        
        return images

    def apply_transit(self, images, transit_indices, transit_depth, frames_to_apply):
        """
        Apply transit effect to specific frames.
        
        Parameters:
        - images: List of 2D numpy arrays, each representing star data in an image.
        - transit_indices: List of indices indicating which stars are affected by the transit.
        - transit_depth: The amount by which to increase the magnitude (decrease brightness).
        - frames_to_apply: List of indices of images where the transit effect should be applied.
        
        Returns:
        - Modified list of images with the transit effect applied.
        """
        for frame_idx in frames_to_apply:
            if frame_idx < len(images):
                image = images[frame_idx]
                for idx in transit_indices:
                    if idx < len(image):
                        new_mag = image[idx, 2] * transit_depth
                        image[idx, 2] = new_mag  # Ensure magnitude doesn't go below 0
        return images
        
