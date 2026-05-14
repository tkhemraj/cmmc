"""Windows endpoint security posture collector."""

import logging
from typing import List, Optional
from .base import CollectorBase
from ..models.artifacts import Endpoint

logger = logging.getLogger(__name__)


class EndpointCollector(CollectorBase):
    """Collects Windows endpoint security data (OS, patches, firewall, AV).

    In production this would use WMI/WinRM for local and remote collection.
    Currently returns demo data to exercise the pipeline without a live network.
    """

    def collect(self) -> List[Endpoint]:
        """Return a list of Endpoint objects for all discovered machines."""
        logger.info("Collecting endpoint data...")
        endpoints: List[Endpoint] = []
        try:
            endpoints.append(Endpoint(
                hostname="WORKSTATION-001",
                ip_address="192.168.1.100",
                os_version="Windows 10 Enterprise (Build 19045)",
                installed_updates=["KB5001640", "KB5001631"],
                security_products=["Windows Defender"],
                firewall_status="Enabled",
                antivirus_status="Active",
            ))
            logger.info(f"Endpoint collection complete: {len(endpoints)} machine(s)")
        except Exception as e:
            logger.error(f"Failed to collect endpoint data: {e}")
        return endpoints

    def collect_remote(self, hostname: str) -> Optional[Endpoint]:
        """Collect endpoint data from a remote machine via WinRM.

        Args:
            hostname: Target computer name, must be resolvable on the network.

        Returns:
            Endpoint on success, None if the machine is unreachable or collection fails.
        """
        logger.debug(f"Remote collection stub for {hostname}")
        # TODO: Implement WinRM/RPC collection
        return None
