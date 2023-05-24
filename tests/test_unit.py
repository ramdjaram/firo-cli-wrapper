import pytest


@pytest.mark.fstop
def test_stop_firo_core_process(cli):
    cli.stop_firo_core()


@pytest.mark.unit
def test_firo_core_should_be_running(cli):
    with pytest.raises(AssertionError):
        cli.getblockcount()


@pytest.mark.unit
def test_non_existing_rpc(firo_cli):
    with pytest.raises(AttributeError):
        firo_cli.getnonexisting()


@pytest.mark.unit
def test_getsparkbalance_invalid_key(firo_cli):
    with pytest.raises(AssertionError):
        firo_cli.getsparkbalance(bad_key='invalid')


@pytest.mark.unit
def test_getsparkbalance_valid_and_invalid_key(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(input='valid key', bad_key='invalid')


@pytest.mark.unit
def test_getsparkbalance_invalid_value(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(input='invalid value')


@pytest.mark.unit
def test_spendspark_bad_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark(input='invalid value')


@pytest.mark.unit
def test_spendspark_no_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark()
