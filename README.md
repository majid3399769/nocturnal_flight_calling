# Nocturnal Flight Calling

# Quickstart

Clone the project using following command or unzip the .zip file. The code was written using VS code 

> git clone git@github.com:majidshaik/nocturnal_flight_calling.git

Install the libaries using
> pip install requirements.txt

You can use the following command in your terminal. Make sure you specify your input and output files in config.ini 
> python.exe src/main.py --config_file_path config/config.ini

<br></br>
# Input Files

## config.ini
Configuration file for specifying input and output directory. Along with names for input files needed for run at input directory path

    [Env]
    env = dev

    [Input]
    path = data/input/
    chicago_collision = chicago_collision_data.json
    flight_call = flight_call.json
    light_levels = light_levels.json

    [Output]
    path = data/output/
    cleaned_raw_data = cleaned_raw_data.csv
    chicago_collision_season = chicago_collision_season.csv
    light_score_mp_fct = light_score_mp_fct.csv

## chicago_collision_data.json

Collision data recorded from 1978 to 2016 for Chicago area

|variable    |class     |description |
|:-----------|:---------|:-----------|
|genus       | string | Bird Genus          |
|species     | string | Bird species           |
|date        | date    | Date of collision death (ymd)           |
|locality    | string | MP or CHI - recording at either McCormick Place or greater Chicago area           |
## flight_call.json

|variable    |class     |description |
|:-----------|:---------|:-----------|
|genus       | string | Bird Genus          |
|species     | string | Bird species           |
|family      | string | Bird Family          |
|flight_call | string | Does the bird use a flight call - yes or no           |
|habitat     | string | Open, Forest, Edge - their habitat affinity          |
|stratum     | string  | Typical occupied stratum - ground/low or canopy/upper           |

## light_levels.json

|variable    |class  |description |
|:-----------|:------|:-----------|
|date        | date | Date of light recording  (ymd)        |
|light_score | integer | Number of windows lit at the McCormick Place, Chicago - higher = more light          |

<br></br>
# Input file Cleaning

## chicago_collision_data.json

1. Add column season as paper has model constructed as per season on page 7 where spring is described as March to May
and Autum is described as August to November
2. Change Species and Genus to lower case
3. Change genus as per flight_call data. For instance ammodramus henslowii is also known as centronyx henslowii https://en.wikipedia.org/wiki/Henslow%27s_sparrow 

## flight_call.json

1. Rename Columns as per the given instructions
2. Change flight call variable to lower case
3. Change Habitat to lower case
4. Change Stratum to lower case and remove \t characters
5. Change flight_call variable to "no" as per section 2.a Flight Call 
Categorization from paper


## light_levels.json

1. Remove duplicate rows 
2. Remove rows where Date is Null or Light Score is Null

<br></br>
## Transformation 
1. Read chicago_collision_data.json,flight_call.json, light_levels.json
2. Clean the data as per instructions given above for each data 
3. Join flight_call data with chicago_collision_data based on 'Genus','Species'
4. The paper describes the Chi square model was created based on season so the data autumn and spring were added as column given in paper page 7 table.1
5. The light_level data were joined with the above table based on 'Date' 
6. The final raw table is saved as cleaned_raw_data.csv
7. Create aggregate tables chicago_collision_season.csv which calculates collisions and collisions_days were calculated based on paper and the result was saved as csv
8. Created aggregated table light_score_mp_fct.csv which had columns collisions_per_species, log_collision_per_species for McCormick Place based on which relationship between collisions per species vs light level can be constructed as shown in figure 4. of paper 


<br></br>
## Output File Dictionary

|variable    |class     |description |
|:-----------|:---------|:-----------|
|collisions       | integer | Collisions           |
|season     | string | autumn or spring seasons           |
|collisions_days      | integer | Number of days in a particular season where we have collisions          |
|collision_per_species | float | Number of collisions per species          |
|log_collision_per_species     | float | Log of collision_per_species          |
|num_species     | integer  | Number of unique species           |
|sum_collisions | integer | Sum of collisions


## Analysis 
By plotting light level vs collision mean count per species we can clearly see flight call is positively correlated with light score for McCormick Place where green points on figure represent collision with flight calls and blue repreesent collision without flight calls 

![Plot](data/output/mc_light_vs_collision.png)