from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd

from sklearn.model_selection._split import *
from sklearn.model_selection import TimeSeriesSplit
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples

__all__ = ['BaseCrossValidator',
           'KFold',
           'GroupKFold',
           'LeaveOneGroupOut',
           'LeaveOneOut',
           'LeavePGroupsOut',
           'LeavePOut',
           'RepeatedStratifiedKFold',
           'RepeatedKFold',
           'ShuffleSplit',
           'GroupShuffleSplit',
           'StratifiedKFold',
           'StratifiedShuffleSplit',
           'PredefinedSplit',
           'train_test_split',
           'check_cv',
           'ExtendedTimeSeriesSplit',
           'DateExpandingWindowSplit',
           'DateSlidingWindowSplit']


class ExtendedTimeSeriesSplit():
    
    def __init__(self, 
                 n_splits=5,
                 *,
                 max_train_size=None,
                 valid_size=None,
                 min_train_size=None,
                 step_size=None):
        
        self.n_splits = n_splits
        self.max_train_size = max_train_size
        self.valid_size = valid_size
        self.step_size = step_size
        self.min_train_size = min_train_size
        
    def split(self, data, orderby=None):

        if self.step_size is None:
            self.step_size = 0


        
        if self.valid_size < 1:
            self.valid_size = int(len(data) * self.valid_size)
            
        if orderby is None and isinstance(self.min_train_size, str):
            raise ValueError()

        if self.n_splits is None:
            self.n_splits = int((len(data) - 1)/ self.valid_size)

        if self.n_splits >= int((len(data))/ self.valid_size):
            self.n_splits = int((len(data) - 1)/ self.valid_size)

            # From sklearn: ~/Codes/Codes/Notebooks/venv3/lib/python3.6/site-packages/sklearn/model_selection/_split.py in split(self, X, y, groups)
            #     872         if n_samples - gap - (test_size * n_splits) <= 0:  # greater than EQUALS
            #     873             raise ValueError(
            # --> 874                 (f"Too many splits={n_splits} for number of samples"
            #     875                  f"={n_samples} with test_size={test_size} and gap={gap}."))
        
        if isinstance(self.min_train_size, str):
            
            _cv = TimeSeriesSplit(n_splits=self.n_splits, max_train_size=self.max_train_size,
                                  gap=self.step_size, test_size=self.valid_size)
            
            min_train_size = pd.Timedelta(self.min_train_size)
        
            for train_index, valid_index in _cv.split(data):
                
                if data[orderby].iloc[train_index].max() - data[orderby].iloc[train_index].min() < min_train_size:
                    
                    continue

                yield train_index, valid_index

        else:
            
            if self.min_train_size < 1:
                self.min_train_size = len(data) * self.min_train_size
            
            _cv = TimeSeriesSplit(n_splits=self.n_splits, max_train_size=self.max_train_size,
                              gap=self.step_size, test_size=self.valid_size)

            for train_index, valid_index in _cv.split(data):
                
                if len(train_index) < self.min_train_size:
                    
                    continue

                yield train_index, valid_index

    def get_n_splits(self, data=None, orderby=None, y=None, groups=None):
        
        split_cnt = 0
        
        for i in self._iter_indices(data, orderby, y=None, groups=None):
            split_cnt+=1
            
        return split_cnt
        
        
def time_denominator(time_inputs):
    """
    0 - seconds
    1 - minutes
    2 - hours
    3 - days
    4 - months
    5 - numeric
    """
    denom = 99
    
    for time_input in time_inputs:
    
        if isinstance(time_input, str):
            
            if 'seconds' in time_input:
                cur_denom = 0
                denom = min(cur_denom, denom)
                
            elif 'minutes' in time_input:
                cur_denom = 1
                denom = min(cur_denom, denom)
                
            elif 'hours' in time_input:
                cur_denom = 2
                denom = min(cur_denom, denom)
                
            elif 'days' in time_input:
                cur_denom = 3
                denom = min(cur_denom, denom)
                
            elif 'months' in time_input:
                cur_denom = 4
                denom = min(cur_denom, denom)
    
    if denom==0: 
        return 's'
    elif denom==1: 
        return 'min'
    elif denom==2: 
        return 'H'
    elif denom==3: 
        return 'd'
    elif denom==4: 
        return 'd'
    else: 
        return None
                

class BaseDateWindowSplit(metaclass=ABCMeta):
    
    def __init__(self, train_size=None, min_train_size=None, 
                 valid_size=None, step_size=None, random_state=None, n_splits=None):
        
        self.train_size = train_size
        self.min_train_size = min_train_size
        self.valid_size = valid_size
        self.step_size = step_size
        self.random_state = random_state
        self.n_splits = n_splits
        
        self.dt_time_unit = time_denominator([self.train_size, 
                                              self.min_train_size,
                                              self.valid_size,
                                              self.step_size])
        
    def split(self, data, orderby, y=None, groups=None):
        data, y, groups = indexable(data, y, groups)
        for train, valid in self._iter_indices(data, orderby, y, groups):
            yield train, valid
    
    @abstractmethod
    def _iter_indices(self, data, orderby, y=None, groups=None):
        """Generate (train, test) indices"""
    
    @abstractmethod
    def get_n_splits(self, data=None, orderby=None, y=None, groups=None):
        """Get the total number of splits"""
    

