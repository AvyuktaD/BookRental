from pymongo import MongoClient
import random
#from bson import ObjectId

URL = "mongodb://localhost:27017/book"

try:
    client = MongoClient(URL)
    db = client.get_database()
    print("Connection successful!")

except Exception as e:
    print("Connection failed:", e)
    

def read(collection, query, specific_valuee):
    try:
        a = []
        #, "$options": "i"
        #result = collection.find({specific_valuee: {"$regex": query, "$options": "i"}})
        result = collection.find({'title':{'$regex':f'^{query}'}})
        for doc in result:
            a.append(doc[specific_valuee])

        for ei in a:
            if query in ei:
                print(ei)

    except Exception as e:
        print(f"There was an error: {e}")

def rent_A_Book(allbooks,userDB,rentedBooks,newDoc,specificvalue):
    try:
        result = rentedBooks.find({specificvalue : newDoc})
        findUser = userDB.find({"ID" : 1})
        findBook = allbooks.find({specificvalue : newDoc})

        if result:
            print("Book is already rented")

        elif findBook:
            print("We don't have your book")

        else:
            
            if findUser:
                insert_result = rentedBooks.insert_one({specificvalue : newDoc,"ID" : 1})
                print(f"Inserted doc ID: {insert_result}")
            else:
                print("You need to sign up")

    except Exception as e:
        print(f"There was an error {e}")

def return_Book(rentedbooksCollection,query):
    try:
        rentedbooksCollection.delete_one(query)
    except Exception as e:
        print(f"There was an error: {e}")

def generate_UserID(userCollection):
    try:
        
        num1 = random.randint(0,9)
        num2 = random.randint(0,9)
        num3 = random.randint(0,9)
        num4 = random.randint(0,9)
        num5 = random.randint(0,9)
        num6 = random.randint(0,9)

        numbers = [num1,num2,num3,num4,num5,num6]

        ud = [str(num) for num in numbers]

        userID = ud[0] + ud[1] + ud[2] + ud[3] + ud[4] + ud[5]

        findUserID = userCollection.find({"ID": userID})

        return userID
    except Exception as e:
        print(f"There was an error {e}") 

def SignUp(userCollection,email,number):
    try:
        e = userCollection.find({"email":email}) 
        n = userCollection.find({"number" : number})

        if n == True or e == True:
            print("You've already signed up here before with this email or number")
        else:
            userID = 1
            userInfo = {"email":email,"number" : number, "ID" : userID}
            userCollection.insert_one({"email":email,"number" : number, "ID" : userID})
            print("Inserted user info")
            del(userInfo,e,n,userID)

    except Exception as e:
        print(f"There was an error function SIgn up: {e}")

# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher

try:
    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    userDB = db["user"]

    #SignUp(userDB,"afkldafdsf@gmail.com","123-456-7890")
    rent_A_Book(allbooks,userDB,rentedBooks,"A Short History of Nearly Everything","title")

except Exception as e:
    print(f"There was an error {e}")