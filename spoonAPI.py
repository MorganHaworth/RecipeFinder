import requests
import ast
import json
import os

#global Variable
#Title, instructions, ingredients, cook time, serves, diffictuly, category


#Pass in a List(array) of ingredients and number of results wanted
def getResultsFromAPI(ingredients, numResults):
    API_KEY = os.getenv(u'API_KEY')

    #Referenced API example from: https://rapidapi.com/spoonacular/api/recipe-food-nutrition?endpoint=55e1b3e1e4b0b74f06703be6
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    #This sets the parameters for search
    #ex:{"number":"Max number to return","ranking":"Ingrediant Priority","ignorePantry":"ignore basic ingredients (water)","ingredients":"Ingredients to search for"}
    querystring = {"number":numResults,"ranking":"1","ignorePantry":"false","ingredients":""}
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

    #Convert formatted string to array. Each array index is a recipie with its related info (Except the instructions SMH)
    resultsArr = ast.literal_eval(response.text)
    instructionsArr = []

    for x in resultsArr:
        #DEBUGGING: print(f"\n{x['title']}") #Each x is a dictionary
        id = x['id'] #unique for each recipie
        url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
            }
        response = {}
        response = requests.request("GET", url, headers=headers)
        resultsDict = response.json()
        #DEBUGGING: print(f"Instructions: {resultsDict['instructions']}")
        resultsDict['id'] = id # add id in to use for offline searching 

        instructionsArr.append(resultsDict)
    
    saveListToFile("offlineInstructionsResults.txt", instructionsArr)
    
    #If you want to get the instructions for each recipie, you can use the 
    #getInstructionsById(id) method which pulls the instructions from offline text file
    return resultsArr



#Save 'searchByIngrediant' results to a local textfile
def saveResults(fileName, text):
    f = open(fileName, "w")
    f.write(text)
    f.close()
    print(f"Saved Results to ./{fileName}")



#Save a list of instructions per recipie to a local text file
def saveListToFile(fileName, list):
    with open(f"./{fileName}", "w") as f:
        for item in list:
           f.write("{}\n".format(item))



#Get results from offline text files
def getResultsFromFile():
    with open(f"./offlineInstructionsResults.txt", "r") as f:
        instructionsArr = f.read().splitlines()
    f.close()
    print(f"instructionsArr size = {len(instructionsArr)}\n")
    f = open(f"./offlineResults.txt", "r")

    #Convert formatted string to array. Each array is a recipie with its related info
    resultsArr = ast.literal_eval(f.read())
    print(f"results arr: {resultsArr}\n")
    index = 0
    for x in resultsArr:
        print(f"Title: {x['title']}") #Each x is a dict. Get the varibles that we need
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



#Resturns a dict of recipe titles and their corresponding id
def getListOfRecipeTitlesAndIds():
    f = open(f"./offlineResults.txt", "r")

    #Convert formatted string to array. Each array is a recipie with its related info
    resultsArr = ast.literal_eval(f.read())

    recipeDict = {}
    for x in resultsArr:
        recipeDict[x['id']] = x['title']

    f.close()
    return recipeDict



#Resturns a instructions of requests recipe
def getInstructionsById(id):
    with open(f"./offlineInstructionsResults.txt", "r") as f:
        instructionsArr = f.read().splitlines()
    
    instructions = f"No instructions found for id:{id}"

    index = 0
    for i in instructionsArr:
        if ast.literal_eval(i)['id'] == id:
            instructions = f"{ast.literal_eval(i)['instructions']}"
            break
        index += 1

    f.close()
    return instructions


 
#Returns title of recipe
def getTitleById(id):
    f = open(f"./offlineResults.txt", "r")

    #Convert formatted string to array. Each array is a recipie with its related info
    resultsArr = ast.literal_eval(f.read())

    recipeTitle = f"Could not find recipe with the id:{id}"
    for x in resultsArr:
        if x['id'] == id:
            recipeTitle = x['title']

    f.close()
    return recipeTitle



#Run program, ask user if they want to use an API call
if __name__ == "__main__":
    print("Must use API once to save results for offline use.\n")
    useAPI = input("Would you like to use an API call? (y/n)")
    if (useAPI.lower() == 'y'):
        print("USing API Results\n")
        numResults = input("how many results?")
        ingredients = ['apple','eggs','milk']
        getResultsFromAPI(ingredients, numResults)
    elif (useAPI.lower() == 'n'):
        print("Using Offline Results\n")
        #getResultsFromFile("offlineResults.txt")
        recipes = getListOfRecipeTitlesAndIds()
        print(recipes)
        print(f"{recipes.values()}")
        print(f"{recipes.keys()}")
        print(getInstructionsById(1110961))
        print(getTitleById(1110961))

    else:
        print("Not a valid answer")
