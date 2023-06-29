from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..core.database import Base

class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = {'schema': 'targets'}

    id = Column(Integer, primary_key=True, index=True)  # Primary domain identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When domain added
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  # When row updated
    domain = Column(String, unique=True, nullable=False)  # Unique domain name
    active = Column(Boolean)  # Should we analyze this domain?
    org_id = Column(Integer, ForeignKey('orgs.entities.id'))  # Corresponding Entity ID

    # Relationships
    org = relationship('Entity', back_populates='domains')
    urls = relationship('Url', back_populates='domain')  # Relationship to urls


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = {'schema': 'orgs'}

    id = Column(Integer, primary_key=True, index=True)  # Use sequence in PostgreSQL, like: id = Column(Integer, Sequence('fed_agencies_id_seq'), primary_key=True,)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When added
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  # When row updated
    name = Column(String, unique=True)  # Entity name
    # type = Column(String, ForeignKey('refs.org_types.name'))  # What type of org is this? From refs.org_types
    acronym = Column(String)  # Entity acronym
    active = Column(Boolean, default=False)  # Is this entity active?

    # Relationships
    domains = relationship('Domain', back_populates='org')


class Url(Base):
    __tablename__ = "urls"
    __table_args__ = {'schema': 'targets'}

    id = Column(BigInteger, primary_key=True, index=True)  # ID of URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String, unique=True, nullable=False)  # Target URL
    active_scan_axe = Column(Boolean, default=True)  # Should URL be scanned by Axe?
    active_main = Column(Boolean, default=True)  # URL Kill Switch - Use to stop all activity
    scanned_at_axe = Column(DateTime(timezone=True))
    domain_id = Column(Integer, ForeignKey('targets.domains.id'))  # Matched domain to domain ID
    active_scan_tech = Column(Boolean, default=True)  # Should this URL be tech checked?
    scanned_at_tech = Column(DateTime(timezone=True))
    discovery_crawl_id = Column(Integer)
    source_url = Column(String)
    recent_crawl_id = Column(Integer)
    sitemapped = Column(Boolean, default=False)  # Has this url been found in the sitemap?
    uppies_at = Column(DateTime(timezone=True))  # When Uppies was last checked
    # uppies_code = Column(Integer, ForeignKey('refs.uppies_codes.code'))  # Last Uppies Response Code
    crawled_at_rosevelt = Column(DateTime(timezone=True)) # When Rosevelt last crawled this URL
    source_url_id = Column(Integer)
    is_objective = Column(Boolean, default=False)  # Are we focusing on this url?
    queued_at_axe = Column(DateTime(timezone=True))
    queued_at_uppies = Column(DateTime(timezone=True)) # When added to Uppies queue
    queued_at_tech = Column(DateTime(timezone=True)) # When added to tech check queue
    active_scan_uppies = Column(Boolean, default=True)
    scanned_at_uppies = Column(DateTime(timezone=True))
    active_crawler = Column(Boolean, default=True)
    errored = Column(Boolean, default=False)
    queued_at_crawler = Column(DateTime(timezone=True))
    crawled_at = Column(DateTime(timezone=True))

    # Relationships
    domain = relationship('Domain', back_populates='urls')


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

    url = relationship('Url', back_populates='scan_data')
    rules = relationship('Rule', back_populates='scan_data')


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

    scan_data = relationship('ScanData', back_populates='rules')
    tests = relationship('Test', back_populates='rule')


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

    rule = relationship('Rule', back_populates='tests')
    url = relationship('Url', back_populates='tests')