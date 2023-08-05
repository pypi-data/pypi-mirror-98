"""
This example script creates a movie with the satellite track superposed.
"""
from datetime import datetime

import numpy as np

from asilib import plot_movie_generator
from asilib import lla_to_skyfield
from asilib import load_cal_file


# ASI parameters
mission = 'THEMIS'
station = 'RANK'
time_range = (datetime(2017, 9, 15, 2, 34, 0), datetime(2017, 9, 15, 2, 36, 0))

# Load the calibration data.
cal_dict = load_cal_file(mission, station)

# Create the satellite track's latitude, longitude, altitude (LLA) coordinates.
# This is an imaginary north-south satellite track oriented to the east
# of the THEMIS/RANK station.
n = int((time_range[1] - time_range[0]).total_seconds() / 3)  # 3 second cadence.
lats = np.linspace(cal_dict["SITE_MAP_LATITUDE"] + 10, cal_dict["SITE_MAP_LATITUDE"] - 10, n)
lons = (cal_dict["SITE_MAP_LONGITUDE"] + 3) * np.ones(n)
alts = 500 * np.ones(n)
lla = np.array([lats, lons, alts]).T

# Map the satellite track to the station's azimuth and elevation coordinates as well as the
# image pixels
# The mapping is not along the magnetic field lines! You need to install IRBEM and then use
# asilib.map_along_magnetic_field().
sat_azel, sat_azel_pixels = lla_to_skyfield(mission, station, lla)

# Initiate the movie generator function.
movie_generator = plot_movie_generator(
    time_range, mission, station, azel_contours=True, overwrite=True
)

for i, (time, frame, ax, im) in enumerate(movie_generator):
    # Plot the entire satellite track
    ax.plot(sat_azel_pixels[:, 0], sat_azel_pixels[:, 1], 'red')
    # Plot the current satellite position.
    ax.scatter(sat_azel_pixels[i, 0], sat_azel_pixels[i, 1], c='red', marker='x', s=100)

    # Annotate the station and satellite info in the top-left corner.
    station_str = (
        f'{mission}/{station} '
        f'LLA=({cal_dict["SITE_MAP_LATITUDE"]:.2f}, '
        f'{cal_dict["SITE_MAP_LONGITUDE"]:.2f}, {cal_dict["SITE_MAP_ALTITUDE"]:.2f})'
    )
    satellite_str = f'Satellite LLA=({lla[i, 0]:.2f}, {lla[i, 1]:.2f}, {lla[i, 2]:.2f})'
    ax.text(0, 1, station_str + '\n' + satellite_str, va='top', 
            transform=ax.transAxes, color='red')