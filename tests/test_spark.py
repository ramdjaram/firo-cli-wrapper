import pytest


@pytest.mark.noargs
def test_listunspentsparkmints(firo_cli):
    firo_cli.listunspentsparkmints()


@pytest.mark.noargs
def test_listsparkmints(firo_cli):
    firo_cli.listsparkmints()


@pytest.mark.noargs
def test_listsparkspends(firo_cli):
    firo_cli.listsparkspends()


@pytest.mark.noargs
def test_getsparkdefaultaddress(firo_cli):
    firo_cli.getsparkdefaultaddress()


@pytest.mark.noargs
def test_getallsparkaddresses(firo_cli):
    firo_cli.getallsparkaddresses()


def test_getnewsparkaddress(firo_cli):
    firo_cli.getnewsparkaddress()


def test_getsparkbalance(firo_cli):
    firo_cli.getsparkbalance()


def test_getsparkaddressbalance(firo_cli):
    firo_cli.getsparkaddressbalance()


def test_resetsparkmints(firo_cli):
    firo_cli.resetsparkmints()


def test_setsparkmintstatus(firo_cli):
    firo_cli.setsparkmintstatus()


def test_mintspark(firo_cli):
    firo_cli.mintspark()


def test_spendspark(firo_cli):
    firo_cli.spendspark()


def test_lelantustospark(firo_cli):
    firo_cli.lelantustospark()