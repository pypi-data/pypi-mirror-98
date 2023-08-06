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
from .MosaicRestrictionTypeDto import MosaicRestrictionTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class MosaicGlobalRestrictionTransactionBodyBuilder:
    """Binary layout for a mosaic global restriction transaction.

    Attributes:
        mosaicId: Identifier of the mosaic being restricted.
        referenceMosaicId: Identifier of the mosaic providing the restriction key.
        restrictionKey: Restriction key relative to the reference mosaic identifier.
        previousRestrictionValue: Previous restriction value.
        newRestrictionValue: New restriction value.
        previousRestrictionType: Previous restriction type.
        newRestrictionType: New restriction type.
    """
    def __init__(self):
        """ Constructor."""
        self.mosaicId = UnresolvedMosaicIdDto().unresolvedMosaicId
        self.referenceMosaicId = UnresolvedMosaicIdDto().unresolvedMosaicId
        self.restrictionKey = int()
        self.previousRestrictionValue = int()
        self.newRestrictionValue = int()
        self.previousRestrictionType = MosaicRestrictionTypeDto(0).value
        self.newRestrictionType = MosaicRestrictionTypeDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicGlobalRestrictionTransactionBodyBuilder:
        """Creates an instance of MosaicGlobalRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicGlobalRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaicId_ = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        mosaicId = mosaicId_.unresolvedMosaicId
        bytes_ = bytes_[mosaicId_.getSize():]
        referenceMosaicId_ = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        referenceMosaicId = referenceMosaicId_.unresolvedMosaicId
        bytes_ = bytes_[referenceMosaicId_.getSize():]
        restrictionKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        newRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionType_ = MosaicRestrictionTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        previousRestrictionType = previousRestrictionType_.value
        bytes_ = bytes_[previousRestrictionType_.getSize():]
        newRestrictionType_ = MosaicRestrictionTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        newRestrictionType = newRestrictionType_.value
        bytes_ = bytes_[newRestrictionType_.getSize():]

        # create object and call
        result = MosaicGlobalRestrictionTransactionBodyBuilder()
        result.mosaicId = mosaicId
        result.referenceMosaicId = referenceMosaicId
        result.restrictionKey = restrictionKey
        result.previousRestrictionValue = previousRestrictionValue
        result.newRestrictionValue = newRestrictionValue
        result.previousRestrictionType = previousRestrictionType
        result.newRestrictionType = newRestrictionType
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedMosaicIdDto(self.mosaicId).getSize()
        size += UnresolvedMosaicIdDto(self.referenceMosaicId).getSize()
        size += 8  # restrictionKey
        size += 8  # previousRestrictionValue
        size += 8  # newRestrictionValue
        size += MosaicRestrictionTypeDto(self.previousRestrictionType).getSize()
        size += MosaicRestrictionTypeDto(self.newRestrictionType).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicIdDto(self.mosaicId).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicIdDto(self.referenceMosaicId).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.restrictionKey, 8))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.previousRestrictionValue, 8))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.newRestrictionValue, 8))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicRestrictionTypeDto(self.previousRestrictionType).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicRestrictionTypeDto(self.newRestrictionType).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('mosaicId', toHexString(UnresolvedMosaicIdDto(self.mosaicId).serialize()))
        result += '{:24s} : {}\n'.format('referenceMosaicId', toHexString(UnresolvedMosaicIdDto(self.referenceMosaicId).serialize()))
        result += '{:24s} : {}\n'.format('restrictionKey', toHexString(GeneratorUtils.uintToBuffer(self.restrictionKey, 8)))
        result += '{:24s} : {}\n'.format('previousRestrictionValue', toHexString(GeneratorUtils.uintToBuffer(self.previousRestrictionValue, 8)))
        result += '{:24s} : {}\n'.format('newRestrictionValue', toHexString(GeneratorUtils.uintToBuffer(self.newRestrictionValue, 8)))
        result += '{:24s} : {}\n'.format('previousRestrictionType', toHexString(MosaicRestrictionTypeDto(self.previousRestrictionType).serialize()))
        result += '{:24s} : {}\n'.format('newRestrictionType', toHexString(MosaicRestrictionTypeDto(self.newRestrictionType).serialize()))
        return result
