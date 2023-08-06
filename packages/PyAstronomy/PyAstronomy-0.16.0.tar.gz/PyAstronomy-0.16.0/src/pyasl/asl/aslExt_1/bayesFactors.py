from scipy.stats import f
import numpy as np
import scipy.special as ss
from PyAstronomy.pyaC import pyaErrors as PE
import scipy.stats as ss
import scipy.integrate as sci
import scipy.special as ssp

def bf_density(x, nu1, nu2, s1, s2, iq=0.001, fullOut=False):
    """
    Numerical evaluation of the Behrens-Fisher density
    
    BF density as given in Dalay et al. Eq. 2.8.
    
    Parameters
    ----------
    n1, n2 : float (>0)
        Degrees of freedom of the individual t-distributions
    s1, s2 : float (>0)
        Scales of the t-distributions
        
    Returns
    -------
    Density : float
        Density of the BF density
    Integration results : tuple
        Full output of scipy quadrature integration
    """
    if sum([nu1>0, nu2>0, s1>0, s2>0, iq>0]) != 5:
        raise(PE.PyAValError("All of nu1, nu2, s1, s2, iq must be positive. One found zero or negative."))
    
    # Point at which CDF of t-density reaches iq and 1-iq
    p10, p11 = ss.t.ppf(iq, nu1, scale=s1), ss.t.ppf(1-iq, nu1, scale=s1)
    p20, p21 = ss.t.ppf(iq, nu2, scale=s2), ss.t.ppf(1-iq, nu2, scale=s2)
    # Define integration boundaries
    p0 = min(p10, p20)
    p1 = max(p11, p21)
    f = lambda z: ss.t.pdf(x-z, nu1, scale=s1) * ss.t.pdf(z, nu2, scale=s2)
    r = sci.quad(f, p0, p1)
    if not fullOut:
        return r[0]
    else:
        return r[0], r


def c2_eq28(n1, n2, rho, S1, S2, nus, ss2):
    """
    Constant c**2
    
    between Eqs. 2.8 and 2.9 (Dayal)
    
    Parameters
    ----------
    n1, n2 : int (>0)
        Number of data points
    rho : float (>0)
        Ratio of standard deviations (s2 = rho*s1)
    S1, S2 : float (>0)
        Sums of squares
    nus : float (>0)
        Half the degrees of freedom of inv-chi-square prior
        of the variance
    ss2 : float (>0) 
        Scale parameter of the inv-chi-square prior
        of the variance
    """
    return (1/n1 + rho**2/n2) * (S1 + S2/rho**2 + 2*nus*ss2) / (n1+n2-2+2*nus)

