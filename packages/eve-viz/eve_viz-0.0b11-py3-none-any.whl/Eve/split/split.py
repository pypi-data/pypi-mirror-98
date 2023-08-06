from ._split import * 

import numpy as np 
import pandas as pd


class Split():
    
    def __init__(self, cv_method, n_splits=None,
                 train_size=None, min_train_size=None, valid_size=None, step_size=None,
                 random_state=None):
        
        # assume it is preordered by orderby
        # assume orderby is present
        
        if cv_method=='OrderedKFold':
            
            self.cv = KFold(n_splits=n_splits, 
                            shuffle=False)

        elif cv_method=='ShuffledKFold':
            
            self.cv = KFold(n_splits=n_splits, 
                            shuffle=True)
            
        elif cv_method=='SlidingWindow':
            
            self.cv = DateSlidingWindowSplit(train_size=train_size, 
                                             min_train_size=min_train_size,
                                             valid_size=valid_size, 
                                             step_size=step_size)
            
        elif cv_method=='ExpandingWindow':
            
            if isinstance(valid_size, str):
            
                self.cv = DateExpandingWindowSplit(min_train_size=min_train_size,
                                                   valid_size=valid_size,
                                                   step_size=step_size,
                                                   n_splits=n_splits)
            
            else:
                
                self.cv = ExtendedTimeSeriesSplit(min_train_size=min_train_size,
                                                   valid_size=valid_size,
                                                   n_splits=n_splits,
                                                   step_size=step_size)
            
        self.cv_method = cv_method
        
    def split(self, data, orderby=None):
        
        if self.cv_method in ('SlidingWindow', 'ExpandingWindow'):
            return self.cv.split(data, orderby)
        else:
            return self.cv.split(data)

    def ith_split(self, i, data, orderby=None):

        if self.cv_method in ('SlidingWindow', 'ExpandingWindow'):
            for idx, (train, valid) in enumerate(self.split(data, orderby)):
                if idx==i:
                    return train, valid

        else:
            for idx, (train, valid) in enumerate(self.split(data)):
                if idx==i:
                    return train, valid

    def get_n_splits(self, data, orderby=None):

        if self.cv_method in ('SlidingWindow', 'ExpandingWindow'):
            return self.cv.get_n_splits(data, orderby)
        else:
            return self.cv.get_n_splits(data)
        
    def show_layout(self, data, orderby=None, display=False):
        
        if self.cv_method=='OrderedKFold':
            
            train_left_indices = []
            valid_indices = []
            train_right_indices = []

            for train_index, valid_index in self.cv.split(data):

                train_left_indices.append(valid_index[0] - 0)
                valid_indices.append(valid_index[-1] - valid_index[0] + 1)
                train_right_indices.append(len(data) - valid_index[-1] - 1)

            train_left_indices = train_left_indices[::-1]
            valid_indices = valid_indices[::-1]
            train_right_indices = train_right_indices[::-1]
            
            if display:

                df = pd.DataFrame({'train' : train_left_indices,'validation' : valid_indices, 'placeholder': train_right_indices})
                ax = df.plot.barh(stacked=True, color=['#1f77b4','#ff7f0e']);

                ax.figure.set_size_inches(10, 2.5)
                ax.set_title("cross validation folds layout")
                ax.legend(["train", "validation"], loc='center left',bbox_to_anchor=(1.0, 0.5))
            
        elif self.cv_method=='ExpandingWindow':
            
            train_indices = []
            valid_indices = []

            for train_index, valid_index in self.cv.split(data, orderby):
                train_indices.append(train_index[-1])
                valid_indices.append(valid_index[-1]-valid_index[0])

            train_indices = train_indices[::-1]
            valid_indices = valid_indices[::-1]
            
            if display:
            
                df = pd.DataFrame({'train' : train_indices,'validation' : valid_indices})
                ax = df.plot.barh(stacked=True, color=['#1f77b4','#ff7f0e']);

                ax.figure.set_size_inches(10, 2.5)
                ax.set_title("cross validation folds layout")
                ax.legend(["train", "validation"], loc='center left',bbox_to_anchor=(1.0, 0.5));
            
        elif self.cv_method=='SlidingWindow':
            
            empty_indices = []
            train_indices = []
            valid_indices = []

            for train_index, valid_index in self.cv.split(data, orderby):

                empty_indices.append(train_index[0])
                train_indices.append(train_index[-1] - train_index[0] + 1)
                valid_indices.append(valid_index[-1] - valid_index[0] + 1)

            empty_indices = empty_indices[::-1]
            train_indices = train_indices[::-1]
            valid_indices = valid_indices[::-1]
            
            if display:

                df = pd.DataFrame({'empty' : empty_indices, 'train' : train_indices, 'validation': valid_indices})
                ax = df.plot.barh(stacked=True, color=['white', '#1f77b4','#ff7f0e'])

                ax.figure.set_size_inches(10, 2.5)
                ax.set_title("cross validation folds layout")
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[1:], ["train", "validation"], loc='center left', bbox_to_anchor=(1.0, 0.5));

        return True

        