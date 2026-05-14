"""Base collector class for all CMMC data collectors."""

from abc import ABC, abstractmethod
from typing import List, Any
import logging

logger = logging.getLogger(__name__)


class CollectorBase(ABC):
    """Abstract base for all CMMC data collectors.

    Subclasses must implement collect(), which returns a list of artifacts.
    Implementations should log errors and return partial data rather than
    raising exceptions, so a single failing collector doesn't abort the run.
    """

    @abstractmethod
    def collect(self) -> List[Any]:
        """Collect and return a list of artifacts from the data source."""
        pass
