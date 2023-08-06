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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .NetworkTypeDto import NetworkTypeDto
from .SecretLockTransactionBodyBuilder import SecretLockTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class EmbeddedSecretLockTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded secret lock transaction.

    Attributes:
        body: Secret lock transaction body.
    """
    type_hints = {
        'embeddedTransaction' : 'EmbeddedTransactionBuilder',
        'signerPublicKey' : 'KeyDto',
        'network' : 'NetworkTypeDto',
        'type' : 'EntityTypeDto',
        'recipientAddress' : 'UnresolvedAddressDto',
        'secret' : 'Hash256Dto',
        'mosaic' : 'UnresolvedMosaicBuilder',
        'duration' : 'BlockDurationDto',
        'hashAlgorithm' : 'LockHashAlgorithmDto',
    }

    VERSION = 1
    ENTITY_TYPE = 0x4152

    def __init__(self, signerPublicKey, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = SecretLockTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedSecretLockTransactionBuilder:
        """Creates an instance of EmbeddedSecretLockTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedSecretLockTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = SecretLockTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = EmbeddedSecretLockTransactionBuilder(superObject.signerPublicKey, superObject.network)
        # nothing needed to copy into EmbeddedTransaction
        result.body = body
        return result

    @property
    def recipientAddress(self):
        return self.body.recipientAddress

    @recipientAddress.setter
    def recipientAddress(self, recipientAddress): # MARKER1 AttributeKind.CUSTOM
        self.body.recipientAddress = recipientAddress

    @property
    def secret(self):
        return self.body.secret

    @secret.setter
    def secret(self, secret): # MARKER1 AttributeKind.CUSTOM
        self.body.secret = secret

    @property
    def mosaic(self):
        return self.body.mosaic

    @mosaic.setter
    def mosaic(self, mosaic): # MARKER1 AttributeKind.CUSTOM
        self.body.mosaic = mosaic

    @property
    def duration(self):
        return self.body.duration

    @duration.setter
    def duration(self, duration): # MARKER1 AttributeKind.CUSTOM
        self.body.duration = duration

    @property
    def hashAlgorithm(self):
        return self.body.hashAlgorithm

    @hashAlgorithm.setter
    def hashAlgorithm(self, hashAlgorithm): # MARKER1 AttributeKind.CUSTOM
        self.body.hashAlgorithm = hashAlgorithm

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.body.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.body.serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += super().__str__()
        result += self.body.__str__()
        return result
