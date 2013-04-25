



CREATE TABLE clients(
    user varchar(80), 
    mac varchar(80), 
    ip4 varchar(80), 
    ip6 varchar(80), 
    active int);
    
CREATE TABLE stats (
    user varchar(80), 
    connections bigint(255), 
    tx_total bigint(255), 
    rx_total bigint(255), 
    txs bigint(255), 
    rxs bigint(255), 
    time timestamp);

CREATE TABLE limited (
    User varchar(255),
    CONNLIMIT int(8),
    RXLIMIT int(8),
    TXLIMIT int(8))

