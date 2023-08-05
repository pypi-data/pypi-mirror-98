import numpy as np
from .kernels import GWRKernel, GTWRKernel
from scipy import linalg

def _compute_betas_gwr(y, x, wi):
    """
    compute MLE coefficients using iwls routine

    Methods: p189, Iteratively (Re)weighted Least Squares (IWLS),
    Fotheringham, A. S., Brunsdon, C., & Charlton, M. (2002).
    Geographically weighted regression: the analysis of spatially varying relationships.
    """
    xT = (x * wi).T
    xtx = np.dot(xT, x)
    xtx_inv_xt = linalg.solve(xtx, xT)
    betas = np.dot(xtx_inv_xt, y)
    return betas, xtx_inv_xt


class GWR(object):
    
    def __init__(self, coords, y, X, bw, kernel = 'gaussian', 
                 fixed = False, constant = True):
        
        self.coords = coords
        self.y = y
        self.n = X.shape[0]
        self.bw = bw
        self.kernel = kernel
        self.fixed = fixed
        self.constant = constant
        if self.constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]
            
    def _build_wi(self, i, bw):

        try:
            wi = GWRKernel(i, self.coords, bw, fixed=self.fixed,
                        function=self.kernel).kernel
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi
    
    def _local_fit(self, i, final = True):
        
        wi = self._build_wi(i, self.bw).reshape(-1, 1)
        betas, xtx_inv_xt = _compute_betas_gwr(self.y, self.X, wi)
        predy = np.dot(self.X[i], betas)[0]
        resid = self.y[i] - predy
        influ = np.dot(self.X[i], xtx_inv_xt[:, i])
        if not final:
            return resid * resid, influ
        else:
            Si = np.dot(self.X[i], xtx_inv_xt).reshape(-1)
            CCT = np.diag(np.dot(xtx_inv_xt, xtx_inv_xt.T)).reshape(-1)
            Si2 = np.sum(Si**2)
            return influ, resid, predy, betas.reshape(-1), CCT, Si2
    
    def fit(self, final = True):
        
        if not final:
            RSS = 0
            tr_S = 0
            aa = 0
            for i in range(self.n):
                err2, hat = self._local_fit(i, final = False)
                aa += err2 / ((1 - hat) ** 2)
                RSS += err2
                tr_S += hat
            llf = -np.log(RSS) * self.n / \
                2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
            return Notfinal(float(RSS), tr_S, float(llf), float(aa), self.n)
        else:   
            influ, resid, predy = np.empty((self.n, 1)), \
                np.empty((self.n, 1)), np.empty((self.n, 1))
            betas, CCT = np.empty((self.n, self.k)), np.empty((self.n, self.k))
            tr_STS = 0
            for i in range(self.n):
                influi, residi, predyi, betasi, CCTi, tr_STSi = self._local_fit(i)
                influ[i] = influi
                resid[i] = residi
                predy[i] = predyi
                betas[i] = betasi
                CCT[i] = CCTi                 
                tr_STS += tr_STSi        
            return Final(self.coords, None, self.y, self.X, self.bw, None, 
                         self.kernel, self.fixed, self.constant, influ, resid, predy, 
                        betas, CCT, tr_STS, model = 'GWR')
        
        

