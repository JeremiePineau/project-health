{{ config (
    materialized="view"
)}}

with cte_workout_logs as (
    select 
        timestamp
        , exercice
        , cast(if(weight = "N/A","0",weight) as integer) as weight
        , reps
        , sets
    from {{source('dbt_project_health', 'workout_logs')}}
)

select *
from cte_workout_logs