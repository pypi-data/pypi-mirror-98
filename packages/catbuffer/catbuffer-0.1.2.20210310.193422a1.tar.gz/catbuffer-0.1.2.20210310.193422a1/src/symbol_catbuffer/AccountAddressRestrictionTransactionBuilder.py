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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .AccountAddressRestrictionTransactionBodyBuilder import AccountAddressRestrictionTransactionBodyBuilder
from .AccountRestrictionFlagsDto import AccountRestrictionFlagsDto
from .AmountDto import AmountDto
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .NetworkTypeDto import NetworkTypeDto
from .SignatureDto import SignatureDto
from .TimestampDto import TimestampDto
from .TransactionBuilder import TransactionBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class AccountAddressRestrictionTransactionBuilder(TransactionBuilder):
    """Binary layout for a non-embedded account address restriction transaction.

    Attributes:
        body: Account address restriction transaction body.
    """
    type_hints = {
        'signature' : 'SignatureDto',
        'signerPublicKey' : 'KeyDto',
        'network' : 'NetworkTypeDto',
        'type' : 'EntityTypeDto',
        'fee' : 'AmountDto',
        'deadline' : 'TimestampDto',
        'restrictionAdditions' : 'array',
        'restrictionDeletions' : 'array',
    }

    VERSION = 1
    ENTITY_TYPE = 0x4150

    def __init__(self, signerPublicKey, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = AccountAddressRestrictionTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountAddressRestrictionTransactionBuilder:
        """Creates an instance of AccountAddressRestrictionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountAddressRestrictionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = TransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = AccountAddressRestrictionTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = AccountAddressRestrictionTransactionBuilder(superObject.signerPublicKey, superObject.network)
        result.signature = superObject.signature
        result.fee = superObject.fee
        result.deadline = superObject.deadline
        result.body = body
        return result

    @property
    def restrictionFlags(self):
        return self.body.restrictionFlags

    @restrictionFlags.setter
    def restrictionFlags(self, restrictionFlags): # MARKER1 AttributeKind.FLAGS
        self.body.restrictionFlags = restrictionFlags

    @property
    def restrictionAdditions(self):
        return self.body.restrictionAdditions

    @property
    def restrictionDeletions(self):
        return self.body.restrictionDeletions

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
