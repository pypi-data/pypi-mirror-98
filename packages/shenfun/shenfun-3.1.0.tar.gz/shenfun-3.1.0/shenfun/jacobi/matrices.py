import functools
import numpy as np
from scipy.special import gamma
from shenfun.matrixbase import SpectralMatrix

from . import bases
from ..legendre.la import TDMA

J  = bases.Orthogonal
SD = bases.ShenDirichlet
SB = bases.ShenBiharmonic


class BJJmat(SpectralMatrix):
    r"""Mass matrix for inner product

    .. math::

        B_{kj} = (\psi_j, \psi_k)

    where

    .. math::

        j = 0, 1, ..., N-1 \text{ and } k = 0, 1, ..., N-1

    and :math:`\psi_k` is the Jacobi basis function.

    """
    def __init__(self, test, trial, scale=1., measure=1):
        assert isinstance(test[0], J)
        assert isinstance(trial[0], J)
        N = test[0].N
        k = np.arange(N, dtype=int)
        a = test[0].alpha
        b = test[0].beta
        #import mpmath
        #f = np.zeros(N)
        #for l in k:
        #    f[l] = mpmath.gammaprod([l+a+1, l+b+1], [l+1, l+a+b+1])
        #f *= (2**(a+b+1)/(2*k+a+b+1))
        if abs(a+b+1) < 1e-8:
            f = 0.5*gamma(k+a+1)*gamma(k+b+1)/gamma(k+1)**2
            f[0] *= 2
        else:
            f = 2**(a+b+1)*gamma(k+a+1)*gamma(k+b+1)/(2*k+a+b+1)/gamma(k+1)/gamma(k+a+b+1)
        d = {0: f}
        SpectralMatrix.__init__(self, d, test, trial, scale=scale)

    def solve(self, b, u=None, axis=0):
        N = self.shape[0]
        assert N == b.shape[axis]
        s = self.trialfunction[0].slice()

        if u is None:
            u = b
        else:
            assert u.shape == b.shape

        # Move axis to first
        if axis > 0:
            u = np.moveaxis(u, axis, 0)
            if u is not b:
                b = np.moveaxis(b, axis, 0)

        bs = b[s]
        us = u[s]
        d = 1./self[0]
        sl = [np.newaxis]*bs.ndim
        sl[0] = slice(None)
        us[:] = bs*d[tuple(sl)]
        u /= self.scale

        if axis > 0:
            u = np.moveaxis(u, 0, axis)
            if u is not b:
                b = np.moveaxis(b, axis, 0)

        return u


class BSDSDmat(SpectralMatrix):
    r"""Mass matrix for inner product

    .. math::

        B_{kj} = (\psi_j, \psi_k)

    where

    .. math::

        j = 0, 1, ..., N-2 \text{ and } k = 0, 1, ..., N-2

    and :math:`\psi_k` is the Jacobi Dirichlet basis function.

    """
    def __init__(self, test, trial, measure=1):
        assert isinstance(test[0], SD)
        assert isinstance(trial[0], SD)
        N = test[0].N
        k = np.arange(N-2, dtype=float)
        d = {-2: 4*(k[2:]-1)*(k[2:]+1)/(2*k[2:]-1)/(2*k[2:]+3)*(-2./(2*k[2:] + 1)),
              0: 4*(k+1)**2/(2*k+3)**2*(2./(2.*k+1) + 2./(2*k+5))}

        d[2] = d[-2]
        SpectralMatrix.__init__(self, d, test, trial)
        self.solve = TDMA(self)


class ASDSDmat(SpectralMatrix):
    r"""Stiffness matrix for inner product

    .. math::

        A_{kj} = (\psi'_j, \psi'_k)

    where

    .. math::

        j = 0, 1, ..., N-2 \text{ and } k = 0, 1, ..., N-2

    and :math:`\psi_k` is the Jacobi Dirichlet basis function.

    """
    def __init__(self, test, trial, scale=1., measure=1):
        assert isinstance(test[0], SD)
        assert isinstance(trial[0], SD)
        N = test[0].N
        k = np.arange(N-2, dtype=float)
        d = {0: 4*(4*k+6)*(k+1)**2/(2*k+3)**2}
        SpectralMatrix.__init__(self, d, test, trial, scale=scale)

    def solve(self, b, u=None, axis=0):
        N = self.shape[0] + 2
        assert N == b.shape[axis]
        s = self.trialfunction[0].slice()

        if u is None:
            u = b
        else:
            assert u.shape == b.shape

        # Move axis to first
        if axis > 0:
            u = np.moveaxis(u, axis, 0)
            if u is not b:
                b = np.moveaxis(b, axis, 0)

        bs = b[s]
        us = u[s]
        d = 1./self[0]
        sl = [np.newaxis]*bs.ndim
        sl[0] = slice(None)
        us[:] = bs*d[tuple(sl)]
        u /= self.scale
        self.testfunction[0].bc.set_boundary_dofs(u, True)

        if axis > 0:
            u = np.moveaxis(u, 0, axis)
            if u is not b:
                b = np.moveaxis(b, axis, 0)

        return u


