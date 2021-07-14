create table if not exists dbt_project_health.workout_logs (
    date_ts     timestamp,
    exercice       STRING,
    weight  INTEGER,
    reps    INTEGER,
    sets    INTEGER
)