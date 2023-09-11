import array
import threading
import typing
from typing import (
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Dict,
    Optional,
    TextIO,
    Tuple,
    Union,
)

# --- Globals ----------------------------------------------------------------

_TARGET_CPU: str
_AVX2_RUNTIME_SUPPORT: bool
_NEON_RUNTIME_SUPPORT: bool
_SSE2_RUNTIME_SUPPORT: bool
_MMX_RUNTIME_SUPPORT: bool
_AVX2_BUILD_SUPPORT: bool
_NEON_BUILD_SUPPORT: bool
_SSE2_BUILD_SUPPORT: bool
_MMX_BUILD_SUPPORT: bool

TRANSLATION_TABLES: FrozenSet[int]
METAGENOMIC_BINS: MetagenomicBins
MIN_SINGLE_GENOME: int
IDEAL_SINGLE_GENOME: int
PRODIGAL_VERSION: str

# --- Sequence mask ----------------------------------------------------------

class Mask:
    def __init__(self, begin: int, end: int) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def begin(self) -> int: ...
    @property
    def end(self) -> int: ...
    def intersects(self, begin: int, end: int) -> bool: ...

class Masks(typing.Sequence[Mask]):
    def __init__(self) -> None: ...
    def __sizeof__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Mask: ...  # type: ignore
    def __iter__(self) -> Iterator[Mask]: ...
    def __reversed__(self) -> Iterator[Mask]: ...
    def __getstate__(self) -> List[Tuple[int, int]]: ...
    def __setstate__(self, state: List[Tuple[int, int]]) -> None: ...
    def clear(self) -> None: ...
    def copy(self) -> Masks: ...

# --- Input sequence ---------------------------------------------------------

class Sequence(typing.Sized):
    gc: float
    masks: Masks
    def __init__(
        self,
        sequence: Union[str, bytes, bytearray, Sequence],
        mask: bool = False
    ) -> None: ...
    def __len__(self) -> int: ...
    def __sizeof__(self) -> int: ...
    def __str__(self) -> str: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
    def max_gc_frame_plot(self, window_size: int = 120) -> array.array[int]: ...
    def shine_dalgarno(
        self,
        pos: int,
        start: int,
        training_info: TrainingInfo,
        strand: int = 1,
        exact: bool = True,
    ) -> int: ...

# --- Connection Scorer ------------------------------------------------------

class ConnectionScorer:
    def __init__(self, backend: str = "detect") -> None: ...
    def index(self, nodes: Nodes) -> None: ...
    def compute_skippable(self, min: int, i: int) -> None: ...
    def score_connections(
        self, nodes: Nodes, min: int, i: int, tinf: TrainingInfo, final: bool = False
    ) -> None: ...

# --- Nodes ------------------------------------------------------------------

class Node:
    owner: Nodes
    def __repr__(self) -> str: ...
    @property
    def index(self) -> int: ...
    @property
    def strand(self) -> int: ...
    @property
    def type(self) -> str: ...
    @property
    def edge(self) -> bool: ...
    @property
    def gc_bias(self) -> int: ...
    @property
    def cscore(self) -> float: ...
    @property
    def gc_cont(self) -> float: ...
    @property
    def score(self) -> float: ...
    @property
    def rscore(self) -> float: ...
    @property
    def sscore(self) -> float: ...
    @property
    def tscore(self) -> float: ...

class Nodes(typing.Sequence[Node]):
    def __init__(self) -> None: ...
    def __copy__(self) -> Nodes: ...
    def __sizeof__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Node: ...  # type: ignore
    def __iter__(self) -> Iterator[Node]: ...
    def __reversed__(self) -> Iterator[Node]: ...
    def __getstate__(self) -> List[Dict[str, object]]: ...
    def __setstate__(self, state: List[Dict[str, object]]) -> None: ...
    def copy(self) -> Nodes: ...
    def clear(self) -> None: ...
    def extract(
        self,
        sequence: Sequence,
        *,
        closed: bool = False,
        min_gene: int = 90,
        min_edge_gene: int = 60,
        translation_table: int = 11,
    ) -> int: ...
    def reset_scores(self) -> None: ...
    def score(
        self,
        sequence: Sequence,
        training_info: TrainingInfo,
        *,
        closed: bool = False,
        is_meta: bool = False,
    ) -> None: ...
    def sort(self) -> None: ...

