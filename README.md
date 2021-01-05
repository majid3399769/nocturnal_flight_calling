# Nocturnal Flight Calling

# Quickstart

Clone the project using following command

> git clone 

Install the libaries using
> pip install requirements.txt

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

## chicago_collision_data.json

Collision data recorded from 1978 to 2016 for Chicago area

|variable    |class     |description |
|:-----------|:---------|:-----------|
|genus       | factor | Bird Genus          |
|species     | factor | Bird species           |
|date        | date    | Date of collision death (ymd)           |
|locality    | factor | MP or CHI - recording at either McCormick Place or greater Chicago area           |
## flight_call.json

|variable    |class     |description |
|:-----------|:---------|:-----------|
|genus       | factor | Bird Genus          |
|species     | factor | Bird species           |
|family      | factor | Bird Family          |
|flight_call | factor | Does the bird use a flight call - yes or no           |
|habitat     | factor | Open, Forest, Edge - their habitat affinity          |
|stratum     | factor  | Typical occupied stratum - ground/low or canopy/upper           |

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