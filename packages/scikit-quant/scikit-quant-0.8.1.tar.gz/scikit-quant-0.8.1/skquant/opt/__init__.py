from __future__ import print_function

import logging
import subprocess
import sys
from SQCommon import Result, ObjectiveFunction


__all__ = [
    'methods',
    'minimize',
    'log',
    ]

log = logging.getLogger('SKQ')


def _check_orbit_prerequisites():
    try:
        import rpy2
        return True
    except ImportError:
        pass
    return False

def methods():
    """Returns a list of available optimizer methods"""

    m = ['imfil', 'snobfit', 'nomad', 'bobyqa']
    if _check_orbit_prerequisites():
        m.append('orbit')

    return m


def minimize(func, x0, bounds, budget=10000, method='imfil', options=None, **optkwds):
    optimizer = None

    method_ = method.lower()
    if 'imfil' in method_:
        import SQImFil as optimizer
        import SQImFil._optset as _optset   # ImFil standalone has a different API
        _optset.STANDALONE = False
    elif 'snobfit' in method_ :
        import SQSnobFit as optimizer
    elif 'nomad' in method_ :
        import SQNomad as optimizer
    elif 'bobyqa' in method_:
        import skquant.opt._pybobyqa as optimizer
    elif 'orbit' in method_:
        if not _check_orbit_prerequisites():
            raise RuntimeError("ORBIT requires rpy2 (and octave) to be installed")
        import skquant.opt._norbitR as optimizer

    if optimizer is not None:
        return optimizer.minimize(func, x0, bounds, budget, options, **optkwds)

    raise RuntimeError('unknown optimizer "%s"' % method)
