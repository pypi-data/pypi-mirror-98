# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging

import pytest

from requre.online_replacing import recording_requests
from requre.utils import StorageMode, get_datafile_filename

logger = logging.getLogger(__name__)


@pytest.fixture
def record_requests_fixture(request):
    storage_file = get_datafile_filename(request.node)
    with recording_requests(storage_file=storage_file) as cassette:
        mode_description = {
            StorageMode.read: "replaying",
            StorageMode.write: "recording",
            StorageMode.append: "appending",
            StorageMode.default: "in default mode",
        }[cassette.mode]
        logger.debug(
            f"Start requre {mode_description} with storage file: {storage_file}"
        )
        yield cassette
        cassette.dump()
        logger.debug(f"End requre {mode_description} with storage file: {storage_file}")
