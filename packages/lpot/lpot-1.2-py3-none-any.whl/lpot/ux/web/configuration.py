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

"""Configuration module for UX server."""

import argparse
import socket
from typing import Dict

from numpy.random import randint

from lpot.utils.utility import singleton
from lpot.ux.utils.exceptions import NotFoundException
from lpot.ux.utils.utils import determine_ip


@singleton
class Configuration:
    """Configuration object for UX server."""

    PORT_DEFAULT = 5000
    MAX_PORTS_TRIED = 10

    def __init__(self) -> None:
        """Set the variables."""
        self.ip = determine_ip()
        args = self.get_command_line_args()
        self.port = self.determine_port(args)

    def get_command_line_args(self) -> Dict:
        """Return arguments passed in command line."""
        parser = argparse.ArgumentParser(description="Run UX server.")
        parser.add_argument(
            "-p",
            "--port",
            type=int,
            help="port number to listen on",
        )
        return vars(parser.parse_args())

    def determine_port(self, args: Dict) -> int:
        """
        Return port to be used by the server.

        Will raise a NotFoundException if port is already in use.

        When port given in command line, only that port will be tried.
        When no port specified will try self.MAX_PORTS_TRIED times,
        starting with self.PORT_DEFAULT.
        """
        command_line_port = args.get("port")
        if command_line_port is not None:
            if self.is_port_taken(command_line_port):
                raise NotFoundException(
                    f"Port {command_line_port} already in use, exiting.",
                )
            else:
                return command_line_port

        ports = [self.PORT_DEFAULT] + randint(
            1025,
            65536,
            self.MAX_PORTS_TRIED - 1,
        ).tolist()

        for port in ports:
            if not self.is_port_taken(port):
                return port

        raise NotFoundException(
            f"Unable to find a free port in {len(ports)} attempts, exiting.",
        )

    def is_port_taken(self, port: int) -> bool:
        """Return if given port is already in use."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((self.ip, port))
        except socket.error:
            return True
        finally:
            s.close()

        return False
