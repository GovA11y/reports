# axe.py
# Relative Path: insight/api/models/axe.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..core.database import Base


# Axe Schema
class ScanData(Base):
    __tablename__ = 'scan_data'
    __table_args__ = {'schema': 'axe'}

    id = Column(BigInteger, primary_key=True, index=True)
    engine_name = Column(String(20))
    engine_version = Column(String(10))
    orientation_angle = Column(String(5))
    orientation_type = Column(String(25))
    user_agent = Column(String(250))
    window_height = Column(Integer)
    window_width = Column(Integer)
    reporter = Column(String(50))
    runner_name = Column(String(50))
    scanned_at = Column(DateTime(timezone=True))
    url = Column(String)
    url_id = Column(BigInteger, ForeignKey('targets.urls.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    url = relationship('targets.Url', back_populates='scan_data')
    rules = relationship('axe.Rule', back_populates='scan_data')


class Rule(Base):
    __tablename__ = 'rules'
    __table_args__ = {'schema': 'axe'}

    id = Column(BigInteger, primary_key=True, index=True)
    scan_id = Column(BigInteger, ForeignKey('axe.scan_data.id'))
    rule_type = Column(String(20))
    description = Column(String(250))
    help = Column(String(250))
    help_url = Column(String(250))
    axe_id = Column(String(35), ForeignKey('refs.a11y_rules.axe_id'))
    impact = Column(String(25))
    tags = Column(JSONB)
    nodes = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    scan_data = relationship('axe.ScanData', back_populates='rules')
    tests = relationship('axe.Test', back_populates='rule')


class Test(Base):
    __tablename__ = 'tests'
    __table_args__ = {'schema': 'axe'}

    id = Column(BigInteger, primary_key=True, index=True)
    rule_id = Column(BigInteger, ForeignKey('axe.rules.id'))
    url_id = Column(BigInteger, ForeignKey('targets.urls.id'))
    rule_type = Column(String)
    target = Column(String)
    axe_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(Boolean, default=True)
    impact = Column(String, ForeignKey('refs.axe_impact.name'))
    tested_at = Column(DateTime(timezone=True))
    html = Column(String)
    failure_summary = Column(String)

    rule = relationship('axe.Rule', back_populates='tests')
    url = relationship('axe.Url', back_populates='tests')