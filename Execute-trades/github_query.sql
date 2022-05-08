SELECT
  date,
  ticker,
  MAX(Signal) AS signal,
  MAX(rsi) AS rsi,
  MAX(close) AS close,
  max (open) AS open,
  MAX(high) AS high,
  MAX(low) AS low
FROM
  `saleswebpage.trading.trading_data`
WHERE
  date > '2022-01-03'
  and  ticker in (select ticker from `saleswebpage.trading.trading_data` where date > '2022-01-02' and Signal != 'KEEP' )
GROUP BY
  ticker,
  date
ORDER BY
  ticker,
  date