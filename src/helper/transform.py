import pandas as pd
import logging

logger = logging.getLogger()

def corrected_genus(genus, species):
    """ Function to correct genus as per flight_call data

    Args:
        genus ([String]): Genus of bird
        species ([String]): Species of bird

    Returns:
        [String]: [Genus of the bird as per flight_call data]
    """
    if(genus == "ammodramus" and species == "henslowii"):
        return "centronyx"
    elif(genus == "ammodramus" and species == "nelsoni" ):
        return "ammospiza"
    elif(genus == "ammodramus" and species == "leconteii" ):
        return "ammospiza"
    else:
        return genus


def clean_chicago_collision(df):
    """The function is used to clean chicago collision data from
    1. Add column season as paper has model constructed as per season on page 7 where spring is described as March to May
    and Autum is described as August to November
    2. Change Species and Genus to lower case 
    3. Change genus as per flight_call data. For instance ammodramus henslowii is also known as centronyx henslowii https://en.wikipedia.org/wiki/Henslow%27s_sparrow 


    Args:
        df ([pandas.DataFrame]): [collision Pandas dataframe]
    """
    # Add column season as paper has model constructed as per season on page 7 where spring is described as March to May
    # and Autum is described as August to November
    df['Month'] = pd.DatetimeIndex(df['Date']).month
    df['Season'] = df['Month'].map({3:"spring",4:"spring",5:"spring",8:"autumn",9:"autumn",10:"autumn",11:"autumn"})
    df.drop(labels=["Month"], axis=1, inplace= True)
    # Standardize it to lower for joining with flight call data 
    df["Species"]= df["Species"].str.lower()
    df["Genus"]= df["Genus"].str.lower()

    #Change genus as per flight_call data. For instance ammodramus henslowii is also known as centronyx henslowii https://en.wikipedia.org/wiki/Henslow%27s_sparrow 
    df["Genus"] = df.apply(lambda x: corrected_genus(x["Genus"],x["Species"]), axis= 1)
    logger.info("Cleaned Chicago data")
    return df


def clean_flight_call(df):
    """The function is used to transform flight_call data
    1. Rename Columns as per the given instructions
    2. Change flight call variable to lower case
    3. Change Habitat to lower case
    4. Change Stratum to lower case and remove \t characters
    5. Change flight_call variable to "no" as per section 2.a Flight Call 
    Categorization from paper
 
    Args:
        df ([pandas.DataFrame]): [flight Call Pandas dataframe]
    """
    # Rename Columns
    rename_cols ={"Species": "Genus", "Family": "Species", 
                  "Collisions": "Family", "Call": "Flight_Call", 
                  "Flight": "Collisions"}
    df = df.rename(columns=rename_cols)

    # Change flight call variable to lower case
    df["Flight_Call"] = df["Flight_Call"].str.lower()
    df["Flight_Call"] = df["Flight_Call"].map({"yes":"yes","no":"no", "rare":"no"})

    # Change Habitat to lower case and remove \t character
    df["Stratum"] = df["Stratum"].str.replace("\t", "")
    df["Stratum"] = df["Stratum"].str.lower()

    #  Change Habitat to lower case
    df["Habitat"] = df["Habitat"].str.lower()

    # Change Species, Genus, to lower as it some names were not properly casted 
    # which would cause problem in joining table 

    df["Species"]= df["Species"].str.lower()
    df["Genus"]= df["Genus"].str.lower()
    df.drop_duplicates(inplace=True)
    logger.info("Cleaned Flight data")
    return df


def clean_light_level(df):
    """Function is used to clean and transform the light_level data 

    Args:
        df : light_level dataframe

    Returns:
        [pd.DataFrame]: clean light_level data
    """
    rename_cols ={"Light Score ": "Light_Score"}
    df = df.rename(columns=rename_cols)
    df.drop_duplicates(inplace=True)
    df = df[df["Date"].notnull() & df["Light_Score"].notnull()]
    logger.info("Cleaned Light Level data")
    return df
