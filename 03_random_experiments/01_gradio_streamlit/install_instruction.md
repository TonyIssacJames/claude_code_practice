# Installing & Running in a Restricted / Offline Environment

How to install the requirements and run the apps when the target machine has
limited or no internet access. Commands work the same on Windows and Linux;
only the venv activation line differs by OS.

The two real problems are:
1. **Where packages install** — solved by a virtual environment (no admin rights needed).
2. **Blocked network** — solved by either an internal package mirror or carrying wheels in by hand.

---

## Step 1 — Diagnose the target machine first

Run these on the target machine to learn what you're dealing with:

```bash
python3 --version                 # what Python you have (matters for offline wheels)
python3 -m pip --version          # is pip installed?
python3 -m pip config list        # is an internal package mirror configured?
python3 -m pip install --dry-run streamlit   # can it reach an index at all?
```

The `pip config list` output is the key one. If you see an `index-url` pointing
at an internal host, you can likely use the easy path (Step 3a).

---

## Step 2 — Always use a virtual environment

A venv puts every package inside a `.venv/` folder **in your project** —
predictable location, no admin/root needed, nothing touches the system Python.
This answers "where do packages get installed": exactly where you create the venv.

**Create + activate** (only the activate step differs by OS):

```bash
# 1. Create it (same on both)
python -m venv .venv          # Windows: 'python'   Linux: maybe 'python3'

# 2a. Activate — Windows PowerShell
.venv\Scripts\Activate.ps1

# 2b. Activate — Windows cmd.exe
.venv\Scripts\activate.bat

# 2c. Activate — Linux / macOS
source .venv/bin/activate
```

Once activated, your prompt shows `(.venv)` and `python`/`pip` now mean the
venv's copy. To leave: `deactivate`.

> Tip: to dodge the activation difference in scripts, call the venv's tools directly:
> - Windows: `.venv\Scripts\python -m pip ...`
> - Linux:   `.venv/bin/python -m pip ...`

### Creating the venv with a SPECIFIC Python version

`python -m venv .venv` uses whatever `python` resolves to on your PATH. If the
machine has several Python versions installed, point at the exact one you want.

First, find out which Pythons are available:

```bash
# Linux / macOS
which -a python3 python3.11 python3.12     # show full paths of each
ls /usr/bin/python*                        # list installed interpreters

# Windows (PowerShell) — the 'py' launcher lists installed versions
py --list
```

Then create the venv **using that exact interpreter** — whichever `python`
you run `-m venv` with becomes the venv's Python, so just call the one you want:

```bash
# Linux / macOS — call the versioned binary by name or full path
python3.11 -m venv .venv
/usr/bin/python3.11 -m venv .venv          # or the full path if not on PATH

# Windows — use the 'py' launcher to pick a version
py -3.11 -m venv .venv
"C:\Path\To\Python311\python.exe" -m venv .venv   # or a full path
```

Confirm the venv got the version you expected:

```bash
# after activating (or call .venv's python directly)
python --version
```

> The Python version matters for offline wheels (Step 3b): the venv's version
> must match the `--python-version` you used when downloading wheels.

---

## Step 3a — If the machine reaches an index (internet OR internal mirror)

The easy path. With the venv active:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you know an internal mirror URL but it isn't configured:

```bash
python -m pip install -r requirements.txt \
  --index-url https://your-internal-mirror/simple \
  --trusted-host your-internal-mirror
```

---

## Step 3b — Fully offline (network blocked, no mirror)

Download the packages on a machine that **does** have internet, carry them to
the target machine, and install from the local folder.

> **Critical gotcha:** some dependencies (numpy, pandas, pyarrow, pydantic-core)
> ship *compiled* wheels that are **OS- and Python-version-specific**. Wheels
> downloaded on Windows will **not** run on a Linux machine. Download them on a
> machine that **matches the target's OS and Python version**, or use the
> `--platform` flags below.

**On the internet-connected machine** — download everything into `wheelhouse/`:

```bash
# Simplest: if the download machine matches the target's OS + Python
python -m pip download -r requirements.txt -d wheelhouse

# OR: from Windows, targeting a Linux x86-64 machine with Python 3.11
python -m pip download -r requirements.txt -d wheelhouse \
  --platform manylinux2014_x86_64 \
  --python-version 3.11 \
  --only-binary=:all:
```

**Transfer the `wheelhouse/` folder** to the target machine.

**On the target machine**, with the venv active, install with no network:

```bash
python -m pip install --no-index --find-links=wheelhouse -r requirements.txt
```

`--no-index` tells pip not to try PyPI; `--find-links` points it at your folder.

---

## Step 4 — Run the apps

```bash
python gradio_app.py                  # Gradio    -> http://127.0.0.1:7860
streamlit run streamlit_app.py        # Streamlit -> http://localhost:8501
```

On a **headless server** (no browser / accessed over SSH), listen on all
interfaces and stop Streamlit from trying to open a browser:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
```

For Gradio, change the last line of `gradio_app.py` to:

```python
demo.launch(server_name="0.0.0.0", server_port=7860)
```

(Firewall rules may still block the port — that's a separate networking task.)

---

## Quick recommendation

1. Run the **Step 1 diagnostics** first — they tell you whether you're in the
   easy case (3a) or the offline case (3b).
2. **Always** use the venv (Step 2) regardless — it's the clean answer to
   "where do packages go."
3. You can practice the exact venv + install + run flow on Windows first; only
   the activate line changes on Linux.
