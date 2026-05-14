"""MSP-specific compliance report exporter."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from .base import ExporterBase
from ..utils.compliance import ComplianceScorer

logger = logging.getLogger(__name__)


class MSPReportExporter(ExporterBase):
    """Exports a professional HTML compliance report suitable for MSP client presentation."""

    def export(
        self,
        artifacts: Any,
        output_path: str,
        customer_name: Optional[str] = None,
        assessment_id: Optional[str] = None,
        **_,
    ) -> bool:
        try:
            html_content = self._generate_msp_report(artifacts, customer_name, assessment_id)
            with open(output_path, 'w') as f:
                f.write(html_content)
            logger.info(f"Exported MSP report: {output_path}")
            return True
        except Exception as e:
            logger.error(f"MSP report export failed: {e}")
            return False

    def _generate_msp_report(
        self,
        artifacts: Any,
        customer_name: Optional[str],
        assessment_id: Optional[str],
    ) -> str:
        compliance_score = ComplianceScorer.calculate_overall_score(artifacts)
        findings = self._generate_findings(artifacts)

        customer_name = customer_name or "Unnamed Customer"
        assessment_id = assessment_id or "CMMC-" + datetime.now().strftime("%Y%m%d%H%M%S")
        score_class = 'good' if compliance_score >= 80 else ('warning' if compliance_score >= 60 else 'critical')

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>CMMC Compliance Assessment Report</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 1.2em; opacity: 0.9; }}
        .content {{ max-width: 900px; margin: 0 auto; padding: 30px; }}
        .section {{ margin: 30px 0; page-break-inside: avoid; }}
        .section h2 {{ color: #667eea; border-bottom: 3px solid #667eea;
                       padding-bottom: 10px; margin-bottom: 15px; }}
        .score-card {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .score {{ background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center;
                 flex: 1; margin: 0 10px; }}
        .score .number {{ font-size: 3em; font-weight: bold; color: #667eea; }}
        .score .label {{ color: #666; margin-top: 5px; }}
        .score.good {{ background: #e8f5e9; }}
        .score.good .number {{ color: #4caf50; }}
        .score.warning {{ background: #fff3e0; }}
        .score.warning .number {{ color: #ff9800; }}
        .score.critical {{ background: #ffebee; }}
        .score.critical .number {{ color: #f44336; }}
        .finding {{ margin: 15px 0; padding: 15px; border-left: 4px solid #ff9800;
                   background: #fff9c4; border-radius: 4px; }}
        .finding.critical {{ border-left-color: #f44336; background: #ffebee; }}
        .finding.resolved {{ border-left-color: #4caf50; background: #e8f5e9; }}
        .finding h4 {{ margin-bottom: 5px; }}
        .finding p {{ font-size: 0.95em; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background-color: #f5f5f5; padding: 12px; text-align: left;
              border-bottom: 2px solid #ddd; }}
        td {{ padding: 10px; border-bottom: 1px solid #eee; }}
        .recommendation {{ background: #e3f2fd; padding: 15px;
                          border-left: 4px solid #2196F3; margin: 10px 0; }}
        .footer {{ background: #f5f5f5; padding: 20px; text-align: center;
                  margin-top: 40px; border-top: 1px solid #ddd; color: #999; }}
        .summary-table td {{ padding: 8px; }}
        .summary-table td:first-child {{ font-weight: bold; width: 30%; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CMMC Compliance Assessment Report</h1>
        <div class="subtitle">Third-Party Audit Ready</div>
    </div>

    <div class="content">
        <div class="section">
            <h2>Executive Summary</h2>
            <table class="summary-table">
                <tr><td>Customer:</td><td>{customer_name}</td></tr>
                <tr><td>Assessment ID:</td><td>{assessment_id}</td></tr>
                <tr><td>Assessment Date:</td><td>{datetime.now().strftime("%Y-%m-%d")}</td></tr>
                <tr><td>Overall Compliance Score:</td><td>{compliance_score}%</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>Compliance Score</h2>
            <div class="score-card">
                <div class="score {score_class}">
                    <div class="number">{compliance_score}%</div>
                    <div class="label">Overall Compliance</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Infrastructure Overview</h2>
            <table>
                <tr><th>Metric</th><th>Count</th></tr>
                <tr><td>Windows Endpoints</td><td>{len(artifacts.endpoints)}</td></tr>
                <tr><td>Active Directory Objects</td><td>{len(artifacts.ad_objects)}</td></tr>
                <tr><td>Security Policies</td><td>{len(artifacts.policies)}</td></tr>
                <tr><td>Security Events Analyzed</td><td>{len(artifacts.security_events)}</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>Endpoint Status</h2>
            <table>
                <tr>
                    <th>Hostname</th><th>IP Address</th><th>OS Version</th>
                    <th>Firewall</th><th>Antivirus</th>
                </tr>
"""
        for ep in artifacts.endpoints:
            fw_color = 'green' if ep.firewall_status == 'Enabled' else 'red'
            av_color = 'green' if ep.antivirus_status == 'Active' else 'red'
            html += (
                f"                <tr><td>{ep.hostname}</td><td>{ep.ip_address}</td>"
                f"<td>{ep.os_version}</td>"
                f"<td><span style=\"color:{fw_color}\">{ep.firewall_status or 'Unknown'}</span></td>"
                f"<td><span style=\"color:{av_color}\">{ep.antivirus_status or 'Unknown'}</span></td>"
                f"</tr>\n"
            )

        html += """            </table>
        </div>

        <div class="section">
            <h2>Findings &amp; Recommendations</h2>
"""
        for finding in findings:
            finding_class = "finding critical" if finding['severity'] == 'Critical' else "finding"
            if finding['severity'] == 'Resolved':
                finding_class = "finding resolved"
            html += (
                f"            <div class=\"{finding_class}\">\n"
                f"                <h4>{finding['title']}</h4>\n"
                f"                <p><strong>Severity:</strong> {finding['severity']}</p>\n"
                f"                <p><strong>Description:</strong> {finding['description']}</p>\n"
                f"            </div>\n"
                f"            <div class=\"recommendation\">"
                f"<strong>Recommendation:</strong> {finding['recommendation']}</div>\n"
            )

        html += """        </div>

        <div class="section">
            <h2>Policy Compliance</h2>
            <table>
                <tr><th>Policy</th><th>Type</th><th>Status</th><th>Current Value</th></tr>
"""
        for policy in artifacts.policies:
            status_color = 'green' if policy.status == 'Enabled' else 'orange'
            html += (
                f"                <tr><td>{policy.policy_name}</td><td>{policy.policy_type}</td>"
                f"<td><span style=\"color:{status_color}\">{policy.status}</span></td>"
                f"<td>{policy.value or 'N/A'}</td></tr>\n"
            )

        html += f"""            </table>
        </div>

        <div class="section">
            <h2>Assessment Scope</h2>
            <p>This assessment evaluated:</p>
            <ul>
                <li>Windows endpoint security configurations</li>
                <li>Active Directory policy implementations</li>
                <li>Security event logging and monitoring</li>
                <li>Group Policy compliance</li>
                <li>Firewall and antivirus deployment status</li>
            </ul>
        </div>

        <div class="footer">
            <p><strong>Assessment Disclaimer:</strong> This report is generated for compliance
            assessment purposes. Recommendations should be reviewed by qualified security
            professionals before implementation.</p>
            <p>Generated by: CMMC Artifact Gathering Tool v1.0 | Assessment ID: {assessment_id}</p>
        </div>
    </div>
</body>
</html>"""
        return html

    def _generate_findings(self, artifacts: Any) -> List[Dict[str, str]]:
        findings = []

        disabled_firewalls = [
            ep.hostname for ep in artifacts.endpoints if ep.firewall_status != "Enabled"
        ]
        if disabled_firewalls:
            findings.append({
                'title': 'Firewall Not Enabled',
                'severity': 'Critical',
                'description': f'Firewall is disabled on: {", ".join(disabled_firewalls)}',
                'recommendation': 'Enable Windows Firewall on all endpoints immediately',
            })

        inactive_av = [
            ep.hostname for ep in artifacts.endpoints if ep.antivirus_status != "Active"
        ]
        if inactive_av:
            findings.append({
                'title': 'Antivirus Not Active',
                'severity': 'Critical',
                'description': f'Antivirus is inactive on: {", ".join(inactive_av)}',
                'recommendation': 'Deploy and activate antivirus protection on all endpoints',
            })

        disabled_policies = [p.policy_name for p in artifacts.policies if p.status == "Disabled"]
        if disabled_policies:
            findings.append({
                'title': 'Security Policies Disabled',
                'severity': 'High',
                'description': f'The following policies are disabled: {", ".join(disabled_policies)}',
                'recommendation': 'Review and enable critical security policies through Group Policy',
            })

        if not findings:
            findings.append({
                'title': 'Security Baseline Met',
                'severity': 'Resolved',
                'description': 'All monitored security controls are properly configured',
                'recommendation': 'Continue regular compliance monitoring and updates',
            })

        return findings
