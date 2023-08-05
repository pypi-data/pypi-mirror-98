# experimental block start
# ##########################################################################################
# Copyright (c) 2021, INRIA                                                              #
# All rights reserved.                                                                   #
#                                                                                        #
# BSD License 2.0                                                                        #
#                                                                                        #
# Redistribution and use in source and binary forms, with or without                     #
# modification, are permitted provided that the following conditions are met:            #
# * Redistributions of source code must retain the above copyright notice,               #
# this list of conditions and the following disclaimer.                                  #
# * Redistributions in binary form must reproduce the above copyright notice,            #
# this list of conditions and the following disclaimer in the documentation              #
# and/or other materials provided with the distribution.                                 #
# * Neither the name of the <copyright holder> nor the names of its contributors         #
# may be used to endorse or promote products derived from this software without          #
# specific prior written permission.                                                     #
#                                                                                        #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND        #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED          #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.     #
# IN NO EVENT SHALL INRIA BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,       #
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF     #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,  #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS  #
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                           #
#                                                                                        #
# Contacts:                                                                              #
# 	Remi Gribonval  : remi.gribonval@inria.fr                                        #
# 	Hakim Hadj-dji. : hakim.hadj-djilani@inria.fr                                    #
#                                                                                        #
# Authors:                                                                               #
# 	Software Engineers:                                                              #
# 		Nicolas Bellot                                                           #
# 		Thomas Gautrais,                                                         #
# 		Hakim Hadj-Djilani,                                                      #
# 		Adrien Leman,                                                            #
#                                                                                        #
# 	Researchers:                                                                     #
# 		Luc Le Magoarou,                                                         #
# 		Remi Gribonval                                                           #
#                                                                                        #
# 	INRIA Rennes, FRANCE                                                             #
# 	http://www.inria.fr/                                                             #
##########################################################################################

## @package pyfaust.poly @brief This module provides polynomials as Faust objects.

import scipy.sparse as sp
from scipy.sparse import csr_matrix
import pyfaust as pf
from scipy.sparse.linalg import eigsh


def ChebyshevPhi(L, K, phi=None, dev='cpu'):
    """
    Builds the Faust of the Chebyshev polynomials defined on the symmetric matrix L using its greatest eigenvalue phi.

    Args:
        L: the symmetric matrix.
        phi: the greatest eigen value of the L matrix (if None, it is computed
        automatically using scipy.sparse.linalg.eigsh).
        K: the degree of the last polynomial, i.e. the K+1 first polynomials are built.
        dev: the destination device of the polynomial Faust.

    Returns:
        The Faust of the K+1 Chebyshev polynomials.

    """
    if phi is None:
        phi = eigsh(L, k=1, return_eigenvectors=False)[0] / 2
    d = L.shape[0]
    if not isinstance(L, csr_matrix):
        L = csr_matrix(L)
    L_phi = (1/phi)*L
    Id = T0 = sp.eye(d, format="csr")
    T1 = sp.vstack((Id, -Id+L_phi))
    rR = sp.hstack((-Id, 2*(L_phi-Id)), format="csr")
    return _chebyshev(L, K, T0, T1, rR, dev)

def Chebyshev(L, K, dev='cpu'):
    """
    Builds the Faust of the Chebyshev polynomials defined on the symmetric matrix L.

    Args:
        L: the symmetric matrix.
        K: the degree of the last polynomial, i.e. the K+1 first polynomials are built.
        dev: the destination device of the polynomial Faust.

    Returns:
        The Faust of the K+1 Chebyshev polynomials.
    """
    if not isinstance(L, csr_matrix):
        L = csr_matrix(L)
    twoL = 2*L
    d = L.shape[0]
    Id = T0 = sp.eye(d, format="csr")
    T1 = sp.vstack((Id, L))
    rR = sp.hstack((-Id, twoL), format="csr")
    return _chebyshev(L, K, T0, T1, rR, dev)


def _chebyshev(L, K, T0, T1, rR, dev='cpu'):
    Id = T0
    d = L.shape[0]
    factors = [Id]
    if(K > 0):
        factors.insert(0, T1)
        for i in range(2, K + 1):
            if i <= 2:
                R = rR
            else:
                zero = csr_matrix((d, (i-2)*d), dtype=float)
                R = sp.hstack((zero, rR), format="csr")
            Ti = sp.vstack((sp.eye(d*i, format="csr"), R),
                           format="csr")
            factors.insert(0, Ti)
    T = pf.Faust(factors, dev=dev)
    return T  # K-th poly is T[K*L.shape[0]:,:]


def polyFaust(coeffs, L=None, poly=Chebyshev, dev='cpu'):
    """
        Returns the linear combination of the polynomials defined by poly.

        Args:
            coeffs: the linear combination coefficients (numpy.array).
            poly: either the function to build the polynomials on L or the Faust of
            polynomials if already built.
            L: the symmetric matrix on which the polynomials are built, can't be None
            if poly is a function (not a Faust).
            dev: the device to instantiate the returned Faust ('cpu' or 'gpu').

        Returns:
            The linear combination Faust.
    """
    K = coeffs.size-1
    if pf.isFaust(poly):
        F = poly
        if F.device != dev:
            F = F.clone(dev=dev)
    else:
        if L is None:
            raise ValueError('The L matrix must be set to build the'
                             ' polynomials.')
        F = poly(L, K, dev=dev)
    Id = sp.eye(F.shape[1], format="csr")
    scoeffs = sp.hstack(tuple(Id*coeffs[i] for i in range(0, K+1)),
                        format="csr")
    Fc = pf.Faust(scoeffs, dev=dev) @ F
    return Fc
# experimental block end
