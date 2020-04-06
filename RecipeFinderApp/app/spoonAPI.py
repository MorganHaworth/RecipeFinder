import requests
import ast
import os


'''getResultsFromAPI()========================================================
    Desc: uses 1 api call to get a list of recipes searched by ingrediants
    Param:
        ingredients: list/array of ingredients that recipes should utilize
        numResults: Number of results wanted to return
    Return:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
============================================================================'''
def getResultsFromAPI(ingredients, numResults):
    API_KEY = os.getenv(u'API_KEY')

    # Referenced API example from: https://rapidapi.com/spoonacular/api/recipe-food-nutrition?endpoint=55e1b3e1e4b0b74f06703be6
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    # This sets the parameters for search
    # ex:{"number":"Max number to return","ranking":"Ingrediant Priority","ignorePantry":"ignore basic ingredients (water)","ingredients":"Ingredients to search for"}
    querystring = {
        "number": numResults,
        "ranking": "1",
        "ignorePantry": "false",
        "ingredients": ""
    }
    ingredientsString = ""
    index = 0
    for x in ingredients:
        if index < len(ingredients):
            ingredientsString += f"{x}%2C"
        else:
            ingredientsString += f"{x}"
        index += 1
    querystring['ingredients'] = ingredientsString
    print(querystring)

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    # Convert formatted string to array. Each array index is a recipie with its related info (Except the instructions SMH)
    resultsArr = ast.literal_eval(response.text)
    return resultsArr


'''getAllResultsFormatted()===================================================
    Desc: returns string of each recipe's title, img src, & ingredients it uses
    Param:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
    Return:
        formattedResults: String of formatted recipe information
============================================================================'''
def getAllResultsFormatted(resultsArr):
    formattedResults = ""
    index = 0
    for x in resultsArr:
        formattedResults += (f"\nTitle: {x['title']}")  # Each x is a dict. Get varibles that we need
        formattedResults += (f"\n{x['image']}")
        formattedResults += (f"\n\tIngredients You Have:")
        index = 0
        for i in x['usedIngredients']:
            formattedResults += (f"\n\t\t{x['usedIngredients'][index]['name']}")
            index += 1
        formattedResults += (f"\n\tIngredients Missing:")
        index = 0
        for i in x['missedIngredients']:
            formattedResults += (f"\n\t\t{x['missedIngredients'][index]['name']}")
            index += 1

        formattedResults += ('\n')
    return formattedResults


'''getResultFormattedById()===================================================
    Desc: returns a string of ONE recipe's title, img src, and ingredients it uses
    Param:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
        id: unique id of recipe to be formatted
    Return:
        formattedResults: String of formatted recipe information
============================================================================'''
def getResultFormattedById(resultsArr, id):
    formattedResults = ""
    index = 0
    for x in resultsArr:
        if x['id'] == id:
            formattedResults += (f"\nTitle: {x['title']}")  # Each x is a dict. Get the varibles that we need
            formattedResults += (f"\n{x['image']}")
            formattedResults += (f"\n\tIngredients You Have:")
            index = 0
            for i in x['usedIngredients']:
                formattedResults += (f"\n\t\t{x['usedIngredients'][index]['name']}")
                index += 1
            formattedResults += (f"\n\tIngredients Missing:")
            index = 0
            for i in x['missedIngredients']:
                formattedResults += (f"\n\t\t{x['missedIngredients'][index]['name']}")
                index += 1
            formattedResults += ('\n')
            break
    return formattedResults


'''getListOfRecipeTitlesAndIds()==============================================
    Desc: returns dict of titles and ids of a list/array
    Param:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
    Return:
        recipeDict: Dict of recipe titles and corresponding Id
============================================================================'''
def getListOfRecipeTitlesAndIds(resultsArr):
    recipeDict = {}
    for x in resultsArr:
        recipeDict[x['id']] = x['title']

    return recipeDict


'''getInstructionsById()=====================================================
    Desc: uses 1 API call to get summary & instructins for recipe via id
    Param:
        id: Int id of recipe to get instructins of
    Return:
        instructions: String of instructions of recipe
============================================================================'''
def getInstructionsById(id):
    API_KEY = os.getenv(u'API_KEY')

    try:
        #Call for instructions of recipe by its unique id
        url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
            }
        response = {}
        response = requests.request("GET", url, headers=headers)
        resultsDict = response.json()
    except:
        resultsDict = {'response': f"No instructions found for id:{id}"}
    return resultsDict


'''getTitleById()=============================================================
    Desc: returns the title corresponding to the unique id
    Param:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
        id: unique id of recipe
    Return:
        recipeTitle: String of the recipe title
============================================================================'''
def getTitleById(resultsArr, id):
    recipeTitle = f"Error, could not find recipe by id: {id}"
    for x in resultsArr:
        if x['id'] == id:
            recipeTitle += (f"={x['title']}")  # E ach x is a dict. Get the variables that we need
            break
    return recipeTitle


