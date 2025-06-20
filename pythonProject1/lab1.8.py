date_str = '2025-12-31'
date_parts = date_str.split('-')
date_dict = {
    'year': date_parts[0],
    'month': date_parts[1],
    'day': date_parts[2]
}
print(date_dict)  # {'year': '2025', 'month': '12', 'day': '31'}