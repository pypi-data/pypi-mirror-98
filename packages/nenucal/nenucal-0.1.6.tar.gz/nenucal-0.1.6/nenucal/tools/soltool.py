#!/usr/bin/env python

import os
from multiprocessing import Pool

import click

import numpy as np
import astropy.stats as astats

import scipy.ndimage

from losoto.h5parm import h5parm

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

from nenucal import __version__


mpl.rcParams['image.cmap'] = 'Spectral_r'
mpl.rcParams['image.origin'] = 'lower'
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['axes.grid'] = True

t_file = click.Path(exists=True, dir_okay=False)


class GainSol(object):

    def __init__(self, time, freqs, ant, directions, pol, amp, phase):
        self.time = time
        self.freqs = freqs
        self.ant = ant
        self.dir = directions
        self.pol = pol
        self.amp = amp
        self.phase = phase
        self.d = self.amp * np.exp(1j * self.phase)


@click.group()
@click.version_option(__version__)
def main():
    ''' DPPP gains solution utilities ...'''


def ctoap(r, i):
    c = r + 1j * i
    return abs(c), np.angle(c)


def aptoc(amp, phase):
    c = amp * np.exp(1j * phase)
    return c.real, c.imag


def gauss_filter(arr, dx, kernel_fwhm, axis=0):
    """"Apply a gaussian filter to an array with nans.
        Allows intensity to leak into the nan area.

    Source: https://stackoverflow.com/questions/18697532/gaussian-filtering-a-image-with-nan-in-python
    """
    sigma = kernel_fwhm / dx / 2.3
    nan_msk = np.isnan(arr) | arr.mask

    gauss = arr.copy()
    gauss[nan_msk] = 0
    gauss = scipy.ndimage.gaussian_filter1d(gauss, sigma=sigma, axis=axis)

    norm = np.ones(shape=arr.shape)
    norm[nan_msk] = 0
    norm = scipy.ndimage.gaussian_filter1d(norm, sigma=sigma, axis=axis)

    # avoid RuntimeWarning: invalid value encountered in true_divide
    norm = np.where(norm == 0, 1, norm)
    gauss = gauss / norm
    gauss[nan_msk] = np.nan

    return gauss


def filter(amp, phase, dx, kernel_fwhm, axis=0, sigma_clip=None):
    real, imag = aptoc(amp, phase)
    s_real = gauss_filter(real, dx, kernel_fwhm, axis=axis)
    s_imag = gauss_filter(imag, dx, kernel_fwhm, axis=axis)

    if sigma_clip is not None:
        m_real = astats.sigma_clip(real, axis=axis, sigma=sigma_clip).mask
        m_imag = astats.sigma_clip(imag, axis=axis, sigma=sigma_clip).mask
        real[m_real | m_imag] = s_real[m_real | m_imag]
        imag[m_imag | m_imag] = s_imag[m_imag | m_imag]
        s_real = gauss_filter(real, dx, kernel_fwhm, axis=axis)
        s_imag = gauss_filter(imag, dx, kernel_fwhm, axis=axis)

    return ctoap(s_real, s_imag)


def open_sol(file_h5):
    import losoto.h5parm
    sol_file = losoto.h5parm.h5parm(file_h5)
    solset = sol_file.getSolsets()[0]
    soltab, soltab_phase = solset.getSoltabs(useCache=True)

    ant = soltab.getAxisValues('ant')
    directions = soltab.getAxisValues('dir')
    time = soltab.getAxisValues('time')
    pol = soltab.getAxisValues('pol')

    freqs = soltab.getAxisValues('freq')

    weight = soltab.getValues(weight=True)[0].astype(bool)
    amp = np.ma.array(soltab.getValues(weight=False)[0], mask=~weight)
    phase = np.ma.array(soltab_phase.getValues(weight=False)[0], mask=~weight)

    amp = amp[:, :, :]
    phase = phase[:, :, :]

    sol_file.close()

    return GainSol(time, freqs, ant, directions, pol, amp, phase)