class TWR(object):
    
    def __init__(self, t, y, X, h, kernel = 'gaussian', 
                 fixed = False, constant = True):
        
        self.t = t
        self.y = y
        self.n = X.shape[0]
        self.h = h
        self.kernel = kernel
        self.fixed = fixed
        self.constant = constant
        if self.constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]
            
    def _build_wi(self, i, h):

        try:
            wi = GWRKernel(i, self.t, h, fixed=self.fixed,
                        function=self.kernel).kernel
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi
    
    def _local_fit(self, i, final = True):
        
        wi = self._build_wi(i, self.h).reshape(-1, 1)
        X_derivative = self.X * (self.t-self.t[i])
        X_new = np.hstack([self.X, X_derivative])
        xT = (X_new * wi).T
        xtx_inv_xt = np.dot(np.linalg.inv(np.dot(xT, X_new)), xT)
        xstack = np.hstack([self.X[i].reshape(1,self.k),np.zeros((1,self.k))])
        predy = (np.dot(np.dot(xstack, xtx_inv_xt), self.y))[0] 
        resid = self.y[i] - predy
        influ = np.dot(xstack, xtx_inv_xt[:,i])[0]  
        if not final:
            return resid * resid, influ
        else:
            betas = np.dot(xtx_inv_xt, self.y)[:self.k]
            zeros = np.zeros((1,self.k))
            Si = np.dot(np.hstack([self.X[i].reshape(1,self.k),zeros]), xtx_inv_xt).reshape(-1)
            Si2 = np.sum(Si**2)
            return influ, resid, predy, betas.reshape(-1), Si2
    
    def fit(self, final = True):
        
        if not final:
            RSS = 0
            tr_S = 0
            aa = 0
            for i in range(self.n):
                err2, hat = self._local_fit(i, final = False)
                aa += err2 / ((1 - hat) ** 2)
                RSS += err2
                tr_S += hat
            llf = -np.log(RSS) * self.n / \
                2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
            return Notfinal(float(RSS), tr_S, float(llf), float(aa), self.n)
        else:   
            influ, resid, predy = np.empty((self.n, 1)), \
                np.empty((self.n, 1)), np.empty((self.n, 1))
            betas = np.empty((self.n, self.k))
            tr_STS = 0
            for i in range(self.n):
                influi, residi, predyi, betasi, tr_STSi = self._local_fit(i)
                influ[i] = influi
                resid[i] = residi
                predy[i] = predyi
                betas[i] = betasi                
                tr_STS += tr_STSi        
            return Final(self.t, None, self.y, self.X, self.h, None, 
                         self.kernel, self.fixed, self.constant, influ, resid, predy, 
                        betas, None, tr_STS, model = 'TWR')
       

class GTWR(object):

    def __init__(self, coords, t, y, X, bw, tau, kernel = 'gaussian', 
                 fixed = False, constant = True):
        self.coords = coords
        self.t = t
        self.y = y
        self.n = X.shape[0]
        self.bw = bw
        self.tau = tau
        self.kernel = kernel
        self.fixed = fixed
        self.constant = constant
        if self.constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]
        self.bw_s = self.bw
        self.bw_t = np.sqrt(self.bw**2 / self.tau)
        
    def _build_wi(self, i, bw, tau):

        try:
            wi = GTWRKernel(i, self.coords, self.t, bw, tau, fixed=self.fixed,
                        function=self.kernel).kernel
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi

    def _local_fit(self, i, final = True, multi = False):
        
        wi = self._build_wi(i, self.bw, self.tau).reshape(-1, 1)
        betas, xtx_inv_xt = _compute_betas_gwr(self.y, self.X, wi)
        predy = np.dot(self.X[i], betas)[0]
        resid = self.y[i] - predy
        influ = np.dot(self.X[i], xtx_inv_xt[:, i])
        if not final:
            return resid * resid, influ
        else:
            Si = np.dot(self.X[i], xtx_inv_xt).reshape(-1)
            CCT = np.diag(np.dot(xtx_inv_xt, xtx_inv_xt.T)).reshape(-1)
            Si2 = np.sum(Si**2)
            return influ, resid, predy, betas.reshape(-1), CCT, Si2 
        
    def fit(self, final = True, mpi = False):
        
        if mpi:
            from mpi4py import MPI
            import math
            comm = MPI.COMM_WORLD
            size = comm.Get_size()
            rank = comm.Get_rank()
            iter = np.arange(self.n)
            m = int(math.ceil(float(len(iter)) / size))
            x_chunk = iter[rank * m:(rank + 1) * m]
        if not final: 
            if mpi:
                RSS = 0
                tr_S = 0
                aa = 0
                for i in x_chunk:       
                    err2, hat = self._local_fit(i, final = False)
                    aa += err2 / ((1 - hat) ** 2)
                    RSS += err2
                    tr_S += hat
                aa_list = comm.gather(aa, root=0)
                RSS_list = comm.gather(RSS, root=0)
                trS_list = comm.gather(tr_S, root=0)
                if rank == 0:
                    RSS = sum(RSS_list)
                    tr_S = sum(trS_list)
                    aa = sum(aa_list)
                    llf = -np.log(RSS) * self.n / \
                    2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
                    return Notfinal(float(RSS), tr_S, float(llf), float(aa), self.n)
            else:
                RSS = 0
                tr_S = 0
                aa = 0
                for i in range(self.n):
                    err2, hat = self._local_fit(i, final = False)
                    aa += err2 / ((1 - hat) ** 2)
                    RSS += err2
                    tr_S += hat
                llf = -np.log(RSS) * self.n / \
                    2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
                return Notfinal(float(RSS), tr_S, float(llf), float(aa), self.n)
        else:
            if mpi:
                n_chunk = x_chunk.shape[0]
                influ, resid, predy = np.empty((n_chunk, 1)), \
                np.empty((n_chunk, 1)), np.empty((n_chunk, 1))
                betas, CCT = np.empty((n_chunk, self.k)), np.empty((n_chunk, self.k))
                tr_STS = 0
                pos = 0
                for i in x_chunk:
                    influi, residi, predyi, betasi, CCTi, tr_STSi = self._local_fit(i)
                    influ[pos] = influi
                    resid[pos] = residi
                    predy[pos] = predyi
                    betas[pos] = betasi
                    CCT[pos] = CCTi                   
                    tr_STS += tr_STSi
                    pos += 1
                influ_list = comm.gather(influ, root=0)
                resid_list = comm.gather(resid, root=0)
                predy_list = comm.gather(predy, root=0)
                betas_list = comm.gather(betas, root=0)
                CCT_list = comm.gather(CCT, root=0)
                tr_STS_list = comm.gather(tr_STS, root=0)   
                if rank == 0:
                    influ = np.vstack(influ_list)
                    resid = np.vstack(resid_list)
                    predy = np.vstack(predy_list)
                    betas = np.vstack(betas_list)
                    CCT = np.vstack(CCT_list)
                    tr_STS = sum(tr_STS_list)                        
                    return Final(self.coords, self.t, self.y, self.X, self.bw, 
                                 self.tau, self.kernel, self.fixed, self.constant, 
                                 influ, resid, predy, betas, CCT, tr_STS, model = 'GTWR')
                            
            else:   
                influ, resid, predy = np.empty((self.n, 1)), \
                    np.empty((self.n, 1)), np.empty((self.n, 1))
                betas, CCT = np.empty((self.n, self.k)), np.empty((self.n, self.k))
                tr_STS = 0
                for i in range(self.n):
                    influi, residi, predyi, betasi, CCTi, tr_STSi = self._local_fit(i)
                    influ[i] = influi
                    resid[i] = residi
                    predy[i] = predyi
                    betas[i] = betasi
                    CCT[i] = CCTi                   
                    tr_STS += tr_STSi           
                return Final(self.coords, self.t, self.y, self.X, self.bw, 
                             self.tau, self.kernel, self.fixed, self.constant, 
                             influ, resid, predy, betas, CCT, tr_STS, model = 'GTWR')
        
        
        
        
        
        
    