'''getImageById()=============================================================
    Desc: returns the recipe image corresponding to the unique id
    Param:
        resultArr: A list/array of recipes. Each array index is a recipe dict.
        id: unique id of recipe
    Return:
        recipeImage: String of the recipe image source
============================================================================'''
def getImageById(resultsArr, id):
    recipeImage = f"Error, could not find recipe by id: {id}"
    for x in resultsArr:
        if x['id'] == id:
            recipeImage += (f"{x['image']}")
            break
    return recipeImage


#  Pass in a List(array) of ingredients and number of results wanted
def getResultsFromAPIOld(ingredients, numResults):
    API_KEY = os.getenv(u'API_KEY')

    # Referenced API example from: https://rapidapi.com/spoonacular/api/recipe-food-nutrition?endpoint=55e1b3e1e4b0b74f06703be6
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    # This sets the parameters for search
    # ex:{"number":"Max number to return","ranking":"Ingrediant Priority","ignorePantry":"ignore basic ingredients (water)","ingredients":"Ingredients to search for"}
    querystring = {
        "number": numResults,
        "ranking": "1",
        "ignorePantry": "false",
        "ingredients": ""
    }
    ingredientsString = ""
    index = 0
    for x in ingredients:
        if index < len(ingredients):
            ingredientsString += f"{x}%2C"
        else:
            ingredientsString += f"{x}"
        index += 1
    querystring['ingredients'] = ingredientsString
    print(querystring)

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    saveResults("offlineResults.txt", response.text)

    # Convert formatted string to array. Each array index is a recipie with its related info (Except the instructions SMH)
    resultsArr = ast.literal_eval(response.text)
    instructionsArr = []

    for x in resultsArr:
        # DEBUGGING: print(f"\n{x['title']}") #Each x is a dictionary
        id = x['id']  # unique for each recipie
        url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
            }
        response = {}
        response = requests.request("GET", url, headers=headers)
        resultsDict = response.json()
        # DEBUGGING: print(f"Instructions: {resultsDict['instructions']}")
        resultsDict['id'] = id  # add id in to use for offline searching

        instructionsArr.append(resultsDict)

    saveListToFile("offlineInstructionsResults.txt", instructionsArr)

    # If you want to get the instructions for each recipie, you can use the
    # getInstructionsById(id) method which pulls the instructions from offline text file
    return resultsArr


# Save 'searchByIngrediant' results to a local textfile
def saveResults(fileName, text):
    f = open(fileName, "w")
    f.write(text)
    f.close()
    print(f"Saved Results to ./{fileName}")


# Save a list of instructions per recipie to a local text file
def saveListToFile(fileName, list):
    with open(f"./{fileName}", "w") as f:
        for item in list:
            f.write("{}\n".format(item))


# Get results from offline text files
def getResultsFromFile():
    with open(f"./offlineInstructionsResults.txt", "r") as f:
        instructionsArr = f.read().splitlines()
    f.close()
    print(f"instructionsArr size = {len(instructionsArr)}\n")
    f = open(f"./offlineResults.txt", "r")

    # Convert formatted string to array. Each array is a recipie with its related info
    resultsArr = ast.literal_eval(f.read())
    print(f"results arr: {resultsArr}\n")
    index = 0
    for x in resultsArr:
        print(f"Title: {x['title']}")  # Each x is a dict. Get the varibles that we need
        print(f"\tIngredients You Have:")
        index = 0
        for i in x['usedIngredients']:
            print(f"\t\t{x['usedIngredients'][index]['name']}")
            index += 1
        print(f"\tIngredients Missing:")
        index = 0
        for i in x['missedIngredients']:
            print(f"\t\t{x['missedIngredients'][index]['name']}")
            index += 1
        index = 0
        for i in instructionsArr:
            if ast.literal_eval(i)['id'] == x['id']:
                print(f"\tInstructions for {x['title']}: {ast.literal_eval(i)['instructions']}")
            print(f"{ast.literal_eval(i)['id']}")
            index += 1

        print('\n')


'''Main=============================================================
    Desc: Runs program for testing methods
===================================================================='''
if __name__ == "__main__":
    print("Must use API once to save results for offline use.\n")
    useAPI = input("Would you like to use an API call? (y/n)")
    if (useAPI.lower() == 'y'):
        print("USing API Results\n")

        numResults = input("how many results?")
        ingredients = ['apple', 'eggs', 'milk']
        resultsArr = getResultsFromAPI(ingredients, numResults)

        print(getAllResultsFormatted(resultsArr))
        print(getInstructionsById(1064833))
        print(getResultFormattedById(resultsArr, 1064833))

    elif (useAPI.lower() == 'n'):
        print("Using Offline Results\n")
        # getResultsFromFile("offlineResults.txt")
        recipes = getListOfRecipeTitlesAndIds()
        print(recipes)
        print(f"{recipes.values()}")
        print(f"{recipes.keys()}")
        print(getInstructionsById(1110961))
        print(getTitleById(1110961))

    else:
        print("Not a valid answer")