class BSBSBmat(SpectralMatrix):
    r"""Mass matrix for inner product

    .. math::

        B_{kj} = (\psi_j, \psi_k)

    where

    .. math::

        j = 0, 1, ..., N-2 \text{ and } k = 0, 1, ..., N-2

    and :math:`\psi_k` is the Biharmonic basis function.

    """
    def __init__(self, test, trial, measure=1):
        from shenfun.la import PDMA
        assert isinstance(test[0], SB)
        assert isinstance(trial[0], SB)
        N = test[0].N
        k = np.arange(N, dtype=float)
        gk = (2*k+3)/(2*k+7)
        hk = -(1+gk)
        ek = 2./(2*k+1)

        p0 = 16*(k[:-4]+2)**2*(k[:-4]+1)**2/(2*k[:-4]+5)**2/(2*k[:-4]+3)**2
        p2 = 16*(k[:-6]+2)*(k[2:-4]+2)*(k[:-6]+1)*(k[2:-4]+1)/(2*k[:-6]+5)/(2*k[2:-4]+5)/(2*k[:-6]+3)/(2*k[2:-4]+3)
        p4 = 16*(k[:-8]+2)*(k[4:-4]+2)*(k[:-8]+1)*(k[4:-4]+1)/(2*k[:-8]+5)/(2*k[4:-4]+5)/(2*k[:-8]+3)/(2*k[4:-4]+3)

        d = {0: p0*(ek[:-4] + hk[:-4]**2*ek[2:-2] + gk[:-4]**2*ek[4:]),
             2: p2*((hk[:-6]*ek[2:-4] + gk[:-6]*hk[2:-4]*ek[4:-2])),
             4: p4*(gk[:-8]*ek[4:-4])}
        d[-2] = d[2]
        d[-4] = d[4]
        SpectralMatrix.__init__(self, d, test, trial)
        self.solve = PDMA(self)


class ASBSBmat(SpectralMatrix):
    r"""Stiffness matrix for inner product

    .. math::

        A_{kj} = (\psi'_j, \psi'_k)_w

    where

    .. math::

        j = 0, 1, ..., N-4 \text{ and } k = 0, 1, ..., N-4

    and :math:`\psi_k` is the Jacobi Biharmonic basis function.

    """
    def __init__(self, test, trial, scale=1, measure=1):
        assert isinstance(test[0], SB)
        assert isinstance(trial[0], SB)
        N = test[0].N
        k = np.arange(N-4, dtype=float)
        p0 = 16*(k+2)**2*(k+1)**2/(2*k+5)**2/(2*k+3)**2
        p2 = 16*(k[:-2]+2)*(k[2:]+2)*(k[:-2]+1)*(k[2:]+1)/(2*k[:-2]+5)/(2*k[2:]+5)/(2*k[:-2]+3)/(2*k[2:]+3)

        gk = (2*k+3)/(2*k+7)
        d = {0: p0*2*(2*k+3)*(1+gk),
             2: p2*(-2*(2*k[:-2]+3))}
        d[-2] = d[2]
        SpectralMatrix.__init__(self, d, test, trial, scale=scale)


class SSBSBmat(SpectralMatrix):
    r"""Stiffness matrix for inner product

    .. math::

        A_{kj} = (\psi''_j, \psi''_k)_w

    where

    .. math::

        j = 0, 1, ..., N-4 \text{ and } k = 0, 1, ..., N-4

    and :math:`\psi_k` is the Jacobi Biharmonic basis function.

    """
    def __init__(self, test, trial, scale=1, measure=1):
        assert isinstance(test[0], SB)
        assert isinstance(trial[0], SB)
        N = test[0].N
        k = np.arange(N-4, dtype=float)
        d = {0: 32*(k+2)**2*(k+1)**2/(2*k+5)}
        SpectralMatrix.__init__(self, d, test, trial, scale=scale)


class OSBSBmat(SpectralMatrix):
    r"""Matrix for inner product

    .. math::

        A_{kj} = (\psi'''_j, \psi'''_k)_w

    where

    .. math::

        j = 0, 1, ..., N-6 \text{ and } k = 0, 1, ..., N-6

    and :math:`\psi_k` is the 6th order Jacobi basis function.

    """
    def __init__(self, test, trial, measure=1):
        assert isinstance(test[0], SB)
        assert isinstance(trial[0], SB)
        N = test[0].N
        k = np.arange(N-6, dtype=float)
        #FIXME Find the correct diagonal
        d = {0: 32*(k+2)**2*(k+1)**2/(2*k+5)}
        SpectralMatrix.__init__(self, d, test, trial)


class _Jacmatrix(SpectralMatrix):
    def __init__(self, test, trial, measure=1):
        SpectralMatrix.__init__(self, {}, test, trial, measure=measure)


class _JacMatDict(dict):
    """Dictionary of inner product matrices

    Matrices that are missing keys are generated from Vandermonde type
    computations.

    """

    def __missing__(self, key):
        measure = 1 if len(key) == 2 else key[3]
        c = functools.partial(_Jacmatrix, measure=measure)
        self[key] = c
        return c

    def __getitem__(self, key):
        matrix = dict.__getitem__(self, key)
        return matrix

mat = _JacMatDict({
    ((J,  0), (J,  0)): BJJmat,
    ((SD, 0), (SD, 0)): BSDSDmat,
    ((SD, 1), (SD, 1)): ASDSDmat,
    ((SD, 0), (SD, 2)): functools.partial(ASDSDmat, scale=-1.),
    ((SD, 2), (SD, 0)): functools.partial(ASDSDmat, scale=-1.),
    ((SB, 0), (SB, 0)): BSBSBmat,
    ((SB, 2), (SB, 2)): SSBSBmat,
    ((SB, 0), (SB, 4)): SSBSBmat,
    ((SB, 4), (SB, 0)): SSBSBmat,
    ((SB, 1), (SB, 1)): ASBSBmat,
    ((SB, 0), (SB, 2)): functools.partial(ASBSBmat, scale=-1.),
    ((SB, 2), (SB, 0)): functools.partial(ASBSBmat, scale=-1.),
})