class DateExpandingWindowSplit(BaseDateWindowSplit):
    
    def __init__(self, min_train_size=None, valid_size=None, step_size=None, random_state=None,
                 n_splits=None):
        super().__init__(train_size=None, min_train_size=min_train_size,
                         valid_size=valid_size, step_size=step_size, n_splits=n_splits,
                         random_state=random_state)
        
    def _iter_indices(self, data, orderby, y, groups):

        if self.step_size is None:
            self.step_size = self.valid_size
        
        data = data[[orderby]].reset_index()
        data[orderby] = data[orderby].dt.floor(self.dt_time_unit)
        
        # train_size = pd.Timedelta(self.train_size)
        valid_size = pd.Timedelta(self.valid_size)
        min_train_size = pd.Timedelta(self.min_train_size)
        step_size = pd.Timedelta(self.step_size)
        
        cutoff = data[orderby].max() - valid_size
        result = [cutoff]
        
        if cutoff < data[orderby].min():
            raise ValueError('Less data than valid_size.')
            
        while result[-1] >= data[orderby].min() + min_train_size:

            cutoff -= step_size
            # train with everything before this

            # If data does not exist in data range (cutoff, cutoff + horizon]
            if not (((cutoff < data[orderby]) & (data[orderby] <= cutoff + valid_size)).any()):

                # Next cutoff point is 'last date before cutoff in data - horizon'
                if cutoff > data[orderby].min():
                    closest_date = data[data[orderby] <= cutoff].max()[orderby]
                    cutoff = closest_date - valid_size

                # else no data left, leave cutoff as is, it will be dropped.

            result.append(cutoff)

        result = result[:-1]  # drop that last cutoff
        
        if self.n_splits is not None:
            result = result[:self.n_splits]
        
        if len(result) == 0:
            raise ValueError(
                'Less data than valid_size after min_train_size window. '
                'Make valid_size or min_train_size shorter.'
            )
            
        cutoffs = list(reversed(result))
        
        for idx, cutoff in enumerate(cutoffs):

            if self.n_splits is not None:
                if idx == self.n_splits:
                    return
            
            train_data = data[data[orderby] <= cutoff]
            valid_data = data[(cutoff < data[orderby]) & (data[orderby] <= cutoff + valid_size)]
            
            yield train_data['index'].values, valid_data['index'].values
            
    def get_n_splits(self, data=None, orderby=None, y=None, groups=None):
        
        split_cnt = 0
        
        for i in self._iter_indices(data, orderby, y=None, groups=None):
            split_cnt+=1
            
        return split_cnt
            

class DateSlidingWindowSplit(BaseDateWindowSplit):
    
    def __init__(self, train_size, valid_size, min_train_size=None, step_size=None, random_state=None):
        super().__init__(train_size=train_size, valid_size=valid_size, min_train_size=min_train_size, step_size=step_size, random_state=random_state)
        
    def _iter_indices(self, data, orderby, y, groups):

        if self.step_size is None:
            self.step_size = self.valid_size


        if isinstance(self.train_size, str):

            data = data[[orderby]].reset_index()
            data[orderby] = data[orderby].dt.floor(self.dt_time_unit)
            
            train_size = pd.Timedelta(self.train_size)
            valid_size = pd.Timedelta(self.valid_size)
            min_train_size = pd.Timedelta(self.min_train_size)
            step_size = pd.Timedelta(self.step_size)
            
            date_head = data[orderby].min()
            last_date = data[orderby].max()
        
            while(date_head + train_size <= last_date):
        
                train_data = data[(date_head <= data[orderby]) & 
                                    (data[orderby] < date_head + train_size)]
                valid_data = data[(date_head + train_size <= data[orderby]) & 
                                   (data[orderby] < date_head + train_size + valid_size)]

                date_head += step_size
                num_unique_days = len(train_data[orderby].unique())

                if(num_unique_days<min_train_size.days or len(valid_data)==0):
                    continue
                    
                yield train_data['index'].values, valid_data['index'].values

        else:

            data = data[[orderby]].reset_index()

            if self.dt_time_unit is not None:
                data[orderby] = data[orderby].dt.floor(self.dt_time_unit)

            idx_head = 0
            last_idx = len(data)

            if isinstance(self.min_train_size, float) and self.min_train_size < 1:
                self.min_train_size = int(len(data) * self.min_train_size)

            if isinstance(self.min_train_size, str):
                self.min_train_size = pd.Timedelta(self.min_train_size)

            if self.train_size < 1:
                self.train_size = int(len(data) * self.train_size)

            if self.valid_size < 1:
                self.valid_size = int(len(data) * self.valid_size)

            if self.step_size is None:
                self.step_size = self.valid_size
            elif self.step_size < 1:
                self.step_size = int(len(data) * self.step_size)

        
            cutoff = len(data) - self.valid_size
            result = [cutoff]

            if cutoff < 0:
                raise ValueError('Less data than valid_size.')

            while result[-1] >= 1:

                cutoff -= self.step_size
                result.append(cutoff)

            result = result[:-1]

            if self.n_splits is not None:
                result = result[:self.n_splits]
            
            if len(result) == 0:
                raise ValueError(
                    'Less data than valid_size after min_train_size window. '
                    'Make valid_size or min_train_size shorter.'
                )
                
            cutoffs = list(reversed(result))

            for idx, cutoff in enumerate(cutoffs):

                train_index = data.iloc[max(cutoff - self.train_size, 0) : cutoff]['index'].values
                valid_index = data.iloc[cutoff : cutoff + self.valid_size]['index'].values

                if isinstance(self.min_train_size, int):
                    
                    if len(train_index) < self.min_train_size:
                        continue

                elif self.min_train_size is not None:

                    if data[orderby].iloc[train_index].max() - data[orderby].iloc[train_index].min() < self.min_train_size:

                        continue
                
                yield train_index, valid_index

    def get_n_splits(self, data=None, orderby=None, y=None, groups=None):
        
        split_cnt = 0
        
        for i in self._iter_indices(data, orderby, y=None, groups=None):
            split_cnt+=1
            
        return split_cnt




