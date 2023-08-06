from uncertainty_framework.report.margins import MarginReport
from tabulate import tabulate


class ConsoleReport(MarginReport):
    """
    Thin wrapper around the MarginReport class.
    It uses the margin report and formats the output to
    look nicer on the console.
    """
    def render(self, fmt='pretty', agg='median', floatfmt='.1f', **kwargs):
        # run the margin report
        margins = super(ConsoleReport, self).render(agg=agg, **kwargs)

        # determine the header
        if margins.shape[1] == 2:
            headers = ['%5', '95%']
        else:
            headers = ['%5', agg, '95%']
        
        return tabulate(margins, headers=headers, tablefmt=fmt, floatfmt=floatfmt)
