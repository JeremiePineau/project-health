{{ config (
    materialized="view"
)}}

with cte_workout_logs as (
    select 
        *
    from {{source('dbt_project_health', 'workout_logs')}}
)

select *
from cte_workout_logs