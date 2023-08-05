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
from .BlockDurationDto import BlockDurationDto
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class NamespaceRegistrationTransactionBodyBuilder:
    """Binary layout for a namespace registration transaction.

    Attributes:
        duration: Namespace duration.
        parentId: Parent namespace identifier.
        id: Namespace identifier.
        registrationType: Namespace registration type.
        name: Namespace name.
    """
    def __init__(self):
        """ Constructor."""
        self.duration = BlockDurationDto().blockDuration
        self.parentId = NamespaceIdDto().namespaceId
        self.id = NamespaceIdDto().namespaceId
        self.registrationType = NamespaceRegistrationTypeDto(0).value
        self.name = bytes()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceRegistrationTransactionBodyBuilder:
        """Creates an instance of NamespaceRegistrationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceRegistrationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        registrationTypeCondition = bytes_[0:8]
        bytes_ = bytes_[8:]

        id_ = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        id = id_.namespaceId
        bytes_ = bytes_[id_.getSize():]
        registrationType_ = NamespaceRegistrationTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        registrationType = registrationType_.value
        bytes_ = bytes_[registrationType_.getSize():]
        nameSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        name = GeneratorUtils.getBytes(bytes_, nameSize)  # kind:BUFFER
        bytes_ = bytes_[nameSize:]
        duration = None
        if registrationType == NamespaceRegistrationTypeDto.ROOT.value:
            duration = BlockDurationDto.loadFromBinary(registrationTypeCondition).blockDuration  # kind:CUSTOM3
        parentId = None
        if registrationType == NamespaceRegistrationTypeDto.CHILD.value:
            parentId = NamespaceIdDto.loadFromBinary(registrationTypeCondition).namespaceId  # kind:CUSTOM3

        # create object and call
        result = NamespaceRegistrationTransactionBodyBuilder()
        result.duration = duration
        result.parentId = parentId
        result.id = id
        result.registrationType = registrationType
        result.name = name
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT.value:
            size += BlockDurationDto(self.duration).getSize()
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD.value:
            size += NamespaceIdDto(self.parentId).getSize()
        size += NamespaceIdDto(self.id).getSize()
        size += NamespaceRegistrationTypeDto(self.registrationType).getSize()
        size += 1  # nameSize
        size += len(self.name)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT.value:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD.value:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.parentId).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.id).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceRegistrationTypeDto(self.registrationType).serialize())  # kind:CUSTOM
        size_value = len(self.name)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.name)  # kind:BUFFER
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        if self.registrationType == NamespaceRegistrationTypeDto.ROOT.value:
            result += '{:24s} : {}\n'.format('duration', toHexString(BlockDurationDto(self.duration).serialize()))
        if self.registrationType == NamespaceRegistrationTypeDto.CHILD.value:
            result += '{:24s} : {}\n'.format('parentId', toHexString(NamespaceIdDto(self.parentId).serialize()))
        result += '{:24s} : {}\n'.format('id', toHexString(NamespaceIdDto(self.id).serialize()))
        result += '{:24s} : {}\n'.format('registrationType', toHexString(NamespaceRegistrationTypeDto(self.registrationType).serialize()))
        size_value = len(self.name)
        result += '{:24s} : {}\n'.format('nameSize', toHexString(GeneratorUtils.uintToBuffer(size_value, 1)))
        result += '{:24s} : {}\n'.format('name', toHexString(self.name))
        return result
