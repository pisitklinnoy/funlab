import datetime
import pathlib
import importlib
import logging
import os
from flask import g, redirect, url_for, send_from_directory

logger = logging.getLogger(__name__)


def add_date_url(url):
    now = datetime.datetime.now()
    return f'{url}?date={now.strftime("%Y%m%d")}'


def get_subblueprints(directory):
    blueprints = []

    package = directory.parts[len(pathlib.Path.cwd().parts) :]
    parent_module = None
    try:
        parrent_view = directory.with_name("__init__.py")
        pymod_file = f"{'.'.join(package)}"
        pymod = importlib.import_module(pymod_file)

        if "module" in dir(pymod):
            parent_module = pymod.module
            blueprints.append(parent_module)
    except Exception as e:
        logger.exception(e)
        return blueprints

    subblueprints = []
    for module in directory.iterdir():
        if "__" == module.name[:2]:
            continue

        if module.match("*.py"):
            try:
                pymod_file = f"{'.'.join(package)}.{module.stem}"
                pymod = importlib.import_module(pymod_file)

                if "module" in dir(pymod):
                    subblueprints.append(pymod.module)
            except Exception as e:
                logger.exception(e)

        elif module.is_dir():
            subblueprints.extend(get_subblueprints(module))

    for module in subblueprints:
        if parent_module:
            parent_module.register_blueprint(module)
        else:
            blueprints.append(module)

    return blueprints


def register_blueprint(app):
    runs_dir = "funlab/web/views/utils/runs/detect"

    # ค้นหาโฟลเดอร์ที่อยู่ใน runs_dir และเป็นโฟลเดอร์จริง ๆ
    subdirs = [
        d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))
    ]

    # ค้นหาโฟลเดอร์ล่าสุดที่เริ่มต้นด้วย 'exp'
    exp_dirs = sorted(
        [d for d in subdirs if d.startswith("exp")],
        key=lambda x: os.path.getmtime(os.path.join(runs_dir, x)),
        reverse=True,
    )

    app.add_template_filter(add_date_url)
    parent = pathlib.Path(__file__).parent
    blueprints = get_subblueprints(parent)

    @app.route("/")
    def index():
        return redirect(url_for("home.index"))

    @app.route("/images/<filename>")
    def serve_image(filename):

        return send_from_directory(
            os.path.join(app.root_path, f"views/utils/runs/detect/{exp_dirs[0]}"),
            filename,
        )

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
