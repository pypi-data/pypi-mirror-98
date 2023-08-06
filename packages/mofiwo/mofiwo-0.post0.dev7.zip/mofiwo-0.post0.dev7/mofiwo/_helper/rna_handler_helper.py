""" This module contains helper functions for rna_handler"""

from mofiwo import log

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def generate_3utr_location(
    cds_seq_obj, 
    cdna_seq_obj
) -> bool:
    """Check 3 UTR location. If it less than 0, it returns False

    Args:
        cds_seq_obj: Coding sequence of SeqRecord object
        cdna_seq_obj: Whole sequence of SeqRecord object

    Returns:
        bool: True if it locates a valid position
    """
    ret_seq = None
    location_idx = cdna_seq_obj.seq.find(cds_seq_obj.seq)

    if location_idx <= 0:
        log.warning(f'Can not find coding sequence(CDS) position in {cds_seq_obj.id}')
    
    else:
        utr3_seq = cdna_seq_obj.seq[location_idx + len(cds_seq_obj.seq):]
        if len(utr3_seq) <= 0:
            log.warning(f'3UTR sequence is not exist in CDNA ({cdna_seq_obj.id})')
        else:
            ret_seq = SeqRecord(
                utr3_seq,
                id=cdna_seq_obj.id,
                name= cdna_seq_obj.id,
                description= '3UTR region'
            )
    
    return ret_seq
