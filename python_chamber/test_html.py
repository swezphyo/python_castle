def print_ul(elements):
    print("<ul>")
    for s in elements:
        ul = "<li>" + str(s) + "</li>"
        print(ul)
    print("</ul>")

toppings = ['mushrooms', 'peppers', 'pepparoni', 'steak', 'walnuts', 'goat cheese', 'eggplant', 'garlic sauce'];
print_ul(toppings)