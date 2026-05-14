"""Command-line interface for CMMC Gatherer."""

import argparse
import json
import logging
import sys
from pathlib import Path
from .gatherer import CMMCGatherer
from .exporters.exporter_factory import ExporterFactory
from .models.artifacts import ArtifactCollection
from .utils import TenantManager, ComplianceScorer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='CMMC Artifact Gathering Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    collect_parser = subparsers.add_parser('collect', help='Collect artifacts')
    collect_parser.add_argument('--output', '-o', default='artifacts.json', help='Output file path')
    collect_parser.add_argument(
        '--format', '-f',
        choices=['json', 'csv', 'xml', 'html', 'msp_report'],
        default='json',
        help='Output format',
    )

    report_parser = subparsers.add_parser('report', help='Generate compliance report')
    report_parser.add_argument('--customer', '-c', required=True, help='Customer/client name')
    report_parser.add_argument(
        '--format', '-f',
        choices=['html', 'json', 'csv'],
        default='html',
        help='Report format',
    )
    report_parser.add_argument('--output', '-o', default='compliance_report.html', help='Output file path')
    report_parser.add_argument('--assessment-id', '-a', help='Assessment ID')

    export_parser = subparsers.add_parser('export', help='Re-export artifacts from a saved JSON file')
    export_parser.add_argument('--input', '-i', required=True, help='Input artifacts JSON file')
    export_parser.add_argument('--formats', default='json,html', help='Comma-separated format list')
    export_parser.add_argument('--output-dir', '-d', default='./reports', help='Output directory')

    args = parser.parse_args()

    if args.command == 'collect':
        return collect_command(args)
    elif args.command == 'report':
        return report_command(args)
    elif args.command == 'export':
        return export_command(args)
    else:
        parser.print_help()
        return 0


def collect_command(args):
    """Execute collect command."""
    try:
        gatherer = CMMCGatherer()
        gatherer.collect_all()
        gatherer.export(args.format, args.output)
        logger.info(f"Artifacts collected and exported to {args.output}")
        return 0
    except Exception as e:
        logger.error(f"Collection failed: {e}")
        return 1


def report_command(args):
    """Execute report command."""
    try:
        gatherer = CMMCGatherer()
        artifacts = gatherer.collect_all()
        exporter = ExporterFactory.create_exporter(args.format or 'msp_report')
        if not exporter:
            logger.error("Invalid export format")
            return 1
        exporter.export(
            artifacts, args.output,
            customer_name=args.customer,
            assessment_id=args.assessment_id,
        )
        logger.info(f"Report generated: {args.output}")
        return 0
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return 1


def export_command(args):
    """Re-export artifacts loaded from a previously saved JSON file."""
    try:
        with open(args.input, 'r') as f:
            data = json.load(f)

        artifacts = ArtifactCollection.from_dict(data)

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        formats = [f.strip() for f in args.formats.split(',')]
        for fmt in formats:
            exporter = ExporterFactory.create_exporter(fmt)
            if not exporter:
                logger.warning(f"Unsupported format: {fmt}")
                continue
            output_path = output_dir / f"artifacts.{fmt}"
            exporter.export(artifacts, str(output_path))

        logger.info(f"Export complete in {output_dir}")
        return 0
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
