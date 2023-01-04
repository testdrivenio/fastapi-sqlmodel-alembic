create table product
(
    name        varchar not null unique,
    status      boolean not null,
    stock       integer not null,
    description varchar not null,
    price       numeric not null,
    product_id  serial primary key
);

COPY product(name, status, stock, description, price)
FROM '/docker-entrypoint-initdb.d/mock_products.csv'
DELIMITER ','
CSV HEADER
NULL as 'NULL';