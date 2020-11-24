from bin import world

cases = [
    'USA', 'New York', 'Manhattan, NY', 'California', 'Berlin', 'Berlin Hauptbahnhof', 'Braunschweig',
    'Gabelsbergerstraße 38118 Braunschweig'
]

for case in cases:
    print(world.main(case))
