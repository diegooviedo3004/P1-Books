import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://nnobexbojluqje:65098c7989898e4d99ab8b9ae8a7d2b662b7a9f0060ec82df352a42d501fab8e@ec2-54-157-79-121.compute-1.amazonaws.com:5432/d1imfg7f6knr49')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                  {"isbn": isbn, "title": title, "author": author, "year": year})
        print('Añadido')
    db.commit()

if __name__ == "__main__":
    main()

    # db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
    #                 {"origin": origin, "destination": destination, "duration": duration})
    #     print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")