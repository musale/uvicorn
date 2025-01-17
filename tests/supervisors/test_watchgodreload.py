import os
import signal
import time
from pathlib import Path

from uvicorn.config import Config
from uvicorn.supervisors.watchgodreload import WatchGodReload


def run(sockets):
    pass


def test_watchgodreload(
    tls_ca_certificate_pem_path, tls_ca_certificate_private_key_path
):
    config = Config(app=None)
    reloader = WatchGodReload(config, target=run, sockets=[])
    reloader.signal_handler(sig=signal.SIGINT, frame=None)
    reloader.run()


def test_should_reload_when_python_file_is_changed(tmpdir):
    file = "example.py"
    update_file = Path(os.path.join(str(tmpdir), file))
    update_file.touch()

    working_dir = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        config = Config(app=None, reload=True)
        reloader = WatchGodReload(config, target=run, sockets=[])
        reloader.signal_handler(sig=signal.SIGINT, frame=None)
        reloader.startup()

        assert not reloader.should_restart()
        time.sleep(0.1)
        update_file.touch()
        assert reloader.should_restart()

        reloader.restart()
        reloader.shutdown()
    finally:
        os.chdir(working_dir)


def test_should_not_reload_when_dot_file_is_changed(tmpdir):
    file = ".dotted"
    update_file = Path(os.path.join(str(tmpdir), file))
    update_file.touch()

    working_dir = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        config = Config(app=None, reload=True)
        reloader = WatchGodReload(config, target=run, sockets=[])
        reloader.signal_handler(sig=signal.SIGINT, frame=None)
        reloader.startup()

        assert not reloader.should_restart()
        time.sleep(0.1)
        update_file.touch()
        assert not reloader.should_restart()

        reloader.restart()
        reloader.shutdown()
    finally:
        os.chdir(working_dir)
