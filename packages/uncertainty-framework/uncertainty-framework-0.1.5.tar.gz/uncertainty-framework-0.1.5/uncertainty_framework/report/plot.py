import plotly.graph_objects as go
import numpy as np

from uncertainty_framework.report.margins import MarginReport
 

class PlotReport(MarginReport):
    """Plot Report

    Wraps the MarginReport and creates a plot from the
    calculated margins.
    By default they will render to a HTML page opened
    in the browser. PDF or png creation is also possible.

    """
    def render(self, agg='median', mode='area', save=None, **kwargs):
        """
        """
        if agg is None:
            raise AttributeError('NoneType agg arguments not supported for plots')
        
        # run the margin report
        margins = super(PlotReport, self).render(agg=agg, **kwargs)

        # check if the margins are scalar
        if margins.size == 1:
            fig = self._render_scalar(margins, agg, **kwargs)
        else:
            fig = self._render_multi(margins, agg, mode=mode, **kwargs)

        # adjust the legend
        fig.update_layout(
            template=kwargs.get('template', 'plotly_dark'),
            legend=dict(
                yanchor='bottom',
                xanchor='right',
                x=1.,
                y=1.05,
                orientation='h'
            ),
            title=kwargs.get('title', 'Monte-Carlo simulation result')
        )

        # saving not supported yet
        if save is not None:
            fig.write_image(save)
            return 

        return fig
    
    def _render_multi(self, margins: np.ndarray, agg: str, mode='area', **kwargs) -> go.Figure:
        fig = go.Figure()
        x = np.arange(margins.shape[0])

        # Add a area or error bars
        if mode.lower() == 'area':
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=margins[:,0],
                    mode='lines',
                    line_color=kwargs.get('area_color', 'lightsteelblue'),
                    name='%d%% - percentile' % kwargs.get('q', 5)
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=margins[:,2],
                    mode='lines',
                    fill='tonexty',
                    line_color=kwargs.get('area_color', 'lightsteelblue'),
                    name='%d%% - percentile' % (100 - kwargs.get('q', 5))
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=margins[:,1],
                    mode='lines',
                    line=dict(color=kwargs.get('color', 'purple'), width=3),
                    name=agg.capitalize()
                )
            )
        elif mode.lower() == 'errorbar':
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=margins[:,1],
                    mode='lines+markers',
                    line=dict(color=kwargs.get('color', 'purple'), width=4),
                    marker=kwargs.get('marker', {}),
                    name=agg.capitalize(),
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=np.abs(margins[:,1] - margins[:,2]),
                        arrayminus=np.abs(margins[:,1] - margins[:,0])
                    )
                )
            )
        else:
            raise AttributeError("'%s' is not a valid mode." % mode)
        
        return fig


    def _render_scalar(self, margins: np.ndarray, agg: str, **kwargs) -> go.Figure:
        # reshape the margins:
        m = margins.reshape(1, -1)

        # scalar can only use errorbar plots
        mode = 'errorbar'

        marker = dict(size=12)

        return self._render_multi(m, agg, mode=mode, marker=marker, **kwargs)
