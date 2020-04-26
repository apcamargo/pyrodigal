from libc.stdio cimport FILE

from pyrodigal.prodigal.bitmap cimport bitmap_t
from pyrodigal.prodigal.node cimport _node
from pyrodigal.prodigal.training cimport _training


cdef extern from "gene.h":

    cdef size_t MAX_GENES = 30000

    cdef struct _gene:
        int begin
        int end
        int start_ndx
        int end_ndx
        char gene_data[500]
        char score_data[500]

    cdef int add_genes(_gene*, _node*, int)
    cdef void record_gene_data(_gene*, int, _node*, _training*, int)
    void tweak_final_starts(_gene*, int, _node*, int, _training*);

    cdef void write_translations(FILE *fh, _gene* genes, int ng, _node* nod, bitmap_t seq, bitmap_t rseq, bitmap_t useq, int slen, _training* tinf, int sctr, char* short_hdr)
    cdef void print_genes(FILE*, _gene*, int, _node*, int, int, int, int, char*, _training*, char*, char*, char*);
