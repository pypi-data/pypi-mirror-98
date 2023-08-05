import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.colors import LogNorm

from skopi.util import xp, asnumpy


class Visualizer(object):
    def __init__(self, experiment, diffraction_rings=None, log_scale=False):
        self.experiment = experiment
        #self.center = self.experiment.det.geometry.point_coord_indexes((0, 0))
        # ! Wavenumber definition != beam's.
        self.wavenumber = np.linalg.norm(self.experiment.beam.get_wavevector())
        self.distance = self.experiment.det.distance
        self.center = None
        self.pix_width = np.median(asnumpy(self.experiment.det.pixel_width))

        # the following if test is not elegant,
        # but using the more elegant asnumpy method in skopi.util
        # results in
        # TypeError: Implicit conversion to a NumPy array is not allowed. Please use `.get()` to construct a NumPy array explicitly.
        if xp is np:
            self.q_max = np.min((  # Max inscribed radius
                xp.max(self.experiment.det.pixel_position_reciprocal[..., 1]),
                -xp.min(self.experiment.det.pixel_position_reciprocal[..., 1]),
                xp.max(self.experiment.det.pixel_position_reciprocal[..., 0]),
                -xp.min(self.experiment.det.pixel_position_reciprocal[..., 0])))
        else:
            self.q_max = np.min((  # Max inscribed radius
                xp.max(self.experiment.det.pixel_position_reciprocal[..., 1]).get(),
                -xp.min(self.experiment.det.pixel_position_reciprocal[..., 1]).get(),
                xp.max(self.experiment.det.pixel_position_reciprocal[..., 0]).get(),
                -xp.min(self.experiment.det.pixel_position_reciprocal[..., 0]).get()))

        self._auto_rings = False
        if diffraction_rings is not None:
            if diffraction_rings.lower() == "auto":
                self._auto_rings = True
            else:
                raise ValueError(
                    "Unrecognized value '{}' for argument diffraction_rings"
                    "".format(diffraction_rings))

        if log_scale:
            self._norm = LogNorm()
        else:
            self._norm = None

    def imshow(self, img):
        if xp is np:
            img_cpu = img
        else:
            img_cpu = img.get()
        img = np.ma.masked_where(img_cpu==0,img_cpu)
        plt.imshow(img, norm=self._norm, interpolation='none')
        plt.colorbar()
        plt.xlabel('Y')
        plt.ylabel('X')

        self.center = np.array(img.shape) / 2
        if self._auto_rings:
            self.add_diffraction_rings()

    def add_diffraction_ring(self, q):
        """Add a circle on assembled image.

        Takes a reciprocal distance (m-1) for the corresponding radius.
        Call after plt.imshow but before plt.legend.
        """
        # Radius
        s = q/(2*self.wavenumber)
        r = self.distance * 2 * s * np.sqrt(1-s**2) / (1-2*s**2)
        pix_rad = r / self.pix_width

        label = '{:.2g} A'.format((1/q)*1e+10)
        ncenter = self.center[::-1]  # Swap x & y to match coordinate system
        plt.gca().add_patch(
            Circle(ncenter, pix_rad, edgecolor='red', fill=False))
        plt.gca().annotate(label, xy=(ncenter[0], ncenter[1]+pix_rad),
                           ha="center", va="bottom", color="red")

    def add_diffraction_rings(self):
        """Add diffraction rings on assembled image.

        Attemp to find relevant values by itself.
        Call after plt.imshow but before plt.legend.
        """
        q_start = self.q_max * 0.99
        steps = (1, 2, 3, 4, 5)
        i_max = steps[-1]
        for i in steps:
            self.add_diffraction_ring(i*q_start/i_max)
