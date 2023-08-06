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
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class TransactionBuilder:
    """Binary layout for a transaction.

    Attributes:
        signature: Entity signature.
        signerPublicKey: Entity signer's public key.
        version: Entity version.
        network: Entity network.
        type: Entity type.
        fee: Transaction fee.
        deadline: Transaction deadline.
    """
    type_hints = {
        'signature' : 'SignatureDto',
        'signerPublicKey' : 'KeyDto',
        'network' : 'NetworkTypeDto',
        'type' : 'EntityTypeDto',
        'fee' : 'AmountDto',
        'deadline' : 'TimestampDto',
    }

    def __init__(self, signerPublicKey, version, network, type):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
        """
        self.signature = bytes(64)
        self.signerPublicKey = signerPublicKey
        self.version = version
        self.network = network
        self.type = type

        self.fee = 0
        self.deadline = 0


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> TransactionBuilder:
        """Creates an instance of TransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of TransactionBuilder.
        """
        bytes_ = bytes(payload)

        size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        verifiableEntityHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        signature_ = SignatureDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        signature = signature_.signature
        bytes_ = bytes_[signature_.getSize():]
        signerPublicKey_ = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        signerPublicKey = signerPublicKey_.key
        bytes_ = bytes_[signerPublicKey_.getSize():]
        entityBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        version = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        network_ = NetworkTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        network = network_.value
        bytes_ = bytes_[network_.getSize():]
        type_ = EntityTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        type = type_.value
        bytes_ = bytes_[type_.getSize():]
        fee_ = AmountDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        fee = fee_.amount
        bytes_ = bytes_[fee_.getSize():]
        deadline_ = TimestampDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        deadline = deadline_.timestamp
        bytes_ = bytes_[deadline_.getSize():]

        # create object and call
        result = TransactionBuilder(signerPublicKey, version, network, type)
        result.signature = signature
        result.fee = fee
        result.deadline = deadline
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # size
        size += 4  # verifiableEntityHeader_Reserved1
        size += SignatureDto(self.signature).getSize()
        size += KeyDto(self.signerPublicKey).getSize()
        size += 4  # entityBody_Reserved1
        size += 1  # version
        size += NetworkTypeDto(self.network).getSize()
        size += EntityTypeDto(self.type).getSize()
        size += AmountDto(self.fee).getSize()
        size += TimestampDto(self.deadline).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getSize(), 4))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, SignatureDto(self.signature).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, KeyDto(self.signerPublicKey).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.version, 1))  # serial_kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NetworkTypeDto(self.network).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, EntityTypeDto(self.type).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AmountDto(self.fee).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, TimestampDto(self.deadline).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('size', toHexString(GeneratorUtils.uintToBuffer(self.getSize(), 4)))
        result += '{:24s} : {}\n'.format('<reserved>', toHexString(GeneratorUtils.uintToBuffer(0, 4)))
        result += '{:24s} : {}\n'.format('signature', toHexString(SignatureDto(self.signature).serialize()))
        result += '{:24s} : {}\n'.format('signerPublicKey', toHexString(KeyDto(self.signerPublicKey).serialize()))
        result += '{:24s} : {}\n'.format('<reserved>', toHexString(GeneratorUtils.uintToBuffer(0, 4)))
        result += '{:24s} : {}\n'.format('version', toHexString(GeneratorUtils.uintToBuffer(self.version, 1)))
        result += '{:24s} : {}\n'.format('network', toHexString(NetworkTypeDto(self.network).serialize()))
        result += '{:24s} : {}\n'.format('type', toHexString(EntityTypeDto(self.type).serialize()))
        result += '{:24s} : {}\n'.format('fee', toHexString(AmountDto(self.fee).serialize()))
        result += '{:24s} : {}\n'.format('deadline', toHexString(TimestampDto(self.deadline).serialize()))
        return result
