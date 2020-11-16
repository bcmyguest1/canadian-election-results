-- Auto Generated Create Script from pgAdmin

-- Table: bguest.candidates

-- DROP TABLE bguest.candidates;

CREATE TABLE bguest.candidates
(
    "RidingNumber" integer NOT NULL,
    "LibCandidate" character varying(255) COLLATE pg_catalog."default",
    "ConCandidate" character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    "NDPCandidate" character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    "GreenCandidate" character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    "BQCandidate" character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    "PPCCandidate" character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    CONSTRAINT candidates_pkey PRIMARY KEY ("RidingNumber")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE bguest.candidates
    OWNER to bguest;

CREATE INDEX "CandidateNames"
    ON bguest.candidates USING btree
    ("PPCCandidate" COLLATE pg_catalog."default" ASC NULLS LAST, 
    "BQCandidate" COLLATE pg_catalog."default" ASC NULLS LAST, 
    "GreenCandidate" COLLATE pg_catalog."default" ASC NULLS LAST,
     "NDPCandidate" COLLATE pg_catalog."default" ASC NULLS LAST, 
     "ConCandidate" COLLATE pg_catalog."default" ASC NULLS LAST, 
     "LibCandidate" COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE TABLE bguest.vote_share
(
    "RidingNumber" integer NOT NULL,
    "RidingNameEn" character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "RidingNameFr" character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "TotalVotes" integer,
    "Turnout" double precision,
    "ConVoteShare" double precision,
    "LibVoteShare" double precision,
    "NDPVoteShare" double precision,
    "BQVoteShare" double precision,
    "PPCVoteShare" double precision,
    "GreenVoteShare" double precision,
    CONSTRAINT vote_share_pkey PRIMARY KEY ("RidingNumber")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE bguest.vote_share
    OWNER to bguest;
-- Index: VoteShare

-- DROP INDEX bguest."VoteShare";

CREATE INDEX "VoteShare"
    ON bguest.vote_share USING btree
    ("GreenVoteShare" ASC NULLS LAST, "PPCVoteShare" ASC NULLS LAST, 
    "BQVoteShare" ASC NULLS LAST, "NDPVoteShare" ASC NULLS LAST,
     "LibVoteShare" ASC NULLS LAST, "ConVoteShare" ASC NULLS LAST)
    TABLESPACE pg_default;