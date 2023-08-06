# SPDX-FileCopyrightText: Copyright (c) 2021 Martin Stephens
#
# SPDX-License-Identifier: MIT

# Many Pylnt conventions are broken for the sake of test readability
# Others fail because Pylint doesn't understand Pytest.
# Therefore skip this file.
# pylint: skip-file

import time
from collections import namedtuple
from random import random
from unittest.mock import PropertyMock
import pytest
from CircuitPython_AS3935 import biffobear_as3935 as as3935


# @pytest.fixture
# def device(mocker):
#     mocker.patch("as3935.AS3935", autospec=True)
#     return as3935.AS3935_SPI(


def test_as3925_spi_init_called_with_correct_args_and_kwargs(mocker):
    mock_init = mocker.patch.object(
        as3935.AS3935_SPI, "__init__", autospec=True, return_value=None
    )
    # Check that the correct class is subclassed
    assert issubclass(as3935.AS3935_SPI, as3935.AS3935)
    # Check the args and kwargs with default baudrate
    test_class = as3935.AS3935_SPI("spi", "cs", interrupt_pin="pin")
    mock_init.assert_called_once_with(test_class, "spi", "cs", interrupt_pin="pin")
    # Check the args and kwargs with assigned baudrate
    mock_init.reset_mock()
    test_class = as3935.AS3935_SPI("spi", "cs", baudrate=1_000_000, interrupt_pin="pin")
    mock_init.assert_called_once_with(
        test_class, "spi", "cs", baudrate=1_000_000, interrupt_pin="pin"
    )


@pytest.mark.parametrize(
    "spi, cs, cs_pin, interrupt_pin",
    [("spi1", "cs1", "cs_pin1", "int1"), ("spi2", "cs2", "cs_pin2", "int2")],
)
def test_calls_from_init_made_with_correct_args_and_kwargs(
    mocker, spi, cs, cs_pin, interrupt_pin
):
    mock_spi_device = mocker.patch.object(
        as3935.spi_dev, "SPIDevice", autospec=True, return_value="SPIDevice"
    )
    mock_digtalio_digitalinout = mocker.patch.object(
        as3935.digitalio, "DigitalInOut", autospec=True, return_value=cs_pin
    )
    mock_super_init = mocker.patch.object(
        as3935.AS3935, "__init__", autospec=True, return_value=None
    )
    # Test call to SPIDevice
    test_class = as3935.AS3935_SPI(spi, cs, interrupt_pin=interrupt_pin)
    mock_spi_device.assert_called_once_with(
        spi, cs_pin, baudrate=2_000_000, polarity=1, phase=0
    )
    # Check that digitalio is called with the correct pin to set the chip select
    mock_digtalio_digitalinout.assert_called_once_with(cs)
    # Also test that _device is set to the SPIDevice
    assert test_class._device == "SPIDevice"
    # Check that super.__init__ is called with the interrupt pin
    mock_super_init.assert_called_once_with(test_class, interrupt_pin=interrupt_pin)


def test_spi_device_called_with_correct_baudrates(mocker):
    mock_spi_device = mocker.patch.object(
        as3935.spi_dev, "SPIDevice", autospec=True, return_value="SPI_Device"
    )
    mock_digtalio_digitalinout = mocker.patch.object(
        as3935.digitalio, "DigitalInOut", autospec=True, return_value="cs"
    )
    mock_super_init = mocker.patch.object(
        as3935.AS3935, "__init__", autospec=True, return_value=None
    )
    # Confirm SPIDevice is called with the default baudrate
    test_class = as3935.AS3935_SPI("spi", "cs", interrupt_pin="pin")
    mock_spi_device.assert_called_once_with(
        "spi", "cs", baudrate=2_000_000, polarity=1, phase=0
    )
    # Confirm SPIDevice is called with the baudrate passed to __init__
    mock_spi_device.reset_mock()
    test_class = as3935.AS3935_SPI("spi", "cs", baudrate=1_000_000, interrupt_pin="pin")
    mock_spi_device.assert_called_once_with(
        "spi", "cs", baudrate=1_000_000, polarity=1, phase=0
    )


