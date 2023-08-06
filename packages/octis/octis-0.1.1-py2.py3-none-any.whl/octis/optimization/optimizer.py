# Utils
import time
from pathlib import Path
import json

# utils from skopt and sklearn
from sklearn.gaussian_process.kernels import *
from skopt.space.space import *

from octis.dataset.dataset import Dataset
# utils from other files of the framework
from octis.models.model import save_model_output
from octis.optimization.optimizer_tool import BestEvaluation
from octis.optimization.optimizer_tool import plot_bayesian_optimization, plot_model_runs
from octis.optimization.optimizer_tool import early_condition
from octis.optimization.optimizer_tool import choose_optimizer
from octis.optimization.optimizer_tool import select_metric
from octis.optimization.optimizer_tool import load_model
from octis.optimization.optimizer_tool import load_search_space


class Optimizer:
    """
    Class Optimizer to perform Bayesian Optimization on Topic Model
    """

    def optimize(self, model, dataset, metric, search_space, extra_metrics=None,
                 number_of_call=5, n_random_starts=1,
                 initial_point_generator="lhs",  # work only for version skopt 8.0!!!
                 optimization_type='Maximize', model_runs=5, surrogate_model="RF",
                 kernel=1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0), nu=1.5),
                 acq_func="LCB", random_state=False, x0=None, y0=None,
                 save_models=True, save_step=1, save_name="result", save_path="results/", early_stop=False,
                 early_step=5,
                 plot_best_seen=False, plot_model=False, plot_name="B0_plot", log_scale_plot=False, topk=10):

        """
        Hyper-parameter Optimization for Topic Model

        Parameters
        ----------
        model          : model with hyperparameters to optimize
        dataset        : dateset for the topic model
        metric         : initialized metric to use for optimization
        search_space   : a dictionary of hyperparameters to optimize
                       (each parameter is defined as a skopt space)
                       with the name of the hyperparameter given as key
        extra_metrics: list of extra metric computed during BO
        number_of_call : number of calls to f
        n_random_starts: number of evaluations of f with random points before approximating it with minimizer
        initial_point_generator: way to generate random points (lhs, random,sobol,halton,hammersly,grid,)
        optimization_type: maximization or minimization problem
        model_runs     : number of different evaluation of the function using the same hyper-parameter configuration
        surrogate_model: type of surrogate model (from sklearn)
        kernel         : type of kernel (from sklearn)
        acq_func       : function to minimize over the minimizer prior (LCB,EI,PI)
        random_state   : set random state to something other than None for reproducible results.
        x0             : list of initial configurations to test
        y0             : list of values for x0
        save_models    : if True, all the model (number_of_call*model_runs) are saved
        save_step      : integer interval after which save the .pkl about BO file
        save_name      : name of the .csv and .pkl files
        save_path      : path where .pkl, plot and result will be saved.

        early_stop     : if True, an early stop policy is applied fro BO.
        early_step     : integer interval after which a current optimization run is stopped if it doesn't improve.
        plot_best_seen : if True the plot of the best seen for BO is showed
        plot_model     : if True the boxplot of all the model runs is done
        plot_name      : name of the plots (both for model runs or best_seen)
        log_scale_plot : if True the "y_axis" of the plot is set to log_scale

        """
        # Set the attributes
        if extra_metrics is None:
            extra_metrics = []
        if y0 is None:
            y0 = []
        if x0 is None:
            x0 = dict()
        self.model = model
        self.dataset = dataset
        self.metric = metric
        self.search_space = search_space
        self.extra_metrics = extra_metrics
        self.optimization_type = optimization_type
        self.number_of_call = number_of_call
        self.n_random_starts = n_random_starts
        self.initial_point_generator = initial_point_generator
        self.model_runs = model_runs
        self.surrogate_model = surrogate_model
        self.kernel = kernel
        self.acq_func = acq_func
        self.random_state = random_state
        self.x0 = x0
        self.y0 = y0
        self.save_path = save_path
        self.save_step = save_step
        self.save_name = save_name
        self.save_models = save_models
        self.early_stop = early_stop
        self.early_step = early_step
        self.plot_model = plot_model
        self.plot_best_seen = plot_best_seen
        self.plot_name = plot_name
        self.log_scale_plot = log_scale_plot
        self.topk = topk

        self.hyperparameters = list(sorted(self.search_space.keys()))
        self.dict_model_runs = dict()
        self.number_of_previous_calls = 0
        self.current_call = 0
        self.time_eval = []

        self.name_optimized_metric = metric.__class__.__name__
        self.dict_model_runs[self.name_optimized_metric] = dict()

        # Info about extra metrics
        i = 0
        self.extra_metric_names = []
        for extra_metric in extra_metrics:
            self.extra_metric_names.append(str(i) + '_' + extra_metric.__class__.__name__)
            self.dict_model_runs[self.extra_metric_names[i]] = dict()
            i = i + 1

        # Control about the correctness of BO parameters
        if self._check_BO_parameters() == -1:
            print("ERROR: wrong initialitation of BO parameters")
            return None

        # Create the directory where the results are saved
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

        # Initialize the directories about model_runs
        if self.save_models:
            self.model_path_models = self.save_path + "models/"
            Path(self.model_path_models).mkdir(parents=True, exist_ok=True)

        # Choice of the optimizer
        opt = choose_optimizer(self)

        # Perform Bayesian Optimization
        results = self._optimization_loop(opt)

        return results

    def resume_optimization(self, name_path, extra_evaluations=0):
        """
        Method to restart the optimization from the json file.

        Parameters
        ----------
        name_path: path of the json file

        extra_evaluations: extra iterations for the BO optimization

        """

        # Restore of the parameters
        res, opt = self._restore_parameters(name_path)

        # Set the number of total calls
        self.number_of_call = self.number_of_call + extra_evaluations

        # Check if there are other iterations to do
        if self.number_of_previous_calls == self.number_of_call:
            return BestEvaluation(self, resultsBO=res)

        # Control about the correctness of BO parameters
        if self._check_BO_parameters() == -1:
            print("ERROR: wrong inizialitation of BO parameters")
            return None

        results = self._optimization_loop(opt)

        return results

    def _objective_function(self, hyperparameter_values):
        """
        Method to evaluate the objective function
        """

        # Retrieve parameters labels
        params = {}
        for i in range(len(self.hyperparameters)):
            params[self.hyperparameters[i]] = hyperparameter_values[i]

        # Compute the score of the hyper-parameter configuration
        different_model_runs = []
        different_model_runs_extra_metrics = [[] for i in range(len(self.extra_metrics))]

        for i in range(self.model_runs):

            # Prepare model
            model_output = self.model.train_model(self.dataset, params,
                                                  self.topk)
            # Score of the model
            score = self.metric.score(model_output)
            different_model_runs.append(score)

            # Update of the extra metric values
            for j, extra_metric in enumerate(self.extra_metrics):
                different_model_runs_extra_metrics[j].append(extra_metric.score(model_output))

            # Save the model for each run
            if self.save_models:
                name = str(self.current_call) + "_" + str(i)
                save_model_path = self.model_path_models + name
                save_model_output(model_output, save_model_path)

        # Update of the dictionaries
        self.dict_model_runs[self.name_optimized_metric][
            'iteration_' + str(self.current_call)] = different_model_runs

        for j, extra_metric in enumerate(self.extra_metrics):
            self.dict_model_runs[self.extra_metric_names[j]]['iteration_' + str(self.current_call)] = \
                different_model_runs_extra_metrics[j]

        # The output for BO is the median over different_model_runs
        result = np.median(different_model_runs)

        if self.optimization_type == 'Maximize':
            result = - result

        # Boxplot for matrix_model_runs
        if self.plot_model:
            name_plot = self.save_path + self.plot_name + "_model_runs_" + self.name_optimized_metric
            plot_model_runs(self.dict_model_runs[self.name_optimized_metric], self.current_call, name_plot)

            # Boxplot of extrametrics (if any)
            j = 0
            for extra_metric in self.extra_metrics:
                name_plot = self.save_path + self.plot_name + "_model_runs_" + self.extra_metric_names[j]
                plot_model_runs(self.dict_model_runs[self.extra_metric_names[j]], self.current_call, name_plot)
                j = j + 1
        return result

    def _optimization_loop(self, opt):
        """
        Method to perform the BO iterations
        """

        # For loop to perform Bayesian Optimization
        for i in range(self.number_of_previous_calls, self.number_of_call):

            # Next point proposed by BO and evaluation of the objective function
            print("Current call: ", self.current_call)
            start_time = time.time()

            # Next point proposed by BO and evaluation of the objective function
            if i < self.lenx0:
                next_x = [self.x0[name][i] for name in self.hyperparameters]
                # next_x = self.x0[i]
                if len(self.y0) == 0:
                    f_val = self._objective_function(next_x)
                else:
                    self.dict_model_runs[self.name_optimized_metric]['iteration_' + str(i)] = self.y0[i]
                    f_val = -self.y0[i] if self.optimization_type == 'Maximize' else self.y0[i]

            else:
                next_x = opt.ask()
                f_val = self._objective_function(next_x)

            # Update the opt using (next_x,f_val)
            res = opt.tell(next_x, f_val)

            # Update the computational time for next_x (BO+Function evaluation)
            end_time = time.time()
            total_time_function = end_time - start_time
            self.time_eval.append(total_time_function)

            # Plot best seen
            if self.plot_best_seen:
                plot_bayesian_optimization(res.func_vals, self.save_path + self.plot_name + "_best_seen",
                                           self.log_scale_plot, conv_max=self.optimization_type == 'Maximize')

            # Create an object related to the BO optimization
            results = BestEvaluation(self, resultsBO=res)

            # Save the object
            if i % self.save_step == 0:
                name_json = self.save_path + self.save_name + ".json"
                results.save(name_json)

            # Early stop condition
            if i >= len(self.x0) and self.early_stop and early_condition(res.func_vals, self.early_step,
                                                                         self.n_random_starts):
                print("Stop because of early stopping condition")
                break

            # Update current_call
            self.current_call = self.current_call + 1

        return results

    def _load_metric(self, optimization_object, dataset):
        """
        Method to load the metric from the json file, useful for the resume method

        Parameters
        ----------

        """
        # Optimized Metric
        self.name_optimized_metric = optimization_object['metric_name']
        metric_parameters = optimization_object['metric_attributes']

        if self.name_optimized_metric.startswith('Coherence'):
            metric_parameters.update({'texts': dataset.get_corpus()})
        if self.name_optimized_metric.startswith('F1Score'):
            metric_parameters.update({'dataset': dataset})

        self.metric = select_metric(metric_parameters, self.name_optimized_metric)

        # Extra metrics
        self.extra_metrics = []
        self.extra_metric_names = optimization_object['extra_metric_names']
        dict_extra_metric_parameters = optimization_object['extra_metric_attributes']

        for name in self.extra_metric_names:
            metric_parameters = dict_extra_metric_parameters[name]
            if 'Coherence' in name:
                metric_parameters.update({'texts': dataset.get_corpus()})
            if self.name_optimized_metric.startswith('F1Score'):
                metric_parameters.update({'dataset': dataset})

            metric = select_metric(metric_parameters, name[2:])
            self.extra_metrics.append(metric)

    def _restore_parameters(self, name_path):
        """
        Restore the parameters of the BO from the json file
        """

        # Load the previous results
        with open(name_path, 'rb') as file:
            optimization_object = json.load(file)

        self.search_space = load_search_space(optimization_object["search_space"])
        self.acq_func = optimization_object["acq_func"]
        self.surrogate_model = optimization_object["surrogate_model"]
        self.kernel = eval(optimization_object["kernel"])
        self.optimization_type = optimization_object["optimization_type"]
        self.model_runs = optimization_object["model_runs"]
        self.save_models = optimization_object["save_models"]
        self.save_step = optimization_object["save_step"]
        self.save_name = optimization_object["save_name"]
        self.save_models = optimization_object["save_models"]
        self.save_path = optimization_object["save_path"]
        self.early_stop = optimization_object["early_stop"]
        self.early_step = optimization_object["early_step"]
        self.plot_model = optimization_object["plot_model"]
        self.plot_best_seen = optimization_object["plot_best_seen"]
        self.plot_name = optimization_object["plot_name"]
        self.log_scale_plot = optimization_object["log_scale_plot"]
        self.random_state = optimization_object["random_state"]
        self.dict_model_runs = optimization_object['dict_model_runs']
        self.number_of_previous_calls = optimization_object['current_call'] + 1
        self.current_call = optimization_object['current_call'] + 1
        self.number_of_call = optimization_object['number_of_call']
        self.save_path = optimization_object['save_path']
        self.x0 = optimization_object['x0']
        self.y0 = optimization_object['y0']
        self.n_random_starts = optimization_object['n_random_starts']
        self.initial_point_generator = optimization_object['initial_point_generator']
        self.topk = optimization_object['topk']
        self.time_eval = optimization_object["time_eval"]

        # Load the dataset
        dataset = Dataset()
        dataset.load(optimization_object["dataset_path"])
        self.dataset = dataset

        # Load the metric
        self._load_metric(optimization_object, dataset)

        # Load the model
        self.model = load_model(optimization_object)

        # Creation of the hyperparameters
        self.hyperparameters = list(sorted(self.search_space.keys()))

        # Choice of the optimizer
        opt = choose_optimizer(self)

        # Update number_of_call for restarting
        for i in range(self.number_of_previous_calls):
            next_x = [optimization_object["x_iters"][key][i] for key in self.hyperparameters]
            f_val = -optimization_object["f_val"][i] if self.optimization_type == 'Maximize' else \
                optimization_object["f_val"][i]
            res = opt.tell(next_x, f_val)

            # Create the directory where the results are saved
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

        self.model_path_models = self.save_path + "models/"

        return res, opt

    def _check_BO_parameters(self):
        """
        Controls about the BO parameters
        """
        # Controls about BO parameters
        if self.optimization_type not in ['Maximize', 'Minimize']:
            print("Error: optimization type must be Maximize or Minimize")
            return -1

        if self.surrogate_model not in ['RF', 'RS', 'GP', 'ET']:
            print("Error: surrogate model must be RF, ET, RS or GP")
            return -1

        if self.acq_func not in ['PI', 'EI', 'LCB']:
            print("Error: acquisition function must be PI, EI or LCB")
            return -1

        if self.number_of_call <= 0:
            print("Error: number_of_call can't be <= 0")
            return -1

        if self.number_of_call - len(self.x0) <= 0:
            print("Error: number_of_call is less then len(x0)")
            return None

        if not isinstance(self.model_runs, int):
            print("Error: model_run must be an integer")
            return -1

        if not isinstance(self.number_of_call, int):
            print("Error: number_of_call must be an integer")
            return -1

        if not isinstance(self.n_random_starts, int):
            print("Error: n_random_starts must be an integer")
            return -1

        if not isinstance(self.save_step, int):
            print("Error: save_step must be an integer")
            return -1

        if not isinstance(self.save_step, int):
            print("Error: save_step must be an integer")
            return -1

        if self.n_random_starts <= 0:
            print("Error: the number of initial_points must be >=1 !!!")
            return -1

        if self.initial_point_generator not in ['lhs', 'sobol', 'halton', 'hammersly', 'grid', 'random']:
            print("Error: wrong initial_point_generator")
            return -1

        if not isinstance(self.x0, dict):
            print("Error: x0 must be a dictionary!")
            return -1

        if not isinstance(self.y0, list):
            print("Error: y0 must be a dictionary!")
            return -1

        if len(self.x0) > 0:
            self.lenx0 = len(list(self.x0.values())[0])
            for i in range(len(self.x0.values())):
                lenC = len(list(self.x0.values())[i])
                if lenC != self.lenx0:
                    print("Error: dimension of x0 is not consistent!")
                    return -1

            if len(self.y0) > 0:
                if self.lenx0 != len(self.y0):
                    print("Error: different dimension for x0 and y0!")
                    return -1

        else:
            self.lenx0 = 0
            self.leny0 = 0

        if self.plot_name.endswith(".png"):
            self.plot_name = self.plot_name[:-4]

        if self.save_name.endswith(".json"):
            self.save_name = self.save_name[:-4]

        if self.save_path[-1] != '/':
            self.save_path = self.save_path + '/'

        return 0
