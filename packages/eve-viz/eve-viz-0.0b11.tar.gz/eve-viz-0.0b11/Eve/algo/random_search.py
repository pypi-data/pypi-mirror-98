import HMF
from ezFutures import ezFutures
from sklearn.model_selection import ParameterSampler

from scipy.stats.distributions import loguniform
from scipy.stats.distributions import uniform

from ..split import Split
from .default_search_space import default_search_space_dict
from .default_eval_method import default_eval_method_dict

import numpy as np
import pandas as pd
import os
import multiprocessing

EVE_ORDERBY_ENCODED_NAME = '__specialEve__orderbyIntEncoded'

DATA_REQ = ['data', 'feature_names', 'target_name']
CV_REQ = ['cv_method']
AVAILABLE_CV_METHODS = ['OrderedKFold', 'ShuffledKFold', 'SlidingWindow', 'ExpandingWindow']

ExpandingWindow_REQ_ARGS = ['orderby', 'min_train_size', 'valid_size', 'step_size', 'n_splits']
SlidingWindow_REQ_ARGS = ['orderby', 'min_train_size', 'train_size', 'valid_size', 'step_size', 'n_splits']
ShuffledKFold_REQ_ARGS = ['n_splits']
OrderedKFold_REQ_ARGS = ['orderby', 'n_splits']

SEARCH_REQ1 = ['search_space', 'n_iters']
SEARCH_REQ2 = ['eval_user_method']

OPTIONAL = ['groupby', 'n_procs', 'random_state']

LOGUNIF_SCALE_PARAM = 0.0325


