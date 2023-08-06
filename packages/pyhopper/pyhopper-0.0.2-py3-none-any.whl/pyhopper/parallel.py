# Copyright 2021 Mathias Lechner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import loky
import os
from types import FunctionType, GeneratorType
import numpy as np
import sys


class CancelEvaluation(Exception):
    pass


class EvaluationResult:
    def __init__(self):
        self.value = None
        self.was_cancelled = None
        self.cancelled_by_user = False
        self.cancelled_by_nan = False
        self.intermediate_results = None


def execute(objective_function, candidate, canceller, kwargs):

    eval_result = EvaluationResult()
    try:
        iter_or_result = objective_function(candidate, **kwargs)
        if iter_or_result is None:
            raise ValueError(
                "Objective function returned 'None'. This probably means you forgot to add a 'return' (or 'yield') statement at the end of the function."
            )
        if isinstance(iter_or_result, GeneratorType):
            repeat = True
            eval_result.intermediate_results = []
            while repeat:
                try:
                    ir = next(iter_or_result)
                    eval_result.intermediate_results.append(ir)
                    eval_result.value = ir
                    if np.isnan(ir):
                        eval_result.was_cancelled = True
                        eval_result.cancelled_by_nan = True
                        repeat = False
                    if canceller is not None and canceller.should_cancel(
                        eval_result.intermediate_results
                    ):
                        # Let's not continue from here on
                        eval_result.was_cancelled = True
                        repeat = False
                except StopIteration:
                    repeat = False
        else:
            eval_result.value = iter_or_result
            if np.isnan(iter_or_result):
                eval_result.was_cancelled = True
                eval_result.cancelled_by_nan = True
    except CancelEvaluation:
        # If objective function raises this error, the evaluation will be treated as being cancelled
        eval_result.was_cancelled = True
        # we may need the information if the cancellation was done by the user inside the objective function
        # or by an EarlyCanceller
        eval_result.cancelled_by_user = True
    return eval_result


class TaskManager:
    def __init__(self, n_jobs):
        self._pending_candidates = []
        self._pending_futures = []
        if isinstance(n_jobs, int):
            backend = "loky"
            if n_jobs <= 0:
                n_jobs = len(os.sched_getaffinity(0))
            self._queue_max = n_jobs
        elif n_jobs == "per_gpu":
            backend = "cuda-dask"
        else:
            raise ValueError(
                "Could not prase ```n_jobs``` argument. Valid options are positive integers, -1 (all CPU cores), and 'per_gpu'"
            )

        if backend == "cuda-dask":
            try:
                from dask_cuda import LocalCUDACluster
                from dask.distributed import Client, wait
            except:
                raise ValueError(
                    "Could not import cuda-dask. Make sure dask is installed ```pip3 install -U cuda-dask```. "
                    + str(sys.exc_info()[0])
                )
            self._backend_FIRST_COMPLETED = "FIRST_COMPLETED"
            self._backend_ALL_COMPLETED = "ALL_COMPLETED"
            cluster = LocalCUDACluster()
            self._queue_max = len(cluster.cuda_visible_devices)
            self._backend_task_executor = Client(cluster)
            self._backend_wait_func = wait
        elif backend == "loky":
            self._backend_wait_func = loky.wait
            self._backend_FIRST_COMPLETED = loky.FIRST_COMPLETED
            self._backend_ALL_COMPLETED = loky.ALL_COMPLETED
            self._backend_task_executor = loky.get_reusable_executor(max_workers=n_jobs)
        elif backend == "dask":
            try:
                from dask.distributed import Client, LocalCluster, wait
            except:
                raise ValueError(
                    "Could not import dask. Make sure dask is installed ```pip3 install -U dask[distributed]```."
                    + str(sys.exc_info()[0])
                )
            self._backend_FIRST_COMPLETED = "FIRST_COMPLETED"
            self._backend_ALL_COMPLETED = "ALL_COMPLETED"
            cluster = LocalCluster(n_workers=n_jobs)
            self._backend_task_executor = Client(cluster)
            self._backend_wait_func = wait
        else:
            raise ValueError(f"Unknown backend '{backend}'")

    def submit(self, objective_function, candidate_type, candidate, canceller, kwargs):
        res = self._backend_task_executor.submit(
            execute, objective_function, candidate, canceller, kwargs
        )
        self._pending_futures.append(res)
        self._pending_candidates.append((candidate_type, candidate))

    def wait_for_first_to_complete(self):
        if len(self._pending_futures) <= 0:
            # Nothing to do
            return
        self._backend_wait_func(
            self._pending_futures, return_when=self._backend_FIRST_COMPLETED
        )

    def wait_for_all_to_complete(self):
        if len(self._pending_futures) <= 0:
            # Nothing to do
            return
        self._backend_wait_func(
            self._pending_futures, return_when=self._backend_ALL_COMPLETED
        )

    def iterate_done_tasks(self):
        i = 0
        while i < len(self._pending_futures):
            if self._pending_futures[i].done():
                candidate_type, candidate = self._pending_candidates[i]
                future = self._pending_futures[i]
                self._pending_futures.pop(i)
                self._pending_candidates.pop(i)
                yield candidate_type, candidate, future.result()
            else:
                i += 1

    @property
    def is_full(self):
        return len(self._pending_futures) >= self._queue_max