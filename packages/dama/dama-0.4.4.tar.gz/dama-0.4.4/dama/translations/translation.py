from __future__ import absolute_import
'''Module providing a data base class for translation methods'''
import numpy as np
import dama as dm

__license__ = '''Copyright 2019 Philipp Eller

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''


class Translation():
    '''Base class for translation methods'''
    def __init__(
        self,
        source,
        *args,
        source_needs_grid=False,
        dest_needs_grid=False,
        **kwargs
        ):

        self.source = source
        self.source_has_grid = isinstance(
            self.source, (dm.GridData, dm.GridArray, dm.Grid)
            )
        if source_needs_grid:
            assert self.source_has_grid, 'Source must provide grid'
        self.dest = self.generate_destination(*args, **kwargs)
        self.dest_has_grid = isinstance(
            self.dest, (dm.GridData, dm.GridArray, dm.Grid)
            )
        if dest_needs_grid:
            assert self.dest_has_grid, 'Destination must provide grid'

        if self.dest_has_grid:
            self.wrt = self.dest.grid.vars
        elif self.source_has_grid:
            self.wrt = self.source.grid.vars
        else:
            self.wrt = self.dest.vars

        # checks
        if not isinstance(self.source, dm.GridArray):
            if not set(self.wrt) <= set(source.vars):
                raise TypeError(
                    'the following variables are missing in the source: %s' %
                    ', '.
                    join(set(self.vars) - (set(self.vars) & set(source.vars)))
                    )

        self.source_sample = None
        self.dest_sample = None

        # if there are any special, additional runs to be performed,
        # for example for histograms and KDE without source_data
        self.additional_runs = {}

    def generate_destination(self, *args, **kwargs):
        '''Correctly set up a destination data format
        depending on the supplied input
        
        Parameters
        ----------
        args, kwargs

        '''
        if len(args) == 1 and len(kwargs) == 0:
            dest = args[0]
            if isinstance(dest, dm.GridData):
                grid = dest.grid
                grid.initialize(self.source)
                return dm.GridData(grid)
            if isinstance(dest, dm.Grid):
                grid = dest
                grid.initialize(self.source)
                return dm.GridData(grid)
            if isinstance(dest, dm.GridArray):
                grid = dest.grid
                grid.initialize(self.source)
                return dm.GridArray(np.empty(grid.shape), grid=grid)
            if isinstance(dest, dm.PointData):
                # check which vars we need:
                if self.source_has_grid:
                    return dest[self.source.grid.vars]
                else:
                    return dest

        # check if source has a grid and if any args are in there
        if isinstance(self.source, (dm.GridData, dm.GridArray)):
            dims = []
            for arg in args:
                # in this case the source may have a grid, get those edges
                if isinstance(arg, str):
                    if arg in self.source.grid.vars:
                        dims.append(self.source.grid[arg])
                        continue
                dims.append(arg)
            args = dims

        # instantiate
        grid = dm.Grid(*args, **kwargs)
        grid.initialize(self.source)

        if isinstance(self.source, dm.GridArray):
            return dm.GridArray(np.empty(grid.shape), grid=grid)

        return dm.GridData(grid)

    def prepare_source_sample(self, flat=True, stacked=True, transposed=False):
        if transposed: assert stacked
        self.source_sample = [
            self.source.get_array(var, flat=flat) for var in self.wrt
            ]
        if stacked:
            self.source_sample = np.stack(self.source_sample)
        if transposed:
            self.source_sample = self.source_sample.T

    def prepare_dest_sample(self, flat=True, stacked=True, transposed=False):
        if transposed: assert stacked
        self.dest_sample = [
            self.dest.get_array(var, flat=flat) for var in self.wrt
            ]
        if stacked:
            self.dest_sample = np.stack(self.dest_sample)
        if transposed:
            self.dest_sample = self.dest_sample.T

    def setup(self):
        pass

    def run(self):

        self.setup()

        if isinstance(self.dest, dm.GridArray):
            # in this case it is a single array, no vars
            if isinstance(self.source, (dm.GridData, dm.PointData)):
                assert len(self.source.vars) - len(self.wrt) == 1
                for var in self.source.vars:
                    if var in self.wrt:
                        continue
                    source_data = self.source[var]
            else:
                source_data = self.source

            result = self.eval(source_data)
            self.dest = dm.GridArray(result, grid=self.dest.grid)
            return self.dest

        if isinstance(self.source, dm.GridArray):
            source_data = self.source
            result = self.eval(source_data)
            self.dest['result'] = result
            return self.dest

        def make_closure(data):
            def f():
                return self.eval(data)
            return f

        for var in self.source.vars:
            if var in self.wrt:
                continue
            self.dest[var] = make_closure(self.source[var])

        for var, data in self.additional_runs.items():
            self.dest[var] = make_closure(data)


        return self.dest

    def eval(self, data):
        raise NotImplementedError('Translation method must implement this')

    def get_empty_output_array(
        self, element_shape=tuple(), fill_value=np.nan, flat=False
        ):
        '''make empty array in shape of destinaion
    
        element_shape : tuple
            additional dimensions of the output
        fill_value : value
            fill value
        flat : bool
            if True, make flat in array dimensions
        '''
        array_shape = self.dest.array_shape
        if flat:
            array_shape = tuple([np.product(array_shape)])
        array_shape += element_shape

        if fill_value is None:
            return np.empty(array_shape)
        return np.full(array_shape, fill_value)
