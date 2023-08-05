import numpy as np
from .diagnosis import get_AICc, get_AIC, get_BIC, get_CV
from scipy.spatial.distance import pdist
from .model import GWR, TWR, GTWR
from .search import golden_section, twostep_golden_section

getDiag = {'AICc': get_AICc, 'AIC': get_AIC, 'BIC': get_BIC, 'CV': get_CV}

delta = 0.38197
class search_GWRparameter(object):
    
    def __init__(self, coords, y, X, kernel = 'exponential', fixed = False, constant=True):
        self.coords = coords
        self.y = y
        self.X = X
        self.n = X.shape[0]
        self.constant = constant
        if constant:
            self.k = X.shape[1] + 1
        else:
            self.k = X.shape[1]
        self.kernel = kernel
        self.fixed = fixed
        self.int_score = not self.fixed
        
    def search(self, criterion='AICc', bw_min = None, bw_max = None, tol=1.0e-6, bwdecimal = 0, 
               max_iter = 200, verbose = False):
        
        self.criterion = criterion
        self.bw_min = bw_min
        self.bw_max = bw_max
        self.tol = tol
        self.bwdecimal = bwdecimal
        self.max_iter = max_iter
        self.verbose = verbose
        
        self._bw()
        return self.bw
    
    def _bw(self):
        
        gwr_func = lambda bw : getDiag[self.criterion](GWR(
                self.coords, self.y, self.X, bw, kernel=self.kernel, 
                fixed=self.fixed, constant=self.constant).fit(final = False))
        
        self.bw_min, self.bw_max = self._init_section(self.X, self.coords, self.constant)
        self.bw = golden_section(self.bw_min, self.bw_max, delta, self.bwdecimal, 
                                 gwr_func, self.tol,self.max_iter, self.verbose)
    
    def _init_section(self, X, coords, constant):

        if len(X) > 0:
            n_glob = X.shape[1]
        else:
            n_glob = 0
        if constant:
            n_vars = n_glob + 1
        else:
            n_vars = n_glob
        n = np.array(coords).shape[0]

        if self.int_score:
            a = 40 + 2 * n_vars
            c = n
        else:
            sq_dists = pdist(coords)
            a = np.min(sq_dists) / 2.0
            c = np.max(sq_dists) 
        if self.bw_min is not None:
            a = self.bw_min
        if self.bw_max is not None:
            c = self.bw_max
            
        return a, c
    
class search_TWRparameter(object):
    
    def __init__(self, t, y, X, kernel = 'exponential', fixed = False, constant=True):
        self.t = t
        self.y = y
        self.X = X
        self.n = X.shape[0]
        self.constant = constant
        if constant:
            self.k = X.shape[1] + 1
        else:
            self.k = X.shape[1]
        self.kernel = kernel
        self.fixed = fixed
        
    def search(self, criterion='AICc', h_min = None, h_max = None, tol=1.0e-6, hdecimal = 0, 
               max_iter = 200, verbose = False):
        
        self.criterion = criterion
        self.h_min = h_min
        self.h_max = h_max
        self.tol = tol
        self.hdecimal = hdecimal
        self.max_iter = max_iter
        self.verbose = verbose
        
        self._h()
        return self.h
    
    def _h(self):
        
        twr_func = lambda h : getDiag[self.criterion](TWR(
                self.t, self.y, self.X, h, kernel=self.kernel, 
                fixed=self.fixed, constant=self.constant).fit(final = False))
        
        self.h_min, self.h_max = self._init_section(self.X, self.t, self.constant)
        self.h = golden_section(self.h_min, self.h_max, delta, self.hdecimal, 
                                 twr_func, self.tol,self.max_iter, self.verbose)
    
    def _init_section(self, X, t, constant):

        sq_dists = pdist(t)
        a = np.min(sq_dists) / 2.0
        c = np.max(sq_dists) 
        if self.h_min is not None:
            a = self.h_min
        if self.h_max is not None:
            c = self.h_max
        return a, c
        
class search_GTWRparameter(object):
    
    def __init__(self, coords, t, y, X, kernel = 'exponential', fixed = False, constant=True):
        self.coords = coords
        self.t = t
        self.y = y
        self.X = X
        self.n = X.shape[0]
        self.constant = constant
        if constant:
            self.k = X.shape[1] + 1
        else:
            self.k = X.shape[1]
        self.kernel = kernel
        self.fixed = fixed
        self.int_score = not self.fixed
        
    def search(self, criterion='AICc', bw_min = None, bw_max = None, tau_min = None, 
               tau_max = None, tol=1.0e-6, bwdecimal = 0, taudecimal = 1, max_iter = 200,
               verbose = False, mpi = False):
        
        self.criterion = criterion
        self.bw_min = bw_min
        self.bw_max = bw_max
        self.tau_min = tau_min
        self.tau_max = tau_max
        self.tol = tol
        self.bwdecimal = bwdecimal
        self.taudecimal = taudecimal
        self.max_iter = max_iter
        self.verbose = verbose
        self.mpi = mpi
        
        self._bwtau()
        return self.bw, self.tau
    
    def _bwtau(self):
        if self.mpi:
            gtwr_func = lambda bw, tau: getDiag[self.criterion](GTWR(
                self.coords, self.t, self.y, self.X, bw, tau, kernel=self.kernel, 
                fixed=self.fixed, constant=self.constant).fit(final = False,mpi=True),mpi=True)
            self.bw_min, self.bw_max, self.tau_min, self.tau_max = \
                self._init_section(self.X, self.coords, self.constant)
            self.bw, self.tau = twostep_golden_section(self.bw_min, self.bw_max, 
                self.tau_min, self.tau_max, delta, gtwr_func, self.tol, self.max_iter, 
                self.bwdecimal, self.taudecimal, self.verbose, self.mpi)
        else:    
            gtwr_func = lambda bw, tau: getDiag[self.criterion](GTWR(
                self.coords, self.t, self.y, self.X, bw, tau, kernel=self.kernel, 
                fixed=self.fixed, constant=self.constant).fit(final = False))
            self.bw_min, self.bw_max, self.tau_min, self.tau_max = \
                self._init_section(self.X, self.coords, self.constant)
            self.bw, self.tau = twostep_golden_section(self.bw_min, self.bw_max, 
                self.tau_min, self.tau_max, delta, gtwr_func, self.tol,
                self.max_iter, self.bwdecimal, self.taudecimal, self.verbose)
            
    def _init_section(self, X, coords, constant):
        if len(X) > 0:
            n_glob = X.shape[1]
        else:
            n_glob = 0
        if constant:
            n_vars = n_glob + 1
        else:
            n_vars = n_glob
        n = np.array(coords).shape[0]

        if self.int_score:
            a = 40 + 2 * n_vars
            c = n
        else:
            sq_dists = pdist(coords)
            a = np.min(sq_dists) / 2.0
            c = np.max(sq_dists) 

        if self.bw_min is not None:
            a = self.bw_min
        if self.bw_max is not None:
            c = self.bw_max
        
        if self.tau_min is not None:
            A = self.tau_min
        else:
            A = 0
        if self.tau_max is not None:
            C = self.tau_max
        else:
            C = 4       
        return a, c, A, C

        

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    