class Notfinal(object):
    
     def __init__(self, RSS, tr_S, llf, aa, n):
         self.RSS = RSS
         self.tr_S = tr_S
         self.llf = llf
         self.aa = aa
         self.n = n      
    
class Final(object):
   
    def __init__(self, coords, t, y, X, bw, tau, kernel, fixed, constant,
                 influ, resid, predy, betas, CCT, tr_STS, model):
        if model == 'GWR':
            GWR.__init__(self, coords, y, X, bw,  kernel, fixed, constant=False)
        if model == 'GTWR':
            GTWR.__init__(self, coords, t, y, X, bw, tau, kernel, fixed, constant=False)
        if model == 'TWR':
            TWR.__init__(self, t, y, X, bw,  kernel, fixed, constant=False)
        self.influ = influ
        self.resid = resid
        self.predy = predy
        self.betas = betas
        self.tr_S = np.sum(influ)
        self.ENP = self.tr_S
        self.tr_STS = tr_STS
        self.TSS = np.sum((y - np.mean(y))**2)
        self.RSS = np.sum(resid**2)
        self.sigma2 = self.RSS / (self.n - self.tr_S)
        if CCT is not None:
            self.CCT = CCT * self.sigma2
            self.bse = np.sqrt(self.CCT)
            self.tvalues = self.betas / self.bse
        else:
            self.CCT = None
            self.bse = None
            self.tvalues = None
        self.std_res = self.resid / (np.sqrt(self.sigma2 * (1.0 - self.influ)))      
        self.cooksD = self.std_res**2 * self.influ / \
            (self.tr_S * (1.0 - self.influ))    
        self.df_model = self.n - self.tr_S
        self.df_resid = self.n - 2.0 * self.tr_S + self.tr_STS
        self.R2 = 1 - self.RSS / self.TSS
        self.adj_R2 = 1 - (1 - self.R2) * (self.n - 1) / (self.n - self.ENP - 1)
        self.llf = -np.log(self.RSS) * self.n / \
                2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        self.aic = -2.0 * self.llf + 2.0 * (self.tr_S + 1)
        self.aicc = self.aic + 2.0 * self.tr_S * (self.tr_S + 1.0) / \
                  (self.n - self.tr_S - 1.0)
        self.bic = -2.0 * self.llf + (self.k + 1) * \
            np.log(self.n)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    