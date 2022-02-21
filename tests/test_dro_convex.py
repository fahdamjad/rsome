import rsome as rso
from rsome import dro
from rsome import grb_solver as grb
from rsome import E
import numpy as np
import numpy.random as rd
import pytest


@pytest.mark.parametrize('array, const', [
    (rd.rand(3, 8), rd.rand()),
    (rd.rand(4, 8), rd.rand()),
    (rd.rand(5, 1), rd.rand())
])
def test_norm_one(array, const):

    target = abs(array).sum(axis=1) + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = rso.norm(x, 1) + const
    m.minsup(E(a), fset)
    m.st(a >= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] - abs(array[s]).sum() - const) < 1e-4

    target = -abs(array).sum(axis=1) + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = - rso.norm(x, 1) + const
    m.maxinf(E(a), fset)
    m.st(a <= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] + abs(array[s]).sum() - const) < 1e-4

    with pytest.raises(ValueError):
        rso.norm(x, 1) + const >= 0

    with pytest.raises(ValueError):
        -rso.norm(x, 1) + const <= 0

    with pytest.raises(TypeError):
        rso.norm(x, 1) + const == 0


@pytest.mark.parametrize('array, const', [
    (rd.rand(3, 8), rd.rand()),
    (rd.rand(4, 8), rd.rand()),
    (rd.rand(5, 1), rd.rand())
])
def test_norm_two(array, const):

    target = (array**2).sum(axis=1)**0.5 + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = rso.norm(x, 2) + const
    m.minsup(E(a), fset)
    m.st(a >= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] - (array[s]**2).sum()**0.5 - const) < 1e-4

    target = -(array**2).sum(axis=1)**0.5 + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = - rso.norm(x, 2) + const
    m.maxinf(E(a), fset)
    m.st(a <= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] + (array[s]**2).sum()**0.5 - const) < 1e-4

    with pytest.raises(ValueError):
        rso.norm(x, 2) + const >= 0

    with pytest.raises(ValueError):
        -rso.norm(x, 2) + const <= 0

    with pytest.raises(TypeError):
        rso.norm(x, 2) + const == 0


@pytest.mark.parametrize('array, const', [
    (rd.rand(3, 8), rd.rand()),
    (rd.rand(4, 8), rd.rand()),
    (rd.rand(5, 1), rd.rand())
])
def test_norm_inf(array, const):

    target = array.max(axis=1) + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = rso.norm(x, 'inf') + const
    m.minsup(E(a), fset)
    m.st(a >= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] - (array[s]).max() - const) < 1e-4

    target = -array.max(axis=1) + const
    ns = array.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])

    z = m.rvar(array.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)

    expr = -rso.norm(x, 'inf') + const
    m.maxinf(E(a), fset)
    m.st(a <= expr)
    m.st(x == z)
    m.solve(grb)

    assert abs(m.get() - target.mean()) < 1e-4
    for s in range(ns):
        assert abs(a.get()[s] + (array[s]).max() - const) < 1e-4

    with pytest.raises(ValueError):
        rso.norm(x, 'inf') + const >= 0

    with pytest.raises(ValueError):
        -rso.norm(x, 'inf') + const <= 0

    with pytest.raises(TypeError):
        rso.norm(x, 'inf') + const == 0


