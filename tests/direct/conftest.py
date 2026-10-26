from pathlib import Path
import os
import pytest


CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "promise_ratchet.py"


@pytest.fixture
def ratchet(direct_deploy):
    return direct_deploy(str(CONTRACT), sdk_version="v0.2.16")


@pytest.fixture(autouse=True)
def windows_gltest_stdin_cleanup(request, monkeypatch):
    """Work around genlayer-test's Windows open-stdin cleanup behavior."""
    if os.name != "nt":
        yield
        return
    saved_stdin = os.dup(0)
    pending_paths = []
    original_unlink = os.unlink

    def unlink_or_defer(path, *args, **kwargs):
        try:
            original_unlink(path, *args, **kwargs)
        except PermissionError:
            pending_paths.append(path)

    monkeypatch.setattr(os, "unlink", unlink_or_defer)
    yield
    vm = request.node.funcargs.get("direct_vm")
    try:
        os.dup2(saved_stdin, 0)
        original_fd = getattr(vm, "_original_stdin_fd", None)
        if original_fd is not None:
            os.close(original_fd)
    except OSError:
        pass
    monkeypatch.setattr(os, "unlink", original_unlink)
    for path in pending_paths:
        try:
            original_unlink(path)
        except (FileNotFoundError, PermissionError):
            pass
    os.close(saved_stdin)
