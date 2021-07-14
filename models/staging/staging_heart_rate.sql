{{ config (
    materialized="view"
)}}

with cte_heart_rate as (
    select 
        date_ts
        , hours
        , heart_rate
    from dbt_project_health.raw_heart_rate
)

, date_formatted as (
    select 
        format_timestamp('%Y-%m-%d %H:%M:%S', cast(concat(cast(date_ts as string), " ", cast(hours as string)) as timestamp)) as date_ts
        , regexp_replace(cast(date_ts as string), "-","") as dateid
        , heart_rate
    from cte_heart_rate
)

, last_ts as (
    select *
        , coalesce(lag(date_ts) over(order by date_ts), date_ts) as last_date_ts 
    from date_formatted
)

select *
, unix_seconds(cast(date_ts as timestamp)) - unix_seconds(cast(last_date_ts as timestamp)) as seconds_diff 
from last_ts
order by date_ts