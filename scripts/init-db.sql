-- Enable useful PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";   -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";     -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "unaccent";    -- Accent-insensitive search

SELECT 'TTEK SIS database ready' AS status;
