create table Jobs (
    job_ID numeric (10,0),
    designation text,
    company_id numeric(5,1),
    name text,
    work_type text,
    involvement text,
    employees_count numeric(5,0),
    total_applicants numeric(5,0),
    followers numeric,
    job_details text,
    details_id numeric(5,0),
    industry text,
    level text,
    City text,
    State text,
    PRIMARY KEY (job_ID)
);