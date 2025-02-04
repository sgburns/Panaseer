# Panaseer
Panaseer – Data Ingest Engineer - Technical Exercise Transforming Cocktail Data into a Common Information Model

Required Python Libraries
- json
- requests
- validate, ValidationError

1. Data Ingestion
   Example ingests all Cocktails beginning with the letter "A".

2. Data Transformation
   schema_in - defines fields of interest and mandatory fields.
   
   - idDrink (CocktailID) is the primary key and is converted to an integer.
   - strAlcoholic (IsAlcoholic) has been converted to a boolean and accepts "non alcoholic" or "non-alcoholic" for an evaluation of False; "alcoholic" for True.
   - All strings have had their leading and trailing whitespace removed.
  
3. Edge Case Handling
   - "strIngredientN and strMeasureN" (Ingredients) is considered an object. If there's a mismatch in the number of items, then the dataset is considerd corrupted; unable to definitively match one ingredient to a measure.
   - Measurements of oz (ounces) have been converted to ml (millilitres).
  
4. Options and choices
   - Raw data is saved as cocktails_in.json
   - Validated and data-typed data is saved as cocktails_out.json
   - It's useful to have a snapshot of the raw data at the time it was ingested, for comparison at a later data.
   - The data transformation is performed in-memory, as this has performance advantages over reading from the saved raw data file.
