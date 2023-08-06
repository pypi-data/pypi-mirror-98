"""Resolwe Bioinformatics configuration."""
from django.apps import AppConfig


class BaseConfig(AppConfig):
    """App configuration."""

    name = "resolwe_bio"
    verbose_name = "Resolwe Bioinformatics"

    def ready(self):
        """Application initialization."""
        # Register custom python process.
        from resolwe_bio.process.runtime import ProcessBio  # noqa: F401
