"""
Stream operations for Runa programming language.

This module provides functions for working with various types of streams,
including text streams, binary streams, and network streams.
"""

import io
import sys
import socket
from typing import Dict, Optional, List, Any, BinaryIO, TextIO
from ...vm.vm import VirtualMachine, VMValue, VMValueType


# Store open streams by handle for proper resource management
_open_streams: Dict[int, Any] = {}
_next_stream_handle = 1


def register_stream_functions(vm: VirtualMachine) -> None:
    """
    Register stream operation functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    # Text stream operations
    vm.native_functions["open_text"] = _open_text
    vm.native_functions["read_text"] = _read_text
    vm.native_functions["write_text"] = _write_text
    vm.native_functions["readline"] = _readline
    vm.native_functions["readlines"] = _readlines
    
    # Binary stream operations
    vm.native_functions["open_binary"] = _open_binary
    vm.native_functions["read_binary"] = _read_binary
    vm.native_functions["write_binary"] = _write_binary
    
    # Common stream operations
    vm.native_functions["close_stream"] = _close_stream
    vm.native_functions["flush_stream"] = _flush_stream
    vm.native_functions["seek"] = _seek
    vm.native_functions["tell"] = _tell
    
    # TCP socket operations
    vm.native_functions["tcp_connect"] = _tcp_connect
    vm.native_functions["tcp_listen"] = _tcp_listen
    vm.native_functions["tcp_accept"] = _tcp_accept
    vm.native_functions["tcp_send"] = _tcp_send
    vm.native_functions["tcp_receive"] = _tcp_receive
    
    # Register a shutdown hook to close all streams
    vm.native_functions["_cleanup_streams"] = _cleanup_streams
    # TODO: Add proper shutdown hook registration when VM supports it


def _get_next_handle() -> int:
    """
    Get the next available stream handle.
    
    Returns:
        An integer handle
    """
    global _next_stream_handle
    handle = _next_stream_handle
    _next_stream_handle += 1
    return handle


def _cleanup_streams(vm: VirtualMachine) -> VMValue:
    """
    Close all open streams when VM shuts down.
    
    Args:
        vm: The virtual machine
        
    Returns:
        A null VM value
    """
    global _open_streams
    
    for handle, stream in list(_open_streams.items()):
        try:
            if hasattr(stream, 'close'):
                stream.close()
        except Exception:
            pass  # Ignore errors during cleanup
    
    _open_streams.clear()
    return VMValue(VMValueType.NULL, None)


def _open_text(vm: VirtualMachine, filepath: VMValue, mode: VMValue = None, encoding: VMValue = None) -> VMValue:
    """
    Open a text file stream.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        mode: The open mode (default: 'r')
        encoding: The text encoding (default: 'utf-8')
        
    Returns:
        An integer VM value with the stream handle
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.INTEGER, -1)
    
    file_mode = 'r'
    if mode and mode.type == VMValueType.STRING:
        file_mode = mode.value
    
    file_encoding = 'utf-8'
    if encoding and encoding.type == VMValueType.STRING:
        file_encoding = encoding.value
    
    try:
        file = open(filepath.value, mode=file_mode, encoding=file_encoding)
        handle = _get_next_handle()
        _open_streams[handle] = file
        return VMValue(VMValueType.INTEGER, handle)
    except Exception as e:
        print(f"Error opening text file: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _read_text(vm: VirtualMachine, handle: VMValue, size: VMValue = None) -> VMValue:
    """
    Read from a text stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        size: The number of characters to read (default: read all)
        
    Returns:
        A string VM value with the read content
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.NULL, None)
    
    stream = _open_streams[handle.value]
    read_size = -1
    if size and size.type == VMValueType.INTEGER:
        read_size = size.value
    
    try:
        if read_size < 0:
            content = stream.read()
        else:
            content = stream.read(read_size)
        return VMValue(VMValueType.STRING, content)
    except Exception as e:
        print(f"Error reading from text stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _write_text(vm: VirtualMachine, handle: VMValue, content: VMValue) -> VMValue:
    """
    Write to a text stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        content: The content to write
        
    Returns:
        An integer VM value with the number of characters written
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.INTEGER, -1)
    
    stream = _open_streams[handle.value]
    
    try:
        count = stream.write(str(content.value))
        return VMValue(VMValueType.INTEGER, count)
    except Exception as e:
        print(f"Error writing to text stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _readline(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Read a line from a text stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        
    Returns:
        A string VM value with the line
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.NULL, None)
    
    stream = _open_streams[handle.value]
    
    try:
        line = stream.readline()
        return VMValue(VMValueType.STRING, line)
    except Exception as e:
        print(f"Error reading line from text stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _readlines(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Read all lines from a text stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        
    Returns:
        A list VM value with the lines
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.LIST, [])
    
    stream = _open_streams[handle.value]
    
    try:
        lines = stream.readlines()
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.STRING, line) for line in lines
        ])
    except Exception as e:
        print(f"Error reading lines from text stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.LIST, [])


def _open_binary(vm: VirtualMachine, filepath: VMValue, mode: VMValue = None) -> VMValue:
    """
    Open a binary file stream.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        mode: The open mode (default: 'rb')
        
    Returns:
        An integer VM value with the stream handle
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.INTEGER, -1)
    
    file_mode = 'rb'
    if mode and mode.type == VMValueType.STRING:
        file_mode = mode.value
        if 'b' not in file_mode:
            file_mode += 'b'  # Ensure binary mode
    
    try:
        file = open(filepath.value, mode=file_mode)
        handle = _get_next_handle()
        _open_streams[handle] = file
        return VMValue(VMValueType.INTEGER, handle)
    except Exception as e:
        print(f"Error opening binary file: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _read_binary(vm: VirtualMachine, handle: VMValue, size: VMValue = None) -> VMValue:
    """
    Read from a binary stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        size: The number of bytes to read (default: read all)
        
    Returns:
        A list VM value with the bytes (as integers)
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.LIST, [])
    
    stream = _open_streams[handle.value]
    read_size = -1
    if size and size.type == VMValueType.INTEGER:
        read_size = size.value
    
    try:
        if read_size < 0:
            content = stream.read()
        else:
            content = stream.read(read_size)
        
        # Convert bytes to list of integers
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.INTEGER, b) for b in content
        ])
    except Exception as e:
        print(f"Error reading from binary stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.LIST, [])


def _write_binary(vm: VirtualMachine, handle: VMValue, data: VMValue) -> VMValue:
    """
    Write to a binary stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        data: The data to write (list of integers)
        
    Returns:
        An integer VM value with the number of bytes written
    """
    if (handle.type != VMValueType.INTEGER or 
        handle.value not in _open_streams or
        data.type != VMValueType.LIST):
        return VMValue(VMValueType.INTEGER, -1)
    
    stream = _open_streams[handle.value]
    
    try:
        # Convert list of integers to bytes
        byte_data = bytes([
            item.value if item.type == VMValueType.INTEGER else 0
            for item in data.value
        ])
        
        count = stream.write(byte_data)
        return VMValue(VMValueType.INTEGER, count)
    except Exception as e:
        print(f"Error writing to binary stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _close_stream(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Close a stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        
    Returns:
        A boolean VM value indicating success
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.BOOLEAN, False)
    
    stream = _open_streams[handle.value]
    
    try:
        stream.close()
        del _open_streams[handle.value]
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error closing stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _flush_stream(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Flush a stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        
    Returns:
        A boolean VM value indicating success
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.BOOLEAN, False)
    
    stream = _open_streams[handle.value]
    
    try:
        stream.flush()
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error flushing stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _seek(vm: VirtualMachine, handle: VMValue, offset: VMValue, whence: VMValue = None) -> VMValue:
    """
    Seek to a position in a stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        offset: The offset to seek to
        whence: The reference position (0=start, 1=current, 2=end, default: 0)
        
    Returns:
        A boolean VM value indicating success
    """
    if (handle.type != VMValueType.INTEGER or 
        handle.value not in _open_streams or
        offset.type != VMValueType.INTEGER):
        return VMValue(VMValueType.BOOLEAN, False)
    
    stream = _open_streams[handle.value]
    
    seek_whence = 0  # Default to start
    if whence and whence.type == VMValueType.INTEGER:
        seek_whence = whence.value
    
    try:
        stream.seek(offset.value, seek_whence)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error seeking in stream: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _tell(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Get the current position in a stream.
    
    Args:
        vm: The virtual machine
        handle: The stream handle
        
    Returns:
        An integer VM value with the position
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.INTEGER, -1)
    
    stream = _open_streams[handle.value]
    
    try:
        position = stream.tell()
        return VMValue(VMValueType.INTEGER, position)
    except Exception as e:
        print(f"Error getting stream position: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _tcp_connect(vm: VirtualMachine, host: VMValue, port: VMValue) -> VMValue:
    """
    Connect to a TCP server.
    
    Args:
        vm: The virtual machine
        host: The host to connect to
        port: The port to connect to
        
    Returns:
        An integer VM value with the socket handle
    """
    if host.type != VMValueType.STRING or port.type != VMValueType.INTEGER:
        return VMValue(VMValueType.INTEGER, -1)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host.value, port.value))
        handle = _get_next_handle()
        _open_streams[handle] = sock
        return VMValue(VMValueType.INTEGER, handle)
    except Exception as e:
        print(f"Error connecting to TCP server: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _tcp_listen(vm: VirtualMachine, host: VMValue, port: VMValue, backlog: VMValue = None) -> VMValue:
    """
    Create a TCP server socket.
    
    Args:
        vm: The virtual machine
        host: The host to bind to
        port: The port to bind to
        backlog: The connection backlog (default: 5)
        
    Returns:
        An integer VM value with the socket handle
    """
    if host.type != VMValueType.STRING or port.type != VMValueType.INTEGER:
        return VMValue(VMValueType.INTEGER, -1)
    
    connection_backlog = 5
    if backlog and backlog.type == VMValueType.INTEGER:
        connection_backlog = backlog.value
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host.value, port.value))
        sock.listen(connection_backlog)
        handle = _get_next_handle()
        _open_streams[handle] = sock
        return VMValue(VMValueType.INTEGER, handle)
    except Exception as e:
        print(f"Error creating TCP server socket: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _tcp_accept(vm: VirtualMachine, server_handle: VMValue) -> VMValue:
    """
    Accept a connection on a TCP server socket.
    
    Args:
        vm: The virtual machine
        server_handle: The server socket handle
        
    Returns:
        A list VM value with [client_handle, client_address]
    """
    if (server_handle.type != VMValueType.INTEGER or 
        server_handle.value not in _open_streams):
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.INTEGER, -1),
            VMValue(VMValueType.STRING, "")
        ])
    
    server_sock = _open_streams[server_handle.value]
    
    try:
        client_sock, client_addr = server_sock.accept()
        client_handle = _get_next_handle()
        _open_streams[client_handle] = client_sock
        
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.INTEGER, client_handle),
            VMValue(VMValueType.STRING, f"{client_addr[0]}:{client_addr[1]}")
        ])
    except Exception as e:
        print(f"Error accepting TCP connection: {e}", file=sys.stderr)
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.INTEGER, -1),
            VMValue(VMValueType.STRING, "")
        ])


