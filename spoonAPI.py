import requests
import ast
import json
import os

#global Variable
#Title, instructions, ingrediants, cook time, serves, diffictuly, category
API_KEY = os.environ.get('API_KEY')


def getResultsFromAPI():
    #Referenced API example from: https://rapidapi.com/spoonacular/api/recipe-food-nutrition?endpoint=55e1b3e1e4b0b74f06703be6
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    #This sets the parameters for search
    #ex:{"number":"Max number to return","ranking":"Ingrediant Priority","ignorePantry":"ignore basic ingrediants (water)","ingredients":"Ingrediants to search for"}
    querystring = {"number":"3","ranking":"1","ignorePantry":"false","ingredients":"egg%2Cflour%2Ccheese%2Cmilk%2Cwater%2Cbacon%2Cham"}

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
        print(f"\n{x['title']}") #Each x is a dictionary
        id = x['id'] #unique for each recipie
        url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
            }
        response = {}
        response = requests.request("GET", url, headers=headers)
        resultsDict = response.json()
        print(f"Instructions: {resultsDict['instructions']}")
        resultsDict['id'] = id # add id in to use for offline searching 

        instructionsArr.append(resultsDict)
    
    saveListToFile("offlineInstructionsResults.txt", instructionsArr)
    print(f"SIZE OF ARR = {len(instructionsArr)}")

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
def getResultsFromFile(fileName):
    with open(f"./offlineInstructionsResults.txt", "r") as f:
        instructionsArr = f.read().splitlines()
    f.close()
    print(f"instructionsArr size = {len(instructionsArr)}\n")
    f = open(f"./{fileName}", "r")

    #Convert formatted string to array. Each array is a recipie with its related info
    resultsArr = ast.literal_eval(f.read())
    print(f"results arr: {resultsArr}\n")
    index = 0
    for x in resultsArr:
        print(f"Title: {x['title']}") #Each x is a dict. Get the varibles that we need
        print(f"\tIngrediants You Have:")
        index = 0
        for i in x['usedIngredients']:
            print(f"\t\t{x['usedIngredients'][index]['name']}")
            index += 1
        print(f"\tIngrediants Missing:")
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

#Run program, ask user if they want to use an API call
if __name__ == "__main__":
    print("Must use API once to save results for offline use.\n")
    useAPI = input("Would you like to use an API call? (y/n)")
    if (useAPI.lower() == 'y'):
        print("USing API Results\n")
        getResultsFromAPI()
    elif (useAPI.lower() == 'n'):
        print("Using Offline Results\n")
        getResultsFromFile("offlineResults.txt")
    else:
        print("Not a valid answer")
