import pytest


def test_stop_firo_core_process(cli):
    cli.stop_firo_core()


@pytest.mark.unit
def test_firo_core_should_be_running(cli):
    with pytest.raises(AssertionError):
        cli.getblockcount()


@pytest.mark.unit
def test_non_existing_rpc(firo_cli):
    with pytest.raises(AssertionError):
        firo_cli.getnonexisting()