def _tcp_send(vm: VirtualMachine, handle: VMValue, data: VMValue) -> VMValue:
    """
    Send data over a TCP socket.
    
    Args:
        vm: The virtual machine
        handle: The socket handle
        data: The data to send
        
    Returns:
        An integer VM value with the number of bytes sent
    """
    if handle.type != VMValueType.INTEGER or handle.value not in _open_streams:
        return VMValue(VMValueType.INTEGER, -1)
    
    sock = _open_streams[handle.value]
    
    try:
        if data.type == VMValueType.STRING:
            send_data = data.value.encode('utf-8')
        elif data.type == VMValueType.LIST:
            # Convert list of integers to bytes
            send_data = bytes([
                item.value if item.type == VMValueType.INTEGER else 0
                for item in data.value
            ])
        else:
            send_data = str(data.value).encode('utf-8')
        
        count = sock.send(send_data)
        return VMValue(VMValueType.INTEGER, count)
    except Exception as e:
        print(f"Error sending data over TCP: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _tcp_receive(vm: VirtualMachine, handle: VMValue, size: VMValue, as_text: VMValue = None) -> VMValue:
    """
    Receive data from a TCP socket.
    
    Args:
        vm: The virtual machine
        handle: The socket handle
        size: The maximum number of bytes to receive
        as_text: Whether to return the data as text (default: False)
        
    Returns:
        A string VM value (if as_text) or a list VM value with bytes
    """
    if (handle.type != VMValueType.INTEGER or 
        handle.value not in _open_streams or
        size.type != VMValueType.INTEGER):
        return VMValue(VMValueType.NULL, None)
    
    sock = _open_streams[handle.value]
    
    try:
        data = sock.recv(size.value)
        
        is_text = as_text and as_text.type == VMValueType.BOOLEAN and as_text.value
        if is_text:
            # Return as string
            try:
                text = data.decode('utf-8')
                return VMValue(VMValueType.STRING, text)
            except UnicodeDecodeError:
                # Fall back to binary if not valid UTF-8
                is_text = False
        
        if not is_text:
            # Return as list of integers
            return VMValue(VMValueType.LIST, [
                VMValue(VMValueType.INTEGER, b) for b in data
            ])
    except Exception as e:
        print(f"Error receiving data from TCP: {e}", file=sys.stderr)
        if is_text:
            return VMValue(VMValueType.STRING, "")
        else:
            return VMValue(VMValueType.LIST, []) 