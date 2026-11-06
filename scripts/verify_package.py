"""Verify distributed files and exact figure-data identities."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / "MATERIALS_MANIFEST.json").read_text())
    for item in manifest["files"]:
        p = ROOT / item["path"]
        assert p.is_file(), f"Missing file: {p}"
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"], p
    for p in (ROOT / "publication/data").glob("*.csv"):
        assert p.read_bytes() == (ROOT / "model/results" / p.name).read_bytes(), p.name
    print(json.dumps({"all_passed": True, "files_verified": len(manifest["files"])}))

if __name__ == "__main__":
    main()