# --- Genes ------------------------------------------------------------------

class Gene:
    def __repr__(self) -> str: ...
    @property
    def begin(self) -> int: ...
    @property
    def end(self) -> int: ...
    @property
    def start_node(self) -> None: ...
    @property
    def stop_node(self) -> None: ...
    @property
    def _gene_data(self) -> str: ...
    @property
    def _score_data(self) -> str: ...
    @property
    def strand(self) -> int: ...
    @property
    def partial_begin(self) -> bool: ...
    @property
    def partial_end(self) -> bool: ...
    @property
    def start_type(self) -> str: ...
    @property
    def rbs_motif(self) -> Optional[str]: ...
    @property
    def rbs_spacer(self) -> Optional[str]: ...
    @property
    def gc_cont(self) -> float: ...
    @property
    def translation_table(self) -> int: ...
    @property
    def cscore(self) -> float: ...
    @property
    def rscore(self) -> float: ...
    @property
    def sscore(self) -> float: ...
    @property
    def tscore(self) -> float: ...
    @property
    def uscore(self) -> float: ...
    @property
    def score(self) -> float: ...
    def confidence(self) -> float: ...
    def sequence(self) -> str: ...
    def translate(
        self, translation_table: Optional[int] = None, unknown_residue: str = "X"
    ) -> str: ...

class Genes(typing.Sequence[Gene]):
    _num_seq: int
    @property
    def sequence(self) -> Sequence: ...
    @property
    def training_info(self) -> TrainingInfo: ...
    @property
    def nodes(self) -> Nodes: ...
    @property
    def meta(self) -> bool: ...
    @property
    def metagenomic_bin(self) -> Optional[MetagenomicBin]: ...
    def __bool__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Gene: ...  # type: ignore
    def __iter__(self) -> Iterator[Gene]: ...
    def __reversed__(self) -> Iterator[Gene]: ...
    def __sizeof__(self) -> int: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
    def clear(self) -> None: ...
    def write_gff(
        self,
        file: TextIO,
        sequence_id: str,
        header: bool = True,
    ) -> int: ...
    def write_genes(
        self,
        file: TextIO,
        sequence_id: str,
        width: typing.Optional[int] = 70
    ) -> int: ...
    def write_translations(
        self,
        file: TextIO,
        sequence_id: str,
        width: typing.Optional[int] = 60,
        translation_table: typing.Optional[int] = None,
    ) -> int: ...
    def write_scores(
        self,
        file: TextIO,
        sequence_id: str,
        header: bool = True,
    ) -> int: ...

# --- Training Info ----------------------------------------------------------

