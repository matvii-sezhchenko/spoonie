# Spoonie

Spoonie is a small Python application to help manage feeding flows and mixture timers.
It provides controllers, database handlers, and simple repository code to store and retrieve
feeding schedules and mixture-timer data.

**Project Goals**
- **Simple:** Minimal dependencies and easy local setup.
- **Extensible:** Clear structure for controllers, handlers, and repository code.
- **Shareable:** Config and JSON timers can be adapted for different devices or UIs.

**Features**
- **Feeding management:** create, store and query feeding records.
- **Mixture timer:** JSON-driven timers for mixtures and scheduled tasks.
- **Lightweight DB layer:** repository and query helpers under `app/repository`.

**Getting Started**

Requirements: Python 3.10+ recommended.

Installation (recommended, using a virtual environment):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app (simple entry point):

```bash
python main.py
```

If your environment uses a different entry point, check [main.py](main.py) for details.

**Configuration**
- **App config:** see [app/config.py](app/config.py) for runtime settings.
- **Timers:** example timer definitions live in [jsons/mixture_timer.json](jsons/mixture_timer.json).
- **Requirements:** see [requirements.txt](requirements.txt) for Python dependencies.

**Project Structure (high level)**
- `main.py` — application entry point.
- `app/` — main package containing controllers, models and repository code.
  - `app/controllers/` — request or CLI controllers (e.g. feeding and mixture controllers).
  - `app/models/` — domain models (e.g. `feeding.py`).
  - `app/repository/` — database manager and query helpers.
  - `app/database/handlers/` — lower-level database handlers and keyboards/timers.
- `jsons/` — example JSON data such as mixture timers.

**Development**
- Use the virtual environment above when developing.
- Run linters or formatters as configured in your editor.

**Contributing**
- Open issues or pull requests. Describe the bug or feature and include steps to reproduce.

**License**
- No license specified. Add a `LICENSE` file to make the terms explicit.

**Support**
- For questions or help, open an issue on the project repository or contact the maintainer.

---

If you'd like, I can:
- add a short example of how to create a feeding record,
- add a one-line CLI usage example, or
- create a minimal `LICENSE` file (MIT) and commit it for you.

Enjoy working on Spoonie!
