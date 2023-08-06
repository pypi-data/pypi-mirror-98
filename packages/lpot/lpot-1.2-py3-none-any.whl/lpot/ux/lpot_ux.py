#!/usr/bin/env python3
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

"""WSGI Web Server."""

import sys
import uuid

from lpot.ux.utils.exceptions import NotFoundException
from lpot.ux.web.configuration import Configuration
from lpot.ux.web.server import run_server


def main() -> None:
    """Get parameters and initialize server."""
    try:
        configuration = Configuration()
    except NotFoundException as e:
        print(str(e))
        sys.exit(1)

    address = configuration.ip
    port = configuration.port
    token = uuid.uuid4().hex

    print(
        f"Visit http://{address}:{port}/?token={token} in your browser to access the UX.",
    )

    run_server(address, port, token)


if __name__ == "__main__":
    main()
