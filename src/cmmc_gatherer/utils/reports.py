"""Report-building utilities for CMMC compliance data."""

import logging
from typing import Dict, List, Any, Optional
from ..models.artifacts import ArtifactCollection
from .compliance import ComplianceScorer

logger = logging.getLogger(__name__)


class TenantManager:
    """Manages artifact collections for multiple MSP tenants."""

    def __init__(self):
        self.tenants: Dict[str, ArtifactCollection] = {}

    def add_tenant(self, tenant_id: str, artifacts: ArtifactCollection) -> bool:
        """Store artifacts for a tenant. Returns True on success."""
        try:
            self.tenants[tenant_id] = artifacts
            logger.info(f"Added tenant: {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add tenant {tenant_id}: {e}")
            return False

    def get_tenant(self, tenant_id: str) -> Optional[ArtifactCollection]:
        """Return artifacts for a tenant, or None if not found."""
        return self.tenants.get(tenant_id)

    def get_all_tenants(self) -> Dict[str, ArtifactCollection]:
        """Return all tenant artifacts keyed by tenant ID."""
        return self.tenants

    def calculate_tenant_scores(self) -> Dict[str, int]:
        """Return compliance scores (0-100) for every stored tenant."""
        return {
            tenant_id: ComplianceScorer.calculate_overall_score(artifacts)
            for tenant_id, artifacts in self.tenants.items()
        }


class ReportBuilder:
    """Builds structured compliance report data from an ArtifactCollection."""

    @staticmethod
    def build_executive_summary(
        artifacts: ArtifactCollection,
        customer_name: str,
        assessment_date: str,
    ) -> Dict[str, Any]:
        """Return a dict summarising the compliance posture for a customer.

        Args:
            artifacts: Collected compliance data.
            customer_name: Display name of the customer/client.
            assessment_date: ISO date string for the assessment.

        Returns:
            Dict with counts, score, and critical finding count.
        """
        return {
            'customer_name': customer_name,
            'assessment_date': assessment_date,
            'compliance_score': ComplianceScorer.calculate_overall_score(artifacts),
            'endpoints_count': len(artifacts.endpoints),
            'policies_count': len(artifacts.policies),
            'security_events_count': len(artifacts.security_events),
            'ad_objects_count': len(artifacts.ad_objects),
            'critical_findings': sum(
                1 for p in artifacts.policies if p.status == 'Disabled'
            ),
        }

    @staticmethod
    def build_recommendations(artifacts: ArtifactCollection) -> List[Dict[str, str]]:
        """Return a prioritised list of remediation recommendations.

        Args:
            artifacts: Collected compliance data.

        Returns:
            List of dicts with keys: priority, area, recommendation, impact.
        """
        recommendations = []

        disabled_fw = [ep for ep in artifacts.endpoints if ep.firewall_status != 'Enabled']
        if disabled_fw:
            recommendations.append({
                'priority': 'Critical',
                'area': 'Firewall Configuration',
                'recommendation': f'Enable Windows Firewall on {len(disabled_fw)} endpoint(s)',
                'impact': 'High - Reduces network attack surface',
            })

        inactive_av = [ep for ep in artifacts.endpoints if ep.antivirus_status != 'Active']
        if inactive_av:
            recommendations.append({
                'priority': 'Critical',
                'area': 'Antivirus Protection',
                'recommendation': f'Activate antivirus on {len(inactive_av)} endpoint(s)',
                'impact': 'High - Protects against malware threats',
            })

        disabled_policies = [p for p in artifacts.policies if p.status == 'Disabled']
        if disabled_policies:
            recommendations.append({
                'priority': 'High',
                'area': 'Security Policies',
                'recommendation': f'Enable {len(disabled_policies)} security policy(ies)',
                'impact': 'Medium - Improves overall security posture',
            })

        if not recommendations:
            recommendations.append({
                'priority': 'Low',
                'area': 'Maintenance',
                'recommendation': 'Continue regular security updates and patches',
                'impact': 'Medium - Maintains current security posture',
            })

        return recommendations
