dishes = [
    {"name": "Burger", "price": "$8.99"},
    {"name": "Pizza", "price": "$12.49"},
    {"name": "Chicken Wings", "price": "$10.99"},
    {"name": "Fish Fry", "price": "$14.99"},
    {"name": "Steak Dinner", "price": "$24.99"},
    {"name": "Salad", "price": "$6.49"},
    {"name": "Sandwich", "price": "$7.49"},
    {"name": "Soup", "price": "$4.99"},
    {"name": "Fries", "price": "$2.99"},
    {"name": "Breadsticks", "price": "$3.99"},
    {"name": "Milkshake", "price": "$5.49"},
    {"name": "Ice Cream", "price": "$4.99"},
    {"name": "Waffles", "price": "$8.49"},
    {"name": "Eggs Benedict", "price": "$9.99"},
    {"name": "Breakfast Burrito", "price": "$6.99"},
    {"name": "Chicken Quesadilla", "price": "$7.99"},
    {"name": "Grilled Cheese", "price": "$5.49"},
    {"name": "Falafel Wrap", "price": "$6.99"},
    {"name": "Tacos", "price": "$8.49"}
    ]

total_order_list = list()
bill = 0

def order_list(order):
    global bill
    for dish in dishes:
        if order.lower() == dish["name"].lower():
            price = float(dish["price"].replace("$",""))
            total_order_list.append((dish["name"],price))
            bill += price


action = input("order or quit: ")
while True:
    if action == "order":
        order_list(input("order: "))
        print(total_order_list)
        print(f"Total Bill: ${bill:.2f}")
    elif action == "quit":
        break
