COPY nagoya(code, party, instrument, deposit, signature)
FROM '/nagoya_countries.csv'
      WITH CSV
           DELIMITER ','
           HEADER
           FORCE NULL party, instrument, deposit, signature
           QUOTE '"'
           ;
