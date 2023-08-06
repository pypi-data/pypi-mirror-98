""".. Ignore pydocstyle D400.

================================
Knowledge Base App Configuration
================================

"""
from django.apps import AppConfig


class KnowledgeBaseConfig(AppConfig):
    """App configuration."""

    name = "resolwe_bio.kb"
    label = "resolwe_bio_kb"
    verbose_name = "Resolwe Bioinformatics Knowledge Base"

    def ready(self):
        """Perform application initialization."""
        from resolwe_bio.kb.listener_plugin import (  # noqa: F401
            ExposeFeature,
            ExposeMapping,
        )
