"""Asynchronous Model-Based Search.

Arguments of AMBS:

* ``surrogate-model``

    * ``RF`` : Random Forest (default)
    * ``ET`` : Extra Trees
    * ``GBRT`` : Gradient Boosting Regression Trees
    * ``DUMMY`` :
    * ``GP`` : Gaussian process

* ``liar-strategy``

    * ``cl_max`` : (default)
    * ``cl_min`` :
    * ``cl_mean`` :

* ``acq-func`` : Acquisition function

    * ``LCB`` :
    * ``EI`` :
    * ``PI`` :
    * ``gp_hedge`` : (default)
"""


import math
import signal
import json

import ConfigSpace as cs
import ConfigSpace.hyperparameters as csh
import numpy as np
import skopt
from deephyper.core.logs.logging import JsonMessage as jm
from deephyper.search import util
from deephyper.search.nas import NeuralArchitectureSearch
from deephyper.evaluator.evaluate import Encoder

dhlogger = util.conf_logger("deephyper.search.nas.ambs")

SERVICE_PERIOD = 2  # Delay (seconds) between main loop iterations
CHECKPOINT_INTERVAL = 1  # How many jobs to complete between optimizer checkpoints
EXIT_FLAG = False


def on_exit(signum, stack):
    global EXIT_FLAG
    EXIT_FLAG = True


