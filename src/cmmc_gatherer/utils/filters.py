"""Data filtering utilities for CMMC artifacts."""

import copy
import logging
from typing import List
from ..models.artifacts import ArtifactCollection, SecurityEvent

logger = logging.getLogger(__name__)

_SEVERITY_ORDER = {'Critical': 0, 'Error': 1, 'Warning': 2, 'Information': 3}


class DataFilter:
    """Filters and redacts artifact collections for specific reporting needs."""

    @staticmethod
    def filter_for_third_party(
        artifacts: ArtifactCollection,
        exclude_user_data: bool = True,
        exclude_sensitive: bool = True,
    ) -> ArtifactCollection:
        """Return a copy of artifacts safe for third-party sharing.

        Args:
            artifacts: Source ArtifactCollection (not mutated).
            exclude_user_data: Redact usernames in security events.
            exclude_sensitive: Clear endpoint metadata dicts.

        Returns:
            New ArtifactCollection with sensitive fields removed/redacted.
        """
        filtered = ArtifactCollection()
        filtered.collection_timestamp = artifacts.collection_timestamp

        for ep in artifacts.endpoints:
            ep_copy = copy.copy(ep)
            if exclude_sensitive:
                ep_copy.metadata = {}
            filtered.endpoints.append(ep_copy)

        for event in artifacts.security_events:
            event_copy = copy.copy(event)
            if exclude_user_data and event_copy.user:
                event_copy.user = "REDACTED"
            filtered.security_events.append(event_copy)

        filtered.policies = list(artifacts.policies)
        filtered.ad_objects = list(artifacts.ad_objects)
        return filtered

    @staticmethod
    def filter_by_severity(
        artifacts: ArtifactCollection,
        severity_threshold: str = 'Warning',
    ) -> List[SecurityEvent]:
        """Return security events at or above the given severity level.

        Args:
            artifacts: ArtifactCollection to filter.
            severity_threshold: Minimum level — 'Critical', 'Error',
                'Warning', or 'Information'.

        Returns:
            List of SecurityEvent objects meeting the threshold.
        """
        threshold_level = _SEVERITY_ORDER.get(severity_threshold, 3)
        return [
            event for event in artifacts.security_events
            if _SEVERITY_ORDER.get(event.level, 3) <= threshold_level
        ]
