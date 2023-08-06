# -*- coding: utf-8 -*-
import celerite2
import numpy as np
import pytest
from celerite2 import terms as pyterms
from celerite2.jax import GaussianProcess, terms
from celerite2.testing import check_gp_models

term_mark = pytest.mark.parametrize(
    "name,args",
    [
        ("RealTerm", dict(a=1.5, c=0.3)),
        ("ComplexTerm", dict(a=1.5, b=0.7, c=0.3, d=0.1)),
        ("SHOTerm", dict(S0=1.5, w0=2.456, Q=0.1)),
        ("SHOTerm", dict(S0=1.5, w0=2.456, Q=3.4)),
        ("SHOTerm", dict(sigma=1.5, w0=2.456, Q=3.4)),
        ("Matern32Term", dict(sigma=1.5, rho=3.5)),
        ("RotationTerm", dict(sigma=1.5, Q0=2.1, dQ=0.5, period=1.3, f=0.7)),
    ],
)


@term_mark
@pytest.mark.parametrize("mean", [0.0, 10.5])
def test_consistency(name, args, mean):
    # Generate fake data
    np.random.seed(40582)
    x = np.sort(np.random.uniform(0, 10, 50))
    t = np.sort(np.random.uniform(-1, 12, 100))
    diag = np.random.uniform(0.1, 0.3, len(x))
    y = np.sin(x)

    term = getattr(terms, name)(**args)
    gp = GaussianProcess(term, mean=mean)
    gp.compute(x, diag=diag)

    pyterm = getattr(pyterms, name)(**args)
    pygp = celerite2.GaussianProcess(pyterm, mean=mean)
    pygp.compute(x, diag=diag)

    check_gp_models(lambda x: np.asarray(x), gp, pygp, y, t)


def test_errors():
    # Generate fake data
    np.random.seed(40582)
    x = np.sort(np.random.uniform(0, 10, 50))
    t = np.sort(np.random.uniform(-1, 12, 100))
    diag = np.random.uniform(0.1, 0.3, len(x))
    y = np.sin(x)

    term = terms.SHOTerm(S0=1.0, w0=0.5, Q=3.0)
    gp = GaussianProcess(term)

    # Need to call compute first
    with pytest.raises(RuntimeError):
        gp.log_likelihood(y)

    # 1D
    with pytest.raises(ValueError):
        gp.compute(np.tile(x[:, None], (1, 5)), diag=diag)

    # Only one of diag and yerr
    with pytest.raises(ValueError):
        gp.compute(x, diag=diag, yerr=np.sqrt(diag))

    # Not positive definite
    gp.compute(x, diag=-10 * diag)
    ld = gp._log_det
    assert np.isinf(ld)
    assert ld < 0

    # Compute correctly
    gp.compute(x, diag=diag)
    gp.log_likelihood(y)

    # Dimension mismatch
    with pytest.raises(ValueError):
        gp.log_likelihood(y[:-1])

    with pytest.raises(ValueError):
        gp.log_likelihood(np.tile(y[:, None], (1, 5)))

    with pytest.raises(ValueError):
        gp.predict(y, t=np.tile(t[:, None], (1, 5)))
