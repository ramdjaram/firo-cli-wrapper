### Firo documentation
https://docs.firo.org/en/latest/wallets-guide/firo-cli/#using-the-rpc-interface

### `python-bitcoinrpc` documentation
https://github.com/jgarzik/python-bitcoinrpc


FIRO-CLI SPARK

Git Clone Token :: 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
git clone https://ramdjaram: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@github.com/ramdjaram/firo-cli.git

BUILD
1. cd depends
2. make -j`nproc`
3. cd ..
4. ./autogen.sh
5. ./configure --prefix=`pwd`/depends/`depends/config.guess`
6. make
7. ./src/qt/firo-qt -regtest <-- open QT in regtest

When rebuilding `make clean` then `make`


EXECUTE IN TERMINAL TO RUN FIROD
1. ./firod -regtest
2. ./firo-cli -regtest getsparkbalance


COMMANDS
- [ ] listunspentsparkmints
- [ ] listsparkmints
- [ ] listsparkspends
- [ ] getsparkdefaultaddress
- [ ] getallsparkaddresses
- [ ] getnewsparkaddress
- [ ] getsparkbalance
- [ ] getsparkaddressbalance
- [ ] resetsparkmints
- [ ] setsparkmintstatus
- [ ] mintspark
- [ ] spendspark,
- [ ] lelantustospark



FOR TESTING LELANTUSSPARK IN REGTEST
* mint/spend lelantus will be enabled at block 400 
* mint lelantus will be disabled after block 1000
* spend lelantus will be disabled after block 1500
* mint/spend spark will be enabled at block 1000

Mintspark is for public to private
Spendspark is private to private(or public)

To migrate lelantus, need block number >= 1000 & balance of lelantus >0



Re-broadcast a transaction using firo-cli
getrawtransaction <txid>
sendrawtransaction <hex-encoded-transaction>

Get information about a specific transaction using firo-cli
gettransaction <txid>


Start firo-qt with new blockchain
./firo-qt -regtest -datadir=/Users/milanranisavljevic/Desktop/regtest

Generate 1000 blocks
generate 1000


listaddressbalances
getallsparkaddresses
getsparkaddressbalance <address>

mintspark "{\"pr1nt8jg4su5tzpq2ghaz0vyq79j398uhg9uh6vays2lh6lhttqqtqk506dw5h69nv9zdjg6g9q2t348ag705c4lz3tfvxc7yly6e2xzpl44y5fntduuthe56a3nw0m2yyl7r9989gwvr8et\":{\"amount\":0.01, \"memo\":\"test_memo\"}}"


2 mintspark’s must be executed before spendspark


to public
spendspark "{\"TP65emX7KpovgvfRdTKGJHkcBHvJRXTYsz\": {\"amount\":0.01, \"subtractFee\": false}}" "{}"


to private
spendspark "{}" "{\"sr1zsu5tc4ne94p7zax9af82ax7x489pv20ffd3jruypsmfr8046m8wqpdtw47n9p5v3ca9tz9g8snn8eyqx0mdmjksa5lt2dvk2nc5gzjtl2jdqt3f3ney555e2hvszjcxak32n7csnv44k\":{\"amount\":0.01, \"subtractFee\": false}}"










