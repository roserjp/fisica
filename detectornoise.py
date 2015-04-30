from __future__ import absolute_import
__author__ = 'rjuanola'
import collections
import numpy as np
import scipy.constants as sc

class DetectorNoise(object):
    """Class to compute the kid detector noise
        """
    def __init__(self, parameters, previous_results):
        self.parameters = parameters
        self.previous_results = previous_results
        self.result = collections.OrderedDict()

    def run(self):
        fts = self.previous_results['fts']


        wnmax = fts['wnmax']
        velocity = fts['smec_velocity']
        nsample = fts['fts_nsample']
        nscans = fts['nscans']
        inters_time = fts['smec_interscan_duration']

        delta_t = 1 / velocity / wnmax
        n_total = nsample * nscans + inters_time / delta_t * (nscans -1)

        detector = self.parameters['substages']['Detectors']
        row = detector['knee freq'].keys()[0]
        knee_freq = detector['knee freq'][row]

        #print knee_freq

        delta_f = 1 / (delta_t * n_total)

        freq_vec = np.linspace(0, n_total-1, n_total) * delta_f
        freq_vec[0] = freq_vec[1]
        en = 1
        f_noise = en * np.power((1 + (knee_freq / freq_vec)), 0.5)
        f_noise[0] = f_noise[1]


        self.result['delta_t'] = delta_t
        self.result['n_total'] = n_total
        self.result['freq_vec'] = freq_vec
        self.result['f_noise'] = f_noise


        return self.result

    def __repr__(self):
        return '''
Detector Noise:
  Delta t               : {dt}
  Total samples         : {nt}

'''.format(
          dt=self.result['delta_t'],
          nt=self.result['n_total'])