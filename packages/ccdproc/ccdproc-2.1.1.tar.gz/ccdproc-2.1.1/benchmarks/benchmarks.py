# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import bottleneck as bn

from astropy.io import fits

from ccdproc import combine, ImageFileCollection, Combiner


# class TimeCombine:
#     """
#     An example benchmark that times the performance of various kinds
#     of iterating over dictionaries in Python.
#     """

#     timeout = 240.0  # seconds

#     def setup(self):
#         self.working_dir = TemporaryDirectory()
#         self.path = Path(self.working_dir.name)
#         size = [2024, 2031]
#         n_images = 25

#         base_name = 'test-combine-{num:03d}.fits'

#         for num in range(n_images):
#             data = np.random.normal(size=size)
#             # Now add some outlying pixels so there is something to clip
#             n_bad = 50000
#             bad_x = np.random.randint(0, high=size[0] - 1, size=n_bad)
#             bad_y = np.random.randint(0, high=size[1] - 1, size=n_bad)
#             data[bad_x, bad_y] = np.random.choice([-1, 1], size=n_bad) * (10 + np.random.rand(n_bad))
#             hdu = fits.PrimaryHDU(data=np.asarray(data, dtype='float32'))
#             hdu.header['for_prof'] = 'yes'
#             hdu.header['bunit'] = 'adu'
#             hdu.writeto(self.path / base_name.format(num=num), overwrite=True)

#         self.ic = ImageFileCollection(self.path, '*')
#         self.files = self.ic.files_filtered(for_prof='yes', include_path=True)

    # def time_ma_median_dev_mad_std(self):
    #     combine(self.files, sigma_clip=True,
    #             sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
    #             sigma_clip_func=np.ma.median,
    #             sigma_clip_dev_func=mad_std)


class TimeCombiner:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """

    timeout = 240.0  # seconds

    def setup(self):
        self.working_dir = TemporaryDirectory()
        self.path = Path(self.working_dir.name)
        size = 1 * np.array([1012, 1016])
        n_images = 25

        base_name = 'test-combine-{num:03d}.fits'

        for num in range(n_images):
            data = np.random.normal(size=size)
            # Now add some outlying pixels so there is something to clip
            n_bad = 50000
            bad_x = np.random.randint(0, high=size[0] - 1, size=n_bad)
            bad_y = np.random.randint(0, high=size[1] - 1, size=n_bad)
            data[bad_x, bad_y] = np.random.choice([-1, 1], size=n_bad) * (10 + np.random.rand(n_bad))
            hdu = fits.PrimaryHDU(data=np.asarray(data, dtype='float32'))
            hdu.header['for_prof'] = 'yes'
            hdu.header['bunit'] = 'adu'
            hdu.writeto(self.path / base_name.format(num=num), overwrite=True)

        self.ic = ImageFileCollection(self.path, '*')
        self.files = self.ic.files_filtered(for_prof='yes', include_path=True)
        to_combine = [ccd for ccd in self.ic.ccds()]
        self.combiner = Combiner(to_combine)

    # def time_sigma_clip_default_settings(self):
    #     self.combiner.sigma_clipping()

    # def time_sigma_clip_median_std(self):
    #     self.combiner.sigma_clipping(func=np.ma.median)

    # def time_sigma_clip_bnmedian_std(self):
    #     self.combiner.sigma_clipping(func=bn.median)

    # def time_use_astropy_sigma_clipping(self):
    #     sigma_clip(self.combiner.data_arr.data, axis=0, copy=False, maxiters=1)

    def time_average_combine_no_clip_default_args(self):
        self.combiner.average_combine()

    def time_average_combine_some_masked_default_args(self):
        # Mark a random set of points as masked
        n_bad = 50000
        size = self.combiner.data_arr.shape
        img_num = np.random.randint(0, high=size[0] - 1, size=n_bad)
        bad_x = np.random.randint(0, high=size[1] - 1, size=n_bad)
        bad_y = np.random.randint(0, high=size[2] - 1, size=n_bad)
        self.combiner.data_arr.mask[img_num, bad_x, bad_y] = np.ma.masked
        self.combiner.average_combine()

    def time_average_combine_weights_default_args(self):
        # It shouldn't matter for timing what the weights are
        self.combiner.weights = np.ones_like(self.combiner.data_arr)
        self.combiner.average_combine()

    def time_median_combine_default_args(self):
        self.combiner.median_combine()

    def time_mad_std_sigma_clip_no_astropy_funcs(self):
        self.combiner.sigma_clipping(low_thresh=5, high_thresh=5)

    def time_minmax_clip_median_combine(self):
        """Try doing some fast clipping to generate
        masked values and see if that impacts speed"""
        from astropy.stats import mad_std
        self.combiner.minmax_clipping(min_clip=-4, max_clip=4)
        self.combiner.median_combine(uncertainty_func=bn.nanstd)

    def time_mad_std_astropy_sigma_clip_avg_combine(self):
        from astropy.stats import mad_std, sigma_clip
        self.combiner.data_arr = sigma_clip(self.combiner.data_arr,
                                            sigma=5,
                                            maxiters=1,
                                            stdfunc=mad_std)
        self.combiner.average_combine()

    # def time_mad_banzai_sigma_clip(self):
    #     from banzai.utils.stats import robust_standard_deviation as mad_std
    #     from banzai.utils.stats import median
    #     self.combiner.sigma_clipping(low_thresh=5, high_thresh=5,
    #                                  func=median,
    #                                  dev_func=mad_std)

    # def time_banzai_avg_combine_with_mad_clipping(self):
    #     from banzai.utils.stats import sigma_clipped_mean
    #     sigma_clipped_mean(self.combiner.data_arr, 5, axis=0)

    # def time_DRAGONS_sigma_clip(self):
    #     from gempy.library.nddops import NDStacker
    #     NDStacker.sigclip(self.combiner.data_arr,
    #                       lsigma=5, hsigma=5, max_iters=1)

    # def time_average_combine_no_clip_regular_mean(self):
    #     self.combiner.average_combine(scale_func=np.average)

    # def time_average_combine_no_clip_nanmean(self):
    #     # Fails at the moment because np.mean does not take weights
    #     self.combiner.average_combine(scale_func=np.nanmean)
