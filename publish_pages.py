"""Copy the static website into the GitHub Pages publication folder."""
from pathlib import Path
import shutil
base = Path(__file__).resolve().parent
shutil.copytree(base / "dist", base / "docs", dirs_exist_ok=True)
(base / "docs" / ".nojekyll").touch()
print("GitHub Pages files updated in docs/")
