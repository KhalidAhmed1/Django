from django.shortcuts import render


def food_catalog(request):
    foods = [
        {'id': 1, 'name': 'Beef Burger',        'category': 'Fast Food',    'price': 120, 'available': True},
        {'id': 2, 'name': 'Pepperoni Pizza',     'category': 'Fast Food',    'price': 160, 'available': True},
        {'id': 3, 'name': 'Chicken Shawarma',    'category': 'Street Food',  'price': 85,  'available': True},
        {'id': 4, 'name': 'Falafel Wrap',        'category': 'Street Food',  'price': 55,  'available': False},
        {'id': 5, 'name': 'Grilled Salmon',      'category': 'Seafood',      'price': 250, 'available': True},
        {'id': 6, 'name': 'Shrimp Pasta',        'category': 'Seafood',      'price': 200, 'available': False},
        {'id': 7, 'name': 'Chocolate Lava Cake', 'category': 'Dessert',      'price': 75,  'available': True},
        {'id': 8, 'name': 'Mango Cheesecake',    'category': 'Dessert',      'price': 90,  'available': True},
    ]

    keyword  = request.GET.get('keyword', '').lower().strip()
    category = request.GET.get('category', '').strip()

    results = foods

    if keyword:
        results = [f for f in results if keyword in f['name'].lower()]

    if category and category != 'All':
        results = [f for f in results if f['category'] == category]

    all_categories = sorted(set(f['category'] for f in foods))

    context = {
        'foods':             results,
        'categories':        all_categories,
        'keyword':           keyword,
        'selected_category': category,
    }

    return render(request, 'menu.html', context)