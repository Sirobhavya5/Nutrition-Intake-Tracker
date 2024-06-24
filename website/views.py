import decimal
import datetime

from django.shortcuts import render

from website.utils import nutrition_intakes_dynamodb_table, foods_dynamodb_table

# Main page view
def index(request):
    try:
        # Handle form submission
        if request.method == "POST":
            action = request.POST.get("action")

            # Perform actions based on the value of the "action" field
            if action == "Submit":
                exists = request.POST["exists"]

                # Update the food item if it exists
                if exists == "true":
                    foods_table_attribute_updates = {}

                    food_name = request.POST.get("food-name", None)
                    if food_name is None or food_name == "":
                        raise Exception("Must enter food name to be updated. ")

                    # Update calories if provided
                    calories = request.POST.get("calories", None)
                    if calories is not None and calories != "":
                        foods_table_attribute_updates["Calories"] = {"Value": decimal.Decimal(calories)}

                    # Update protein if provided
                    protein = request.POST.get("protein", None)
                    if protein is not None and protein != "":
                        foods_table_attribute_updates["Protein"] = {"Value": decimal.Decimal(protein)}

                    # Update fat if provided
                    fat = request.POST.get("fat", None)
                    if fat is not None and fat != "":
                        foods_table_attribute_updates["Fat"] = {"Value": decimal.Decimal(fat)}

                    # Update carbohydrates if provided
                    carbohydrates = request.POST.get("carbohydrates", None)
                    if carbohydrates is not None and carbohydrates != "":
                        foods_table_attribute_updates["Carbohydrates"] = {"Value": decimal.Decimal(carbohydrates)}

                    # Update the food item in the foods_dynamodb_table
                    foods_dynamodb_table.update_item(
                        Key={
                            "FoodName": food_name,
                        },
                        AttributeUpdates=foods_table_attribute_updates
                    )
                # Create a new food item if it does not exist
                else:
                    date = request.POST["date"]
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    date = date_obj.strftime('%m/%d/%Y')

                    food_name = request.POST["food-name"]
                    calories = decimal.Decimal(request.POST["calories"])
                    protein = decimal.Decimal(request.POST["protein"])
                    fat = decimal.Decimal(request.POST["fat"])
                    carbohydrates = decimal.Decimal(request.POST["carbohydrates"])

                    # Add a new entry to nutrition_intakes_dynamodb_table
                    nutrition_intakes_dynamodb_table.put_item(
                        Item={
                            "Date": date,
                            "FoodName": food_name
                        }
                    )

                    # Add a new entry to foods_dynamodb_table
                    foods_dynamodb_table.put_item(
                        Item={
                            "FoodName": food_name,
                            "Calories": calories,
                            "Protein": protein,
                            "Fat": fat,
                            "Carbohydrates": carbohydrates
                        }
                    )
            # Delete a food item and its related entries in the nutrition_intakes_dynamodb_table
            elif action == "Delete":
                food_name = request.POST["food-name"]
                foods_dynamodb_table.delete_item(
                    Key={
                        "FoodName": food_name
                    }
                )

                nutrition_intakes = nutrition_intakes_dynamodb_table.scan()["Items"]

                for nutrition_intake in nutrition_intakes:
                    if nutrition_intake["FoodName"] == food_name:
                        nutrition_intakes_dynamodb_table.delete_item(
                            Key={
                                "Date": nutrition_intake["Date"],
                                "FoodName": food_name
                            }
                        )

            # Retrieve and display the updated nutrition intakes
            nutrition_intakes = nutrition_intakes_dynamodb_table.scan()["Items"]
            foods = foods_dynamodb_table.scan()["Items"]

            foods_dict = {}
            for food in foods:
                foods_dict[food["FoodName"]] = food

            for i in range(len(nutrition_intakes)):
                date_obj = datetime.datetime.strptime(nutrition_intakes[i]["Date"], "%m/%d/%Y")
                nutrition_intakes[i]["Date"] = date_obj.strftime("%Y-%m-%d")

                food_name = nutrition_intakes[i]["FoodName"]
                food_attributes = foods_dict[food_name]
                for food_attribute in food_attributes:   
                    nutrition_intakes[i][food_attribute] = food_attributes[food_attribute]

            sorted_nutrition_intakes = sorted(nutrition_intakes, key=lambda x: x["Date"])

            return render(request, "website/index.html", {"message": "Nutrition Intake Successfully Modified", "nutrition_intakes": sorted_nutrition_intakes})
        # If the request is not a POST request, just display the data
        else:
            nutrition_intakes = nutrition_intakes_dynamodb_table.scan()["Items"]
            foods = foods_dynamodb_table.scan()["Items"]

            foods_dict = {}
            for food in foods:
                foods_dict[food["FoodName"]] = food

            for i in range(len(nutrition_intakes)):
                date_obj = datetime.datetime.strptime(nutrition_intakes[i]["Date"], "%m/%d/%Y")
                nutrition_intakes[i]["Date"] = date_obj.strftime("%Y-%m-%d")

                food_name = nutrition_intakes[i]["FoodName"]
                food_attributes = foods_dict[food_name]
                for food_attribute in food_attributes:   
                    nutrition_intakes[i][food_attribute] = food_attributes[food_attribute]

            sorted_nutrition_intakes = sorted(nutrition_intakes, key=lambda x: x["Date"])

            return render(request, "website/index.html", {"nutrition_intakes": sorted_nutrition_intakes})
    except Exception as e:
        return render(request, "website/index.html", {"error": str(e)})

