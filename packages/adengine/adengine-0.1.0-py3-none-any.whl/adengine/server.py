import os
import argparse
import datetime
import socket
import logging
import traceback
import sys

from .engine import ADEngine, TaskNotCompleted, TaskIdNotFound, QueueIsFull
from .messages import *

logger = logging.getLogger('adengine.server')

__all__ = [
    'Server',
]

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK', None) or DEFAULT_UNIX_SOCKET

QUEUE_SIZE_DEFAULT = 20

READ_FILE_TIMEOUT_MIN = 5
READ_FILE_TIMEOUT_MAX = 60
READ_FILE_TIMEOUT_DEFAULT = 5

RESULT_TTL_DEFAULT = datetime.timedelta(minutes=5)
TASKS_BEFORE_SESSION_RESTART_DEFAULT = 100
MAX_CONNECTIONS_DEFAULT = 10


class Server:
    """This class represents ADEngine server."""

    def __init__(self,
                 queue_size: int,
                 read_file_timeout: int,
                 use_virtual_display: bool,
                 result_ttl: datetime.timedelta,
                 tasks_before_session_restart: int,
                 unix_socket: str,
                 max_connections: int):
        self._engine = ADEngine(self._parse_queue_size(queue_size),
                                self._parse_read_file_timeout(read_file_timeout),
                                use_virtual_display,
                                self._parse_result_ttl(result_ttl),
                                self._parse_tasks_before_session_restart(tasks_before_session_restart))
        self._unix_socket = unix_socket
        self._max_connections = self._parse_max_connections(max_connections)

    def start(self):
        logger.info('Staring server...')

        if os.path.exists(self._unix_socket):
            raise Exception(f'Unix socket {self._unix_socket} already exists, can not start server')

        os.makedirs(os.path.dirname(self._unix_socket), exist_ok=True)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self._unix_socket)

        logger.info('Starting ADEngine...')
        self._engine.start()

        sock.listen(self._max_connections)
        logger.info(f'Server is listening on {self._unix_socket}')

        try:
            while True:
                conn, _ = sock.accept()
                try:
                    message = recv(conn)
                except RecvError as e:
                    logger.error(f'An error occurred while receiving message:\n'
                                 f'{traceback.format_exception(RecvError, e, e.__traceback__)}')
                else:
                    logger.info(f'Received {message}')

                    if isinstance(message, TaskMessage):
                        try:
                            task_id = self._engine.put(message.activity,
                                                       message.password,
                                                       message.net_stabilization_delay)
                        except QueueIsFull:
                            send(conn, QueueIsFullMessage())
                        else:
                            send(conn, TaskIdMessage(task_id))

                    elif isinstance(message, TaskIdMessage):
                        try:
                            result = self._engine.get(message.task_id)
                        except TaskIdNotFound:
                            send(conn, TaskIdNotFoundMessage())
                        except TaskNotCompleted:
                            send(conn, TaskNotCompletedMessage())
                        else:
                            send(conn, ResultMessage(result))

                conn.close()
        except Exception as e:
            logger.debug(f'Stop server due to exception: {traceback.format_exc()}')
            raise e
        finally:
            logger.info('Stopping server...')

            sock.close()
            logger.info(f'Remove {self._unix_socket}')
            os.remove(self._unix_socket)

            logger.info('Stopping ADEngine...')
            self._engine.stop()

            logger.info('Server stopped')

    @staticmethod
    def _parse_queue_size(queue_size: int) -> int:
        if not isinstance(queue_size, int):
            raise TypeError()
        elif queue_size < 0:
            raise ValueError()
        else:
            return queue_size

    @staticmethod
    def _parse_read_file_timeout(read_file_timeout: int) -> int:
        if not isinstance(read_file_timeout, int):
            raise TypeError()
        elif read_file_timeout < READ_FILE_TIMEOUT_MIN or read_file_timeout > READ_FILE_TIMEOUT_MAX:
            raise ValueError()
        else:
            return read_file_timeout

    @staticmethod
    def _parse_tasks_before_session_restart(tasks_before_session_restart: int) -> int:
        if not isinstance(tasks_before_session_restart, int):
            raise TypeError()
        elif tasks_before_session_restart < 0:
            raise ValueError()
        else:
            return tasks_before_session_restart

    @staticmethod
    def _parse_result_ttl(result_ttl: datetime.timedelta) -> datetime.timedelta:
        if not isinstance(result_ttl, datetime.timedelta):
            raise TypeError()
        else:
            return result_ttl

    @staticmethod
    def _parse_max_connections(max_connections: int) -> int:
        if not isinstance(max_connections, int):
            raise TypeError()
        elif max_connections < 0:
            raise ValueError()
        else:
            return max_connections


