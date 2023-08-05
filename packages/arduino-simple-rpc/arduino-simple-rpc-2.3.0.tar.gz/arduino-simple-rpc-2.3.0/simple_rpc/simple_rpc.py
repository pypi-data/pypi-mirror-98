from functools import wraps
from time import sleep
from types import MethodType

from serial import serial_for_url
from serial.serialutil import SerialException

from .extras import make_function
from .io import read, read_byte_string, until, write
from .protocol import parse_line


_protocol = b'simpleRPC'
_version = (3, 0, 0)

_list_req = 0xff


class _Interface(object):
    """Generic simpleRPC interface."""
    def __init__(
            self: object, device: str, baudrate: int=9600, wait: int=2,
            autoconnect: bool=True) -> None:
        """
        :arg device: Device name.
        :arg baudrate: Baud rate.
        :arg wait: Time in seconds before communication starts.
        :arg autoconnect: Automatically connect.
        """
        self._wait = wait

        self._connection = serial_for_url(
            device, do_not_open=True, baudrate=baudrate)
        self._version = (0, 0, 0)
        self._endianness = b'<'
        self._size_t = b'H'
        self.methods = {}

        if autoconnect:
            self.open()

    def __enter__(self: object) -> object:
        return self

    def __exit__(
            self: object, exc_type: None, exc_val: None, exc_tb: None) -> None:
        self.close()

    def _open(self: object) -> None:
        try:
            self._connection.open()
        except SerialException:
            raise IOError('could not open device')

    def _close(self: object) -> None:
        self._connection.close()

    def _select(self: object, index: int) -> None:
        """Initiate a remote procedure call, select the method.

        :arg index: Method index.
        """
        self._write(b'B', index)

    def _write(self: object, obj_type: bytes, obj: any) -> None:
        """Provide parameters for a remote procedure call.

        :arg obj_type: Type of the parameter.
        :arg obj: Value of the parameter.
        """
        write(self._connection, self._endianness, self._size_t, obj_type, obj)

    def _read_byte_string(self: object) -> bytes:
        return read_byte_string(self._connection)

    def _read(self: object, obj_type: str) -> any:
        """Read a return value from a remote procedure call.

        :arg obj_type: Return type.

        :returns: Return value.
        """
        return read(self._connection, self._endianness, self._size_t, obj_type)

    def _get_methods(self: object) -> dict:
        """Get remote procedure call methods.

        :returns: Method objects indexed by name.
        """
        self._select(_list_req)

        if self._read_byte_string() != _protocol:
            raise ValueError('missing protocol header')

        self._version = tuple(self._read(b'B') for _ in range(3))
        if self._version[0] != _version[0] or self._version[1] > _version[1]:
            raise ValueError(
                'version mismatch (device: {}, client: {})'.format(
                    '.'.join(map(str, self._version)),
                    '.'.join(map(str, _version))))

        self._endianness, self._size_t = (
            bytes([c]) for c in self._read_byte_string())

        methods = {}
        for index, line in enumerate(
                until(lambda x: x == b'', self._read_byte_string)):
            method = parse_line(index, line)
            methods[method['name']] = method

        return methods

    def is_open(self: object) -> bool:
        """Query interface state."""
        pass

    def open(self: object) -> None:
        """Connect to device."""
        sleep(self._wait)

        self.methods = self._get_methods()
        for method in self.methods.values():
            setattr(
                self, method['name'], MethodType(make_function(method), self))

    def close(self: object) -> None:
        """Disconnect from device."""
        for method in self.methods:
            delattr(self, method)
        self.methods.clear()

    def call_method(self: object, name: str, *args: list) -> any:
        """Execute a method.

        :arg name: Method name.
        :arg *args: Method parameters.

        :returns: Return value of the method.
        """
        if name not in self.methods:
            raise ValueError('invalid method name: {}'.format(name))
        method = self.methods[name]

        parameters = method['parameters']
        if len(args) != len(parameters):
            raise TypeError(
                '{} expected {} arguments, got {}'.format(
                    name, len(parameters), len(args)))

        # Call the method.
        self._select(method['index'])

        # Provide parameters (if any).
        if method['parameters']:
            for index, parameter in enumerate(method['parameters']):
                self._write(parameter['fmt'], args[index])

        # Read return value (if any).
        if method['return']['fmt']:
            return self._read(method['return']['fmt'])
        return None


class SerialInterface(_Interface):
    """Serial simpleRPC interface."""
    @wraps(_Interface.is_open)
    def is_open(self: object) -> bool:
        return self._connection.isOpen()

    @wraps(_Interface.open)
    def open(self: object) -> None:
        self._open()
        super().open()

    @wraps(_Interface.close)
    def close(self: object) -> None:
        super().close()
        self._close()


class SocketInterface(_Interface):
    """Socket simpleRPC interface."""
    def _auto_open(f: callable) -> callable:
        """Decorator for automatic opening and closing of ethernet sockets."""
        @wraps(f)
        def _auto_open_wrapper(
                self: object, *args: list, **kwargs: dict) -> any:
            self._open()
            result = f(self, *args, **kwargs)
            self._close()

            return result

        return _auto_open_wrapper

    @wraps(_Interface.is_open)
    def is_open(self: object) -> bool:
        return len(self.methods) > 0

    open = _auto_open(_Interface.open)
    call_method = _auto_open(_Interface.call_method)


class Interface(object):
    """Generic simpleRPC interface wrapper."""
    @wraps(_Interface.__init__)
    def __new__(
            cls: object, device: str, *args: list, **kwargs: dict) -> object:
        if device.startswith('socket'):
            return SocketInterface(device, *args, **kwargs)
        return SerialInterface(device, *args, **kwargs)
