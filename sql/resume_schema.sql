CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email CITEXT NOT NULL UNIQUE,
    full_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    storage_uri TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes > 0),
    sha256_hash CHAR(64) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    processing_status TEXT NOT NULL DEFAULT 'uploaded',
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_resumes_user_hash_version UNIQUE (user_id, sha256_hash, version)
);

CREATE TABLE parsed_resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    parser_version TEXT NOT NULL,
    language TEXT,
    headline TEXT,
    summary TEXT,
    contact JSONB NOT NULL DEFAULT '{}'::jsonb,
    education JSONB NOT NULL DEFAULT '[]'::jsonb,
    certifications JSONB NOT NULL DEFAULT '[]'::jsonb,
    confidence_score NUMERIC(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    parsed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_parsed_resumes_resume UNIQUE (resume_id)
);

CREATE TABLE skills (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    category TEXT,
    normalized_slug TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_skills_canonical UNIQUE (canonical_name),
    CONSTRAINT uq_skills_slug UNIQUE (normalized_slug)
);

CREATE TABLE parsed_resume_skills (
    parsed_resume_id UUID NOT NULL REFERENCES parsed_resumes(id) ON DELETE CASCADE,
    skill_id BIGINT NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
    source_text TEXT NOT NULL,
    proficiency_level TEXT,
    years_experience NUMERIC(4,2) CHECK (years_experience >= 0),
    is_inferred BOOLEAN NOT NULL DEFAULT false,
    confidence_score NUMERIC(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    PRIMARY KEY (parsed_resume_id, skill_id, source_text)
);

CREATE TABLE experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parsed_resume_id UUID NOT NULL REFERENCES parsed_resumes(id) ON DELETE CASCADE,
    position_order INTEGER NOT NULL CHECK (position_order >= 0),
    company_name TEXT NOT NULL,
    company_normalized TEXT,
    title TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT false,
    location TEXT,
    description TEXT,
    achievements JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_experience_dates CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);

CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
    parsed_resume_id UUID REFERENCES parsed_resumes(id) ON DELETE CASCADE,
    embedding_type TEXT NOT NULL,
    model_name TEXT NOT NULL,
    dimension INTEGER NOT NULL DEFAULT 1536 CHECK (dimension > 0),
    embedding VECTOR(1536) NOT NULL,
    content_scope TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_embedding_owner CHECK (
        (resume_id IS NOT NULL)::int + (parsed_resume_id IS NOT NULL)::int = 1
    )
);

CREATE INDEX idx_resumes_user_created_live
    ON resumes (user_id, created_at DESC)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_resumes_status
    ON resumes (processing_status, uploaded_at DESC)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_parsed_resumes_contact_gin
    ON parsed_resumes USING GIN (contact jsonb_path_ops);

CREATE INDEX idx_parsed_resumes_education_gin
    ON parsed_resumes USING GIN (education jsonb_path_ops);

CREATE INDEX idx_prs_skill
    ON parsed_resume_skills (skill_id, parsed_resume_id);

CREATE INDEX idx_experiences_pr_order
    ON experiences (parsed_resume_id, position_order);

CREATE INDEX idx_embeddings_filter
    ON embeddings (embedding_type, model_name, created_at DESC);

CREATE INDEX idx_embeddings_vector_cosine
    ON embeddings USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