@main.command('smooth')
@click.argument('sols', nargs=-1, type=t_file)
@click.option('--fwhm_time', help='Time coherence scale (min)', type=float, default=16)
@click.option('--fwhm_freq', help='Freq coherence scale (MHz)', type=float, default=2)
@click.option('--main_fwhm_time', help='Time coherence scale (min) for Main direction', type=float, default=20)
@click.option('--main_fwhm_freq', help='Freq coherence scale (MHz) for Main direction', type=float, default=4)
@click.option('--clip_nsigma', help='Clip solution above NSIGMA', type=float, default=4)
@click.option('--main_name', help='Name of the main direction', type=str, default='main')
def smooth(sols, fwhm_time, fwhm_freq, main_fwhm_time, main_fwhm_freq, clip_nsigma, main_name):
    ''' Smooth solutions with a Gaussian kernel'''
    for sol_file in sols:
        sol = h5parm(sol_file, readonly=False)
        try:
            solset = sol.getSolsets()[0]
            soltab_amp = solset.getSoltab('amplitude000')
            soltab_phase = solset.getSoltab('phase000')

            freq = soltab_amp.getAxisValues('freq')
            time = soltab_amp.getAxisValues('time')

            direction = [k.strip('[ ]').lower() for k in soltab_amp.getAxisValues('dir')]
            idx = list(range(len(direction)))

            if 'main' in direction:
                idx_main = (direction.index(main_name.lower()),)
                idx.remove(idx_main[0])
                print(f'Smoothing directions {idx_main} of {sol_file} with fwhm_time={main_fwhm_time}',
                      ' and fwhm_freq={main_fwhm_freq}')

            print(f'Smoothing directions {idx} of {sol_file} with fwhm_time={fwhm_time} and fwhm_freq={fwhm_freq}')

            weight = soltab_amp.getValues(weight=True)[0].astype(bool)
            amp = np.ma.array(soltab_amp.getValues(weight=False)[0], mask=~weight)
            phase = np.ma.array(soltab_phase.getValues(weight=False)[0], mask=~weight)

            if len(time) >= 2:
                dx_min = (time[1] - time[0]) / 60.
                if 'main' in direction and main_fwhm_time > 0:
                    amp[:, :, :, idx_main], phase[:, :, :, idx_main] = filter(amp[:, :, :, idx_main],
                                                                              phase[:, :, :, idx_main], dx_min,
                                                                              main_fwhm_time, sigma_clip=clip_nsigma)
                if fwhm_time > 0:
                    amp[:, :, :, idx], phase[:, :, :, idx] = filter(amp[:, :, :, idx],
                                                                    phase[:, :, :, idx], dx_min, fwhm_time,
                                                                    sigma_clip=clip_nsigma)

            if len(freq) >= 2:
                dx_mhz = (freq[1] - freq[0]) * 1e-6
                if 'main' in direction and main_fwhm_freq > 0:
                    amp[:, :, :, idx_main], phase[:, :, :, idx_main] = filter(amp[:, :, :, idx_main],
                                                                              phase[:, :, :, idx_main], dx_mhz,
                                                                              main_fwhm_freq,
                                                                              sigma_clip=clip_nsigma, axis=1)
                if fwhm_freq > 0:
                    amp[:, :, :, idx], phase[:, :, :, idx] = filter(amp[:, :, :, idx],
                                                                    phase[:, :, :, idx], dx_mhz, fwhm_freq,
                                                                    sigma_clip=clip_nsigma, axis=1)

            soltab_amp.setValues(amp)
            soltab_phase.setValues(phase)
        finally:
            sol.close()


def plot_sol(sol, dir, pol, data_type, filename):
    if data_type == 'Amplitude':
        v = sol.amp[:, :, :, dir, pol]
    elif data_type == 'Phase':
        v = sol.phase[:, :, :, dir, pol]

    vmax = np.nanquantile(v[~v.mask & ~np.isnan(v) & (v != 0)], 0.999)
    vmin = np.nanquantile(v[~v.mask & ~np.isnan(v) & (v != 0)], 0.001)
    extent = [0, len(sol.time), sol.freqs.min() * 1e-6, sol.freqs.max() * 1e-6]

    n = v.shape[2]
    ncols, nrows = int(np.ceil(np.sqrt(n))), int(np.ceil(n / np.ceil(np.sqrt(n))))

    fig, axs = plt.subplots(ncols=ncols, nrows=nrows, sharey=True, figsize=(1 + 2 * ncols, 1 + 1.5 * nrows),
                            sharex=True)

    for i, ax in zip(range(v.shape[2]), axs.flatten()):
        if v.shape[0] > 1 and v.shape[1] > 1:
            im = ax.imshow(v[:, :, i].T, aspect='auto', vmax=vmax, vmin=vmin, extent=extent)
        elif v.shape[0] == 1:
            ax.plot(sol.freqs * 1e-6, v[0, :, i].T)
        elif v.shape[1] == 1:
            ax.plot(v[:, 0, i].T)
        ax.text(0.025, 0.975, sol.ant[i], transform=ax.transAxes, fontsize=11, va='top')

    if v.shape[0] > 1 and v.shape[1] > 1:
        cax = fig.add_axes([0.6, 1.04, 0.39, 0.02])
        cax.set_xlabel(data_type)
        fig.colorbar(im, cax=cax, orientation='horizontal')
        xlabel = 'Time index'
        ylabel = 'Frequency [Mhz]'
    elif v.shape[0] == 1:
        xlabel = 'Frequency [MHz]'
        ylabel = data_type
    elif v.shape[1] == 1:
        xlabel = 'Time index'
        ylabel = data_type

    for ax in axs[:, 0]:
        ax.set_ylabel(ylabel)
    for ax in axs[-1, :]:
        ax.set_xlabel(xlabel)

    fig.tight_layout(pad=0)
    fig.savefig(filename, dpi=120, bbox_inches="tight")


@main.command('plot')
@click.argument('sols', nargs=-1, type=t_file)
@click.option('--plot_dir', help='Plot directory', type=str, default='sol_plots')
@click.option('--n_cpu', help='Number of CPU to use', type=str, default=4)
def plot(sols, plot_dir, n_cpu):
    ''' Plot solutions of the h5 files SOLS '''
    for sol_file in sols:
        sol = open_sol(sol_file)

        with Pool(n_cpu) as pool:
            for data_type in ['Amplitude', 'Phase']:
                for dir in range(len(sol.dir)):
                    for pol in range(len(sol.pol)):
                        filename = f'{data_type}_dir{sol.dir[dir]}_pol{sol.pol[pol]}.png'
                        path = os.path.join(os.path.dirname(sol_file), plot_dir, filename)

                        if not os.path.exists(os.path.dirname(path)):
                            os.makedirs(os.path.dirname(path))

                        # plot_sol(sol, dir, pol, data_type, path)
                        pool.apply_async(plot_sol, [sol, dir, pol, data_type, path])
            pool.close()
            pool.join()


if __name__ == '__main__':
    main()