class TrainingInfo:
    @classmethod
    def load(cls, fp: typing.BinaryIO) -> TrainingInfo: ...
    def __init__(
        self,
        gc: float,
        *,
        translation_table: int = 11,
        start_weight: float = 4.35,
        bias: Optional[Iterable[float]] = None,
        type_weights: Optional[Iterable[float]] = None,
        uses_sd: bool = True,
        rbs_weights: Optional[Iterable[float]] = None,
        upstream_compositions: Optional[Iterable[Iterable[float]]] = None,
        motif_weights: Optional[Iterable[Iterable[Iterable[float]]]] = None,
        missing_motif_weight: float = 0.0,
        coding_statistics: Optional[Iterable[float]] = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
    def __sizeof__(self) -> int: ...
    @property
    def translation_table(self) -> int: ...
    @translation_table.setter
    def translation_table(self, table: int) -> None: ...
    @property
    def gc(self) -> float: ...
    @gc.setter
    def gc(self, gc: float) -> None: ...
    @property
    def bias(self) -> memoryview: ...
    @bias.setter
    def bias(self, bias: Iterable[float]) -> None: ...
    @property
    def type_weights(self) -> memoryview: ...
    @type_weights.setter
    def type_weights(self, type_weights: Iterable[float]) -> None: ...
    @property
    def uses_sd(self) -> bool: ...
    @uses_sd.setter
    def uses_sd(self, uses_sd: bool) -> None: ...
    @property
    def start_weight(self) -> float: ...
    @start_weight.setter
    def start_weight(self, st_wt: float) -> None: ...
    @property
    def rbs_weights(self) -> memoryview: ...
    @rbs_weights.setter
    def rbs_weights(self, rbs_weights: Iterable[float]) -> None: ...
    @property
    def upstream_compositions(self) -> memoryview: ...
    @upstream_compositions.setter
    def upstream_compositions(self, upstream_compositions: Iterable[Iterable[float]]) -> None: ...
    @property
    def motif_weights(self) -> memoryview: ...
    @motif_weights.setter
    def motif_weights(self, motif_weights: Iterable[Iterable[Iterable[float]]]) -> None: ...
    @property
    def missing_motif_weight(self) -> float: ...
    @missing_motif_weight.setter
    def missing_motif_weight(self, missing_motif_weight: float) -> None: ...
    @property
    def coding_statistics(self) -> memoryview: ...
    @coding_statistics.setter
    def coding_statistics(self, coding_statistics: Iterable[float]) -> None: ...
    def to_dict(self) -> Dict[str, object]: ...
    def dump(self, fp: typing.BinaryIO) -> None: ...


# --- Metagenomic Bins -------------------------------------------------------

class MetagenomicBin:
    def __init__(self, training_info: TrainingInfo, description: str) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def training_info(self) -> TrainingInfo: ...
    @property
    def description(self) -> str: ...

class MetagenomicBins(typing.Sequence[MetagenomicBin]):
    def __init__(self, iterable: Iterable[MetagenomicBin]) -> None: ...
    def __len__(self) -> int: ...

    @typing.overload
    def __getitem__(self, index: int) -> MetagenomicBin: ...
    @typing.overload
    def __getitem__(self, index: slice) -> MetagenomicBins: ...
    @typing.overload
    def __getitem__(self, index: Union[int, slice]) -> Union[MetagenomicBin, MetagenomicBins]: ...


# --- Pyrodigal --------------------------------------------------------------

class GeneFinder:
    lock: threading.Lock
    _num_seq: int
    def __init__(
        self,
        training_info: Optional[TrainingInfo] = None,
        *,
        meta: bool = False,
        metagenomic_bins: Optional[MetagenomicBins] = None,
        closed: bool = False,
        mask: bool = False,
        min_gene: int = 90,
        min_edge_gene: int = 60,
        max_overlap: int = 60,
        backend: str = "detect",
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
    @property
    def training_info(self) -> Optional[TrainingInfo]: ...
    @property
    def meta(self) -> bool: ...
    @property
    def closed(self) -> bool: ...
    @property
    def mask(self) -> bool: ...
    @property
    def min_gene(self) -> int: ...
    @property
    def min_edge_gene(self) -> int: ...
    @property
    def max_overlap(self) -> int: ...
    @property
    def backend(self) -> str: ...
    def find_genes(self, sequence: Union[Sequence, str, bytes, bytearray]) -> Genes: ...
    @typing.overload
    def train(
        self,
        sequence: str,
        *sequences: str,
        force_nonsd: bool = False,
        start_weight: float = 4.35,
        translation_table: int = 11,
    ) -> TrainingInfo: ...
    @typing.overload
    def train(
        self,
        sequence: Union[bytes, bytearray],
        *sequences: Union[bytes, bytearray],
        force_nonsd: bool = False,
        start_weight: float = 4.35,
        translation_table: int = 11,
    ) -> TrainingInfo: ...