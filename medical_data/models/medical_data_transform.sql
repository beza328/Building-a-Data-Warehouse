-- models/transformed.sql

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

-- Combine all cleaned data into one table
, all_cleaned_data as (
    select * from cleaned_0
    union all
    select * from cleaned_1
    union all
    select * from cleaned_2
    union all
    select * from cleaned_3
    select * from cleaned_4
)

-- Apply transformations on combined data
select
    Channel Title,
    name, 
    ID,
    Message,
    Date,
    Media Path
from all_cleaned_data
where amount is not null;  -- Filter out records with null amounts
