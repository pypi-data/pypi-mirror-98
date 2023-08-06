"""
Variogram estimation
--------------------

This example illustrates how the MonteCarlo class can be used
to simulate uncertain observations for a Variogram analysis.

"""
import os
import time
from uncertainty_framework import MonteCarlo
import numpy as np
from skgstat import Variogram
import pandas as pd
import plotly.graph_objects as go

PATH = os.path.abspath(os.path.dirname(__file__))


def variogram(**kwargs):
    # create a variogram with the new arguments
    V = Variogram(**kwargs)

    # Monte Carlo forces us to return np.ndarrays
    return np.asarray(V.experimental)


def get_arguments(**kwargs):
    # these will be kept fixed for each run
    args = dict(
        model=kwargs.get('model', 'exponential'),
        fit_method=kwargs.get('fit_method', 'trf'),
        fit_sigma=kwargs.get('fit_sigma'),
        estimator=kwargs.get('estimator', 'matheron'),
        maxlag=kwargs.get('maxlag', 'median'),
        n_lags=kwargs.get('n_lags', 10),
        bin_func=kwargs.get('bin_func', 'even')
    )

    return args

def get_data(data):
    # get the data
    if isinstance(data, str):
        data = pd.read_csv(data)
    if not isinstance(data, pd.DataFrame):
        raise AttributeError('data has to be a path or a Dataframe')
    if not all(col in data.columns for col in ('x', 'y', 'z')):
        raise AttributeError('The data needs a x,y and z column')

    return data


def plot(result):
    # get the number of lags classes
    n = result.shape[1]
    x = np.arange(n)
    
    # get the median
    median = [np.median(result[:,i]) for i in range(n)]

    # get the confidence interval
    high = [np.percentile(result[:,i], q=95) for i in range(n)]
    low = [np.percentile(result[:,i], q=5) for i in range(n)]

    fig = go.Figure(data=[
        go.Scatter(x=x, y=low, mode='lines', line_color='lightsteelblue', name='5% - percentile'),
        go.Scatter(x=x, y=high, fill='tonexty', mode='lines', line_color='lightsteelblue', name='95% - percentile')
    ])
    fig.add_trace(
        go.Scatter(x=x, y=median, mode='lines', line=dict(color='indigo', width=4), name='median')
    )

    return fig


# Main function
def main(data_path=os.path.join(PATH, 'sample.csv'), num_iter=5000, obs_scale=5, verbose=False, render='margin', **kwargs):
    if verbose:
        print('Building job...', end='')
    # get data
    df = get_data(data_path)

    # get the fixed arguments
    args = get_arguments(**kwargs)
    args['coordinates'] = df[['x', 'y']].values     # add the coordinates

    # get the parameters for MC
    parameters = {
        'values': {
            'distribution': 'normal',
            'scale': obs_scale,
            'value': df.z.values
        }
    }

    # instantiate a MC
    mc = MonteCarlo(
        func=variogram,
        num_iter=num_iter,
        parameters=parameters,
        **args
    )

    # run 
    if verbose:
        print('done.\nStarting %d iterations...' % num_iter, end='')
    t1 = time.time()
    result = mc()
    t2 = time.time()

    if verbose:
        print('done. [%s]' % '%.1f%s' % (((t2 - t1) * 1000, 'ms') if t2 - t1 < 4 else (t2 - t1, 'sec')))

    # render the result
    return mc.render(render, result)


if __name__=='__main__':
    import fire
    fire.Fire(main)