@pytest.mark.parametrize("address, data_byte", [(0x01, 0x55), (0x3D, 0xAA)])
def test_read_byte_in_calls_spi_dev_with_correct_arguments(mocker, address, data_byte):
    mock_spi_device = mocker.patch.object(as3935.spi_dev, "SPIDevice", autospec=True)
    mock_digitalinout = mocker.patch.object(
        as3935.digitalio, "DigitalInOut", autospec=True
    )
    test_device = as3935.AS3935_SPI("spi", "cs", interrupt_pin="pin")
    test_register = as3935._Register(address, 0x00, 0x00)
    test_device._DATA_BUFFER[0] = data_byte
    # Reset spi_device mock as it has been called during setup
    mock_spi_device.reset_mock()
    result = test_device._read_byte_in(test_register)
    # Complex mocking to work with "with x as y:" constructs
    calls_to_spidevice = test_device._device.__enter__.return_value.mock_calls
    # Confirm that write was called with the address byte
    name, args, kwargs = calls_to_spidevice[0]
    assert name == "write"
    # Confirm that only 1 byte is written
    assert kwargs == {"end": 1}
    # Extract the contents of the buffer sent to write and compare to expected buffer
    assert args[0][0] == test_device._ADDR_BUFFER[0]
    # Confirm that the bits 14 and 15 were set to 0 and 1 on the address in the buffer
    assert args[0][0] >> 6 == 0x01
    # Confirm that the _ADDR_BUFFER contains the correct address
    assert args[0][0] & 0x3F == address
    # Confirm that readinto was called and the result is correct
    name, args, kwargs = calls_to_spidevice[1]
    assert name == "readinto"
    # Confirm that only 1 byte is read
    assert kwargs == {"end": 1}
    # Confirm that the _DATA_BUFFER matches the buffer in readinto
    assert args[0][0] == test_device._DATA_BUFFER[0]
    # Confirm that the function returns the content of the _DATA_BUFFER
    assert result == test_device._DATA_BUFFER[0]


@pytest.mark.parametrize("address, data_byte", [(0x01, 0x55), (0x3D, 0xAA)])
def test_write_byte_out_calls_spi_dev_with_correct_arguments(
    mocker, address, data_byte
):
    mock_spi_device = mocker.patch.object(as3935.spi_dev, "SPIDevice", autospec=True)
    mock_digitalinout = mocker.patch.object(
        as3935.digitalio, "DigitalInOut", autospec=True
    )
    test_device = as3935.AS3935_SPI("spi", "cs", interrupt_pin="pin")
    test_register = as3935._Register(address, 0x00, 0x00)
    # Reset spi_device mock as it has been called during setup
    mock_spi_device.reset_mock()
    result = test_device._write_byte_out(test_register, data_byte)
    # Complex mocking to work with "with x as y:" constructs
    calls_to_spidevice = test_device._device.__enter__.return_value.mock_calls
    print(calls_to_spidevice)
    # Confirm that write_out was called with the address byte
    name, args, kwargs = calls_to_spidevice[0]
    assert name == "write"
    # Extract the contents of the buffer sent to write and compare to expected buffer
    assert args[0][0] == test_device._ADDR_BUFFER[0]
    # Confirm that the bits 14 and 15 were set to 0 and 0 on the address in the buffer
    assert args[0][0] >> 6 == 0x00
    # Confirm that the _ADDR_BUFFER contains the correct address
    assert args[0][0] & 0x3F == address
    # Confirm that write was called and the result is correct
    name, args, kwargs = calls_to_spidevice[1]
    assert name == "write"
    # Confirm that only 1 byte is written
    assert kwargs == {"end": 1}
    # Confirm that the _DATA_BUFFER matches the buffer in write
    assert args[0][0] == test_device._DATA_BUFFER[0]
