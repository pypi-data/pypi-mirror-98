# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft Models API."""

from datetime import datetime

from invenio_db import db
from invenio_records.models import RecordMetadataBase
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types import UUIDType


def ParentRecordMixin(parent_record_cls):
    """A mixin factory that add the foreign keys to the parent record.

    It is intended to be added to the "child" record class, e.g.:
    ``class MyRecord(RecordBase, ParentRecordMixin(MyRecordParentClass))``.
    """
    class Mixin:
        @declared_attr
        def parent_id(cls):
            return db.Column(UUIDType, db.ForeignKey(parent_record_cls.id))

        @declared_attr
        def parent(cls):
            return db.relationship(parent_record_cls)

        # TODO: Add parent_order and/or parent_latest
        # TODO: Should both records and drafts have an order?
    return Mixin


class DraftMetadataBase(RecordMetadataBase):
    """Represent a base class for draft metadata."""

    fork_version_id = db.Column(db.Integer)
    """Version ID of the record."""

    expires_at = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=True
    )
    """Specifies when the draft expires. If `NULL` the draft doesn't expire."""
