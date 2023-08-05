""" Export production algorithms
"""
import numpy as np

def eppley_1979(pprod):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    eprod =  0.0025 * pprod**2  #\; (PP \leq 200)
    eprod =  0.5 * pprod # (PP > 200)
    return eprod

def suess_1980(pprod, depthlevel):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    depthlevel : array_like
        Depth level over which to calculate export

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)


    Ref
    ---
    """
    return pprod / (0.0238*depthlevel + 0.212)


def betzer_1984(pprod, depthlevel):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    depthlevel : ndarray or scalar
        Depth level over which to calculate export

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    Betzer, P. R. et al. (1984), Primary productivity and particle fluxes 
    on a transect of the equator at 153°w in the pacific ocean, 
    Deep Sea Research Part A. Oceanographic Research Papers, 31(1), 1–11, 
    doi:10.1016/0198- 0149(84)90068-2.
    """
    return (0.0409*pprod**1.41) / (depthlevel**0.628)

def pace_1987(pprod, depthlevel):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    depthlevel : ndarray or scalar
        Depth level over which to calculate export

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    Betzer, P. R. et al. (1984), Primary productivity and particle fluxes 
    on a transect of the equator at 153°w in the pacific ocean, 
    Deep Sea Research Part A. Oceanographic Research Papers, 31(1), 1–11, 
    doi:10.1016/0198- 0149(84)90068-2.
    """
    return 3.523 * depthlevel**-0.734 * pprod**1.000

def baines_1994(pprod, chl):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    chl : array_like
        Chl concentration

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    Betzer, P. R. et al. (1984), Primary productivity and particle fluxes 
    on a transect of the equator at 153°w in the pacific ocean, 
    Deep Sea Research Part A. Oceanographic Research Papers, 31(1), 1–11, 
    doi:10.1016/0198- 0149(84)90068-2.
    """
    return pprod * 10**(0.67 + 0.30*np.log10(chl) + (0.27*np.log10(chl))**2)

def laws_2000(pprod, sst):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    return pprod * (0.62 - 0.02*sst)

def dunne_2005(pprod, sst, z_eup, chl=None):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)
    z_eup : array_like
        Depth of the euphotic zone defined as 1% light (m)
    chl : array_like
        Chl concentration (mg m-3)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    if chl is None:
        e_ratio = -0.0101*sst + 0.0582*np.log(pprod/z_eup) + 0.419
    else:
        e_ratio = -0.0081*sst + 0.0668*np.log(chl/z_eup) + 0.426
    if isinstance(e_ratio,np.ndarray):
        e_ratio[e_ratio>0.72] = 0.72
        e_ratio[e_ratio<0.04] = 0.04
    else:
        e_ratio = np.max([e_ratio, 0.04])
        e_ratio = np.min([e_ratio, 0.72])
    return pprod * e_ratio

def henson_2011(pprod, sst):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    return pprod * 0.23 * np.exp(-0.08 * sst)

def laws_2011a(pprod, sst):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    return pprod * ((0.5857 - 0.0165*sst) * pprod) / (51.7 + pprod)

def laws_2011b(pprod, sst):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    return pprod * 0.04756 * (0.78 - (0.43*sst)/30) * pprod**0.307

def li_2016(pprod, sst):
    """Export production from satellite derived properties
    
    Parameters
    ----------
    pprod: array_like
        Primary Production (mg C m-3)
    sst : array_like
        Sea Surface Temperature (degC)

    Returns
    -------
    eprod : ndarray or scalar
        Export production (mg C m-3)

    Ref
    ---
    """
    return (8.57 * pprod) / (17.9 + sst)




"""
\subsection{Westberry 2012}
\begin{equation}
EP = PP -  1.01 \cdot PP^{0.82} \; (all data) \\
EP = PP -  0.93 \cdot PP^{0.78} \; (open ocean)
\end{equation}Open Ocean


\subsection{Siegel 2014}

\begin{equation}
AlgEP = f_{Alg} \cdot PP{_M}
\end{equation}
\begin{equation}
G_M =  PP_M - \frac{\partial P_M}{\partial t} - m_{ph}P_m - AlgEZ
\end{equation}
\begin{equation}
G_S =  PP_S - \frac{\partial P_S}{\partial t} - m_{ph}P_s 
\end{equation}
\begin{equation}
FecEP = f_{FecM} \cdot G_M +  f_{FecS} \cdot G_S
\end{equation}
\begin{equation}
EP = AlgEP + FecEP
\end{equation}

\noindent $AlgEP$ is the total vertical ﬂux of sinking algal cells and aggregates and $FecEP$ is the total vertical ﬂux of sinking fecal material released from zooplankton grazers.  $f_{Alg}$ is the fraction of microphytoplankton production that sinks out of the base of the euphotic zone (assumed by \citet{Siegel_2014} to be 0.1) and $PP_M$ is the primary production of microphytoplankton. $f_{FecM}$ and $f_{FecS}$ are the fractions of grazing on microphytoplankton and smaller ($<$20 $\mu$m) phytoplankton, respectively, that contribute to fecal matter export from the euphotic zone (assumed by  \citet{Siegel_2014} to be 0.3 and 0.1, respectively). $G_M$ and $G_S$ are the grazing rates on microphytoplankton and small phytoplankton and are derived from phytoplankton mass balance budgets:
"""