"""
Various ways to generate datapoints from the solution space, such that it is well covered.
Uses :class:`IO_Objects.Descriptor` to determine which inputs are valid.
"""

# Python Core Libraries
from typing import Callable, Any

# External Libraries
import numpy as np
import pandas as pd
import pyDOE2

# BESOS Imports
from besos.IO_Objects import Descriptor
from besos.problem import Problem


########################################################################################################
##############################     Static  sampling     ################################################
########################################################################################################


_sampler = Callable[[int, int, Any], np.ndarray]  # the format of all sampler functions


def dist_sampler(
    sampler: _sampler, problem: Problem, num_samples: int, *args, **kwargs
) -> pd.DataFrame:
    """uses the sampling function provided to generate `num_samples` sets of values
    These values will be valid for the corresponding inputs

    :param problem: Problem that the inputs should apply to
    :param sampler: a function that is used to produce the distribution of samples
    :param num_samples: number of samples to take

    :param args: Arguments passed to the sampling function
    :param kwargs: Arguments passed to the sampling function
    :return: pandas DataFrame with one column per parameter, and `num_samples` rows

    """
    samples = sampler(num_samples, problem.num_inputs, *args, **kwargs)
    data = {
        value_descriptor.name: _sample_param(value_descriptor, samples[:, i])
        for i, (value_descriptor) in enumerate(problem.value_descriptors)
    }

    df = pd.DataFrame(data)
    # enforce the correct order in case it was lost by the dictionary
    # this may be unnecessary with python 3.7+
    df = df[problem.names("inputs")]
    return df


def add_extremes(df: pd.DataFrame, problem: Problem) -> pd.DataFrame:
    """Adds two datapoints with the minimum and maximum values for each attribute.

    :param df: existing data to which the extreme values should be added.
    :param problem: the problem defining which values are valid.
    :return: df with 2 added rows, one with maximal values, one with minimal values.
    """
    new = dist_sampler(extremes, problem, 2)
    return pd.concat([df, new], ignore_index=True)


def extremes(samples: int, attributes: int = None) -> np.ndarray:
    """This sampler generates datapoints corresponding to the extremes of a problem.

    :param samples: the number of samples. Must be equal to 2
        (this argument is available in order to implement the sampler interface)
        If only one argument is provided, that argument will be assigned to attributes,
        even though samples is listed first.
    :param attributes: the number of attributes for which to generate samples
    :return: An array containing 2 samples: one with all zeroes, one with all ones.
        When transformed by a problem, these become minimal and maximal values for that problem.
    """
    if attributes is None:
        samples, attributes = 2, samples
    assert samples == 2, "extremes can only produce two samples"
    return np.array([np.zeros(attributes), np.ones(attributes)])


def _sample_param(descriptor: Descriptor, values):
    try:
        # this will only work if p.sample is numpy compatible
        return descriptor.sample(values)
    except TypeError:
        # apply non-vectorised version of p.sample
        return [descriptor.sample(x) for x in values]


# all of the following return a 2d array of shape (samples, attributes)
# which contains values between 0 and 1


random: _sampler = np.random.rand


def seeded_sampler(samples: int, attributes: int, seed=0) -> np.ndarray:
    np.random.seed(seed)
    return np.random.rand(samples, attributes)


def lhs(samples: int, attributes: int, *args, **kwargs) -> np.ndarray:
    return pyDOE2.lhs(attributes, samples, *args, **kwargs)


def full_factorial(samples: int, attributes: int, level: int = None) -> np.ndarray:
    if level is None:
        level = np.int(np.exp(np.log(samples) / attributes))
        if (level ** attributes) > level:
            print(
                f"Total number of samples ({level**attributes}) is smaller  than input ({samples}) "
                f"to have an even number of factor levels ({level}) for all parameters."
            )
    return pyDOE2.fullfact((np.ones([attributes]) * level).astype(int)) / level


########################################################################################################
##############################    Adaptive  sampling    ################################################
########################################################################################################


