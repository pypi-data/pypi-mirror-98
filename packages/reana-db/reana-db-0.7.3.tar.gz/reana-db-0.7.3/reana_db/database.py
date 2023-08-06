# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Database management for REANA."""

from __future__ import absolute_import

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from .config import SQLALCHEMY_DATABASE_URI

from reana_db.models import Base  # isort:skip  # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = Session.query_property()


def init_db():
    """Initialize the DB."""
    import reana_db.models

    reana_schema_name = "__reana"
    if not engine.dialect.has_schema(engine, reana_schema_name):
        event.listen(Base.metadata, "before_create", CreateSchema(reana_schema_name))
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
