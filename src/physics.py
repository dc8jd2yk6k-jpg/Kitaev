"""Numerics for the Kitaev chain (cond-mat/0010440).

Conventions follow the paper: Majorana operators c_{2j-1}, c_{2j} on site j,
H = (i/4) sum_{lm} A_{lm} c_l c_m with A real antisymmetric (eq. 3, 6).
Indices here are 0-based: c_{2j-1} -> 2j, c_{2j} -> 2j+1 for j = 0..L-1.
"""
import numpy as np


def majorana_matrix(L, mu, w, delta, closed=False, boundary=1.0):
    """Real antisymmetric A of eq. (6) for a chain of L sites."""
    A = np.zeros((2 * L, 2 * L))

    def put(l, m, v):
        A[l, m] += v
        A[m, l] -= v

    for j in range(L):
        put(2 * j, 2 * j + 1, -mu)
    links = range(L) if closed else range(L - 1)
    for j in links:
        k = (j + 1) % L
        s = boundary if (closed and k == 0) else 1.0
        put(2 * j + 1, 2 * k, s * (w + delta))
        put(2 * j, 2 * k + 1, s * (-w + delta))
    return A


def energies(A):
    """Non-negative one-particle energies eps_m (eigenvalues of iA are +-eps_m)."""
    ev = np.linalg.eigvalsh(1j * A)
    return np.sort(ev[ev.size // 2:])


def bulk_spectrum(q, mu, w, delta):
    """Eq. (13)."""
    return np.sqrt((2 * w * np.cos(q) + mu) ** 2 + 4 * delta ** 2 * np.sin(q) ** 2)


def normal_band(q, mu, w):
    """Single spectrum eps_0(q) of the U(1)-symmetric part (Delta = 0)."""
    return -2 * w * np.cos(q) - mu


def zero_modes(L, mu, w, delta):
    """Return (eps, left, right): the lowest energy and the site-resolved weights
    of the two Majorana modes b' (left) and b'' (right)."""
    A = majorana_matrix(L, mu, w, delta)
    ev, vec = np.linalg.eigh(1j * A)
    i = np.argmin(np.abs(ev))
    v = vec[:, i]
    # +-eps eigenvectors are complex conjugates; their real and imaginary parts
    # span the two real Majorana modes. Rotate to make them maximally localized.
    re, im = np.real(v), np.imag(v)
    best = None
    for phi in np.linspace(0, np.pi, 721):
        a = np.cos(phi) * re + np.sin(phi) * im
        b = -np.sin(phi) * re + np.cos(phi) * im
        wa = a[0::2] ** 2 + a[1::2] ** 2
        x = np.arange(L)
        score = abs(np.dot(wa, x) / wa.sum() - (L - 1) / 2)
        if best is None or score > best[0]:
            best = (score, a, b)
    _, a, b = best
    wa = a[0::2] ** 2 + a[1::2] ** 2
    wb = b[0::2] ** 2 + b[1::2] ** 2
    wa, wb = wa / wa.sum(), wb / wb.sum()
    if np.dot(wa, np.arange(L)) > np.dot(wb, np.arange(L)):
        wa, wb = wb, wa
    return abs(ev[i]), wa, wb


def pfaffian(M):
    """Pfaffian of a real or complex antisymmetric matrix (Parlett-Reid style)."""
    A = np.array(M, dtype=complex)
    n = A.shape[0]
    if n % 2:
        return 0.0
    pf = 1.0 + 0j
    for k in range(0, n - 1, 2):
        p = k + 1 + np.argmax(np.abs(A[k, k + 1:]))
        if p != k + 1:
            A[[k + 1, p], :] = A[[p, k + 1], :]
            A[:, [k + 1, p]] = A[:, [p, k + 1]]
            pf = -pf
        if A[k, k + 1] == 0:
            return 0.0
        pf *= A[k, k + 1]
        if k + 2 < n:
            tau = A[k, k + 2:] / A[k, k + 1]
            A[k + 2:, k + 2:] += np.outer(tau, A[k + 2:, k + 1]) - np.outer(A[k + 2:, k + 1], tau)
    return pf


def bloch_B(q, mu, w, delta):
    """B~(q) of eq. (22) for the toy model (one site = 2 Majoranas per cell)."""
    B = {0: np.array([[0, -mu], [mu, 0]], float),
         1: np.array([[0, delta - w], [w + delta, 0]], float)}
    B[-1] = -B[1].T
    return sum(np.exp(1j * q * j) * Bj for j, Bj in B.items())


def majorana_number(mu, w, delta):
    """Eq. (26): M = sgn Pf B~(0) * sgn Pf B~(pi)."""
    a = np.real(pfaffian(bloch_B(0.0, mu, w, delta)))
    b = np.real(pfaffian(bloch_B(np.pi, mu, w, delta)))
    return int(np.sign(a) * np.sign(b))


def fermi_point_count(mu, w, n=4001):
    """Number of sign changes of eps_0(q) on [0, pi]."""
    e = normal_band(np.linspace(0, np.pi, n), mu, w)
    return int(np.sum(np.sign(e[1:]) != np.sign(e[:-1])))


def splitting_vs_length(Ls, mu, w, delta):
    return np.array([energies(majorana_matrix(L, mu, w, delta))[0] for L in Ls])


def josephson_branches(theta, t=0.12):
    """Two-valued Josephson energy of fig. 5b: +-cos(theta/2), split by t at theta = pi."""
    e = np.cos(theta / 2)
    return -np.sqrt(e ** 2 + t ** 2), np.sqrt(e ** 2 + t ** 2), -e, e


def _selftest():
    rng = np.random.default_rng(1)
    # 1. eq. (13) equals the spectrum of a closed chain at allowed momenta
    for _ in range(5):
        mu, w, d = rng.normal(size=3)
        L = 40
        # antiperiodic boundary removes the explicit q=0 subtleties; use periodic
        A = majorana_matrix(L, mu, w, d, closed=True)
        q = 2 * np.pi * np.arange(L) / L
        ref = np.sort(bulk_spectrum(q, mu, w, d))
        got = np.sort(energies(A))
        assert np.allclose(ref, got, atol=1e-9), (ref[:4], got[:4])
    # 2. zero modes iff 2|w| > |mu|
    for mu, w, d in [(0.5, 1, 0.7), (-1.2, 1, 0.3), (0.0, 1, 1.0)]:
        assert energies(majorana_matrix(60, mu, w, d))[0] < 1e-8
    for mu, w, d in [(2.5, 1, 0.7), (-3.0, 1, 0.3)]:
        assert energies(majorana_matrix(60, mu, w, d))[0] > 0.1
    # 3. Majorana number matches the phase diagram
    for _ in range(200):
        mu, w, d = rng.normal(size=3) * 2
        if abs(abs(2 * w) - abs(mu)) < 1e-3 or abs(d) < 1e-3:
            continue
        assert majorana_number(mu, w, d) == (-1 if 2 * abs(w) > abs(mu) else 1)
        # eq. (28): (-1)^(# Fermi points in [0, pi])
        assert (-1) ** fermi_point_count(mu, w) == majorana_number(mu, w, d)
    # 4. Pfaffian squared equals determinant
    for n in (2, 4, 6, 8):
        X = rng.normal(size=(n, n)); X = X - X.T
        assert np.isclose(pfaffian(X) ** 2, np.linalg.det(X))
    # 5. exponential splitting
    Ls = np.arange(6, 30, 2)
    s = splitting_vs_length(Ls, 0.8, 1.0, 0.4)
    slope = np.polyfit(Ls, np.log(s), 1)[0]
    assert slope < -0.1
    eps, l, r = zero_modes(40, 0.5, 1.0, 0.6)
    assert l[:5].sum() > 0.9 and r[-5:].sum() > 0.9
    print("physics self-test passed; splitting decay length l0 =", -1 / slope)


if __name__ == "__main__":
    _selftest()