class RandomSearch():
    
    def __init__(self, cv_method=None, data=None, feature_names=None, target_name=None, orderby=None, groupby=None, 
                 n_splits=None, min_train_size=None, train_size=None, valid_size=None, step_size=None, 
                 random_state=None, n_procs=None, n_iters=None, search_space=None,
                 eval_user_method=None):
        
        self.cv_method = cv_method
        self.data = data
        self.feature_names = feature_names
        self.target_name = target_name
        self.orderby = orderby
        self.groupby = groupby
        self.n_splits = n_splits
        self.min_train_size = min_train_size
        self.train_size = train_size
        self.valid_size = valid_size
        self.step_size = step_size
        self.random_state = random_state
        self.n_procs = n_procs
        self.n_iters = n_iters
        self.search_space = search_space
        self.eval_user_method = eval_user_method

        if self.orderby:
            self.data[EVE_ORDERBY_ENCODED_NAME] = self.data[self.orderby].astype(int)

        if self.n_procs is None:
            self.n_procs = int(multiprocessing.cpu_count()/2)

        self.tell_required_arguments()
        self.use_default_args()

    def use_default_args(self):

        if isinstance(self.search_space, str) and self.search_space in default_search_space_dict:
            arg, str_arg = default_search_space_dict[self.search_space]
            self.search_space = arg
            print('\nDefault [ search_space ] argument used: \n{}'.format(str_arg))
            
        if isinstance(self.eval_user_method, str) and self.eval_user_method in default_eval_method_dict:
            arg, str_arg = default_eval_method_dict[self.eval_user_method]
            self.eval_user_method = arg
            print('\nDefault [ eval_user_method ] argument used: \n{}'.format(str_arg))

    def missing_required_arguments(self, required_args):
        
        missing_required_arguments = []
        for k, v in self.__dict__.items():
            if v is None and k in required_args:
                missing_required_arguments.append(k)
                
        return missing_required_arguments

    def tell_required_arguments(self):

        # data requirements

        print("\u2714 Checking data requirements...    ", end="", flush=True)

        missing_args = self.missing_required_arguments(DATA_REQ)

        if len(missing_args)>0:
            print("Failed!")
            print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_args)))
            return

        else:
            print("Passed!")

        print("\u2714 Checking cross validation requirements...    ", end="", flush=True)

        # cross validation requirements
        
        missing_args = self.missing_required_arguments(CV_REQ)

        if len(missing_args)>0:
            print("Failed!")
            print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_args)))

            print('\nAvailable [ cv_method ] options:\n\n'
                  '\u25BA {}'.format('  '.join(AVAILABLE_CV_METHODS)))

            return

        try:

            if self.groupby is not None:

                data = self.data[self.data[self.groupby]==self.data[self.groupby].iloc[0]]

            else:

                data = self.data

            sample_data = self.data[[self.orderby]]
            sample_data = sample_data.sort_values(by=self.orderby)
            sample_data = sample_data.reset_index(drop=True)

            cv = self.get_cv()
            cv.show_layout(sample_data, self.orderby)

            print("Passed!")
            cv.show_layout(sample_data, self.orderby, True)

        except:

            print("Failed!")

            if self.cv_method == 'OrderedKFold':

                print('\nRequired argument(s) for [ {} ] cross validation method:\n\n\u25BA {}'.format(self.cv_method,
                  '  '.join(OrderedKFold_REQ_ARGS)))


            if self.cv_method == 'ShuffledKFold':

                print('\nRequired argument(s) for [ {} ] cross validation method:\n\n\u25BA {}'.format(self.cv_method,
                  '  '.join(ShuffledKFold_REQ_ARGS)))


            if self.cv_method == 'ExpandingWindow':

                print('\nRequired argument(s) for [ {} ] cross validation method:\n\n\u25BA {}'.format(self.cv_method,
                  '  '.join(ExpandingWindow_REQ_ARGS)))

                print('\n\u25BA [ orderby ] must be datetime type')

                print('\n(E.g. "5 days", 1000, 0.15)')

            elif self.cv_method == 'SlidingWindow':

                print('\nRequired argument(s) for [ {} ] cross validation method:\n\n\u25BA {}'.format(self.cv_method,
                  '  '.join(SlidingWindow_REQ_ARGS)))

                print('\n\u25BA [ orderby ] must be datetime type')

            return
                

        # search requirements

        print("\u2714 Checking search requirements...    ", end="", flush=True)

        missing_args = self.missing_required_arguments(SEARCH_REQ1)

        if len(missing_args)>0:
            print("Failed!")
            print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_args)))

            if 'search_space' in missing_args:

                print('\nAvailable default arguments for [ search_space ] :\n\n\u25BA {}'.format(
                  '  '.join(default_search_space_dict.keys())))

                print('\nExample [ search_space ] argument: (the example is not meant for actual use!)')

                print("""\n\u25BA search_space={'learning_rate': [ (0.01, 0.2), 'real', 'loguniform'],
                'gamma': [ (0, 5), 'real', 'uniform'],
                'n_estimators': [ (10, 125), 'discrete'],
                'tree_method': [ ('auto', 'exact', 'approx', 'hist'), 'choice']}""")

            return


        missing_args = self.missing_required_arguments(SEARCH_REQ2)

        if len(missing_args)>0:
            print("Failed!")

            print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_args)))

            print('\nAvailable default arguments for [ eval_user_method ] :\n\n\u25BA {}'.format(
                  '  '.join(default_eval_method_dict.keys())))

            print('\nRequired method signature for [ eval_user_method ]:\n'
                  '\n\u25BA {}'.format('method_name(train_X, train_y, valid_X, valid_y, parameters): (The method must return the evaluation score!)'))

            print("\nInvoke sample_fold() method to sample a (train_X, train_y, valid_X, valid_y, parameters) tuple")

            print("\n\u25BA Example:")
            print("algo = ev.RandomSearch(args, kwargs)")
            print("train_X, train_y, valid_X, valid_y, parameters = algo.sample_fold()")

            return

        else:
            print("Passed!")

        # remaining optional arguments

        print('\nOptional argument(s):\n\n\u25BA {}'.format('  '.join(OPTIONAL)))

    
    @staticmethod
    def fetch_fold_data(cv, f, search_idx, fold_idx, parameters, cv_method, group_name):

        if not f.has_groups():
    
            if f.get_node_attr('/', key='has_orderby'):
                orderby_data = f.get_dataframe('/{}'.format(EVE_ORDERBY_ENCODED_NAME))
                orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])
                orderby = EVE_ORDERBY_ENCODED_NAME

            else:
                orderby_data = f.get_group_sizes()[0]
                orderby_data = np.arange(orderby_data)
                orderby = None

            train_idx, valid_idx = cv.ith_split(fold_idx, orderby_data, orderby)

            train_X = f.get_dataframe('/X', train_idx)
            train_y = f.get_dataframe('/y', train_idx)
            valid_X = f.get_dataframe('/X', valid_idx)
            valid_y = f.get_dataframe('/y', valid_idx)
            
            return train_X, train_y, valid_X, valid_y, parameters

        else:

            if f.get_node_attr('/', key='has_orderby'):
                orderby_data = f.get_dataframe('/{}/{}'.format(group_name, EVE_ORDERBY_ENCODED_NAME))
                orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])
                orderby = EVE_ORDERBY_ENCODED_NAME

            else:
                orderby_data = f.get_group_sizes()[0]
                orderby_data = np.arange(orderby_data)
                orderby = None

            train_idx, valid_idx = cv.ith_split(fold_idx, orderby_data, orderby)

            train_X = f.get_dataframe('/{}/X'.format(group_name), train_idx)
            train_y = f.get_dataframe('/{}/y'.format(group_name), train_idx)
            valid_X = f.get_dataframe('/{}/X'.format(group_name), valid_idx)
            valid_y = f.get_dataframe('/{}/y'.format(group_name), valid_idx)
            
            return train_X, train_y, valid_X, valid_y, parameters
    
    @staticmethod
    def evaluate_fold_data(evaluate_user_method, cv, f, search_idx, fold_idx, parameters, 
                           cv_method, group_name):
        
        train_X, train_y, valid_X, valid_y, parameters = RandomSearch.fetch_fold_data(
            cv, f, search_idx, fold_idx, parameters, cv_method, group_name)
        
        result = evaluate_user_method(train_X, train_y, valid_X, valid_y, parameters)
        
        return group_name, search_idx, result
    
    def get_f(self, show_progress):

        if not isinstance(self.feature_names, list):
            self.feature_names = [self.feature_names]

        if not isinstance(self.target_name, list):
            self.target_name = [self.target_name]
        
        dirpath = os.path.join(os.getcwd(), '__HMF__specialTmpDir')
        f = HMF.open_file(dirpath, mode='w+')
        f.from_pandas(self.data, orderby=self.orderby, groupby=self.groupby)
        f.register_dataframe('X', self.feature_names)
        f.register_dataframe('y', self.target_name)
        
        if self.orderby:
            f.set_node_attr('/', key='has_orderby', value=True)
            f.register_dataframe(EVE_ORDERBY_ENCODED_NAME, [EVE_ORDERBY_ENCODED_NAME])
        else:
            f.set_node_attr('/', key='has_orderby', value=False)
            
        print('Writing numpy memmap...')
        f.close(show_progress=show_progress)
            
        return f, dirpath
    
    def get_cv(self):
        
        cv = Split(self.cv_method, self.n_splits,
                   self.train_size, self.min_train_size, self.valid_size, self.step_size,
                   self.random_state)
        
        return cv
    
    def get_p(self):

        temp_placeholder = dict()

        for k, v in self.search_space.items():
            
            if len(v)==2:
                
                v.append('uniform')
            
            temp_placeholder[k] = v

        param_sampler_input = dict()

        for k, (val_tuple, val_type, dist_name) in temp_placeholder.items():
            
            if val_type=='choice':

                param_sampler_input[k] = val_tuple
            
            elif val_type=='real':
                
                if dist_name=='uniform':
                    
                    param_sampler_input[k] = uniform(val_tuple[0], val_tuple[1] - val_tuple[0])  # loc, scale
                    
                elif dist_name=='loguniform':
                    
                    param_sampler_input[k] = loguniform(LOGUNIF_SCALE_PARAM, 1 + LOGUNIF_SCALE_PARAM)
                    
            elif val_type=='discrete':
                
                param_sampler_input[k] = np.arange(val_tuple[0], val_tuple[1]+1)
                
        p = ParameterSampler(param_sampler_input, n_iter=self.n_iters)
        logunif_keys = {k: v[0] for k, v in self.search_space.items() if v[-1]=='loguniform'}
        
        return p, logunif_keys

    def _scale_logunif(self, raw, a, b):

        scaled = a + ( (b + LOGUNIF_SCALE_PARAM * 2) - a * 
            (1 + LOGUNIF_SCALE_PARAM) - LOGUNIF_SCALE_PARAM) * (raw - LOGUNIF_SCALE_PARAM)
        return scaled
    
    def get_ez(self):
        
        n_procs = self.n_procs
        
        ez = ezFutures(n_procs=n_procs, n_retries=2)
        return ez
    
    def sample_fold(self):
        
        f, dirpath = self.get_f()
        cv = self.get_cv()
        p, logunif_keys = self.get_p()

        parameters_record = []

        for group_idx, group_name in enumerate(f.get_sorted_group_names()):

            if f.get_node_attr('/', key='has_orderby'):

                if f.has_groups():

                    orderby_data = f.get_dataframe('/{}/{}'.format(group_name, EVE_ORDERBY_ENCODED_NAME))
                    orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])

                else:

                    orderby_data = f.get_dataframe('/{}'.format(EVE_ORDERBY_ENCODED_NAME))
                    orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])

                split_cnt = cv.get_n_splits(orderby_data, EVE_ORDERBY_ENCODED_NAME)

            else:

                group_size = f.get_group_items()[group_name]
                split_cnt = cv.get_n_splits(np.arange(group_size))


            for search_idx, parameters in enumerate(p):

                parameters = {k: (self._scale_logunif(v, logunif_keys[k][0], logunif_keys[k][1]) 
                    if k in logunif_keys else v) for k, v in parameters.items()}

                parameters_record.append((group_name, search_idx, parameters))

                for fold_idx in range(split_cnt):

                    return RandomSearch.fetch_fold_data(
                        cv, f, search_idx, fold_idx, parameters, self.cv_method, group_name)
        
    def run(self, debug_mode=False, show_progress=True):
        
        f, dirpath = self.get_f(show_progress)
        cv = self.get_cv()
        p, logunif_keys = self.get_p()
        self.ez = self.get_ez()

        parameters_record = []

        for group_idx, group_name in enumerate(f.get_sorted_group_names()):

            if f.get_node_attr('/', key='has_orderby'):

                if f.has_groups():

                    orderby_data = f.get_dataframe('/{}/{}'.format(group_name, EVE_ORDERBY_ENCODED_NAME))
                    orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])

                else:

                    orderby_data = f.get_dataframe('/{}'.format(EVE_ORDERBY_ENCODED_NAME))
                    orderby_data[EVE_ORDERBY_ENCODED_NAME] = pd.to_datetime(orderby_data[EVE_ORDERBY_ENCODED_NAME])

                split_cnt = cv.get_n_splits(orderby_data, EVE_ORDERBY_ENCODED_NAME)

            else:

                group_size = f.get_group_items()[group_name]
                split_cnt = cv.get_n_splits(np.arange(group_size))


            for search_idx, parameters in enumerate(p):

                parameters = {k: (self._scale_logunif(v, logunif_keys[k][0], logunif_keys[k][1]) 
                    if k in logunif_keys else v) for k, v in parameters.items()}

                parameters_record.append((group_name, search_idx, parameters))

                for fold_idx in range(split_cnt):

                    if debug_mode:

                        re = RandomSearch.evaluate_fold_data(self.eval_user_method,
                                                    cv, f, search_idx, fold_idx, parameters,
                                                    self.cv_method, group_name)

                        return re
                    
                    self.ez.submit(RandomSearch.evaluate_fold_data, self.eval_user_method,
                                                    cv, f, search_idx, fold_idx, parameters,
                                                    self.cv_method, group_name)
        
        print('Running search algorithm...')
        results = self.ez.results(show_progress=show_progress)

        result_pdf = pd.DataFrame(data=results, columns=['group_name', 'search_idx', 'score'])
        result_pdf = result_pdf.groupby(['group_name', 'search_idx'])['score'].mean().reset_index()

        param_pdf = pd.DataFrame(data=parameters_record, columns=['group_name', 'search_idx', 'parameters'])

        final_result_pdf = result_pdf.merge(param_pdf, on=['group_name', 'search_idx'])

        if f.has_groups():

            def get_best_params(pdf):
                best_params = pdf[pdf['score']==pdf['score'].min()]['parameters'].values[0]
                return best_params

            best_params = pd.DataFrame(final_result_pdf.groupby('group_name').apply(get_best_params), 
                columns=['best_params']).to_dict()['best_params']
            return best_params, final_result_pdf
    
        else:

            best_params = final_result_pdf[final_result_pdf['score']==final_result_pdf['score'].min()]['parameters'].values[0]
            return best_params, final_result_pdf[['search_idx', 'score', 'parameters']]

    def errors(self):

        return self.ez.errors()
        
        