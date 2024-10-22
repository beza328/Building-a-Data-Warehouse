-- models/combined_cleaned_data.sql
with cleaned_0 as (
    select * from {{ source('cleaned_data', 'cleaned_data_0') }}
),
cleaned_1 as (
    select * from {{ source('cleaned_data', 'cleaned_data_1') }}
),
cleaned_2 as (
    select * from {{ source('cleaned_data', 'cleaned_data_2') }}
),
cleaned_3 as (
    select * from {{ source('cleaned_data', 'cleaned_data_3') }}
),
cleaned_4 as (
    select * from {{ source('cleaned_data', 'cleaned_data_4') }}
)
select
    "Channel Title",  -- Selecting your required columns
    "Name",
    "ID",
    "Message",
    "Date",
    "Media Path"
from raw_data
where "Message" is not null;