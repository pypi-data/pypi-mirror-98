from .__about__ import __version__

from .serial_interface import SerialInterface

from .protocol import (
    PollAction,
    PollResponse,
    PowerOnResetCompletePollResponse,
    KeystrokePollResponse,
    TerminalType,
    Control,
    SecondaryControl,
    poll,
    poll_ack,
    read_status,
    read_terminal_id,
    read_extended_id,
    read_address_counter_hi,
    read_address_counter_lo,
    read_data,
    read_multiple,
    reset,
    load_control_register,
    load_secondary_control,
    load_mask,
    load_address_counter_hi,
    load_address_counter_lo,
    write_data,
    clear,
    search_forward,
    search_backward,
    insert_byte,
    start_operation,
    diagnostic_reset,
    read_feature_id,
    eab_read_data,
    eab_load_mask,
    eab_write_alternate,
    eab_read_multiple,
    eab_write_under_mask,
    eab_read_status
)

from .features import (
    Feature,
    get_features
)

from .exceptions import (
    InterfaceError,
    ReceiveError,
    InterfaceTimeout,
    ReceiveTimeout,
    ProtocolError
)
