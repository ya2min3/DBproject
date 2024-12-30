#used to create sql insert statements from csv file
import csv
# Open the CSV file
with open('jobs.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, quotechar='"', skipinitialspace=True)  # Use quotechar to handle quotes in fields
    next(csvfile)
    # Read each row
    for row in reader:
        # Start the SQL line
        insert_line = f"INSERT INTO Jobs VALUES ("
        # Escape and format each item in the row
        escaped_items = []
        for item in row:
            # Escape single quotes in the data by doubling them
            escaped_item = item.replace("'", "''")
            # Wrap the item in single quotes
            escaped_items.append(f"'{escaped_item}'")

        # Join all escaped items and complete the SQL statement
        insert_line += ", ".join(escaped_items)
        insert_line += ");"

