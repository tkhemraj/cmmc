"""
Test suite for CMMC Gatherer
"""

import unittest
from cmmc_gatherer.models.artifacts import (
    Endpoint, ADObject, SecurityEvent, Policy, ArtifactCollection
)
from cmmc_gatherer.utils import ComplianceScorer, DataFilter, TenantManager, ReportBuilder


class TestArtifactModels(unittest.TestCase):
    """Test artifact data models."""

    def test_endpoint_creation(self):
        """Test creating an endpoint artifact."""
        ep = Endpoint(
            hostname="TEST-PC",
            ip_address="192.168.1.1",
            os_version="Windows 10",
            firewall_status="Enabled"
        )
        self.assertEqual(ep.hostname, "TEST-PC")
        self.assertEqual(ep.firewall_status, "Enabled")

    def test_endpoint_to_dict(self):
        """Test endpoint serialization."""
        ep = Endpoint(
            hostname="TEST-PC",
            ip_address="192.168.1.1",
            os_version="Windows 10"
        )
        data = ep.to_dict()
        self.assertIn('hostname', data)
        self.assertEqual(data['hostname'], "TEST-PC")

    def test_artifact_collection(self):
        """Test artifact collection."""
        collection = ArtifactCollection()
        ep = Endpoint(
            hostname="TEST-PC",
            ip_address="192.168.1.1",
            os_version="Windows 10"
        )
        collection.endpoints.append(ep)
        
        self.assertEqual(len(collection.endpoints), 1)
        self.assertIsNotNone(collection.collection_timestamp)


class TestComplianceScoring(unittest.TestCase):
    """Test compliance scoring."""

    def test_firewall_scoring(self):
        """Test firewall scoring."""
        collection = ArtifactCollection()
        collection.endpoints = [
            Endpoint("PC1", "192.168.1.1", "Win10", firewall_status="Enabled"),
            Endpoint("PC2", "192.168.1.2", "Win10", firewall_status="Disabled"),
        ]
        
        score = ComplianceScorer._score_firewall(collection)
        self.assertEqual(score, 50)

    def test_antivirus_scoring(self):
        """Test antivirus scoring."""
        collection = ArtifactCollection()
        collection.endpoints = [
            Endpoint("PC1", "192.168.1.1", "Win10", antivirus_status="Active"),
            Endpoint("PC2", "192.168.1.2", "Win10", antivirus_status="Inactive"),
        ]
        
        score = ComplianceScorer._score_antivirus(collection)
        self.assertEqual(score, 50)

    def test_overall_scoring(self):
        """Test overall compliance score."""
        collection = ArtifactCollection()
        collection.endpoints = [
            Endpoint(
                "PC1", "192.168.1.1", "Win10",
                firewall_status="Enabled",
                antivirus_status="Active",
                installed_updates=["KB5001"]
            )
        ]
        collection.policies = [
            Policy("Test Policy", "Group Policy", "Enabled", "Computer")
        ]
        
        score = ComplianceScorer.calculate_overall_score(collection)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)


class TestDataFilter(unittest.TestCase):
    """Test data filtering."""

    def test_third_party_filtering(self):
        """Test filtering for third-party sharing."""
        collection = ArtifactCollection()
        event = SecurityEvent(
            event_id=4624,
            source="Security",
            timestamp="2026-05-14T10:00:00Z",
            message="Login event",
            level="Information",
            computer="TEST-PC",
            user="DOMAIN\\user"
        )
        collection.security_events.append(event)
        
        filtered = DataFilter.filter_for_third_party(collection, exclude_user_data=True)
        self.assertEqual(filtered.security_events[0].user, "REDACTED")

    def test_severity_filtering(self):
        """Test severity filtering."""
        collection = ArtifactCollection()
        collection.security_events = [
            SecurityEvent(4624, "Security", "2026-05-14T10:00:00Z",
                         "Event 1", "Information", "PC1"),
            SecurityEvent(4625, "Security", "2026-05-14T10:01:00Z",
                         "Event 2", "Critical", "PC1"),
        ]
        
        critical = DataFilter.filter_by_severity(collection, 'Critical')
        self.assertEqual(len(critical), 1)


class TestTenantManager(unittest.TestCase):
    """Test multi-tenant support."""

    def test_add_tenant(self):
        """Test adding tenant."""
        manager = TenantManager()
        collection = ArtifactCollection()
        
        result = manager.add_tenant("customer1", collection)
        self.assertTrue(result)
        self.assertIn("customer1", manager.tenants)

    def test_get_tenant(self):
        """Test retrieving tenant data."""
        manager = TenantManager()
        collection = ArtifactCollection()
        collection.endpoints.append(
            Endpoint("PC1", "192.168.1.1", "Win10")
        )
        
        manager.add_tenant("customer1", collection)
        retrieved = manager.get_tenant("customer1")
        
        self.assertEqual(len(retrieved.endpoints), 1)


class TestReportBuilder(unittest.TestCase):
    """Test report building."""

    def test_executive_summary(self):
        """Test building executive summary."""
        collection = ArtifactCollection()
        collection.endpoints = [
            Endpoint("PC1", "192.168.1.1", "Win10")
        ]
        collection.policies = [
            Policy("Policy1", "Group Policy", "Enabled", "Computer")
        ]
        
        summary = ReportBuilder.build_executive_summary(
            collection, "Test Customer", "2026-05-14"
        )
        
        self.assertEqual(summary['customer_name'], "Test Customer")
        self.assertEqual(summary['endpoints_count'], 1)

    def test_recommendations(self):
        """Test building recommendations."""
        collection = ArtifactCollection()
        collection.endpoints = [
            Endpoint("PC1", "192.168.1.1", "Win10",
                    firewall_status="Disabled")
        ]
        
        recommendations = ReportBuilder.build_recommendations(collection)
        self.assertGreater(len(recommendations), 0)


if __name__ == '__main__':
    unittest.main()