@pytest.mark.parametrize('array, const', [
    (rd.rand(4, 8), rd.rand(4, 1)),
    (rd.rand(4, 8), rd.rand(4, 8)),
    (rd.rand(3, 1), rd.rand(3, 1)),
    (rd.rand(5, 1, 8), rd.rand(5, 3, 8)),
    (rd.rand(2, 3, 5), rd.rand(2, 3, 1)),
    (rd.rand(4, 3, 5), rd.rand(4, 1, 5)),
    (rd.rand(4, 1, 3, 5), rd.rand(4, 2, 3, 5)),
    (rd.rand(4, 2, 3, 5), rd.rand(4, 1, 3, 5))
])
def test_squares(array, const):

    target = array**2 + const
    ns = target.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    d = m.dvar(target.shape[1:])
    x = m.dvar(array.shape[1:])
    y = m.dvar(const.shape[1:])

    z = m.rvar(array.shape[1:])
    u = m.rvar(const.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s], u == const[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        d.adapt(s)
        x.adapt(s)
        y.adapt(s)

    expr = rso.square(x) + y
    m.minsup(E(a), fset)
    m.st(a >= d.sum())
    m.st(d >= expr)
    m.st(x == z, y == u)
    m.solve(grb)

    assert abs(m.get() - target.mean(axis=0).sum()) < 1e-4
    for s in range(ns):
        assert (abs(d.get()[s] - (array**2 + const)[s]) < 1e-4).all()

    target = -array**2 + const
    ns = target.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    d = m.dvar(target.shape[1:])
    x = m.dvar(array.shape[1:])
    y = m.dvar(const.shape[1:])

    z = m.rvar(array.shape[1:])
    u = m.rvar(const.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s], u == const[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        d.adapt(s)
        x.adapt(s)
        y.adapt(s)

    expr = -rso.square(x) + y
    m.maxinf(E(a), fset)
    m.st(a <= d.sum())
    m.st(d <= expr)
    m.st(x == z, y == u)
    m.solve(grb)

    assert abs(m.get() - target.mean(axis=0).sum()) < 1e-4
    for s in range(ns):
        assert (abs(d.get()[s] - (-array**2 + const)[s]) < 1e-4).all()

    with pytest.raises(ValueError):
        rso.square(x) + y >= 0

    with pytest.raises(ValueError):
        -rso.square(x) + y <= 0

    with pytest.raises(TypeError):
        rso.square(x) + y == 0


@pytest.mark.parametrize('array, const', [
    (rd.rand(3, 8), rd.rand(3)),
    (rd.rand(4, 8), rd.rand(4)),
    (rd.rand(5, 1), rd.rand(5))
])
def test_square_sum(array, const):

    target = (array**2).sum(axis=1) + const
    ns = target.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])
    y = m.dvar(const.shape[1:])

    z = m.rvar(array.shape[1:])
    u = m.rvar(const.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s], u == const[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)
        y.adapt(s)

    expr = rso.sumsqr(x) + y
    m.minsup(E(a), fset)
    m.st(a >= expr)
    m.st(x == z, y == u)
    m.solve(grb)

    assert (abs(a.get().values - target) < 1e-4).all()
    assert abs(m.get() - target.mean()) < 1e-4

    target = -(array**2).sum(axis=1) + const
    ns = target.shape[0]

    m = dro.Model(ns)
    a = m.dvar()
    x = m.dvar(array.shape[1:])
    y = m.dvar(const.shape[1:])

    z = m.rvar(array.shape[1:])
    u = m.rvar(const.shape[1:])
    fset = m.ambiguity()
    for s in range(ns):
        fset[s].suppset(z == array[s], u == const[s])
    p = m.p
    fset.probset(p == 1/ns)

    for s in range(ns):
        a.adapt(s)
        x.adapt(s)
        y.adapt(s)

    expr = -rso.sumsqr(x) + y
    m.maxinf(E(a), fset)
    m.st(a <= expr)
    m.st(x == z, y == u)
    m.solve(grb)

    assert (abs(a.get().values - target) < 1e-4).all()
    assert abs(m.get() - target.mean()) < 1e-4

    with pytest.raises(ValueError):
        rso.sumsqr(x) + y >= 0

    with pytest.raises(ValueError):
        -rso.sumsqr(x) + y <= 0

    with pytest.raises(TypeError):
        rso.sumsqr(x) + y == 0


@pytest.mark.parametrize('array, const', [
    (rd.rand(5), rd.rand()),
    (rd.rand(3), rd.rand(2)),
    (rd.rand(1), rd.rand(1))
])
def test_quad(array, const):

    vec = rd.rand(array.shape[0]).round(4)
    # qmat = vec.reshape((vec.size, 1)) @ vec.reshape((1, vec.size))
    qmat = np.diag(vec)

    target = array@qmat@array + const

    m = dro.Model()
    a = m.dvar()
    x = m.dvar(array.shape)

    expr = x.quad(qmat) + const
    m.min(a)
    m.st(a >= expr)
    m.st(x == array)
    m.solve(grb)

    assert abs(m.get() - target.max()) < 1e-4
    assert type(expr) == rso.lp.DecConvex
    if target.shape == ():
        assert expr.__repr__() == 'a sum of squares expression'
    else:
        shape_str = 'x'.join([str(dim) for dim in target.shape])
        suffix = 's' if target.size > 1 else ''
        assert expr.__repr__() == f'{shape_str} sum of squares expression{suffix}'

    target = -array@qmat@array + const

    m = dro.Model()
    a = m.dvar()
    x = m.dvar(array.shape)

    expr = - x.quad(qmat) + const
    m.max(a)
    m.st(a <= expr)
    m.st(x == array)
    m.solve(grb)

    assert abs(m.get() - target.min()) < 1e-4
    assert type(expr) == rso.lp.DecConvex
    if target.shape == ():
        assert expr.__repr__() == 'a sum of squares expression'
    else:
        shape_str = 'x'.join([str(dim) for dim in target.shape])
        suffix = 's' if target.size > 1 else ''
        assert expr.__repr__() == f'{shape_str} sum of squares expression{suffix}'

    with pytest.raises(ValueError):
        x.quad(qmat) + const >= 0

    with pytest.raises(ValueError):
        -x.quad(qmat) + const <= 0

    with pytest.raises(TypeError):
        rso.quad(x, qmat) + const == 0


def test_convex_err():

    model = dro.Model()
    x = model.dvar(5)
    xx = model.dvar((6, 7))

    with pytest.raises(ValueError):
        rso.norm(xx, 1)

    with pytest.raises(ValueError):
        rso.norm(xx, 2)

    with pytest.raises(ValueError):
        rso.norm(xx, 'inf')

    with pytest.raises(ValueError):
        rso.sumsqr(xx)

    vec = rd.rand(7)
    qmat = vec.reshape((vec.size, 1)) @ vec.reshape((1, vec.size))
    with pytest.raises(ValueError):
        rso.quad(xx, qmat)

    qmat = rd.rand(5, 5)
    with pytest.raises(ValueError):
        rso.quad(x, qmat)
