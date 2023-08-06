from typing import Union, Callable, List, Tuple
import numpy as np
from numpy import random
from joblib import Parallel, delayed
from tqdm import tqdm

from uncertainty_framework.simulators._simulator import Simulator

class MonteCarlo(Simulator):
    def __init__(
        self,
        func: Union[str, Callable],
        num_iter: int =5000,
        parameters: dict ={},
        n_jobs=-1,
        **kwargs 
    ) -> None:
        """Monte-Carlo simulator

        [Description]

        """
        super(MonteCarlo, self).__init__()

        # set the parameters
        self.num_iter = num_iter
        self.n_jobs = n_jobs
        self._kwargs = kwargs

        # set the function
        if callable(func):
            self.func = func
        else:
            # TODO: use helper function to wrap the script
            raise NotImplementedError
            
        # build the parameter list
        self.parameters = self._build_run_strategy(parameters=parameters)

    def _build_run_strategy(self, parameters: dict) -> List[Tuple[str, Callable]]:
        # TODO: this logic has to be more flexible and be fed by utility functions

        # container
        params = []

        # build each one
        for name, opt in parameters.items():
            # build argument object - this can be extended
            if not isinstance(opt, dict):
                args = {'value': opt}
            else:
                args = opt
            
            # get the function properties
            if 'value' in args:
                distribution = getattr(random, args.get('distribution', 'normal'))
                props = [args['value'], args.get('scale', 1.0)]

            elif 'range' in args:
                distribution = getattr(random, args.get('distribution', 'uniform'))
                props = (args['range'][0], args['range'][1])
            
            else:
                raise ValueError("Neither 'value' nor 'range' is defined for parameter %s" % name)
            
            # add args to props
            props.extend(args.get('args', []))
            params.append((name, lambda: distribution(*props)))
            
        return params

    def get_next_params(self) -> dict:
        """Builds the next set of arguments
        """
        params = {arg_name: caller() for arg_name, caller in self.parameters}
        return params

    def run(self, num_iter: Union[int, None] =None) -> np.ndarray:
        """run simulation

        Start the Monte-Carlo simulation. The num_iter parameter and verbose parameter
        can be overwritten and will update the instance arguments.
        The passed function or script will be run multiple times and the function
        result is stored into a result matrix. This matrix will be returned, after
        simulation has finished. Confidence intervals can be calculated from the
        result matrix, the class will not do that for you.

        """
        # update iterations
        if num_iter is not None:
            self.num_iter = num_iter

        # run once to get the output shape
        out = np.asarray(self.func(**self.get_next_params(), **self._kwargs))

        # output container
        result = np.ones((self.num_iter, out.shape[0])) * np.nan

        # build input parameter
        params = (({**self.get_next_params(), **self._kwargs},i) for i in range(self.num_iter))

        # build the wrapper 
        def wrap(tup):
            # unwrap the tuple
            par, i = tup
            
            # save result
            result[i] = self.func(**par)

        # create the parallel worker
        parallel_worker = Parallel(n_jobs=self.n_jobs, require='sharedmem')

        # create verbose or non verbose parameter generator
        if self._kwargs.get('verbose', False):
            func_gen = (delayed(wrap)(param) for param in params)
        else:
            func_gen = (delayed(wrap)(param) for param in tqdm(params, total=self.num_iter))
        
        # run the job in parallel
        parallel_worker(func_gen)

        # finished - return the result
        return result
            

if __name__ == '__main__':
    import fire
    fire.Fire(MonteCarlo)