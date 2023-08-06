import pytest
import sys
import subprocess
import signal
import datetime
import os
import time
import tempfile
import multiprocessing as mp
import random

from adengine.client import Client
from adengine.engine import TaskNotCompleted
from adengine.pt import WrongPassword, ActivityFileReadingError, ActivityNeedsPassword, TopologyFilesNotSupported

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT, read_file_binary

QUEUE_SIZE = 100
RESULT_TTL = datetime.timedelta(hours=1)
TASKS_BEFORE_SESSION_RESTART = 100
MAX_CONNECTIONS = QUEUE_SIZE
UNIX_SOCKET = tempfile.mktemp()


@pytest.fixture(scope='module')
def run_server():
    server = subprocess.Popen([sys.executable, '-m', 'adengine.server',
                               '--queue-size', str(QUEUE_SIZE),
                               '--read-file-timeout', str(READ_FILE_TIMEOUT),
                               '--use-virtual-display' if USE_VIRTUAL_DISPLAY else '',
                               '--result-ttl', str(RESULT_TTL),
                               '--tasks-before-session-restart', str(TASKS_BEFORE_SESSION_RESTART),
                               '--unix-socket', UNIX_SOCKET,
                               '--max-connections', str(MAX_CONNECTIONS)])
    time.sleep(10)
    yield
    server.send_signal(signal.SIGINT)
    server.wait()


def extract_sequentially(tasks: list):
    client = Client(UNIX_SOCKET)
    for activity, password, net_stabilization_delay, error, total_percentage in tasks:
        task_id = client.put(activity, password, net_stabilization_delay)
        result = None
        while not result:
            try:
                result = client.get(task_id)
            except TaskNotCompleted:
                time.sleep(0.5)
        if error:
            assert isinstance(result.error, error)
            assert result.data is None
        else:
            assert result.error is None
            assert result.data is not None
            assert abs(result.data['totalPercentage'] - total_percentage) < 1.0


@pytest.mark.stress
def test_stress(run_server):
    tasks = [
        ('no_such_file.pka'.encode('utf-8'), 'password', 0, ActivityFileReadingError, None),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), 'wrong_password', 0, WrongPassword, None),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), None, 0, ActivityNeedsPassword, None),
        (read_file_binary(os.path.join(TEST_DATA, 'topology.pkt')), None, 0, TopologyFilesNotSupported, None),

        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123', 0, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'without_password.pka')), None, 0, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_small.pka')), '123', 5, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_big.pka')), '123', 20, None, 97.0),
    ]

    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(extract_sequentially, (random.sample(tasks, len(tasks)) for _ in range(mp.cpu_count())))
