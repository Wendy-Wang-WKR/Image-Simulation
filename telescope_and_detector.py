import pista as pt

data_path = pt.data_dir

#Telescope parameter Dictionary (sample) Using the INSIST telescope for now
def tele_params(PSF):
    result = {

                        'aperture' : 40, 
                        'pixel_scale' : 0.57, # float, arcseconds/pixel
                        'psf_file' : PSF, #fits, npy -> path to the file that contains point spread function data in the form of a 2D array. Can use to fits or npy. 
                        'response_funcs' : [f'{data_path}/INSIST/UV/Filter.dat,1,100', 

                                  f'{data_path}/INSIST/UV/Coating.dat,5,100',   # 5 mirrors

                                  f'{data_path}/INSIST/UV/Dichroic.dat,2,100', #2 dichronics

                                  ] # if response_funcs is not provided, use 'coeffs' which is a float, the total multiplicate factor that needs to go into the effective area
                        }
    return result

#Detector parameter dictionary
det_params = {
                'shot_noise' :  'Poisson', # options are 'Gaussian' and 'Poisson'
                'M_sky'      :  20, #background = 20 mag/SAS
                'G1'         :  1, # Detector gain
                'PRNU_frac'  :  0.25/100, # Photon Responce non uniformity fraction
                'qe_response': [f'{data_path}/INSIST/UV/QE.dat,1,100'],
                'RN'         :  13.5, # Read Noise 1 electron
                'T'          :  218, # Temperature of the detector in Kelvin
                'DCNU'       :  0.1/100, # Dark Current Non Uniformity
                'DFM'        :  0.01 # dark current 0.01 e-/pixel/sec
             }
