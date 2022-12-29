#!/usr/bin/env bash

PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME} -d ${DB_NAME} -c \
"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '${DB_NAME}' AND pid <> pg_backend_pid();"

PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME} -d postgres -c \
"DROP DATABASE IF EXISTS ${DB_NAME}"
PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME} -d postgres -c \
"CREATE DATABASE ${DB_NAME};"