def parse_timedelta(time_str: str):
    """Converts string hh:mm:ss to timedelta."""
    try:
        parts = time_str.split(':')
        time_params = dict(zip(['hours', 'minutes', 'seconds'],
                               (int(part) for part in parts)))
        return datetime.timedelta(**time_params)
    except Exception as e:
        raise ValueError(e)


def parse_positive_int(value: str):
    value = int(value)
    if value < 0:
        raise ValueError('Value must be positive')
    return value


def parse_read_file_timeout(min_file_read_timeout: int, max_file_read_timeout: int):
    def _parse_read_file_timeout(value: str):
        value = int(value)
        if value < min_file_read_timeout or value > max_file_read_timeout:
            raise ValueError(f'File reading timeout must not be lower than {min_file_read_timeout} '
                             f'and not greater than {max_file_read_timeout}')
        return value

    return _parse_read_file_timeout


def parse_args() -> dict:
    parser = argparse.ArgumentParser(prog='ADEngine server',
                                     description='ADEngine server runs ADEngine to extract data from activities.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--queue-size',
                        help='Maximum size of the queue with tasks',
                        dest='queue_size',
                        type=parse_positive_int,
                        default=QUEUE_SIZE_DEFAULT)
    parser.add_argument('--read-file-timeout',
                        help='Timout for reading activity file (in seconds)',
                        dest='read_file_timeout',
                        type=parse_read_file_timeout(READ_FILE_TIMEOUT_MIN, READ_FILE_TIMEOUT_MAX),
                        default=READ_FILE_TIMEOUT_DEFAULT)
    parser.add_argument('--use-virtual-display',
                        help='Use virtual display',
                        dest='virtual_display',
                        action='store_true')
    parser.add_argument('--result-ttl',
                        help='Result ttl like hh:mm:ss',
                        dest='result_ttl',
                        type=parse_timedelta,
                        default=RESULT_TTL_DEFAULT)
    parser.add_argument('--tasks-before-session-restart',
                        help='Number of tasks before restarting PacketTracer session',
                        dest='tasks_before_session_restart',
                        type=parse_positive_int,
                        default=TASKS_BEFORE_SESSION_RESTART_DEFAULT)
    parser.add_argument('--unix-socket',
                        help='Path to unix socket',
                        dest='unix_socket',
                        default=ADENGINE_UNIX_SOCK)
    parser.add_argument('--max-connections',
                        help='Maximum number of connections to server',
                        dest='max_connections',
                        type=parse_positive_int,
                        default=MAX_CONNECTIONS_DEFAULT)
    return vars(parser.parse_args())


def main():
    args = parse_args()

    server = Server(args['queue_size'],
                    args['read_file_timeout'],
                    args['virtual_display'],
                    args['result_ttl'],
                    args['tasks_before_session_restart'],
                    args['unix_socket'],
                    args['max_connections'])

    try:
        server.start()
    except KeyboardInterrupt:
        return 0
    except Exception:
        logger.error(f'Unexpected exception:\n{traceback.format_exc()}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
