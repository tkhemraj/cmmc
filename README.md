# CMMC Artifact Gathering Tool

A comprehensive Python tool for collecting CMMC compliance artifacts from Windows environments. Designed for MSPs and enterprises to gather, analyze, and present compliance data to third parties.

## Features

- **Multi-Source Data Collection**
  - Windows endpoint data (OS, security status, updates)
  - Active Directory objects and configurations
  - Windows Security Event Logs
  - Group Policy and security policy configurations

- **MSP-Specific Capabilities**
  - Multi-tenant support for managing multiple customers
  - Professional compliance reporting for third-party presentation
  - Executive summary generation
  - Automated compliance scoring
  - Findings and recommendations

- **Multiple Export Formats**
  - JSON for data interchange
  - CSV for spreadsheet analysis
  - XML for enterprise integration
  - HTML for professional reports
  - MSP Report format with compliance findings

- **Compliance Analysis**
  - Automatic compliance scoring (0-100)
  - Security posture assessment
  - Policy compliance evaluation
  - Recommendation generation

## Installation

### Prerequisites
- Python 3.8+
- Windows 10/11 or Windows Server 2016+
- Administrator privileges (for some data collectors)

### Install from source
```bash
git clone https://github.com/yourusername/cmmc-gatherer.git
cd cmmc-gatherer
pip install -r requirements.txt
pip install -e .
```

## Quick Start

### Basic Usage
```python
from cmmc_gatherer import CMMCGatherer

# Initialize gatherer
gatherer = CMMCGatherer()

# Collect all artifacts
artifacts = gatherer.collect_all()

# Export as MSP report
gatherer.export('msp_report', 'compliance_report.html')
```

### Multi-Tenant Reporting
```python
from cmmc_gatherer.utils import TenantManager, ComplianceScorer
from cmmc_gatherer.exporters.exporter_factory import ExporterFactory

# Manage multiple customers
tenant_manager = TenantManager()

# Collect for each tenant
for customer_id in ['customer_a', 'customer_b']:
    gatherer = CMMCGatherer()
    artifacts = gatherer.collect_all()
    tenant_manager.add_tenant(customer_id, artifacts)

# Generate scores for all tenants
scores = tenant_manager.calculate_tenant_scores()
print(f"Compliance Scores: {scores}")

# Export MSP report
exporter = ExporterFactory.create_exporter('msp_report')
tenant_artifacts = tenant_manager.get_tenant('customer_a')
exporter.export(tenant_artifacts, 'customer_a_report.html', 
                customer_name='Customer A', assessment_id='CMMC-20260514')
```

### Data Filtering for Third Parties
```python
from cmmc_gatherer.utils import DataFilter

# Filter sensitive data for third-party sharing
filtered = DataFilter.filter_for_third_party(artifacts, 
                                             exclude_user_data=True,
                                             exclude_sensitive=True)

# Export filtered data
gatherer.artifacts = filtered
gatherer.export('json', 'filtered_report.json')
```

## Architecture

### Collectors
- **EndpointCollector**: Gathers Windows endpoint data (OS, security products, updates)
- **ActiveDirectoryCollector**: Retrieves AD objects and configurations
- **EventLogCollector**: Collects Windows Security Event Logs
- **PolicyCollector**: Gathers Group Policy and security policy configurations

### Exporters
- **JSONExporter**: Exports to JSON format
- **CSVExporter**: Exports to CSV format
- **XMLExporter**: Exports to XML format
- **HTMLExporter**: Exports to formatted HTML
- **MSPReportExporter**: Professional MSP compliance report

### Utilities
- **ComplianceScorer**: Calculates compliance scores based on collected data
- **DataFilter**: Filters and sanitizes data for different audiences
- **TenantManager**: Manages multi-tenant data collection and reporting
- **ReportBuilder**: Builds executive summaries and recommendations

## Configuration

Create a `config.yaml` file to customize behavior:

```yaml
# Windows endpoint collection settings
endpoints:
  collect_updates: true
  collect_security_products: true

# Active Directory settings
ad:
  domain: contoso.com
  include_disabled_objects: false

# Event Log settings
event_logs:
  days_back: 30
  log_sources:
    - Security
    - System

# Report settings
reporting:
  include_recommendations: true
  compliance_threshold: 80
```

## Command-Line Usage

```bash
# Collect artifacts
cmmc-gatherer collect --output report.json

# Generate MSP report
cmmc-gatherer report --customer "Acme Corp" --format msp_report --output acme_report.html

# Export to multiple formats
cmmc-gatherer export --input artifacts.json --formats json,csv,xml,html --output-dir ./reports/

# Multi-tenant reporting
cmmc-gatherer multi-tenant --config tenants.yaml --output-dir ./reports/
```

## Compliance Standards

This tool assists with CMMC (Cybersecurity Maturity Model Certification) assessments by collecting relevant artifacts from Windows environments related to:

- Access Control (AC)
- Identification and Authentication (IA)
- System and Communications Protection (SC)
- System and Information Integrity (SI)
- Security Assessment and Authorization (CA)

## Output Examples

### MSP Report Includes:
- Executive Summary with compliance score
- Infrastructure overview
- Endpoint security status
- Policy compliance matrix
- Security findings and recommendations
- Assessment metadata

### HTML Report Features:
- Professional styling for client presentations
- Color-coded status indicators
- Severity-based finding organization
- Compliance scoring visualization
- Recommendations with implementation guidance

## Limitations

- Windows-specific data collection (uses WMI, Registry, WinRM)
- Requires appropriate Windows account permissions
- Event log collection may be time-consuming on large deployments
- AD collection requires domain connectivity

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with tests

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Authors

- CMMC Team

## Changelog

### v1.0.0 (2026-05-14)
- Initial release
- Core collectors for Windows endpoints, AD, event logs, and policies
- Multiple export formats including MSP report
- Multi-tenant support
- Compliance scoring
- Data filtering for third-party sharing