class adaptive_sampler_lv:
    """Represents an adaptive sampler which iteratively picks simulation samples and runs them."""

    def __init__(
        self,
        P,
        P_out,
        n_new,
        problem,
        evaluator,
        reg,
        test_in,
        test_out,
        scaler=None,
        scaler_out=None,
        verbose=False,
    ):
        if len(P[:, 0]) < 2 * len(P[0, :]):
            print(
                "Size of initial number of samples needs to be bigger than 2 times no. inputs."
            )
        self.P = P
        self.P_out = P_out
        self.n_new = n_new
        self.problem = problem
        self.evaluator = evaluator
        self.reg = reg
        self.scaler = scaler
        self.scaler_out = scaler_out
        self.verbose = verbose
        self.test_in = test_in
        self.test_out = test_out

    def run(self, no_iter):

        self.score = np.empty([no_iter + 1])
        self.score[0] = self.reg.score(self.test_in, self.test_out)

        self.N_P, self.S_P = init_Neighborhood(self.P)
        self.pick_new_samples()
        self.update_model()

        for i in range(no_iter):
            print(i)
            for p_new in self.P_new:
                self.N_P, self.S_P = update_Neighborhood(
                    self.N_P, self.P, self.S_P, p_new
                )
                if self.verbose == True:
                    print("initialize neighborhood for new samples")
                N_P_new, S_P_new = init_Neighborhood(self.P, p_new)
                self.N_P = np.append(self.N_P, N_P_new, axis=2)
                self.S_P = np.append(self.S_P, S_P_new, axis=0)
            # update existing set of samples
            self.P = np.append(self.P, self.P_new, axis=0)
            self.P_out = np.append(self.P_out, self.P_out_new, axis=0)
            self.pick_new_samples()

            self.update_model()

            self.score[i + 1] = self.reg.score(self.test_in, self.test_out)

    def update_model(self):
        self.reg.fit(self.P, self.P_out)
        if self.verbose == True:
            print(self.reg.score(self.P, self.P_out))

    def pick_new_samples(self):
        # 2) Compute nonlinearity measure and Voronoi Cell
        E = LOLA_estimate(
            self.N_P, self.P, self.reg, scaler=self.scaler, scaler_out=self.scaler_out
        )
        V_P, samples = MC_Voronoi_estimate(self.P, self.problem)
        H = hybrid_score(E, V_P)
        ind_new = np.argsort(H)
        P_sorted = self.P[ind_new, :]
        if self.verbose == True:
            print("Collecting new samples around:")
            print(P_sorted[-self.n_new :, :])

        # Generate new samples in Voronoi cell taking the mean of the neighborhood
        ind = 2
        self.P_new = np.empty([self.n_new, len(self.P[0, :])])
        for i in range(self.n_new):
            candidates = containedin_Voronoi(P_sorted[-i - 1, :], self.P, samples)
            # print(len(candidates))
            while len(candidates) <= 1:
                # print('in loop')
                candidates = containedin_Voronoi(P_sorted[-i - ind, :], self.P, samples)
                ind += 1
            self.P_new[i, :] = select_newSamp(
                P_sorted[-i - 1, :], self.N_P[:, :, ind_new][:, :, -i - 1], candidates
            )
        self.P_out_new = self.evaluator.df_apply(pd.DataFrame(self.P_new))


###############################################################
def hybrid_score(E, V):
    return V + E / sum(E)


def select_newSamp(p_r, N, candidates, verbose=False):
    N = np.append(N, [p_r], axis=0)
    max_dist = 0
    if verbose == True:
        print(len(candidates[1:, :]))
    for c in candidates[1:, :]:
        d = 0
        for n in N:
            d = d + np.linalg.norm(c - n)
        if d > max_dist:
            max_dist = d
            max_cand = c
    return max_cand


def MC_Voronoi_estimate(P, problem):
    # P are the existing points

    # initialize arrays
    V_P = np.zeros(
        [
            len(P),
        ]
    )  # Vector of all Voronoi sample estimates
    # per existing point collect randomly selected 100 points

    S = dist_sampler(
        lhs, problem, 500
    )  # for now 100 random samples per point to estimate Voronoi cell

    for s in S.values:
        d = np.inf
        ind = 0
        for p in P:
            if np.linalg.norm(p - s) < d:
                d = np.linalg.norm(p - s)
                ind_fin = ind
            ind = ind + 1
        V_P[ind_fin] = V_P[ind_fin] + 1 / len(S)
    # plt.plot(S.values[:, 0], S.values[:, 1], 'x')
    return V_P, S


def LOLA_estimate(N_P, P, model, scaler, scaler_out):
    # N_P is a 3-D array with all neighbors for each sample (mxdx#samples)
    # S_P is a 1_D array with the neighborhood score for all samples
    # P is the array including all samples

    n = len(P)
    ind = 0
    E = np.empty(
        [
            n,
        ]
    )
    for p_r in P:
        grad = Gradient_estimation(
            N_P[:, :, ind], p_r, model, scaler=scaler, scaler_out=scaler_out
        )
        E[ind] = Nonlinearity_measure(
            grad, N_P[:, :, ind], p_r, model, scaler=scaler, scaler_out=scaler_out
        )
        ind = ind + 1

    return E


def update_Neighborhood(N_P, P, S_P, P_new):
    # this function tries to add one new sample p_new to all of the existing neighborhoods
    # S is the neighborhood score
    # N_P are the associated neighbors of all points in P
    # P is the matrix of reference points
    # p_new the candidate
    if np.ndim(P) == 1:
        P = np.expand_dims(P, axis=0)
        N_P = np.reshape(N_P, (len(N_P[:, 0]), len(N_P[0, :]), 1))
        S_P = np.expand_dims(S_P, axis=0)

    if np.ndim(P_new) == 1:
        P_new = np.expand_dims(P_new, axis=0)

    m = 2 * len(P[0, :])
    ind = 0
    for p_new in P_new:
        for p_r in P:
            if sum(p_r == p_new) < len(P[0, :]):
                N_temp = np.dstack([N_P[:, :, ind]] * m)
                S_temp = np.zeros(
                    [
                        m,
                    ]
                )
                for i in range(m):
                    # replace one sample with the new one
                    if sum(sum(N_temp[:, :, i] == p_new)) < len(P[0, :]):
                        N_temp[i, :, i] = p_new
                    else:
                        pass
                    # compute neighborhood score for all possible combinations
                    S_temp[i] = Neighborhood_score(N_temp[:, :, i], p_r)
                    # if neighborhood score is better than the score without the new sample, update the neighborhood
                ind_min = np.argmin(S_temp)
                # print(ind_min)
                # print(S_temp)
                N_P[:, :, ind] = N_temp[:, :, ind_min]
                S_P[ind] = S_temp[ind_min]
                ind = ind + 1
            else:
                pass
                # print(N_P[:,:,1])
    return N_P, S_P


