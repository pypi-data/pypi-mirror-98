import math
from .material import Medium
from .dispersion import DispersionModel, Sellmeier, Lorentz
from .constants import C_0, HBAR


class cSi(Medium):
    """Crystalline silicon at 26 deg C.

    Refs:
    
    * A. Deinega, I. Valuev, B. Potapkin, and Y. Lozovik, Minimizing light
      reflection from dielectric textured surfaces,
      J. Optical Society of America A, 28, 770-77 (2011).
    * M. A. Green and M. Keevers, Optical properties of intrinsic silicon
      at 300 K, Progress in Photovoltaics, 3, 189-92 (1995).
    * C. D. Salzberg and J. J. Villa. Infrared Refractive Indexes of Silicon,
      Germanium and Modified Selenium Glass,
      J. Opt. Soc. Am., 47, 244-246 (1957).
    * B. Tatian. Fitting refractive-index data with the Sellmeier dispersion
      formula, Appl. Opt. 23, 4477-4485 (1984).

    """

    def __init__(self, variant=None):
        super().__init__(name="cSi")
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Deinega2011"

        if "SalzbergVilla1957" == variant:
            self.dispmod = Sellmeier(
                [
                    (10.6684293, 0.301516485 ** 2),
                    (0.0030434748, 1.13475115 ** 2),
                    (1.54133408, 1104 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 11.00, C_0 / 1.36)
        elif "Deinega2011" == variant:
            self.dispmod = Lorentz(
                self.eps,
                [
                    (8.000, 3.64 * C_0, 0),
                    (2.850, 2.76 * C_0, 0.063 * C_0),
                    (-0.107, 1.73 * C_0, 2.5 * C_0),
                ],
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.0, C_0 / 0.4)

class aSi(Medium):
    """Amorphous silicon

    Refs:

    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
      
    """

    def __init__(self, variant=None):
        super().__init__(name="aSi")
        self.eps = 3.109
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(17.68 - self.eps, 3.93 * eV_to_Hz, 0.5 * 1.92 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)