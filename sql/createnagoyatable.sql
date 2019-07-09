CREATE TYPE nagoya_instrument
AS enum ('ratification','succession','acceptance','approval','accession');

CREATE TABLE nagoya
(   code varchar(2) PRIMARY KEY,
    party date,
    instrument nagoya_instrument,
    deposit date,
    signature date
    );