def goals_summary(request):
    try:
        # Check if request method is POST
        if request.method == "POST":
            # Get start and end dates from the request
            start_date = request.POST["start-date"]
            end_date = request.POST["end-date"]

            # Convert start and end dates to datetime objects
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            # Check if start date is greater than end date
            if start_date > end_date:
                raise Exception("Please make sure that the start date is earlier than end date. ")

            # Get all nutrition intakes from the database
            nutrition_intakes = nutrition_intakes_dynamodb_table.scan()["Items"]

            # Extract unique dates from nutrition intakes
            unique_dates = []
            for nutrition_intake in nutrition_intakes:
                if nutrition_intake["Date"] not in unique_dates:
                    unique_dates.append(nutrition_intake["Date"])

            # Convert date strings to datetime objects
            for i in range(len(unique_dates)):
                date_obj = datetime.datetime.strptime(unique_dates[i], "%m/%d/%Y")
                unique_dates[i] = date_obj

            # Sort unique dates
            unique_dates = sorted(unique_dates)

            # Create a set of continuous dates between start and end dates
            continuous_dates = set([start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)])

            # Check if there are missing dates in the data
            if continuous_dates.difference(set(unique_dates)):
                raise Exception("Please make sure the start and end dates are continuous. ")

            # Set daily nutrition goals
            daily_calories = 2500
            daily_protein = 60
            daily_carbohydrates = 325
            daily_fat = 78

            # Initialize total nutrition counters
            total_calories = 0
            total_protein = 0
            total_carbohydrates = 0
            total_fat = 0

            # Calculate total nutrition values for the selected date range
            for nutrition_intake in nutrition_intakes:
                if datetime.datetime.strptime(nutrition_intake["Date"], "%m/%d/%Y") in continuous_dates:
                    food_object = foods_dynamodb_table.get_item(
                        Key={
                            "FoodName": nutrition_intake["FoodName"]
                        }
                    )["Item"]

                    total_calories += food_object["Calories"]
                    total_protein += food_object["Protein"]
                    total_carbohydrates += food_object["Carbohydrates"]
                    total_fat += food_object["Fat"]

            # Calculate the number of days in the date range
            days_count = (end_date - start_date).days + 1

            # Calculate average nutrition values
            average_calories = total_calories / days_count
            average_protein = total_protein / days_count
            average_carbohydrates = total_carbohydrates / days_count
            average_fat = total_fat / days_count

            # Calculate nutrition deviations
            deviation_calories = average_calories / daily_calories * 100
            deviation_protein = average_protein / daily_protein * 100
            deviation_carbohydrates = average_carbohydrates / daily_carbohydrates * 100
            deviation_fat = average_fat / daily_fat * 100

            # Initialize summary dictionary
            summary = {}
            
            # Calculate and store calories deviation
            if average_calories < daily_calories:
                summary["calories"] = "{} cal".format(-1 * (round(average_calories - daily_calories, 2)))
                summary["calories_percentage"] = "{} %".format(-1 * (round(deviation_calories, 2) - 100))
                summary["calories_message"] = "from goal. "
            else:
                summary["calories"] = "{} cal".format(1 * (round(average_calories - daily_calories, 2)))
                summary["calories_percentage"] = "{} %".format(1 * (round(deviation_calories, 2) - 100))
                summary["calories_message"] = "over goal. "

            # Calculate and store carbohydrates deviation
            if average_carbohydrates < daily_carbohydrates:
                summary["carbohydrates"] = "{} cal".format(-1 * (round(average_carbohydrates - daily_carbohydrates, 2)))
                summary["carbohydrates_percentage"] = "{} %".format(-1 * (round(deviation_carbohydrates, 2) - 100))
                summary["carbohydrates_message"] = "from goal. "
            else:
                summary["carbohydrates"] = "{} cal".format(1 * (round(average_carbohydrates - daily_carbohydrates, 2)))
                summary["carbohydrates_percentage"] = "{} %".format(1 * (round(deviation_carbohydrates, 2) - 100))
                summary["carbohydrates_message"] = "over goal. "

            # Calculate and store fat deviation
            if average_fat < daily_fat:
                summary["fat"] = "{} cal".format(-1 * (round(average_fat - daily_fat, 2)))
                summary["fat_percentage"] = "{} %".format(-1 * (round(deviation_fat, 2) - 100))
                summary["fat_message"] = "from goal. "
            else:
                summary["fat"] = "{} cal".format(1 * (round(average_fat - daily_fat, 2)))
                summary["fat_percentage"] = "{} %".format(1 * (round(deviation_fat, 2) - 100))
                summary["fat_message"] = "over goal. "

            # Calculate and store protein deviation
            if average_protein < daily_protein:
                summary["protein"] = "{} cal".format(-1 * (round(average_protein - daily_protein, 2)))
                summary["protein_percentage"] = "{} %".format(-1 * (round(deviation_protein, 2) - 100))
                summary["protein_message"] = "from goal. "
            else:
                summary["protein"] = "{} cal".format(1 * (round(average_protein - daily_protein, 2)))
                summary["protein_percentage"] = "{} %".format(1 * (round(deviation_protein, 2) - 100))
                summary["protein_message"] = "over goal. "

            # Render the goals summary page with the summary data
            return render(request, "website/goals-summary.html", {"goals_summary": summary})
        else:
            # Get all nutrition intakes from the database
            nutrition_intakes = nutrition_intakes_dynamodb_table.scan()["Items"]

            # Extract unique dates from nutrition intakes
            unique_dates = []
            for nutrition_intake in nutrition_intakes:
                if nutrition_intake["Date"] not in unique_dates:
                    unique_dates.append(nutrition_intake["Date"])

            # Convert date strings to datetime objects and format as "YYYY-MM-DD"
            for i in range(len(unique_dates)):
                date_obj = datetime.datetime.strptime(unique_dates[i], "%m/%d/%Y")
                unique_dates[i] = date_obj.strftime("%Y-%m-%d")

            # Sort unique dates
            unique_dates = sorted(unique_dates)

            # Render the goals summary page with the unique dates
            return render(request, "website/goals-summary.html", {"unique_dates": unique_dates})
    except Exception as e:
        # If there is an error, render the goals summary page with the error message
        return render(request, "website/goals-summary.html", {"error": str(e)})
