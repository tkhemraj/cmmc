"""Factory for creating artifact exporters by format name."""

from typing import Optional
import logging
from .base import ExporterBase, JSONExporter, CSVExporter, XMLExporter
from .html_exporter import HTMLExporter
from .msp_report_exporter import MSPReportExporter

logger = logging.getLogger(__name__)


class ExporterFactory:
    """Creates and registers artifact exporters.

    Usage:
        exporter = ExporterFactory.create_exporter('msp_report')
        exporter.export(artifacts, 'report.html', customer_name='Acme Corp')
    """

    _exporters = {
        'json': JSONExporter,
        'csv': CSVExporter,
        'xml': XMLExporter,
        'html': HTMLExporter,
        'msp_report': MSPReportExporter,
    }

    @classmethod
    def create_exporter(cls, format_type: str) -> Optional[ExporterBase]:
        """Return an exporter instance for format_type, or None if unknown."""
        format_type = format_type.lower().strip()
        if format_type not in cls._exporters:
            logger.error(
                f"Unknown export format: '{format_type}'. "
                f"Valid options: {', '.join(cls._exporters.keys())}"
            )
            return None
        logger.debug(f"Creating {format_type} exporter")
        return cls._exporters[format_type]()

    @classmethod
    def get_supported_formats(cls) -> list:
        """Return a list of all supported format names."""
        return list(cls._exporters.keys())

    @classmethod
    def register_exporter(cls, format_name: str, exporter_class) -> None:
        """Register a custom exporter class under format_name."""
        cls._exporters[format_name.lower()] = exporter_class
        logger.info(f"Registered new exporter: {format_name}")
