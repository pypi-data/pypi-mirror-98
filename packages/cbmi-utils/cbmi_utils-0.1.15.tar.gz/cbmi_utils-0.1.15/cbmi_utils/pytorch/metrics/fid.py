import numpy
import torch
from numpy import iscomplexobj
from torchmetrics import Metric

# docu https://torchmetrics.readthedocs.io/en/latest/

# how-to: https://machinelearningmastery.com/how-to-implement-the-frechet-inception-distance-fid-from-scratch/

# git: https://github.com/mseitzer/pytorch-fid
# score source: https://github.com/mseitzer/pytorch-fid/blob/master/src/pytorch_fid/fid_score.py


def cov(m, rowvar=True, inplace=False):
    ''' 
    From https://stackoverflow.com/questions/51416825/calculate-covariance-matrix-for-complex-data-in-two-channels-no-complex-data-ty/51422002

    Estimate a covariance matrix given data.

    Covariance indicates the level to which two variables vary together.
    If we examine N-dimensional samples, `X = [x_1, x_2, ... x_N]^T`,
    then the covariance matrix element `C_{ij}` is the covariance of
    `x_i` and `x_j`. The element `C_{ii}` is the variance of `x_i`.

    Args:
        m: A 1-D or 2-D array containing multiple variables and observations.
            Each row of `m` represents a variable, and each column a single
            observation of all those variables.
        rowvar: If `rowvar` is True, then each row represents a
            variable, with observations in the columns. Otherwise, the
            relationship is transposed: each column represents a variable,
            while the rows contain observations.

    Returns:
        The covariance matrix of the variables.
    '''
    if m.dim() > 2:
        raise ValueError('m has more than 2 dimensions')
    if m.dim() < 2:
        m = m.view(1, -1)
    if not rowvar and m.size(0) != 1:
        m = m.t()
    # m = m.type(torch.double)  # uncomment this line if desired
    fact = 1.0 / (m.size(1) - 1)
    if inplace:
        m -= torch.mean(m, dim=1, keepdim=True)
    else:
        m = m - torch.mean(m, dim=1, keepdim=True)
    mt = m.t()  # if complex: mt = m.t().conj()
    return fact * m.matmul(mt).squeeze()


class FID(Metric):
    """
    Fréchet inception distance

    Paper: https://arxiv.org/abs/1706.08500
    """

    def __init__(self, dist_sync_on_step=False):
        # call `self.add_state`for every internal state that is needed for the metrics computations
        # dist_reduce_fx indicates the function that should be used to reduce
        # state from multiple processes
        super(FID, self).__init__(dist_sync_on_step=dist_sync_on_step)
        self.add_state("score", default=torch.tensor(0), dist_reduce_fx="sum")

    def update(self, preds: torch.Tensor, target: torch.Tensor):
        # TODO update metric states?
        # preds, target = self._input_format(preds, target)
        assert preds.shape == target.shape

        # # calculate mean and covariance statistics
        mu1, sigma1 = preds.mean(axis=0), cov(preds, rowvar=False)
        mu2, sigma2 = target.mean(axis=0), cov(target, rowvar=False)

        # TODO  variant 1 (https://machinelearningmastery.com/how-to-implement-the-frechet-inception-distance-fid-from-scratch/)
        # calculate sum squared difference between means
        ssdiff = torch.sum((mu1 - mu2)**2.0)
        # calculate sqrt of product between cov
        covmean = torch.sqrt(torch.matmul(sigma1, sigma2))
        # check and correct imaginary numbers from sqrt
        if iscomplexobj(covmean):
            covmean = covmean.real
        # calculate score
        self.score = ssdiff + torch.trace(sigma1 + sigma2 - 2.0 * covmean)

        # TODO variant 2 (https://github.com/mseitzer/pytorch-fid/blob/master/src/pytorch_fid/fid_score.py#L178)
        # eps = 1e-6
        # diff = mu1 - mu2

        # # Product might be almost singular
        # covmean, _ = torch.sqrt(torch.matmul(sigma1, sigma2))
        # if not np.isfinite(covmean).all():
        #     msg = ('fid calculation produces singular product; '
        #            'adding %s to diagonal of cov estimates') % eps
        #     print(msg)
        #     offset = torch.eye(sigma1.shape[0]) * eps
        #     covmean = torch.sqrt(torch.matmul(sigma1 + offset), (sigma2 + offset))

        # # Numerical error might give slight imaginary component
        # if np.iscomplexobj(covmean):
        #     if not np.allclose(torch.diagonal(covmean).imag, 0, atol=1e-3):
        #         m = torch.max(torch.abs(covmean.imag))
        #         raise ValueError('Imaginary component {}'.format(m))
        #     covmean = covmean.real

        # tr_covmean = torch.trace(covmean)

        # self.score = (diff.matmul(diff) + torch.trace(sigma1) +
        #               torch.trace(sigma2) - 2 * tr_covmean)

    def compute(self):
        # compute final result
        return self.score

