from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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