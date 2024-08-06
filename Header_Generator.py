# Change the headers so that pipeline can read it properly
import os
import random
from astropy.io import fits
from astropy.time import Time
from datetime import datetime, timedelta

def random_time():
    year = random.randint(2000, 2024) # random year
    month = random.randint(1, 12) # random month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        date = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        date = random.randint(1, 30)
    else: # february
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            date = random.randint(1, 29)
        else:
            date = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    generated_date = f"{year}-{month:02d}-{date:02d}" # Date (YYYY-MM-DD)
    generated_time = f"{hour:02d}:{minute:02d}:{second:02d}" # UTC start time HH:MM:SS
    
    time = f"{generated_date}T{generated_time}"
    t = Time(time, format='isot', scale='utc')
    
    MJD_time = t.mjd # Modified Julian Date (date+start time)
    UTC_Time = time.replace("T", ":") # Date/Start time (YYYY-MM-DD:HH:MM:SS in UTC)
    
    return MJD_time, UTC_Time, generated_date.replace("-", ""), generated_time

def add_seconds_to_time(MJD_time, UTC_Time, date_str, time_str, seconds_to_add = 100):
    # Parse the UTC_Time to a datetime object
    datetime_obj = datetime.strptime(UTC_Time, "%Y-%m-%d:%H:%M:%S")
    
    # Add seconds
    new_datetime_obj = datetime_obj + timedelta(seconds=seconds_to_add)
    
    # Convert back to desired formats
    new_generated_date = new_datetime_obj.strftime("%Y%m%d")
    new_generated_time = new_datetime_obj.strftime("%H:%M:%S")
    new_UTC_Time = new_datetime_obj.strftime("%Y-%m-%d:%H:%M:%S")
    
    new_time_str = new_UTC_Time.replace(":", "T", 1)
    new_t = Time(new_time_str, format='isot', scale='utc')
    new_MJD_time = new_t.mjd
    
    return new_MJD_time, new_UTC_Time, new_generated_date, new_generated_time

# Choose a random filter for the images
filters = ['Bessell U', 'Bessell B', 'Bessell V', 'Bessell R', 'Bessell I', 'SDSS u', 'SDSS g', 'SDSS r', 'SDSS i']
filter_choice = random.choice(filters)

n = input("What is the label of the simulation group? ")
base_folder = f'Simulations/Sim {n}/star_field'
sub_folders = sorted(os.listdir(base_folder))

# Loop over all the nights in the simulation group
for night_index, sub_folder in enumerate(sub_folders):
    night_folder_path = os.path.join(base_folder, sub_folder)
    night_index -= 1
    
    if os.path.isdir(night_folder_path):
        # List all FITS files in the current sub-folder
        fits_files = sorted([f for f in os.listdir(night_folder_path) if f.endswith('.fits')])

        # Loop over all the fits images in the same night
        for file_index, fits_file in enumerate(fits_files):
            file_path = os.path.join(night_folder_path, fits_file)
            
            with fits.open(file_path, mode='update') as hdul:
                header = hdul[0].header
                
                # Update the header as required
                header['RDNOISE'] = 13.5
                if 'RN' in header:
                    del header['RN']
                filter_choice = random.choice(filters)
                header['FILTER'] = filter_choice

                if night_index == 0 and file_index == 0:
                    start_time = random_time()
                    header['MJD-OBS'] = start_time[0] # Modified Julian Date (date+start time)
                    header['DATE-OBS'] = start_time[1] # Date/Start time (YYYY-MM-DD:HH:MM:SS in UTC)
                    header['DAY-OBS'] = start_time[2] # Date (YYYYMMDD)
                    header['UTSTART'] = start_time[3] # UTC start time HH:MM:SS
                else:
                    time_interval = (100 * file_index) + (3600 * 24 * night_index)
                    new_time = add_seconds_to_time(start_time[0], start_time[1], start_time[2], start_time[3], time_interval)
                    header['MJD-OBS'] = new_time[0] 
                    header['DATE-OBS'] = new_time[1] 
                    header['DAY-OBS'] = new_time[2] 
                    header['UTSTART'] = new_time[3]

                print("Night", night_index)
                print("Frame", file_index)
                print("Time", header['DATE-OBS'])
                print()
                # Save changes
                hdul.flush()
