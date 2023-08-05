"""Samtools idxstats."""
from resolwe.process import Cmd, DataField, FileField, Process, SchedulingClass


class SamtoolsIdxstats(Process):
    """Retrieve and print stats in the index file."""

    slug = "samtools-idxstats"
    name = "Samtools idxstats"
    requirements = {
        "expression-engine": "jinja",
        "executor": {
            "docker": {
                "image": "public.ecr.aws/s4q6j6e8/resolwebio/common:2.3.1",
            },
        },
        "resources": {
            "cores": 1,
            "memory": 4096,
        },
    }
    data_name = "Samtools idxstats ({{alignment|sample_name}})"
    version = "1.2.1"
    process_type = "data:samtools:idxstats"
    category = "Other"
    entity = {
        "type": "sample",
        "input": "alignment",
    }
    scheduling_class = SchedulingClass.BATCH

    class Input:
        """Input fields."""

        alignment = DataField("alignment:bam", label="Alignment")

    class Output:
        """Output fields."""

        report = FileField(label="Samtools idxstats report")

    def run(self, inputs, outputs):
        """Run the analysis."""
        (
            Cmd["samtools"]["idxstats", inputs.alignment.output.bam.path]
            > "idxstat_report.txt"
        )()

        outputs.report = "idxstat_report.txt"
