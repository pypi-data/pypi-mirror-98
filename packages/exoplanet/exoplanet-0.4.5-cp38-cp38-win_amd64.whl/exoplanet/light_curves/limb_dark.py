# -*- coding: utf-8 -*-

__all__ = ["LimbDarkLightCurve", "StarryLightCurve"]

import warnings

import aesara_theano_fallback.tensor as tt
import numpy as np

from ..citations import add_citations_to_model
from ..theano_ops.starry import get_cl, limbdark
from ..utils import as_tensor_variable


class LimbDarkLightCurve:
    """A limb darkened light curve computed using starry

    Args:
        u (vector): A vector of limb darkening coefficients.

    """

    __citations__ = ("starry",)

    def __init__(self, u, model=None):
        add_citations_to_model(self.__citations__, model=model)
        self.u = as_tensor_variable(u)
        u_ext = tt.concatenate([-1 + tt.zeros(1, dtype=self.u.dtype), self.u])
        self.c = get_cl(u_ext)
        self.c_norm = self.c / (np.pi * (self.c[0] + 2 * self.c[1] / 3))

    def get_ror_from_approx_transit_depth(self, delta, b, jac=False):
        """Get the radius ratio corresponding to a particular transit depth

        This result will be approximate and it requires ``|b| < 1`` because it
        relies on the small planet approximation.

        Args:
            delta (tensor): The approximate transit depth in relative units
            b (tensor): The impact parameter
            jac (bool): If true, the Jacobian ``d ror / d delta`` is also
                returned

        Returns:
            ror: The radius ratio that approximately corresponds to the depth
            ``delta`` at impact parameter ``b``.

        """
        b = as_tensor_variable(b)
        delta = as_tensor_variable(delta)
        n = 1 + tt.arange(self.u.size)
        f0 = 1 - tt.sum(2 * self.u / (n ** 2 + 3 * n + 2))
        arg = 1 - tt.sqrt(1 - b ** 2)
        f = 1 - tt.sum(self.u[:, None] * arg ** n[:, None], axis=0)
        factor = f0 / f
        ror = tt.sqrt(delta * factor)
        if not jac:
            return tt.reshape(ror, b.shape)
        drorddelta = 0.5 * factor / ror
        return tt.reshape(ror, b.shape), tt.reshape(drorddelta, b.shape)

    def get_light_curve(
        self,
        orbit=None,
        r=None,
        t=None,
        texp=None,
        oversample=7,
        order=0,
        use_in_transit=None,
        light_delay=False,
    ):
        """Get the light curve for an orbit at a set of times

        Args:
            orbit: An object with a ``get_relative_position`` method that
                takes a tensor of times and returns a list of Cartesian
                coordinates of a set of bodies relative to the central source.
                This method should return three tensors (one for each
                coordinate dimension) and each tensor should have the shape
                ``append(t.shape, r.shape)`` or ``append(t.shape, oversample,
                r.shape)`` when ``texp`` is given. The first two coordinate
                dimensions are treated as being in the plane of the sky and the
                third coordinate is the line of sight with positive values
                pointing *away* from the observer. For an example, take a look
                at :class:`orbits.KeplerianOrbit`.
            r (tensor): The radius of the transiting body in the same units as
                ``r_star``. This should have a shape that is consistent with
                the coordinates returned by ``orbit``. In general, this means
                that it should probably be a scalar or a vector with one entry
                for each body in ``orbit``.
            t (tensor): The times where the light curve should be evaluated.
            texp (Optional[tensor]): The exposure time of each observation.
                This can be a scalar or a tensor with the same shape as ``t``.
                If ``texp`` is provided, ``t`` is assumed to indicate the
                timestamp at the *middle* of an exposure of length ``texp``.
            oversample (Optional[int]): The number of function evaluations to
                use when numerically integrating the exposure time.
            order (Optional[int]): The order of the numerical integration
                scheme. This must be one of the following: ``0`` for a
                centered Riemann sum (equivalent to the "resampling" procedure
                suggested by Kipping 2010), ``1`` for the trapezoid rule, or
                ``2`` for Simpson's rule.
            use_in_transit (Optional[bool]): If ``True``, the model will only
                be evaluated for the data points expected to be in transit
                as computed using the ``in_transit`` method on ``orbit``.

        """
        if orbit is None:
            raise ValueError("missing required argument 'orbit'")
        if r is None:
            raise ValueError("missing required argument 'r'")
        if t is None:
            raise ValueError("missing required argument 't'")

        use_in_transit = (
            not light_delay if use_in_transit is None else use_in_transit
        )

        r = as_tensor_variable(r)
        r = tt.reshape(r, (r.size,))
        t = as_tensor_variable(t)

        if use_in_transit:
            transit_model = tt.shape_padleft(
                tt.zeros_like(r), t.ndim
            ) + tt.shape_padright(tt.zeros_like(t), r.ndim)
            inds = orbit.in_transit(t, r=r, texp=texp, light_delay=light_delay)
            t = t[inds]

        if texp is None:
            tgrid = t
            rgrid = tt.shape_padleft(r, tgrid.ndim) + tt.shape_padright(
                tt.zeros_like(tgrid), r.ndim
            )
        else:
            texp = as_tensor_variable(texp)

            oversample = int(oversample)
            oversample += 1 - oversample % 2
            stencil = np.ones(oversample)

            # Construct the exposure time integration stencil
            if order == 0:
                dt = np.linspace(-0.5, 0.5, 2 * oversample + 1)[1:-1:2]
            elif order == 1:
                dt = np.linspace(-0.5, 0.5, oversample)
                stencil[1:-1] = 2
            elif order == 2:
                dt = np.linspace(-0.5, 0.5, oversample)
                stencil[1:-1:2] = 4
                stencil[2:-1:2] = 2
            else:
                raise ValueError("order must be <= 2")
            stencil /= np.sum(stencil)

            if texp.ndim == 0:
                dt = texp * dt
            else:
                if use_in_transit:
                    dt = tt.shape_padright(texp[inds]) * dt
                else:
                    dt = tt.shape_padright(texp) * dt
            tgrid = tt.shape_padright(t) + dt

            # Madness to get the shapes to work out...
            rgrid = tt.shape_padleft(r, tgrid.ndim) + tt.shape_padright(
                tt.zeros_like(tgrid), 1
            )

        coords = orbit.get_relative_position(tgrid, light_delay=light_delay)
        b = tt.sqrt(coords[0] ** 2 + coords[1] ** 2)
        b = tt.reshape(b, rgrid.shape)
        los = tt.reshape(coords[2], rgrid.shape)

        lc = self._compute_light_curve(
            b / orbit.r_star, rgrid / orbit.r_star, los / orbit.r_star
        )

        if texp is not None:
            stencil = tt.shape_padright(tt.shape_padleft(stencil, t.ndim), 1)
            lc = tt.sum(stencil * lc, axis=t.ndim)

        if use_in_transit:
            transit_model = tt.set_subtensor(transit_model[inds], lc)
            return transit_model
        else:
            return lc

    def _compute_light_curve(self, b, r, los=None):
        """Compute the light curve for a set of impact parameters and radii

        .. note:: The stellar radius is *not* included in this method so the
            coordinates should be in units of the star's radius.

        Args:
            b (tensor): A tensor of impact parameter values.
            r (tensor): A tensor of radius ratios with the same shape as ``b``.
            los (Optional[tensor]): The coordinates of the body along the
                line-of-sight. If ``los < 0`` the body is between the observer
                and the source.

        """
        b = as_tensor_variable(b)
        if los is None:
            los = tt.ones_like(b)
        return limbdark(self.c_norm, b, r, los)[0]


class StarryLightCurve(LimbDarkLightCurve):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "StarryLightCurve has been deprecated. "
            "Use LimbDarkLightCurve instead.",
            DeprecationWarning,
        )
        super(StarryLightCurve, self).__init__(*args, **kwargs)
