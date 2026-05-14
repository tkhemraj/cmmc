# CMMC Artifact Gathering Tool

> **Built for MSPs. Ready for auditors.**
> Collect Windows compliance artifacts from every endpoint, score your security posture, and deliver a professional client report — without touching a spreadsheet.

---

## Why This Exists

When a DoD contractor asks their MSP "are we compliant?", the answer usually involves someone manually logging into machines, running PowerShell commands, copying output into a Word doc, and hoping nothing was missed.

This tool automates that entire evidence-gathering process. Point it at a Windows environment and it pulls endpoint security posture, Active Directory configuration, security event logs, and Group Policy — then scores everything and produces a client-ready report your customer can actually hand to an auditor.

---

## What It Does

| Feature | Details |
|---|---|
| **Endpoint Collection** | OS version, patch level, installed KB numbers, Windows Defender status, firewall state, security products |
| **Active Directory** | Users, groups, computers, group memberships, stale objects, privileged account inventory |
| **Event Log Collection** | Windows Security Event Log — logon events, account changes, privilege use, policy changes |
| **Policy Collection** | Group Policy Objects, local security policies, account lockout, password policy, UAC |
| **Compliance Scoring** | Weighted 0–100 score across firewall, AV, patching, policies, event logging, and AD security |
| **MSP Report** | Professional HTML report with executive summary, findings, color-coded status, and recommendations |
| **Multi-Tenant** | Manage assessments for multiple customers in one session, score them all at once |
| **Data Filtering** | Strip PII and sensitive fields before sharing data with third parties or auditors |
| **5 Export Formats** | JSON, CSV, XML, HTML, and the MSP-grade compliance report |

---

## The Output

```python
from cmmc_gatherer import CMMCGatherer

gatherer = CMMCGatherer()
gatherer.collect_all()
gatherer.export('msp_report', 'acme_corp_report.html',
                customer_name='Acme Corp',
                assessment_id='CMMC-2026-001')
```

That produces a professional HTML report with:

- **Executive summary** — compliance score, assessment date, customer info
- **Infrastructure overview** — endpoint count, AD objects, policies assessed, events analyzed
- **Endpoint status table** — firewall and AV status per machine, color-coded
- **Findings & recommendations** — every gap flagged with a specific remediation step
- **Policy compliance matrix** — every policy evaluated, enabled/disabled status highlighted
- **Audit-ready metadata** — assessment ID, date, scope, and disclaimer

---

## Time Savings

| Task | Manual Approach | This Tool |
|---|---|---|
| Inventory endpoints + security status | 30–60 min per site | Seconds |
| Pull AD user and group data | 1–2 hours | Seconds |
| Review event logs for red flags | Half a day | Seconds |
| Check Group Policy compliance | 1–2 hours | Seconds |
| Write up findings in a report | 2–4 hours | Auto-generated |
| **Total per client assessment** | **~1–2 days** | **Under a minute** |

For an MSP with 10 clients on quarterly review cycles, that's weeks of billable time you're either recovering or reinvesting.

---

## Installation

```bash
git clone https://github.com/tkhemraj/cmmc.git
cd cmmc
pip install -e .
```

Requires Python 3.8+. No external dependencies beyond the standard library.

---

## Usage

### Basic — collect everything and export
```bash
cmmc-gatherer collect --format msp_report --output report.html
```

### Generate a named client report
```bash
cmmc-gatherer report --customer "Acme Corp" --format html \
  --assessment-id CMMC-2026-001 --output acme_report.html
```

### Re-export saved artifacts in any format
```bash
cmmc-gatherer export --input artifacts.json \
  --formats json,csv,html --output-dir ./reports/
```

### From Python — full control
```python
from cmmc_gatherer import CMMCGatherer
from cmmc_gatherer.utils import ComplianceScorer, DataFilter

gatherer = CMMCGatherer()
artifacts = gatherer.collect_all()

# Score the environment
score = ComplianceScorer.calculate_overall_score(artifacts)
print(f"Compliance score: {score}/100")

# Strip PII before sharing with a third party
clean = DataFilter.filter_for_third_party(artifacts, exclude_user_data=True)

# Export all formats at once
gatherer.export_multiple(['json', 'csv', 'html'], './reports/')
```

### Multi-tenant — score all your clients at once
```python
from cmmc_gatherer.utils import TenantManager

manager = TenantManager()

for customer in ['acme', 'globex', 'initech']:
    gatherer = CMMCGatherer()
    artifacts = gatherer.collect_all()
    manager.add_tenant(customer, artifacts)

# Compliance scores for every client in one call
scores = manager.calculate_tenant_scores()
# {'acme': 87, 'globex': 74, 'initech': 91}
```

---

## Architecture

### Collectors
Each collector handles one data source and returns typed artifacts:

| Collector | Data Source | What It Captures |
|---|---|---|
| `EndpointCollector` | WMI / Windows Security Center | OS, patches, Defender, firewall |
| `ActiveDirectoryCollector` | LDAP / Domain Controller | Users, groups, computers, memberships |
| `EventLogCollector` | Windows Security Event Log | Logon events, account changes, privilege use |
| `PolicyCollector` | Group Policy / Registry | GPOs, local policies, security settings |

### Exporters
| Format | Use Case |
|---|---|
| `json` | SIEM ingestion, database storage, programmatic analysis |
| `csv` | Excel pivot tables, filtering, stakeholder sharing |
| `xml` | Enterprise tool integration, structured data |
| `html` | Internal compliance reporting |
| `msp_report` | Client-facing professional compliance report |

### Utilities
- **`ComplianceScorer`** — weighted scoring across 6 security dimensions
- **`DataFilter`** — PII redaction and sensitivity filtering for third-party sharing
- **`TenantManager`** — multi-client artifact storage and batch scoring
- **`ReportBuilder`** — executive summary and recommendation generation

---

## Compliance Coverage

This tool gathers evidence relevant to Windows-based controls across:

- **Access Control (AC)** — account restrictions, session policies, remote access
- **Identification & Authentication (IA)** — account inventory, auth configuration
- **System & Info Integrity (SI)** — AV, patching, update status
- **Audit & Accountability (AU)** — event logging, log configuration
- **Configuration Management (CM)** — policy baselines, Group Policy
- **System & Communications (SC)** — firewall, network security posture

---

## Looking for Full CMMC 2.0 Assessment?

This tool handles artifact collection and scoring for Windows environments. If you need a complete **CMMC 2.0 compliance assessment** — covering all 110 NIST SP 800-171 practices, SPRS score calculation, and POAM generation — check out the companion tool:

**[cmmc2 — CMMC 2.0 Full Assessment Tool](https://github.com/tkhemraj/cmmc2)**

---

## Need Help Implementing This For Your Clients?

The tool automates the collection. The compliance work — remediation, documentation, audit prep — is where most organizations get stuck.

**Tarique Khemraj** is an MSP compliance specialist helping defense contractors navigate CMMC from initial posture assessment through certification.

**What I can help with:**
- Deploying this tool against your actual client environments
- Interpreting results and prioritizing remediation
- Building out the documentation your auditors need (SSP, POAM, policies)
- Managing CMMC compliance programs across your entire client base
- Preparing for C3PAO third-party assessment

📧 **t.khemraj@gmail.com**
🐙 **github.com/tkhemraj**

> If you're an MSP with DoD contractor clients and need someone who's already built the tooling and knows the framework — let's talk.

---

## License

MIT — use it, fork it, build on it.

---

*Windows endpoint compliance artifact collection. Built for MSPs managing DoD contractors.*
