# Create PSF and save
import poppy as poy
import astropy.units as u
import numpy as np
from astropy.stats import gaussian_fwhm_to_sigma
from astropy.convolution import Gaussian2DKernel
from scipy.signal import fftconvolve

class PointSpreadFunction_Generator:
    def __init__(self, wavelength_min, wavelength_max, FWHM_in, FOV):
        self.wmin = wavelength_min
        self.wmax = wavelength_max
        self.fwhm_in = FWHM_in
        self.fov = FOV
        
    def PSF(self):
        osys = poy.OpticalSystem(oversample = 10, npix = 2000)
        osys.add_pupil(poy.CircularAperture(radius=40*u.cm))
        osys.add_detector(pixelscale=0.1, fov_arcsec=self.fov)
        psfs = 0
        for wav in np.arange(self.wmin,self.wmax,10): # wavelength
            psf = osys.calc_psf(wav*1e-9)
            psfs += psf[0].data
            psf[0].data = psfs/psfs.sum() 

        pixel_scale = 0.57
        FWHM        = self.fwhm_in/pixel_scale
        sigma       = FWHM*gaussian_fwhm_to_sigma

        off_axis = psfs/psfs.sum()
        kernel = Gaussian2DKernel(sigma,sigma)
        kernel.normalize()

        conv_off = fftconvolve(off_axis, kernel, mode = 'same')
        conv_off_binned = conv_off.reshape(401, 10, 401, 10).sum(axis=(1,3))
        final_psf = conv_off/conv_off.sum()
        return final_psf
