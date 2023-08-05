from resolwe.flow.models import Data
from resolwe.test import tag_process

from resolwe_bio.utils.test import BioProcessTestCase


class AtacSeqWorkflowTestCase(BioProcessTestCase):
    @tag_process("workflow-atac-seq")
    def test_atac_seq_workflow(self):
        with self.preparation_stage():
            inputs = {
                "src": "mm10_chr17_44M-45M.fa.gz",
                "species": "Mus musculus",
                "build": "mm10",
            }
            ref_seq = self.run_process("upload-fasta-nucl", inputs)
            bowtie2_index = self.run_process("bowtie2-index", {"ref_seq": ref_seq.id})
            reads = self.prepare_paired_reads(
                mate1=["atac_R1.fastq.gz"], mate2=["atac_R2.fastq.gz"]
            )
            inputs = {
                "src": "promoters_mm10_chr17_subregion.bed",
                "species": "Mus musculus",
                "build": "mm10",
            }
            promoters = self.run_process("upload-bed", inputs)

        self.run_process(
            "workflow-atac-seq",
            {
                "reads": reads.id,
                "genome": bowtie2_index.id,
                "promoter": promoters.id,
                "settings": {"bedgraph": False},
            },
        )
        for data in Data.objects.all():
            self.assertStatus(data, Data.STATUS_DONE)
        macs2 = Data.objects.last()
        self.assertFile(macs2, "chip_qc", "atac_seq_report.txt")
        self.assertFile(macs2, "case_prepeak_qc", "atac_seq_prepeak_report.txt")
