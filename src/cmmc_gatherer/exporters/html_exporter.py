"""HTML report exporter."""

import logging
from datetime import datetime
from typing import Any
from .base import ExporterBase

logger = logging.getLogger(__name__)


class HTMLExporter(ExporterBase):
    """Exports artifacts as a basic styled HTML report."""

    def export(self, artifacts: Any, output_path: str, **_) -> bool:
        try:
            with open(output_path, 'w') as f:
                f.write(self._generate_html(artifacts))
            logger.info(f"Exported to HTML: {output_path}")
            return True
        except Exception as e:
            logger.error(f"HTML export failed: {e}")
            return False

    def _generate_html(self, artifacts) -> str:
        html = """<!DOCTYPE html>
<html>
<head>
    <title>CMMC Artifact Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th { background-color: #4CAF50; color: white; padding: 10px; text-align: left; }
        td { border: 1px solid #ddd; padding: 8px; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .timestamp { color: #999; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>CMMC Artifact Report</h1>
    <p class="timestamp">Generated: """ + datetime.now().isoformat() + """</p>

    <h2>Endpoints</h2>
    <table>
        <tr>
            <th>Hostname</th><th>IP Address</th><th>OS Version</th>
            <th>Firewall</th><th>Antivirus</th>
        </tr>
"""
        for ep in artifacts.endpoints:
            html += (
                f"        <tr><td>{ep.hostname}</td><td>{ep.ip_address}</td>"
                f"<td>{ep.os_version}</td><td>{ep.firewall_status or 'N/A'}</td>"
                f"<td>{ep.antivirus_status or 'N/A'}</td></tr>\n"
            )

        html += """    </table>

    <h2>Policies</h2>
    <table>
        <tr>
            <th>Policy Name</th><th>Type</th><th>Status</th><th>Value</th>
        </tr>
"""
        for policy in artifacts.policies:
            html += (
                f"        <tr><td>{policy.policy_name}</td><td>{policy.policy_type}</td>"
                f"<td>{policy.status}</td><td>{policy.value or 'N/A'}</td></tr>\n"
            )

        html += "    </table>\n</body>\n</html>"
        return html
