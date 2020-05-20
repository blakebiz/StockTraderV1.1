import mysql.connector, datetime


def main():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='44michigan',
        database='testdatabase'
    )
    mycursor = db.cursor()

    # mycursor.execute(
    #     "CREATE TABLE Person (name VARCHAR (50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)"
    #     )

    # mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Tim", 19))
    #
    # db.commit()

    # mycursor.execute("SELECT * FROM Person")
    #


    # mycursor.execute("CREATE TABLE Test (name varchar(50), created datetime, gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

    # mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)", ("Sarah", datetime.datetime.now(), "F"))
    #
    # db.commit()

    #mycursor.execute("SELECT id, name FROM Test WHERE gender = 'M' ORDER BY id ASC") #ASC or DESC for ascending or descinding order

    # mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")
    mycursor.execute("ALTER TABLE Test DROP COLUMN food")
    mycursor.execute("DESCRIBE Test")
    # print(mycursor.fetchone) #gets only first one, can use fetchmany to get a list of x length


    for x in mycursor:
        print(x)


if __name__ == '__main__':
    main()


