from __future__ import absolute_import
__author__ = 'rjuanola'
import collections
import numpy as np
import scipy.constants as sc

class AddNoise(object):
    """Class to add noise to the simulated interferograms.
    """

    def __init__(self, parameters, previous_results):
        self.parameters = parameters
        self.previous_results = previous_results
        self.result = collections.OrderedDict()

    def run(self):
        fts = self.previous_results['fts']
        noise = self.previous_results['noise']
        dnoise = self.previous_results['detectornoise']

        delta_t = dnoise['delta_t']
        n_total = dnoise['n_total']
        f_noise = dnoise['f_noise']
        kNEPval = dnoise['NEP']
        eta = dnoise['eta']


        #creating time vector
        time_vec = np.linspace(0, n_total-1, n_total) * delta_t

        #photon noise vector
        NEP = noise['NEPtot']
        #NEP all includes background, instrument and g-r
        NEPall= np.sqrt((NEP**2+kNEPval**2)/eta)


        ph_noise_std = NEPall / np.sqrt(delta_t)
        ph_noise_vec = np.random.randn(n_total) * ph_noise_std
        overf = np.fft.fft(ph_noise_vec) * f_noise

        noise_vec = np.real(np.fft.ifft(overf))

        self.result['ph_noise_vec'] = ph_noise_vec
        self.result['time_vec'] = time_vec
        self.result['noise_vec'] = noise_vec


        return self.result


#     def __repr__(self):
#          return '''
# Add Noise:
#   Time vector           : {dt}
#   Noise vector          : {nt}
#
# '''.format(
#           dt=self.result['time_vec'],
#           nt=self.result['noise_vec'])