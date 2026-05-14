"""Data models for CMMC compliance artifacts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Endpoint:
    """Windows endpoint security posture snapshot."""

    hostname: str
    ip_address: str
    os_version: str
    installed_updates: List[str] = field(default_factory=list)
    security_products: List[str] = field(default_factory=list)
    firewall_status: Optional[str] = None
    antivirus_status: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "os_version": self.os_version,
            "installed_updates": self.installed_updates,
            "security_products": self.security_products,
            "firewall_status": self.firewall_status,
            "antivirus_status": self.antivirus_status,
            "metadata": self.metadata,
        }


@dataclass
class ADObject:
    """Active Directory object (user, group, or computer)."""

    distinguished_name: str
    object_class: str
    last_modified: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    group_memberships: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "distinguished_name": self.distinguished_name,
            "object_class": self.object_class,
            "last_modified": self.last_modified,
            "attributes": self.attributes,
            "group_memberships": self.group_memberships,
        }


@dataclass
class SecurityEvent:
    """Windows Security Event Log entry."""

    event_id: int
    source: str
    timestamp: str
    message: str
    level: str  # Critical, Error, Warning, Information
    computer: str
    user: Optional[str] = None
    event_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "source": self.source,
            "timestamp": self.timestamp,
            "message": self.message,
            "level": self.level,
            "computer": self.computer,
            "user": self.user,
            "event_data": self.event_data,
        }


@dataclass
class Policy:
    """Windows security policy configuration entry."""

    policy_name: str
    policy_type: str  # Group Policy, Local Policy, Windows Firewall, etc.
    status: str       # Enabled, Disabled, Not Configured
    target: str       # Computer, User, Domain, etc.
    value: Optional[str] = None
    description: Optional[str] = None
    last_applied: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "policy_type": self.policy_type,
            "status": self.status,
            "target": self.target,
            "value": self.value,
            "description": self.description,
            "last_applied": self.last_applied,
        }


@dataclass
class ArtifactCollection:
    """Container for all CMMC compliance artifacts from a single collection run."""

    endpoints: List[Endpoint] = field(default_factory=list)
    ad_objects: List[ADObject] = field(default_factory=list)
    security_events: List[SecurityEvent] = field(default_factory=list)
    policies: List[Policy] = field(default_factory=list)
    collection_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "collection_timestamp": self.collection_timestamp,
            "endpoints": [e.to_dict() for e in self.endpoints],
            "ad_objects": [a.to_dict() for a in self.ad_objects],
            "security_events": [se.to_dict() for se in self.security_events],
            "policies": [p.to_dict() for p in self.policies],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArtifactCollection":
        """Reconstruct an ArtifactCollection from a to_dict() payload."""
        collection = cls()
        collection.collection_timestamp = data.get(
            "collection_timestamp", collection.collection_timestamp
        )
        collection.endpoints = [Endpoint(**e) for e in data.get("endpoints", [])]
        collection.ad_objects = [ADObject(**a) for a in data.get("ad_objects", [])]
        collection.security_events = [
            SecurityEvent(**e) for e in data.get("security_events", [])
        ]
        collection.policies = [Policy(**p) for p in data.get("policies", [])]
        return collection
