"""Base exporter and standard format exporters (JSON, CSV, XML)."""

import json
import csv
import logging
from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class ExporterBase(ABC):
    """Abstract base class for all artifact exporters."""

    @abstractmethod
    def export(self, artifacts: Any, output_path: str, **kwargs) -> bool:
        """Write artifacts to output_path. Returns True on success."""
        pass


class JSONExporter(ExporterBase):
    """Exports artifacts as pretty-printed JSON."""

    def export(self, artifacts: Any, output_path: str, **_) -> bool:
        try:
            with open(output_path, 'w') as f:
                json.dump(artifacts.to_dict(), f, indent=2, default=str)
            logger.info(f"Exported to JSON: {output_path}")
            return True
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return False


class CSVExporter(ExporterBase):
    """Exports artifacts as a multi-section CSV (endpoints, policies, AD objects)."""

    def export(self, artifacts: Any, output_path: str, **_) -> bool:
        try:
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)

                writer.writerow(['=== ENDPOINTS ==='])
                writer.writerow(['Hostname', 'IP Address', 'OS', 'Firewall', 'Antivirus'])
                for ep in artifacts.endpoints:
                    writer.writerow([
                        ep.hostname, ep.ip_address, ep.os_version,
                        ep.firewall_status or 'Unknown',
                        ep.antivirus_status or 'Unknown',
                    ])

                writer.writerow([])

                writer.writerow(['=== POLICIES ==='])
                writer.writerow(['Policy Name', 'Type', 'Status', 'Value'])
                for policy in artifacts.policies:
                    writer.writerow([
                        policy.policy_name, policy.policy_type,
                        policy.status, policy.value or 'N/A',
                    ])

                writer.writerow([])

                writer.writerow(['=== ACTIVE DIRECTORY ==='])
                writer.writerow(['Distinguished Name', 'Object Class', 'Last Modified'])
                for ad_obj in artifacts.ad_objects:
                    writer.writerow([
                        ad_obj.distinguished_name,
                        ad_obj.object_class,
                        ad_obj.last_modified,
                    ])

            logger.info(f"Exported to CSV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return False


class XMLExporter(ExporterBase):
    """Exports artifacts as structured XML."""

    def export(self, artifacts: Any, output_path: str, **_) -> bool:
        try:
            root = ET.Element('CMMCArtifacts')
            root.set('timestamp', datetime.now().isoformat())
            root.set('version', '1.0')

            endpoints_elem = ET.SubElement(root, 'Endpoints')
            endpoints_elem.set('count', str(len(artifacts.endpoints)))
            for ep in artifacts.endpoints:
                ep_elem = ET.SubElement(endpoints_elem, 'Endpoint')
                ET.SubElement(ep_elem, 'Hostname').text = ep.hostname
                ET.SubElement(ep_elem, 'IPAddress').text = ep.ip_address
                ET.SubElement(ep_elem, 'OSVersion').text = ep.os_version
                ET.SubElement(ep_elem, 'FirewallStatus').text = ep.firewall_status or 'Unknown'
                ET.SubElement(ep_elem, 'AntivirusStatus').text = ep.antivirus_status or 'Unknown'
                ET.SubElement(ep_elem, 'UpdateCount').text = str(len(ep.installed_updates))

            policies_elem = ET.SubElement(root, 'Policies')
            policies_elem.set('count', str(len(artifacts.policies)))
            for policy in artifacts.policies:
                policy_elem = ET.SubElement(policies_elem, 'Policy')
                ET.SubElement(policy_elem, 'Name').text = policy.policy_name
                ET.SubElement(policy_elem, 'Type').text = policy.policy_type
                ET.SubElement(policy_elem, 'Status').text = policy.status
                ET.SubElement(policy_elem, 'Value').text = policy.value or 'Not Set'

            ad_elem = ET.SubElement(root, 'ADObjects')
            ad_elem.set('count', str(len(artifacts.ad_objects)))
            for ad_obj in artifacts.ad_objects:
                obj_elem = ET.SubElement(ad_elem, 'Object')
                ET.SubElement(obj_elem, 'DistinguishedName').text = ad_obj.distinguished_name
                ET.SubElement(obj_elem, 'Class').text = ad_obj.object_class
                ET.SubElement(obj_elem, 'LastModified').text = ad_obj.last_modified

            ET.ElementTree(root).write(output_path, encoding='utf-8', xml_declaration=True)
            logger.info(f"Exported to XML: {output_path}")
            return True
        except Exception as e:
            logger.error(f"XML export failed: {e}")
            return False
