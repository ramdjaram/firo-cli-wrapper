import pytest


@pytest.mark.noargs
@pytest.mark.spark
def test_listunspentsparkmints(firo_cli):
    firo_cli.listunspentsparkmints()


@pytest.mark.noargs
@pytest.mark.spark
def test_listsparkmints(firo_cli):
    firo_cli.listsparkmints()


@pytest.mark.noargs
@pytest.mark.spark
def test_listsparkspends(firo_cli):
    firo_cli.listsparkspends()


@pytest.mark.noargs
@pytest.mark.spark
def test_getsparkdefaultaddress(firo_cli, test_data):
    assert firo_cli.getsparkdefaultaddress()[0] == test_data['spark_default']


@pytest.mark.noargs
@pytest.mark.spark
def test_getallsparkaddresses(firo_cli):
    firo_cli.getallsparkaddresses()


@pytest.mark.spark
def test_getnewsparkaddress(firo_cli):
    firo_cli.getnewsparkaddress()


@pytest.mark.spark
def test_getsparkbalance(firo_cli):
    firo_cli.getsparkbalance()


@pytest.mark.spark
def test_getsparkaddressbalance(firo_cli, test_data):
    firo_cli.getsparkaddressbalance(input=test_data['spark_address1'])


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
