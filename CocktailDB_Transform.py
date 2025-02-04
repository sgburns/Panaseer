import json
import requests
from jsonschema import validate, ValidationError

def mixed_number_to_float(mixed_number):
    """
    Convert a mixed number string (e.g., "1 1/2") to a float (e.g., 1.5).

    :param mixed_number: A string representing a mixed number (e.g., "1 1/2").
    :return: The float representation of the mixed number.
    """
    # Split the string into whole number and fraction parts
    parts = mixed_number.split()

    if len(parts) == 1:
        # If there's no space, it's either a whole number or a fraction
        if "/" in parts[0]:
            # It's a fraction (e.g., "1/2")
            numerator, denominator = parts[0].split("/")
            return float(numerator) / float(denominator)
        else:
            # It's a whole number (e.g., "2")
            return float(parts[0])
    elif len(parts) == 2:
        # It's a mixed number (e.g., "1 1/2")
        whole_number = float(parts[0])
        fraction = parts[1]
        numerator, denominator = fraction.split("/")
        return whole_number + (float(numerator) / float(denominator))
    else:
        raise ValueError("Invalid mixed number format")

def oz_to_ml(oz):
    conversion_factor = 29.5735  # 1 ounce = 29.5735 milliliters
    ml = oz * conversion_factor
    return str(int(ml)) + " ml"

# Define the JSON input schema
schema_in = {
    "type": "object",
    "properties": {
        "drinks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "idDrink": {"type": "string"},
                    "strDrink": {"type": "string"},
                    "strCategory": {"type": "string"},
                    "strAlcoholic": {"type": "string"},
                    "strGlass": {"type": ["string", "null"]},  # Allow string or null
                    "strInstructions": {"type": "string"},
                    "strDrinkThumb": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient1": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient2": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient3": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient4": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient5": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient6": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient7": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient8": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient9": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient10": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient11": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient12": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient13": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient14": {"type": ["string", "null"]},  # Allow string or null
                    "strIngredient15": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure1": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure2": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure3": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure4": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure5": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure6": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure7": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure8": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure9": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure10": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure11": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure12": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure13": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure14": {"type": ["string", "null"]},  # Allow string or null
                    "strMeasure15": {"type": ["string", "null"]},  # Allow string or null
                },
                "required": ["idDrink", "strDrink", "strCategory", "strAlcoholic", "strInstructions", "strIngredient1", "strMeasure1"],
            },
        }
    },
    "required": ["drinks"],
}

# Fetch data from the API
url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    drinks = data.get("drinks", [])
    
    # Specify the raw data output JSON file name
    file_in = "cocktails_in.json"

    # Write raw cocktail data to a JSON file
    with open(file_in, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Unscrubbed Cocktail data successfully imported to {file_in}")

    # Data-type and export scrubbed data
    try:
        # Determine if mandatory fields are populated
        validate(instance=data_in, schema=schema_in)
        print("Mandatory data is populated.")

        # Transform data into CIM schema
        cocktails = []
        for drink in drinks:
            # Convert idDrink to Integer
            idDrink = drink.get("idDrink", "").strip()
            if idDrink.isdigit():
                cocktailID = int(idDrink)
            else:
                cocktailID = None
        
            # Convert strAlcoholic String to a Boolean
            strAlcoholic = drink.get("strAlcoholic", "").lower().strip()
            if strAlcoholic == "alcoholic":
                is_alcoholic = 1
            elif strAlcoholic in ("non alcoholic","non-alcoholic"):
                is_alcoholic = 0
            else:
                is_alcoholic = None
        
            # Extract ingredients and measures
            ingredients = []
            for i in range(1, 16): 
                ingredient = drink.get(f"strIngredient{i}")
                measure = drink.get(f"strMeasure{i}")
                # Convert ml to oz
                if measure != None and measure.strip().endswith("oz"):
                    measure = measure[:-3]
                    measure = mixed_number_to_float(measure)
                    measure = oz_to_ml(measure)
                
                # Discard all ingrediets if the number of ingredients and measures mismatch, since the relationship is not explicity defined
                if ((ingredient == None and measure != None) or (ingredient != None and measure == None)):
                    ingredients = None
                    break
                elif ingredient:
                    ingredients.append({
                        "Ingredient": ingredient.strip(),
                        "Measure": measure
                    })

            # Create a cocktail object
            cocktail = {
                "CocktailID": cocktailID,
                "CocktailName": drink["strDrink"].strip(),
                "CocktailCategory": drink["strCategory"].strip(),
                "IsAlcoholic": is_alcoholic,
                "GlassType": drink["strGlass"].strip(),
                "Instructions": drink["strInstructions"].strip(),
                "ImageURL": drink["strDrinkThumb"],
                "Ingredients": ingredients
            }
            cocktails.append(cocktail)

        # Create the CIM schema
        schema_out = {
            "Cocktails": cocktails
        }
        
        # Specify the output JSON file name
        file_out = "cocktails_out.json"

        # Write the data to a JSON file
        with open(file_out, "w") as file:
            json.dump(schema_out, file, indent=4)

        print(f"Scubbed Cocktail data successfully exported to {file_out}")

    except ValidationError as e:
        print(f"Data validation failed: {e}")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")