"""Compliance scoring based on collected artifacts."""

import logging
from ..models.artifacts import ArtifactCollection

logger = logging.getLogger(__name__)


class ComplianceScorer:
    """Calculates a weighted compliance score (0-100) from an ArtifactCollection."""

    SCORE_WEIGHTS = {
        'firewall': 15,
        'antivirus': 15,
        'updates': 15,
        'policies': 20,
        'event_logging': 15,
        'ad_security': 20,
    }

    @classmethod
    def calculate_overall_score(cls, artifacts: ArtifactCollection) -> int:
        """Return a 0-100 compliance score weighted across all dimensions."""
        score = 0.0
        score += (cls._score_firewall(artifacts) / 100) * cls.SCORE_WEIGHTS['firewall']
        score += (cls._score_antivirus(artifacts) / 100) * cls.SCORE_WEIGHTS['antivirus']
        score += (cls._score_policies(artifacts) / 100) * cls.SCORE_WEIGHTS['policies']
        score += (cls._score_updates(artifacts) / 100) * cls.SCORE_WEIGHTS['updates']
        score += (cls._score_event_logging(artifacts) / 100) * cls.SCORE_WEIGHTS['event_logging']
        score += (cls._score_ad_security(artifacts) / 100) * cls.SCORE_WEIGHTS['ad_security']
        return int(max(0, min(100, score)))

    @classmethod
    def _score_firewall(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.endpoints:
            return 0
        enabled = sum(1 for ep in artifacts.endpoints if ep.firewall_status == "Enabled")
        return int((enabled / len(artifacts.endpoints)) * 100)

    @classmethod
    def _score_antivirus(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.endpoints:
            return 0
        active = sum(1 for ep in artifacts.endpoints if ep.antivirus_status == "Active")
        return int((active / len(artifacts.endpoints)) * 100)

    @classmethod
    def _score_policies(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.policies:
            return 0
        enabled = sum(1 for p in artifacts.policies if p.status == "Enabled")
        return int((enabled / len(artifacts.policies)) * 100)

    @classmethod
    def _score_updates(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.endpoints:
            return 0
        patched = sum(1 for ep in artifacts.endpoints if ep.installed_updates)
        return int((patched / len(artifacts.endpoints)) * 100)

    @classmethod
    def _score_event_logging(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.security_events:
            return 0
        return min(100, len(artifacts.security_events))

    @classmethod
    def _score_ad_security(cls, artifacts: ArtifactCollection) -> int:
        if not artifacts.ad_objects:
            return 0
        return min(100, int((len(artifacts.ad_objects) / 20) * 100))
