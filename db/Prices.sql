CREATE TABLE public."prices" (
    id uuid,
    product varchar(30),
    changed_dt timestamp,
    price integer,
    old_price integer,
    price_trend integer
);

CREATE TABLE public."tickers" (
    id uuid,
    product varchar(30)
);

ALTER TABLE IF EXISTS public."prices"
    OWNER TO postgres;

ALTER TABLE IF EXISTS public."prices_history"
    OWNER TO postgres;