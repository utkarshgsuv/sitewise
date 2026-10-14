"""S-01 acceptance: fixtures have a text layer and reproducible bytes."""
import hashlib
import importlib.util
from pathlib import Path

import pdfplumber

GEN_PATH = Path(__file__).resolve().parents[2] / "db" / "seed" / "generate_fixtures.py"


def _load_gen():
    spec = importlib.util.spec_from_file_location("generate_fixtures", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fixture_bytes_reproducible():
    gen = _load_gen()
    first, second = gen.generate_all(), gen.generate_all()
    assert set(first) == {"contract_CT-2025-118.pdf", "po_PO-7731.pdf",
                          "inv_INV-2026-0417.pdf", "inv_AFW-09-2218.pdf"}
    for name in first:
        assert hashlib.sha256(first[name]).hexdigest() == hashlib.sha256(second[name]).hexdigest()


def test_fixture_text_layer():
    gen = _load_gen()
    for name, pdf_bytes in gen.generate_all().items():
        import io
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        missing = [n for n in gen.EXPECTED_TEXT[name] if n not in text]
        assert not missing, (name, missing)