def init_Neighborhood(P, P_new=None, verbose=False):
    # P is the matrix with all samples
    # pnew optional if the neighborhood for new samples shall be computed
    # for now dim(pnew)=1 is assumed
    m = 2 * len(P[0, :])  # number of samples in neighborhood
    d = len(P[0, :])  # number of dimensions

    if np.any(P_new == None):
        # case I: first initialization after static sampling
        n = len(P)  # number of samples
        N_P = np.empty([m, d, n])
        S_P = np.empty(
            [
                n,
            ]
        )
        P_ref = (
            P * 1.0
        )  # array of all samples to be considered as reference in the next for loop
    else:
        # case II: initialize neighborhoods of new samples p_new
        if np.ndim(P_new) == 1:
            if verbose == True:
                print("ndim")
            P_ref = np.expand_dims(P_new, axis=0)
        else:
            P_ref = P_new * 1.0
        n_new = len(P_ref)  # number of new samples
        N_P = np.empty([m, d, n_new])
        S_P = np.empty(
            [
                n_new,
            ]
        )

    for i in range(len(P_ref)):
        mask = P != P_ref[i, :]
        P_NoRefPoint = P[mask[:, 0], :]
        N_P[:, :, i] = P_NoRefPoint[0:m, :]
        S_P[i] = Neighborhood_score(N_P[:, :, i], P_ref[i, :])
    ind = 0
    for p_cand in P:
        ind += 1
        # at the moment p_new to in P --> only 1 p_new allowed
        N_P, S_P = update_Neighborhood(N_P, P_ref, S_P, p_cand)
    if verbose == True:
        print("Neighborhood initiated!")
    return N_P, S_P


def Neighborhood_score(N, p_r):
    # To Do: make it possible to have 3D arrays as inputs
    # N is the neighborhood
    # P_cand should have m entries
    m = len(N)

    # initialize arrays
    Dist_cand = np.empty(
        [
            m,
        ]
    )
    minDist = np.empty(
        [
            m,
        ]
    )

    # compute distance matrix
    C = 0
    for i in range(m):
        C = C + np.linalg.norm(N[i, :] - p_r)
    C = C / m

    for i in range(m):
        for j in range(m):
            if i == j:
                pass
            else:
                Dist_cand[i] = np.linalg.norm(N[i, :] - N[j, :])
        minDist[i] = min(Dist_cand)

    A = 1 / m * sum(minDist)
    R = A / (np.sqrt(2) * C)
    return R / C


def Gradient_estimation(N, p_r, model, scaler, scaler_out):
    m = len(N)
    d = len(p_r)

    P_mat = np.empty([m, d])
    F_mat = np.empty(
        [
            m,
        ]
    )

    for i in range(m):
        P_mat[i, :] = N[i, :] - p_r
        if scaler == None:
            F_mat[i] = model.predict([N[i, :]])
        else:
            F_mat[i] = scaler_out.inverse_transform(
                model.predict(scaler.transform([N[i, :]]))
            )
    # grad = np.linalg.solve(P_mat,F_mat.reshape((len(F_mat),1)))
    grad = np.linalg.lstsq(P_mat, np.transpose(F_mat), rcond=None)[0].reshape((1, d))
    return [grad]


def Nonlinearity_measure(grad, N, p_r, model, scaler, scaler_out):
    E = 0
    for i in range(len(N)):
        if scaler == None:
            E = E + abs(
                model.predict([N[i, :]])
                - (model.predict([p_r]) + np.dot(grad, (N[i, :] - p_r)))
            )
        else:
            E = E + abs(
                scaler_out.inverse_transform(model.predict(scaler.transform([N[i, :]])))
                - (
                    scaler_out.inverse_transform(model.predict(scaler.transform([p_r])))
                    + np.dot(grad, (N[i, :] - p_r))
                )
            )
    return E


def containedin_Voronoi(p_r, P, samples):
    mask = P != p_r
    P_temp = P[mask[:, 0], :]
    candidates = np.empty([1, len(P[0, :])])
    for s in samples.values:
        for p_j in P_temp:
            if np.linalg.norm(s - p_j) <= np.linalg.norm(s - p_r):
                break
            else:
                continue
        if np.all(p_j == P[-1]):
            candidates = np.append(candidates, [s], axis=0)

    return candidates
