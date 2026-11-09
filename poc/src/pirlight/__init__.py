"""pirlight — PoC for privacy-preserving Zcash light client sync (simulated).

Reference implementation for the ZCG grant proposal: three sync privacy
tiers (direct / Tor / Tor+PIR), a deterministic mock chain, multi-server
PIR, and bandwidth/leakage metrics. No network calls anywhere.
"""

from .chain import CompactBlock, MockChain
from .client import ObserverView, PrivacyTier, SyncClient, SyncResult, TorCircuit
from .metrics import bandwidth_report, privacy_matrix
from .pir import (
    MatrixPIRClient,
    MatrixPIRServer,
    XorPIRClient,
    XorPIRServer,
    next_square,
    pad_to_square,
    xor_bytes,
)

__version__ = "0.1.0"

__all__ = [
    "CompactBlock",
    "MatrixPIRClient",
    "MatrixPIRServer",
    "MockChain",
    "ObserverView",
    "PrivacyTier",
    "SyncClient",
    "SyncResult",
    "TorCircuit",
    "XorPIRClient",
    "XorPIRServer",
    "__version__",
    "bandwidth_report",
    "next_square",
    "pad_to_square",
    "privacy_matrix",
    "xor_bytes",
]
