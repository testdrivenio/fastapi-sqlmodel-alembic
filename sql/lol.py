import csv

with open('./mock_data.csv', mode='r') as csv_file, open('mock_products.csv', mode='w') as employee_file:
    csv_reader = csv.DictReader(csv_file)
    field_names = next(csv_reader).keys()
    employee_writer = csv.DictWriter(employee_file, fieldnames=field_names)
    elements = set()
    temp = []
    for row in csv_reader:

        if (name := row.get('name')) in elements:
            print("Duplicate", name)
        else:

            temp.append({**row, 'price': row.get('price').strip('$')})

        elements.add(name)
    employee_writer.writeheader()
    employee_writer.writerows(temp)
