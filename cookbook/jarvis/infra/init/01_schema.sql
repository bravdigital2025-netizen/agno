-- Auto-executed on first container start (PostgreSQL initdb)
-- Applies the Jarvis schema and demo seed data.
--
-- The actual SQL files live in cookbook/jarvis/database/.
-- Mount them via docker-compose volumes or copy here during CI.
--
-- For local dev, run manually after starting the container:
--   psql postgresql://ai:ai@localhost:5532/ai -f cookbook/jarvis/database/schema.sql
--   psql postgresql://ai:ai@localhost:5532/ai -f cookbook/jarvis/database/seed_demo.sql

SELECT 1;  -- placeholder to keep initdb happy
