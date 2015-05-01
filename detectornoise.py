from __future__ import absolute_import
__author__ = 'rjuanola'
import collections
import numpy as np
import bisect
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

        row = detector['Detector time constant'].keys()[0]
        tau_r = detector['Detector time constant'][row]

        row = detector['Detector optical absorption efficiency'].keys()[0]
        eta = detector['Detector optical absorption efficiency'][row]

        row = detector['Acquisiton frequency (n tau)'].keys()[0]
        f_acq = detector['Acquisiton frequency (n tau)'][row]

        delta_f = 1 / (delta_t * n_total)

        freq_vec = np.linspace(0, n_total-1, n_total) * delta_f
        freq_vec[0] = freq_vec[1]
        en = 1
        f_noise = en * np.power((1 + (knee_freq / freq_vec)), 0.5)
        f_noise[0] = f_noise[1]

        #detector intrinsic params
        dAdN = 5e-7
        DeltaJ = 168e-6 * 1.6e-19   #includes conversion eV to J
        tau_res = 2e-6
        SAdB=-105
        SA=10** (SAdB/10)

        NEPamp = np.sqrt(SA) * np.power((eta * tau_r * dAdN / DeltaJ), -1)
        freqNEP = np.linspace(10**0, 10**5, n_total)
        omega = freqNEP * 2 * np.pi
        NEP = NEPamp * np.sqrt(1 + (omega * tau_r)**2) * np.sqrt(1 + (omega * tau_res)**2)

        index = bisect.bisect(freqNEP, f_acq)
        kNEPval = NEP[index]


        self.result['delta_t'] = delta_t
        self.result['n_total'] = n_total
        self.result['freq_vec'] = freq_vec
        self.result['f_noise'] = f_noise
        self.result['NEP'] = kNEPval


        return self.result

    def __repr__(self):
        return '''
Detector Noise:
  Delta t               : {dt}
  Total samples         : {nt}
  NEP                   : {nep}

'''.format(
          dt=self.result['delta_t'],
          nt=self.result['n_total'],
          nep=self.result['NEP'])