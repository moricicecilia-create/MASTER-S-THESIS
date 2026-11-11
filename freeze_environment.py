"""Record environment separately; never silently overwrite supplied historical lock."""
import subprocess,sys
from pathlib import Path
from src.execution import environment,atomic_json
root=Path(__file__).resolve().parent
atomic_json(root/'environment-current.json',environment())
result=subprocess.run([sys.executable,'-m','pip','freeze'],check=True,capture_output=True,text=True)
(root/'requirements-current.txt').write_text(result.stdout,encoding='utf-8')
print('Created environment-current.json and requirements-current.txt')
