# -*- coding: utf-8 -*-
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Benchmark class."""

import os
import re
from typing import Any, Dict, List

from lpot.ux.components.benchmark.benchmark_model import benchmark_model
from lpot.ux.utils.exceptions import ClientErrorException
from lpot.ux.utils.hw_info import HWInfo
from lpot.ux.utils.workload.workload import Workload


class Benchmark:
    """Benchmark class."""

    def __init__(
        self,
        workload: Workload,
        model_path: str,
        mode: str,
        datatype: str,
    ) -> None:
        """Initialize Benchmark class."""
        self.instances: int = 1
        self.cores_per_instance: int = HWInfo().cores // self.instances
        self.model_path = model_path
        self.datatype = datatype
        self.mode = mode
        self.batch_size = 1
        self.framework = workload.framework
        if (
            workload.config
            and workload.config.evaluation
            and workload.config.evaluation.performance
            and workload.config.evaluation.performance.dataloader
            and workload.config.evaluation.performance.dataloader.batch_size
        ):
            self.batch_size = (
                workload.config.evaluation.performance.dataloader.batch_size
            )

        if not os.path.exists(self.model_path):
            raise ClientErrorException("Could not found model in specified path.")

        self.config_path = workload.config_path
        self.benchmark_script = os.path.join(
            os.path.dirname(__file__),
            "benchmark_model.py",
        )

        self.command = [
            "python",
            self.benchmark_script,
            "--config",
            self.config_path,
            "--input-graph",
            self.model_path,
            "--mode",
            self.mode,
            "--framework",
            self.framework,
        ]

    def execute(self) -> List[Dict[str, Any]]:
        """Execute benchmark and collect results."""
        return benchmark_model(
            input_graph=self.model_path,
            config=self.config_path,
            benchmark_mode=self.mode,
            framework=self.framework,
            datatype=self.datatype,
        )

    def serialize(self) -> Dict[str, Any]:
        """Serialize Benchmark to dict."""
        result = {}
        for key, value in self.__dict__.items():
            variable_name = re.sub(r"^_", "", key)
            if variable_name == "command":
                result[variable_name] = " ".join(value)
            else:
                result[variable_name] = value
        return result
