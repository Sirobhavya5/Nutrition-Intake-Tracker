import decimal

from django.apps import AppConfig

from website.utils import foods_dynamodb_table, nutrition_intakes_dynamodb_table

def populate_database():
    nutrition_intakes = nutrition_intakes_dynamodb_table.scan()
    for nutrition_intake in nutrition_intakes["Items"]:
        nutrition_intakes_dynamodb_table.delete_item(
            Key={
                "Date": nutrition_intake["Date"],
                "FoodName": nutrition_intake["FoodName"]
            }
        )

    foods = foods_dynamodb_table.scan()
    for food in foods["Items"]:
        foods_dynamodb_table.delete_item(
            Key={
                "FoodName": food["FoodName"]
            }
        )

    nutrition_intakes = [
        {"Date": "04/28/2023", "FoodName": "Scrambled Eggs"},
        {"Date": "04/28/2023", "FoodName": "Whole Wheat Toast"},
        {"Date": "04/28/2023", "FoodName": "Grilled Chicken Salad"},
        {"Date": "04/28/2023", "FoodName": "Apple"},
        {"Date": "04/29/2023", "FoodName": "Spaghetti Bolognese"},
        {"Date": "04/29/2023", "FoodName": "Banana"},
        {"Date": "04/29/2023", "FoodName": "Mixed Nuts"},
        {"Date": "04/29/2023", "FoodName": "Caesar Salad"},
        {"Date": "04/30/2023", "FoodName": "Chocolate Chip Cookie"},
        {"Date": "04/30/2023", "FoodName": "Tofu Stir Fry"},
        {"Date": "04/30/2023", "FoodName": "Oatmeal with Berries"},
        {"Date": "04/30/2023", "FoodName": "Turkey Sandwich"},
        {"Date": "05/01/2023", "FoodName": "Greek Yogurt"},
        {"Date": "05/01/2023", "FoodName": "Brown Rice and Vegetables"},
        {"Date": "05/01/2023", "FoodName": "Salmon with Quinoa"},
        {"Date": "05/01/2023", "FoodName": "Avocado Toast"},
        {"Date": "05/02/2023", "FoodName": "Broccoli"},
        {"Date": "05/02/2023", "FoodName": "Grilled Cheese Sandwich"},
        {"Date": "05/02/2023", "FoodName": "Peanut Butter and Jelly Sandwich"},
        {"Date": "05/02/2023", "FoodName": "Baked Ziti"},
        {"Date": "05/03/2023", "FoodName": "Roasted Brussels Sprouts"},
        {"Date": "05/03/2023", "FoodName": "Garlic Bread"},
        {"Date": "05/03/2023", "FoodName": "Hummus and Pita"},
        {"Date": "05/03/2023", "FoodName": "Strawberry Smoothie"},
        {"Date": "05/04/2023", "FoodName": "Cucumber Salad"},
        {"Date": "05/04/2023", "FoodName": "Lentil Soup"},
        {"Date": "05/04/2023", "FoodName": "Mango"},
        {"Date": "05/04/2023", "FoodName": "Sushi Roll"},
        {"Date": "05/05/2023", "FoodName": "Grilled Asparagus"},
        {"Date": "05/05/2023", "FoodName": "Taco"},
        {"Date": "05/05/2023", "FoodName": "Garden Salad"},
        {"Date": "05/05/2023", "FoodName": "Cheeseburger"},
        {"Date": "05/06/2023", "FoodName": "Omelette"},
        {"Date": "05/06/2023", "FoodName": "Bagel with Cream Cheese"},
        {"Date": "05/06/2023", "FoodName": "Chicken Fajitas"},
        {"Date": "05/06/2023", "FoodName": "Quinoa and Black Bean Salad"},
        {"Date": "05/07/2023", "FoodName": "Blueberry Pancakes"},
        {"Date": "05/07/2023", "FoodName": "Spinach and Feta Stuffed Chicken"},
        {"Date": "05/07/2023", "FoodName": "Sweet Potato Fries"},
        {"Date": "05/07/2023", "FoodName": "Fruit Salad"},
        {"Date": "05/08/2023", "FoodName": "Breakfast Burrito"},
        {"Date": "05/08/2023", "FoodName": "Pesto Pasta"},
        {"Date": "05/08/2023", "FoodName": "Roasted Vegetables"},
        {"Date": "05/08/2023", "FoodName": "Greek Salad"},
        {"Date": "05/09/2023", "FoodName": "Granola with Yogurt"},
        {"Date": "05/09/2023", "FoodName": "Steak and Mashed Potatoes"},
        {"Date": "05/09/2023", "FoodName": "Green Beans"},
        {"Date": "05/09/2023", "FoodName": "Dark Chocolate"},
        {"Date": "05/10/2023", "FoodName": "Avocado and Egg Toast"},
        {"Date": "05/10/2023", "FoodName": "Grilled Shrimp"},
        {"Date": "05/10/2023", "FoodName": "Caprese Salad"},
        {"Date": "05/10/2023", "FoodName": "Raspberry Sorbet"}
    ]

    foods = [
        {"FoodName": "Scrambled Eggs", "Calories": 710, "Carbohydrates": 5, "Fat": 55, "Protein": 32},
        {"FoodName": "Whole Wheat Toast", "Calories": 290, "Carbohydrates": 46, "Fat": 6, "Protein": 12},
        {"FoodName": "Grilled Chicken Salad", "Calories": 560, "Carbohydrates": 40, "Fat": 28, "Protein": 43},
        {"FoodName": "Apple", "Calories": 95, "Carbohydrates": 25, "Fat": 0.3, "Protein": 0.5},
        {"FoodName": "Spaghetti Bolognese", "Calories": 880, "Carbohydrates": 110, "Fat": 33, "Protein": 40},
        {"FoodName": "Banana", "Calories": 105, "Carbohydrates": 27, "Fat": 0.4, "Protein": 1.3},
        {"FoodName": "Mixed Nuts", "Calories": 530, "Carbohydrates": 28, "Fat": 44, "Protein": 17},
        {"FoodName": "Caesar Salad", "Calories": 450, "Carbohydrates": 34, "Fat": 30, "Protein": 12},
        {"FoodName": "Chocolate Chip Cookie", "Calories": 200, "Carbohydrates": 22, "Fat": 10, "Protein": 2},
        {"FoodName": "Tofu Stir Fry", "Calories": 960, "Carbohydrates": 120, "Fat": 32, "Protein": 38},
        {"FoodName": "Oatmeal with Berries", "Calories": 340, "Carbohydrates": 61, "Fat": 7, "Protein": 9},
        {"FoodName": "Turkey Sandwich", "Calories": 480, "Carbohydrates": 50, "Fat": 12, "Protein": 34},
        {"FoodName": "Greek Yogurt", "Calories": 220, "Carbohydrates": 18, "Fat": 11, "Protein": 13},
        {"FoodName": "Brown Rice and Vegetables", "Calories": 600, "Carbohydrates": 120, "Fat": 4, "Protein": 12},
        {"FoodName": "Salmon with Quinoa", "Calories": 840, "Carbohydrates": 80, "Fat": 32, "Protein": 60},
        {"FoodName": "Avocado Toast", "Calories": 320, "Carbohydrates": 40, "Fat": 16, "Protein": 8},
        {"FoodName": "Broccoli", "Calories": 200, "Carbohydrates": 40, "Fat": 2.4, "Protein": 16},
        {"FoodName": "Grilled Cheese Sandwich", "Calories": 480, "Carbohydrates": 50, "Fat": 24, "Protein": 20},
        {"FoodName": "Peanut Butter and Jelly Sandwich", "Calories": 660, "Carbohydrates": 90, "Fat": 26, "Protein": 22},
        {"FoodName": "Baked Ziti", "Calories": 1110, "Carbohydrates": 147, "Fat": 36, "Protein": 57},
        {"FoodName": "Roasted Brussels Sprouts", "Calories": 168, "Carbohydrates": 33, "Fat": 3, "Protein": 12},
        {"FoodName": "Garlic Bread", "Calories": 540, "Carbohydrates": 66, "Fat": 24, "Protein": 12},
        {"FoodName": "Hummus and Pita", "Calories": 780, "Carbohydrates": 102, "Fat": 27, "Protein": 27},
        {"FoodName": "Strawberry Smoothie", "Calories": 450, "Carbohydrates": 108, "Fat": 1.5, "Protein": 6},
        {"FoodName": "Cucumber Salad", "Calories": 135, "Carbohydrates": 21, "Fat": 6, "Protein": 3},
        {"FoodName": "Lentil Soup", "Calories": 540, "Carbohydrates": 90, "Fat": 3, "Protein": 36},
        {"FoodName": "Mango", "Calories": 297, "Carbohydrates": 75, "Fat": 1.8, "Protein": 4.2},
        {"FoodName": "Sushi Roll", "Calories": 600, "Carbohydrates": 114, "Fat": 9, "Protein": 18},
        {"FoodName": "Grilled Asparagus", "Calories": 150, "Carbohydrates": 12, "Fat": 12, "Protein": 6},
        {"FoodName": "Taco", "Calories": 510, "Carbohydrates": 39, "Fat": 27, "Protein": 27},
        {"FoodName": "Garden Salad", "Calories": 135, "Carbohydrates": 21, "Fat": 1.5, "Protein": 3},
        {"FoodName": "Cheeseburger", "Calories": 900, "Carbohydrates": 96, "Fat": 42, "Protein": 51},
        {"FoodName": "Omelette", "Calories": 550, "Carbohydrates": 4, "Fat": 40, "Protein": 40},
        {"FoodName": "Bagel with Cream Cheese", "Calories": 450, "Carbohydrates": 56, "Fat": 18, "Protein": 12},
        {"FoodName": "Chicken Fajitas", "Calories": 700, "Carbohydrates": 50, "Fat": 30, "Protein": 55},
        {"FoodName": "Quinoa and Black Bean Salad", "Calories": 400, "Carbohydrates": 60, "Fat": 10, "Protein": 15},
        {"FoodName": "Chicken Alfredo", "Calories": 900, "Carbohydrates": 75, "Fat": 40, "Protein": 55},
        {"FoodName": "Blueberry Pancakes", "Calories": 650, "Carbohydrates": 90, "Fat": 20, "Protein": 15},
        {"FoodName": "Spinach and Feta Stuffed Chicken", "Calories": 650, "Carbohydrates": 10, "Fat": 30, "Protein": 80},
        {"FoodName": "Sweet Potato Fries", "Calories": 300, "Carbohydrates": 45, "Fat": 10, "Protein": 3},
        {"FoodName": "Fruit Salad", "Calories": 250, "Carbohydrates": 60, "Fat": 1, "Protein": 2},
        {"FoodName": "Pizza", "Calories": 1150, "Carbohydrates": 140, "Fat": 45, "Protein": 55},
        {"FoodName": "Breakfast Burrito", "Calories": 600, "Carbohydrates": 50, "Fat": 30, "Protein": 35},
        {"FoodName": "Pesto Pasta", "Calories": 900, "Carbohydrates": 100, "Fat": 45, "Protein": 25},
        {"FoodName": "Roasted Vegetables", "Calories": 200, "Carbohydrates": 30, "Fat": 5, "Protein": 5},
        {"FoodName": "Greek Salad", "Calories": 400, "Carbohydrates": 20, "Fat": 30, "Protein": 10},
        {"FoodName": "Ice Cream", "Calories": 400, "Carbohydrates": 50, "Fat": 20, "Protein": 8},
        {"FoodName": "Granola with Yogurt", "Calories": 450, "Carbohydrates": 60, "Fat": 15, "Protein": 20},
        {"FoodName": "Steak and Mashed Potatoes", "Calories": 800, "Carbohydrates": 40, "Fat": 45, "Protein": 55},
        {"FoodName": "Green Beans", "Calories": 100, "Carbohydrates": 20, "Fat": 0.5, "Protein": 2},
        {"FoodName": "Dark Chocolate", "Calories": 400, "Carbohydrates": 40, "Fat": 24, "Protein": 4},
        {"FoodName": "Pulled Pork Sandwich", "Calories": 850, "Carbohydrates": 60, "Fat": 35, "Protein": 55},
        {"FoodName": "Avocado and Egg Toast", "Calories": 450, "Carbohydrates": 35, "Fat": 25, "Protein": 20},
        {"FoodName": "Grilled Shrimp", "Calories": 300, "Carbohydrates": 2, "Fat": 6, "Protein": 60},
        {"FoodName": "Caprese Salad", "Calories": 300, "Carbohydrates": 10, "Fat": 20, "Protein": 18},
        {"FoodName": "Raspberry Sorbet", "Calories": 150, "Carbohydrates": 37, "Fat": 0, "Protein": 1},
        {"FoodName": "Lasagna", "Calories": 900, "Carbohydrates": 80, "Fat": 40, "Protein": 45}
    ]

    for nutrition_intake in nutrition_intakes:
        nutrition_intakes_dynamodb_table.put_item(
            Item=nutrition_intake
        )

    for food in foods:
        foods_dynamodb_table.put_item(
            Item={
                "FoodName": food["FoodName"], 
                "Calories": decimal.Decimal(str(food["Calories"])), 
                "Carbohydrates": decimal.Decimal(str(food["Carbohydrates"])), 
                "Fat": decimal.Decimal(str(food["Fat"])), 
                "Protein": decimal.Decimal(str(food["Protein"]))
            }
        )

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        populate_database()