class AMBNeuralArchitectureSearch(NeuralArchitectureSearch):
    def __init__(
        self,
        problem,
        run,
        evaluator,
        surrogate_model="RF",
        acq_func="LCB",
        kappa=1.96,
        xi=0.001,
        liar_strategy="cl_min",
        n_jobs=1,
        **kwargs,
    ):
        super().__init__(problem, run, evaluator, **kwargs)
        dhlogger.info("Initializing AMBNAS")

        dhlogger.info(
            jm(
                type="start_infos",
                alg="ambs",
                nworkers=self.evaluator.num_workers,
                encoded_space=json.dumps(self.problem.space, cls=Encoder),
            )
        )
        dhlogger.info(f"kappa={kappa}, xi={xi}")

        self.n_initial_points = self.evaluator.num_workers
        self.liar_strategy = liar_strategy

        # Building search space for SkOptimizer using ConfigSpace
        search_space = self.problem.build_search_space()
        skopt_space = cs.ConfigurationSpace(seed=self.problem.seed)
        for i, vnode in enumerate(search_space.variable_nodes):
            hp = csh.UniformIntegerHyperparameter(
                name=f"vnode_{i}", lower=0, upper=(vnode.num_ops - 1)
            )
            skopt_space.add_hyperparameter(hp)

        self.opt = skopt.Optimizer(
            dimensions=skopt_space,
            base_estimator=self.get_surrogate_model(surrogate_model, n_jobs),
            acq_func=acq_func,
            acq_optimizer="sampling",
            acq_func_kwargs={"xi": xi, "kappa": kappa},
            n_initial_points=self.n_initial_points,
            random_state=self.problem.seed,
        )

    @staticmethod
    def _extend_parser(parser):
        NeuralArchitectureSearch._extend_parser(parser)
        parser.add_argument(
            "--surrogate-model",
            default="RF",
            choices=["RF", "ET", "GBRT", "DUMMY", "GP"],
            help="Type of surrogate model (learner).",
        )
        parser.add_argument(
            "--liar-strategy",
            default="cl_max",
            choices=["cl_min", "cl_mean", "cl_max"],
            help="Constant liar strategy",
        )
        parser.add_argument(
            "--acq-func",
            default="gp_hedge",
            choices=["LCB", "EI", "PI", "gp_hedge"],
            help="Acquisition function type",
        )
        parser.add_argument(
            "--kappa",
            type=float,
            default=1.96,
            help='Controls how much of the variance in the predicted values should be taken into account. If set to be very high, then we are favouring exploration over exploitation and vice versa. Used when the acquisition is "LCB".',
        )

        parser.add_argument(
            "--xi",
            type=float,
            default=0.01,
            help='Controls how much improvement one wants over the previous best values. If set to be very high, then we are favouring exploration over exploitation and vice versa. Used when the acquisition is "EI", "PI".',
        )

        parser.add_argument(
            "--n-jobs",
            type=int,
            default=1,
            help="number of cores to use for the 'surrogate model' (learner), if n_jobs=-1 then it will use all cores available.",
        )
        return parser

    def main(self):
        # timer = util.DelayTimer(max_minutes=None, period=SERVICE_PERIOD)
        # chkpoint_counter = 0

        num_evals_done = 0

        # Filling available nodes at start
        dhlogger.info(f"Generating {self.evaluator.num_workers} initial points...")
        self.evaluator.add_eval_batch(self.get_random_batch(size=self.n_initial_points))

        # Main loop
        while num_evals_done < self.max_evals:

            # Collecting finished evaluations
            new_results = list(self.evaluator.get_finished_evals())

            if len(new_results) > 0:
                stats = {"num_cache_used": self.evaluator.stats["num_cache_used"]}
                dhlogger.info(jm(type="env_stats", **stats))
                self.evaluator.dump_evals(saved_key="arch_seq")

                num_received = len(new_results)
                num_evals_done += num_received

                # Transform configurations to list to fit optimizer
                opt_X = []
                opt_y = []
                for cfg, obj in new_results:
                    x = replace_nan(cfg["arch_seq"])
                    opt_X.append(x)
                    opt_y.append(-obj)  #! maximizing

                self.opt.tell(opt_X, opt_y)  #! fit: costly
                new_X = self.opt.ask(
                    n_points=len(new_results), strategy=self.liar_strategy
                )

                new_batch = []
                for x in new_X:
                    new_cfg = self.to_dict(x)
                    new_batch.append(new_cfg)

                # submit_childs
                if len(new_results) > 0:
                    self.evaluator.add_eval_batch(new_batch)

    def get_surrogate_model(self, name: str, n_jobs: int = None):
        """Get a surrogate model from Scikit-Optimize.

        Args:
            name (str): name of the surrogate model.
            n_jobs (int): number of parallel processes to distribute the computation of the surrogate model.

        Raises:
            ValueError: when the name of the surrogate model is unknown.
        """
        accepted_names = ["RF", "ET", "GBRT", "GP", "DUMMY"]
        if not (name in accepted_names):
            raise ValueError(
                f"Unknown surrogate model {name}, please choose among {accepted_names}."
            )

        if name == "RF":
            surrogate = skopt.learning.RandomForestRegressor(n_jobs=n_jobs)
        elif name == "ET":
            surrogate = skopt.learning.ExtraTreesRegressor(n_jobs=n_jobs)
        elif name == "GBRT":
            surrogate = skopt.learning.GradientBoostingQuantileRegressor(n_jobs=n_jobs)
        else:  # for DUMMY and GP
            surrogate = name

        return surrogate

    def get_random_batch(self, size: int) -> list:
        batch = []
        n_points = max(0, size - len(batch))
        if n_points > 0:
            points = self.opt.ask(n_points=n_points)
            for point in points:
                point_as_dict = self.to_dict(point)
                batch.append(point_as_dict)
        return batch

    def to_dict(self, x: list) -> dict:
        cfg = self.problem.space.copy()
        cfg["arch_seq"] = x
        return cfg


def isnan(x) -> bool:
    """Check if a value is NaN."""
    if isinstance(x, float):
        return math.isnan(x)
    elif isinstance(x, np.float64):
        return np.isnan(x)
    else:
        return False


def replace_nan(x):
    return [np.nan if x_i == "nan" else x_i for x_i in x]


if __name__ == "__main__":
    args = AMBNeuralArchitectureSearch.parse_args()
    search = AMBNeuralArchitectureSearch(**vars(args))
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)
    search.main()
