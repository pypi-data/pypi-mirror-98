#!/usr/bin/python
"""
    Copyright (c) 2016-2019, Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp.
    Copyright (c) 2020-present, Jaguar0625, gimre, BloodyRookie.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations

# pylint: disable=unused-import

from binascii import hexlify
from .GeneratorUtils import GeneratorUtils
from .UnresolvedAddressDto import UnresolvedAddressDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class AccountMetadataTransactionBodyBuilder:
    """Binary layout for an account metadata transaction.

    Attributes:
        targetAddress: Metadata target address.
        scopedMetadataKey: Metadata key scoped to source, target and type.
        valueSizeDelta: Change in value size in bytes.
        value: Difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
    """
    def __init__(self):
        """ Constructor."""
        self.targetAddress = bytes(24)
        self.scopedMetadataKey = int()
        self.valueSizeDelta = int()
        self.value = bytes()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountMetadataTransactionBodyBuilder:
        """Creates an instance of AccountMetadataTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountMetadataTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        targetAddress_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        targetAddress = targetAddress_.unresolvedAddress
        bytes_ = bytes_[targetAddress_.getSize():]
        scopedMetadataKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        valueSizeDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIMPLE
        bytes_ = bytes_[2:]
        valueSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        value = GeneratorUtils.getBytes(bytes_, valueSize)  # kind:BUFFER
        bytes_ = bytes_[valueSize:]

        # create object and call
        result = AccountMetadataTransactionBodyBuilder()
        result.targetAddress = targetAddress
        result.scopedMetadataKey = scopedMetadataKey
        result.valueSizeDelta = valueSizeDelta
        result.value = value
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedAddressDto(self.targetAddress).getSize()
        size += 8  # scopedMetadataKey
        size += 2  # valueSizeDelta
        size += 2  # valueSize
        size += len(self.value)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.targetAddress).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.scopedMetadataKey, 8))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.valueSizeDelta, 2))  # serial_kind:SIMPLE
        size_value = len(self.value)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 2))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.value)  # kind:BUFFER
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('targetAddress', toHexString(UnresolvedAddressDto(self.targetAddress).serialize()))
        result += '{:24s} : {}\n'.format('scopedMetadataKey', toHexString(GeneratorUtils.uintToBuffer(self.scopedMetadataKey, 8)))
        result += '{:24s} : {}\n'.format('valueSizeDelta', toHexString(GeneratorUtils.uintToBuffer(self.valueSizeDelta, 2)))
        size_value = len(self.value)
        result += '{:24s} : {}\n'.format('valueSize', toHexString(GeneratorUtils.uintToBuffer(size_value, 2)))
        result += '{:24s} : {}\n'.format('value', toHexString(self.value))
        return result
