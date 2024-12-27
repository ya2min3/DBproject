import psycopg2 

#connect to postgresql database with user account information.
conn = psycopg2.connect(database="db", user="jass", host="localhost", password="Vomobdd23_")

#we will run SQL queries througout the code using the variable `cursor'.
cursor = conn.cursor()

#a first example query: we wanna retrieve all the jobs proposed in the offers:
cursor.execute("""SELECT distinct designation FROM jobs ORDER BY designation ASC;""") 
conn.commit() 

#we retrieve the answer to the previous query in the variable `rows'.
rows = cursor.fetchall()

#the variable `rows' is a list, where rows[i] is the i-th line of the query answer.
#we print it line by line.
print("Printing rows line by line.")
i = 0
while i < len(rows):
    print("Line ", i, "is: ", rows[i])
    i = i + 1
