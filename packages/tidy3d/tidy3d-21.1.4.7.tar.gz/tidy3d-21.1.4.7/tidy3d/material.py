import numpy as np
import logging

from .utils import listify, log_and_raise
from .constants import int_, float_, EPSILON_0, C_0
from .dispersion import DispersionModel

class Medium(object):
    """
    Base class for a custom defined material.
    """

    def __init__(self, epsilon=1, sigma=0, name=None):
        """ Define a material through frequency-independent values of 
        the relative permittivity and the conductivity, or through a 
        dispersion function.
        
        Parameters
        ----------
        epsilon : float or DispersionModel, optional
            If numeric, real part of the dimensionless relative permittivity. 
            If a :class:`.DispersionModel` is provided, then the model 
            data is copied. Default is ``1.`` (vacuum).
        sigma : float, optional
            (S/micron) Electric conductivity, s.t. 
            ``Im(eps(omega)) = sigma/omega``, where ``eps(omega)`` is the 
            complex permittivity at frequency omega. This conductivity is 
            added on top of any coming from the dispersion model, if used.
        """
        if isinstance(epsilon, DispersionModel):
            self.eps = epsilon._eps_inf
            self.sigma = 0
            self.poles = epsilon._poles
            self.dispmod = epsilon
        else:
            if 0 < epsilon < 1:
                logging.warning(
                    "Permittivity smaller than one could result "
                    "in numerical instability. Use Courant stability factor "
                    "value lower than the smallest refractive index value."
                )


            elif epsilon <= 0:
                err_msg = (
                    "Permittivity smaller than zero can result in "
                    "numerical instability and should be included as a "
                    "dispersive model."
                )

                if epsilon < -100:
                    err_msg += \
                        "For large negative values consider using PEC instead."
                        
                log_and_raise(err_msg, ValueError)

            self.dispmod = None
            self.eps = epsilon
            self.sigma = sigma
            self.poles = []
        
        # If set, this is a tuple (f_lower, f_upper) in Hz of the frequency
        # range of validity of this material model.
        self.frequency_range = None
        
        self.name = None if name is None else str(name)

    def epsilon(self, freqs=None):
        """Evaluate the (complex) relative permittivity of the medium.
        
        Parameters
        ----------
        freqs : array_like or None, optional
            (Hz) Array of frequencies at which to query the permittivity. If 
            ``None``, the instantaneous :math:`\epsilon_\infty` is returned.
        
        Returns
        -------
        array_like
            The permittivity values, same shape as ``freqs``.
        """

        if self.dispmod is None:
            if freqs is None:
                return self.eps
            else:
                return self.eps + 1j*self.sigma/2/np.pi/freqs/EPSILON_0
        else:
            return self.dispmod.epsilon(freqs)

    @classmethod
    def from_nk(cls, n, k, freq, name=None):
        """ Define a material through the real and imaginary part of the 
        refractive index at a given frequency.

        Parameters
        ----------
        n : float
            Real part of the refractive index.
        k : float
            Imaginary part of the refractive index.
        freq : float
            (Hz) Frequency at which ``(n, k)`` are evaluated.
        name : str, optional
            Custom name of the material.
        """
        eps_real = n**2 - k**2
        eps_imag = 2*n*k
        
        sigma = 2*np.pi*freq*eps_imag*EPSILON_0
        return cls(eps_real, sigma, name)

class PEC(object):
    """ Perfect electric conductor. All tangential electric fields vanish.
    """
    def __init__(self, name='PEC'):
        """ Construct.

        Parameters
        ----------
        name : str, optional
            Custom name of the material.
        """
        self.name=name

class PMC(object):
    """ Perfect magnetic conductor. All tangential magnetic fields vanish.
    """
    def __init__(self, name='PMC'):
        """ Construct.

        Parameters
        ----------
        name : str, optional
            Custom name of the material.
        """
        self.name=name

