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
from .KeyDto import KeyDto
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTransactionBodyBuilder import NamespaceRegistrationTransactionBodyBuilder
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto
from .NetworkTypeDto import NetworkTypeDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class EmbeddedNamespaceRegistrationTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded namespace registration transaction.

    Attributes:
        body: Namespace registration transaction body.
    """
    type_hints = {
        'embeddedTransaction' : 'EmbeddedTransactionBuilder',
        'signerPublicKey' : 'KeyDto',
        'network' : 'NetworkTypeDto',
        'type' : 'EntityTypeDto',
        'duration' : 'BlockDurationDto',
        'parentId' : 'NamespaceIdDto',
        'id' : 'NamespaceIdDto',
        'registrationType' : 'NamespaceRegistrationTypeDto',
    }

    VERSION = 1
    ENTITY_TYPE = 0x414e

    def __init__(self, signerPublicKey, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = NamespaceRegistrationTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedNamespaceRegistrationTransactionBuilder:
        """Creates an instance of EmbeddedNamespaceRegistrationTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedNamespaceRegistrationTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = NamespaceRegistrationTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = EmbeddedNamespaceRegistrationTransactionBuilder(superObject.signerPublicKey, superObject.network)
        # nothing needed to copy into EmbeddedTransaction
        result.body = body
        return result

    @property
    def duration(self):
        return self.body.duration

    @duration.setter
    def duration(self, duration): # MARKER1 AttributeKind.CUSTOM
        self.body.duration = duration

    @property
    def parentId(self):
        return self.body.parentId

    @parentId.setter
    def parentId(self, parentId): # MARKER1 AttributeKind.CUSTOM
        self.body.parentId = parentId

    @property
    def id(self):
        return self.body.id

    @id.setter
    def id(self, id): # MARKER1 AttributeKind.CUSTOM
        self.body.id = id

    @property
    def registrationType(self):
        return self.body.registrationType

    @registrationType.setter
    def registrationType(self, registrationType): # MARKER1 AttributeKind.CUSTOM
        self.body.registrationType = registrationType

    @property
    def name(self):
        return self.body.name

    @name.setter
    def name(self, name): # MARKER1 AttributeKind.BUFFER
        self.body.name = name

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
