
ROUTE_NAME = 'VARCHAR(120)'
ROUTE_GRADE = 'VARCHAR(15)'
USER_ID = 'VARCHAR(40)'
FULL_LOCATION = 'VARCHAR(150)'

routes = {
    'dict_name': 'routes',
    'name': ROUTE_NAME,
    'grade': ROUTE_GRADE,
    'area': 'VARCHAR(60)',
    'crag': 'VARCHAR(60)',
    'full_location': FULL_LOCATION,
    'wall': 'VARCHAR(60)',
    'unkey': 'VARCHAR(270) UNIQUE KEY'
}

ticks = {
    'dict_name': 'ticks',
    'id': 'VARCHAR(80) UNIQUE KEY',
    'route_name': ROUTE_NAME,
    'location': FULL_LOCATION,
    'date': 'VARCHAR(20)',
    'style': 'VARCHAR(20)',
    'lead_style': 'VARCHAR(20)',
    'notes': 'VARCHAR(100)',
    'user_id': USER_ID
}

users = {
    'dict_name': 'users',
    'id': USER_ID,
    'name': 'VARCHAR(30)'
}

grades = {
    'dict_name': 'grades',
    'integer_grade': 'TINYINT(2) UNIQUE KEY',
    'route_grade': ROUTE_GRADE
}

tables = [routes, ticks, users, grades]

grade = {'2': '5.2',
         '3': '5.3',
         '4': '5.4',
         '5': '5.5',
         '6': '5.6',
         '7': '5.7',
         '8': '5.8',
         '9': '5.9',
         '10': '5.10a',
         '11': '5.10b',
         '12': '5.10c',
         '13': '5.10d',
         '14': '5.11a',
         '15': '5.11b',
         '16': '5.11c',
         '17': '5.11d'
         }

grade_modifiers = ['+', '-', '/']

display_grade = {
    '7': '5.7',
    '8': '5.8',
    '9': '5.9',
    '10': '5.10a',
    '11': '5.10b',
    '12': '5.10c',
    '13': '5.10d',
}

default_param_dict = {'name_selected': '',
                      'crag': 'all',
                      'view': 'all',
                      'exact_match': 'false',
                      'name_to_search': '',
                      'grade': '9',
                      'all_grades': display_grade,
                      'area': 'Rumney',
                      'user': ''
                      }
header_row = ["Route", "Grade", "Date", "Style", "Lead Style", "Notes"]

bishop = '''https://www.mountainproject.com/route-finder-export?selectedIds=106064825
            &type=rock&diffMinrock=1000&diffMinboulder=20000&diffMinaid=70000&diffMinice=30000
            &diffMinmixed=50000&diffMaxrock=12400&diffMaxboulder=20050&diffMaxaid=75260
            &diffMaxice=38500&diffMaxmixed=60000&is_sport_climb=1&is_top_rope=1&stars=0
            &pitches=1&sort1=popularity+desc&sort2=rating'''
rumney = '''https://www.mountainproject.com/route-finder-export?type=rock
           &diffMinrock=1000&diffMinboulder=20000&diffMinaid=70000&diffMinice=30000
           &diffMinmixed=50000&diffMaxrock=12400&diffMaxboulder=20050&diffMaxaid=75260
           &diffMaxice=38500&diffMaxmixed=60000&is_sport_climb=1&stars=0
           &pitches=0&selectedIds=105867829'''
areas = [rumney, bishop]
ticks_url = 'https://www.mountainproject.com/user/7027752/susan-jensen/tick-export'
