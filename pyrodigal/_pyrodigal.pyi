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
_AVX2_BUILD_SUPPORT: bool
_NEON_BUILD_SUPPORT: bool
_SSE2_BUILD_SUPPORT: bool

TRANSLATION_TABLES: FrozenSet[int]
METAGENOMIC_BINS: Tuple[MetagenomicBin]

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
    @classmethod
    def from_bytes(cls, sequence: Union[bytes, bytearray]) -> Sequence: ...
    @classmethod
    def from_string(cls, sequence: str) -> Sequence: ...
    def __len__(self) -> int: ...
    def __sizeof__(self) -> int: ...
    def __str__(self) -> str: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
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
        self, gc: float, start_weight: float = 4.35, translation_table: int = 11
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __getstate__(self) -> Dict[str, object]: ...
    def __setstate__(self, state: Dict[str, object]) -> None: ...
    def __sizeof__(self) -> int: ...
    @property
    def metagenomic_bin(self) -> Optional[MetagenomicBin]: ...
    @property
    def translation_table(self) -> int: ...
    @translation_table.setter
    def translation_table(self, table: int) -> None: ...
    @property
    def gc(self) -> float: ...
    @gc.setter
    def gc(self, gc: float) -> None: ...
    @property
    def bias(self) -> Tuple[float, float, float]: ...
    @bias.setter
    def bias(self, bias: Iterable[float]) -> None: ...
    @property
    def type_weights(self) -> Tuple[float, float, float]: ...
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
    def dump(self, fp: typing.BinaryIO) -> None: ...

# --- Metagenomic Bins -------------------------------------------------------

class MetagenomicBin:
    training_info: TrainingInfo
    def __repr__(self) -> str: ...
    @property
    def index(self) -> int: ...
    @property
    def description(self) -> str: ...

# --- Pyrodigal --------------------------------------------------------------

class OrfFinder:
    lock: threading.Lock
    _num_seq: int
    def __init__(
        self,
        training_info: Optional[TrainingInfo] = None,
        *,
        meta: bool = False,
        closed: bool = False,
        mask: bool = False,
        min_gene: int = 90,
        min_edge_gene: int = 60,
        max_overlap: int = 60,
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
