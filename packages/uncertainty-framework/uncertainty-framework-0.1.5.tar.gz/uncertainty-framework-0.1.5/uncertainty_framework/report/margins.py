import numpy as np
from uncertainty_framework.report._report import Report


class MarginReport(Report):
    """Margin report

    Report class for returning numerical result margins.
    The default behavior is to return the (low, high) 
    tuples of the result 95% confidence interval 

    """
    def render(self, q=5, agg='median', **kwargs) -> np.ndarray:
        """render

        Renders the report. 

        Parameters
        ----------
        q : int
            the margin to use to calculate the confidence
            interval. will use the q and 100 - q 
            percentile.
        agg : str
            The aggragation function to use to calcualte the
            main simulation result. Can be either 'median'
            or 'mean'. If `None`, the result will not be
            aggregated.
        
        Returns
        -------
        margins : np.ndarray
            Array of (result_len, 2) or (result_len, 3), whether
            the aggreation is added or not. If agg is not None,
            the order of the second axis is [low, agg, high]
        """
        # reshape if needed
        if len(self.result.shape) == 1:
            result = self.result.reshape(-1, 1)
        else:
            result = self.result

        # calculate the margins
        low = np.percentile(result, q=q, axis=0)
        high = np.percentile(result, q=100 - q, axis=0)

        # calculate the agg
        if agg == 'median':
            loc = np.median(result, axis=0)
        elif agg == 'mean':
            loc = np.mean(result, axis=0)
        else:
            loc = None

        # reshape if needed
        if low.size == 1:
            low = low.reshape(-1,)
        if high.size == 1:
            high = high.reshape(-1,)
        if loc is not None and loc.size == 1:
            loc = loc.reshape(-1, )
        
        # stack the result
        if loc is None:
            return np.column_stack((low, high))
        else:
            return np.column_stack((low, loc, high))