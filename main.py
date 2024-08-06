import os
import random
import pandas as pd
import pista as pt
import numpy as np

from Folder_Creation import SimulationFolderManager
from Starfield_Generator import Star_Generator
from telescope_and_detector import tele_params, det_params
from PSF_Generator import PointSpreadFunction_Generator

# Create a new folder for the simulated images and the input data
main_folder = "Simulations"
manager = SimulationFolderManager(main_folder)
folder_name = manager.get_new_folder_name()
manager.create_new_sim_folder()

data_folder_name = "Simulations/" + folder_name + "/data"
image_folder_name = "Simulations/" + folder_name + "/star_field"

print()

# Generate the simulated star field
num_of_nights = int(input("Number of observation nights (default 1): ") or 1)
num_of_stars = int(input("Number of stars in each frame, default 300: ") or 300)
num_of_images = int(input("Number of images, default 30: ") or 30)

Star_gen = Star_Generator(32.0, 45.0, 20.0, num_of_stars, num_of_images)
star_images = Star_gen.generate_images()

# Modify the simulated star field so that it contain stars undergoing transit
num_of_transit = int(input("Number of transit stars in each frame, default 50: ") or 50)

transit_indices = [random.randint(0, num_of_stars - 1) for _ in range(num_of_transit)]
transit_depth = 0.7
transit_frames = list(range(int(num_of_images/4), int(num_of_images/4 * 3)))
transit_images = Star_gen.apply_transit(star_images, transit_indices, transit_depth, transit_frames)

star_images = transit_images

print("Star field succesfully generated")
print()

# Generate the Point Spread Function
PSF_Gen = PointSpreadFunction_Generator(150, 300, 0.7, 40.1).PSF()
PSF_file_path = os.path.join(data_folder_name, f"PSF.npy")
np.save(PSF_file_path, PSF_Gen)

print("PSF succesfully generated")
print()

# Get the telescope parameters and detector parameters
telescope_parameters = tele_params(PSF_file_path)
detector_parameters = det_params

print("Telescope and detector parameters succesfully loaded")
print()

# Simulate the fits images
if num_of_nights == 1:
    for idx, frames in enumerate(star_images):
        df = pd.DataFrame(frames, columns = ['ra', 'dec', 'mag'])
        print(df)
        
        # Save the stars input data locally
        star_data_input = os.path.join(data_folder_name, f"image-{idx + 1}.txt")
        df.to_csv(star_data_input, index=False)

        #In order to render the plots properly, run this file in INTERACTIVE MODE: right click -> "run in interactive window" -> "run this file in interactive window"
        sim = pt.Imager(df = df, tel_params = telescope_parameters, n_x = 3000, n_y = 2000, exp_time = 100) #df fits file, tel_params dictionary, n_x and n_y are the number of pixels along RA and Dec respectively. exp_time is exposure time in seconds.
        sim(det_params = detector_parameters, photometry = 'Aper', detect_source = True)

        # Saves the image locally
        night_folder_name = 'Night 1'
        night_folder_path = os.path.join(image_folder_name, night_folder_name)
        os.makedirs(night_folder_path, exist_ok=True)
        
        sim_file_path = os.path.join(night_folder_path, f"image-{idx + 1}.fits")
        sim.writeto(sim_file_path)

        print(f"Frame {idx + 1} completed.")
        print()
else:
    num_of_frames_each_night = num_of_images / num_of_nights
    # Create the folders to hold the images
    for i in range(0, num_of_nights):
        night_index = i + 1
        night_folder_name = 'Night {night_index}'
        night_folder_path = os.path.join(image_folder_name, night_folder_name)
        os.makedirs(night_folder_path, exist_ok=True)
    # Saves the images into the folders
    for idx, frames in enumerate(star_images):
        df = pd.DataFrame(frames, columns = ['ra', 'dec', 'mag'])
        print(df)

        # Save DataFrame locally
        stars_file_path = os.path.join(data_folder_name, f"image-{idx + 1}.txt")
        df.to_csv(stars_file_path, index=False)

        #In order to render the plots properly, run this file in INTERACTIVE MODE: right click -> "run in interactive window" -> "run this file in interactive window"
        sim = pt.Imager(df = df, tel_params = telescope_parameters, n_x = 3000, n_y = 2000, exp_time = 100) #df fits file, tel_params dictionary, n_x and n_y are the number of pixels along RA and Dec respectively. exp_time is exposure time in seconds.
        sim(det_params = detector_parameters, photometry = 'Aper', detect_source = True)

        night_folder_name = f'Night {int((idx // num_of_frames_each_night) + 1)}'
        night_folder_path = os.path.join(image_folder_name, night_folder_name)
        os.makedirs(night_folder_path, exist_ok=True)
        
        sim_file_path = os.path.join(night_folder_path, f"image-{idx + 1}.fits")
        sim.writeto(sim_file_path)
        
        print(f"Frame {idx + 1} completed.")
        print()
