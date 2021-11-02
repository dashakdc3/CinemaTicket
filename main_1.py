import sqlite3
import webbrowser
import random
import string
from fpdf import FPDF


class User:
    def __init__(self, name):
        self.n = name

    def buy(self, seat, card, ticket, fprice):
        if seat.is_free():
            if card.validate(price=fprice):
                if seat.occupy():
                    return ticket.to_pdf()
                else:
                    return False
        else:
            print("Seat is taken!")
            return False


class Seat:
    databaseSeat = "cinema.db"

    def __init__(self, seat_id):
        self.si = seat_id

    def get_price(self):
        with sqlite3.connect("cinema.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM "Seat"
                """)
            all = cursor.fetchall()
            for a in all:
                if a[0] == self.si:
                    return a[2]

    def is_free(self):
        with sqlite3.connect("cinema.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM "Seat"
                """)
            all_seat = cursor.fetchall()
            for a in all_seat:
                if a[0] == self.si:
                    if a[1] == 1:
                        return False
                    elif a[1] == 0:
                        return True

    def occupy(self):
        if self.is_free():
            with sqlite3.connect("cinema.db") as connection:
                connection.execute("""
                                UPDATE "Seat" SET "taken"=1 WHERE "seat_id" =?
                                """, [self.si])
                connection.commit()
                return True
        else:
            return False


class Card:
    databaseCard = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.t = type
        self.n = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM "Card"
                """)
            all = cursor.fetchall()
            for a in all:
                if a[2] == self.cvc:
                    if a[4] >= price:
                        result = int(a[4]) - price
                        with sqlite3.connect("banking.db") as conn:
                            conn.execute("""
                            UPDATE "Card" SET "balance"=? WHERE "cvc" =?
                                                    """, [result, self.cvc])
                            conn.commit()
                            return True
                    else:
                        print("Non-sufficient funds (NSF)")
                        return False
                else:
                    print("Invalid cvc")
                    return False


class Ticket:
    def __init__(self, id, user, price, seat_number):
        self.id = id
        self.user = user
        self.price = price
        self.seat_n = seat_number

    def to_pdf(self, path="ticket.pdf"):
        pdf = FPDF(orientation='P', unit="pt", format="A4")
        pdf.add_page()
        # Create title
        pdf.set_font(family="Times", size=24, style="B")
        pdf.cell(w=0, h=80, txt="Ticket",
                 border=1, align="C", ln=1)

        # insert first parameter
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=100, h=25, txt="Name:", border=1)
        pdf.cell(w=0, h=25, txt=str(self.user), border=1, ln=1)
        # insert second parameter
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=100, h=25, txt="Ticket id:", border=1)
        pdf.cell(w=0, h=25, txt=str(self.id), border=1, ln=1)
        # insert third parameter
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=100, h=25, txt="Price:", border=1)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        # insert fourth parameter
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=100, h=25, txt="Seat Number:", border=1)
        pdf.cell(w=0, h=25, txt=str(self.seat_n), border=1, ln=1)
        pdf.output(path)
        print("Purchase successful!")
        webbrowser.open(path)


user = User(name=input("Your name: "))
user1 = user.n

seat_id1 = Seat(seat_id=input("Preferred seat number: "))
seat1 = seat_id1.si
fseat = seat_id1

type1 = input("Card type: ")
number1 = input("Card number: ")
cvc1 = input("Card cvc: ")
holder1 = input("Card holder name: ")

fprice = fseat.get_price()
free = fseat.is_free()

fcard = Card(type=type1, number=number1, cvc=cvc1, holder=holder1)
random = "".join(random.choices(string.ascii_letters + string.digits, k=7))
ticket = Ticket(id=random, user=user1, price=fprice, seat_number=seat1)

user.buy(seat=seat_id1, card=fcard, ticket=ticket, fprice=fprice)

# Marry Smith Master Card 23456789
