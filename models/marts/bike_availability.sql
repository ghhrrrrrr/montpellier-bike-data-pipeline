{{ config(materialized='table') }}

with stations as (
    select * from {{ ref('stg_bikes') }}
)

select
    station_id,
    updated_at,
    street_name,
    station_geo,
    bikes_available,
    total_capacity,
    round(safe_divide(bikes_available, total_capacity) * 100, 2) as occupancy_percent,
    case 
        when bikes_available = 0 then 'Empty'
        when bikes_available = total_capacity then 'Full'
        else 'Available'
    end as availability_status
from stations