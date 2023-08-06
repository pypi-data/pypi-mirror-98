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
from .Hash256Dto import Hash256Dto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class SecretProofTransactionBodyBuilder:
    """Binary layout for a secret proof transaction.

    Attributes:
        recipientAddress: Locked mosaic recipient address.
        secret: Secret.
        hashAlgorithm: Hash algorithm.
        proof: Proof data.
    """
    def __init__(self):
        """ Constructor."""
        self.recipientAddress = bytes(24)
        self.secret = bytes(32)
        self.hashAlgorithm = LockHashAlgorithmDto(0).value
        self.proof = bytes()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretProofTransactionBodyBuilder:
        """Creates an instance of SecretProofTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretProofTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        recipientAddress_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        recipientAddress = recipientAddress_.unresolvedAddress
        bytes_ = bytes_[recipientAddress_.getSize():]
        secret_ = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        secret = secret_.hash256
        bytes_ = bytes_[secret_.getSize():]
        proofSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        hashAlgorithm_ = LockHashAlgorithmDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        hashAlgorithm = hashAlgorithm_.value
        bytes_ = bytes_[hashAlgorithm_.getSize():]
        proof = GeneratorUtils.getBytes(bytes_, proofSize)  # kind:BUFFER
        bytes_ = bytes_[proofSize:]

        # create object and call
        result = SecretProofTransactionBodyBuilder()
        result.recipientAddress = recipientAddress
        result.secret = secret
        result.hashAlgorithm = hashAlgorithm
        result.proof = proof
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedAddressDto(self.recipientAddress).getSize()
        size += Hash256Dto(self.secret).getSize()
        size += 2  # proofSize
        size += LockHashAlgorithmDto(self.hashAlgorithm).getSize()
        size += len(self.proof)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.recipientAddress).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, Hash256Dto(self.secret).serialize())  # kind:CUSTOM
        size_value = len(self.proof)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 2))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LockHashAlgorithmDto(self.hashAlgorithm).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.proof)  # kind:BUFFER
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('recipientAddress', toHexString(UnresolvedAddressDto(self.recipientAddress).serialize()))
        result += '{:24s} : {}\n'.format('secret', toHexString(Hash256Dto(self.secret).serialize()))
        size_value = len(self.proof)
        result += '{:24s} : {}\n'.format('proofSize', toHexString(GeneratorUtils.uintToBuffer(size_value, 2)))
        result += '{:24s} : {}\n'.format('hashAlgorithm', toHexString(LockHashAlgorithmDto(self.hashAlgorithm).serialize()))
        result += '{:24s} : {}\n'.format('proof', toHexString(self.proof))
        return result
