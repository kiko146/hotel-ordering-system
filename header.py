def inject_header_data():
    # Shared navigation data for every template.
    return {'navigation_links': [
        ('Home', 'home'), ('Menu', 'menu.menu_page'), ('About', 'about'),
        ('Customer Service', 'customer_service')
    ]}
