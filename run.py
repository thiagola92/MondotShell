import argparse
import importlib.util
from pathlib import Path

from mondot_shell.code import rewrite_user_code
from mondot_shell.shell import Shell

# fmt: off
parser = argparse.ArgumentParser(description="Description to be used on mondot")
parser.add_argument("--code-path", dest="code_path", type=str)
parser.add_argument("--uri", dest="uri", default=[], action="append", type=str)
parser.add_argument("--database", dest="db", default=[], action="append", type=str)
parser.add_argument("--collection", dest="col", default=[], action="append", type=str)
parser.add_argument("--page-size", dest="page_size", default="20", type=int)
parser.add_argument("--timer", dest="timer", default="1.0", type=float)
parser.add_argument("--tmp-path", dest="tmp_path", default="tmp.py", type=str)
# fmt: on

args = parser.parse_args()
args = vars(args)

# Add default if needed
uris = args["uri"] or ["mongodb://127.0.0.1:27017"]
dbs = args["db"] or ["admin"]
cols = args["col"] or ["admin"]

code_path: Path = Path(args["code_path"]).resolve()  # Absolute path
tmp_path: Path = Path(args["tmp_path"]).resolve()  # Absolute path

rewrite_user_code(input_path=code_path, output_path=tmp_path)

# Import temporary code
spec = importlib.util.spec_from_file_location("temporary_code", str(tmp_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Remove temporary code because it's already loaded
tmp_path.unlink(missing_ok=True)

Shell(
    uris=uris,
    dbs=dbs,
    cols=cols,
    filepath=str(code_path),
    page_size=args["page_size"],
    timer=args["timer"],
).run(module.code)
