{{ config(materialized='view') }}

with raw_data as (
    select * from {{ source('montpellier_bikes_raw', 'bikes_table') }}
)
select
    replace(cast(id as string), 'urn:ngsi-ld:station:', '') as station_id,
    address_value_streetAddress as street_name,
    cast(availableBikeNumber_value as int64) as bikes_available,
    cast(freeSlotNumber_value as int64) as slots_available,
    cast(totalSlotNumber_value as int64) as total_capacity,
    status_value as station_status
from raw_data