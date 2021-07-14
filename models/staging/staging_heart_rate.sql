with cte_heart_rate as (
    select 
        date_ts
        , hours
        , heart_rate
    from dbt_project_health.raw_heart_rate
)

select *
from cte_heart_rate