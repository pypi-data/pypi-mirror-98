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
from .MosaicGlobalRestrictionTransactionBodyBuilder import MosaicGlobalRestrictionTransactionBodyBuilder
from .MosaicRestrictionTypeDto import MosaicRestrictionTypeDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class MosaicGlobalRestrictionTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded mosaic global restriction transaction.

    Attributes:
        body: Mosaic global restriction transaction body.
    """
    type_hints = {
        'signature' : 'SignatureDto',
        'signerPublicKey' : 'KeyDto',
        'network' : 'NetworkTypeDto',
        'type' : 'EntityTypeDto',
        'fee' : 'AmountDto',
        'deadline' : 'TimestampDto',
        'mosaicId' : 'UnresolvedMosaicIdDto',
        'referenceMosaicId' : 'UnresolvedMosaicIdDto',
        'previousRestrictionType' : 'MosaicRestrictionTypeDto',
        'newRestrictionType' : 'MosaicRestrictionTypeDto',
    }

    VERSION = 1
    ENTITY_TYPE = 0x4151

    def __init__(self, signerPublicKey, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = MosaicGlobalRestrictionTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicGlobalRestrictionTransactionBuilder:
        """Creates an instance of MosaicGlobalRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicGlobalRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = MosaicGlobalRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = MosaicGlobalRestrictionTransactionBuilder(superObject.signerPublicKey, superObject.network)
        result.signature = superObject.signature
        result.fee = superObject.fee
        result.deadline = superObject.deadline
        result.body = body
        return result

    @property
    def mosaicId(self):
        return self.body.mosaicId

    @mosaicId.setter
    def mosaicId(self, mosaicId): # MARKER1 AttributeKind.CUSTOM
        self.body.mosaicId = mosaicId

    @property
    def referenceMosaicId(self):
        return self.body.referenceMosaicId

    @referenceMosaicId.setter
    def referenceMosaicId(self, referenceMosaicId): # MARKER1 AttributeKind.CUSTOM
        self.body.referenceMosaicId = referenceMosaicId

    @property
    def restrictionKey(self):
        return self.body.restrictionKey

    @restrictionKey.setter
    def restrictionKey(self, restrictionKey): # MARKER1 AttributeKind.SIMPLE
        self.body.restrictionKey = restrictionKey

    @property
    def previousRestrictionValue(self):
        return self.body.previousRestrictionValue

    @previousRestrictionValue.setter
    def previousRestrictionValue(self, previousRestrictionValue): # MARKER1 AttributeKind.SIMPLE
        self.body.previousRestrictionValue = previousRestrictionValue

    @property
    def newRestrictionValue(self):
        return self.body.newRestrictionValue

    @newRestrictionValue.setter
    def newRestrictionValue(self, newRestrictionValue): # MARKER1 AttributeKind.SIMPLE
        self.body.newRestrictionValue = newRestrictionValue

    @property
    def previousRestrictionType(self):
        return self.body.previousRestrictionType

    @previousRestrictionType.setter
    def previousRestrictionType(self, previousRestrictionType): # MARKER1 AttributeKind.CUSTOM
        self.body.previousRestrictionType = previousRestrictionType

    @property
    def newRestrictionType(self):
        return self.body.newRestrictionType

    @newRestrictionType.setter
    def newRestrictionType(self, newRestrictionType): # MARKER1 AttributeKind.CUSTOM
        self.body.newRestrictionType = newRestrictionType

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
