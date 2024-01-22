from models import Client, Account, Transaction, Card, db
from faker import Faker
from app import app 

fake = Faker()

with app.app_context():
    clients = [
        Client(username=fake.user_name(), password=fake.password(), email=fake.email(), phone_number=fake.phone_number(), date_joined=fake.date_time_this_decade()) for _ in range(10)
    ]

    db.session.add_all(clients)
    db.session.commit()

    accounts = []
    for client in clients:
        for _ in range(10):
            account = Account(account_number=fake.random_int(min=1000000000, max=9999999999), balance=fake.pyfloat(), account_type=fake.random_element(elements=('savings', 'checking')), opened_at=fake.date_time_this_decade(), client=client)
            accounts.append(account)

    db.session.add_all(accounts)
    db.session.commit()

    transactions = []
    for account in accounts:
        for _ in range(10):
            transaction = Transaction(
                amount=fake.pyfloat(),
                transaction_type=fake.random_element(elements=('credit', 'debit')),
                description=fake.text(),
                timestamp=fake.date_time_this_decade(),
                account_id=account.id 
            )
            transactions.append(transaction)

    cards = []
    for client in clients:
        for _ in range(10):
            card = Card(
                card_number=fake.credit_card_number(),
                expiration_date=fake.future_date(end_date='+5y'),
                cvv=fake.credit_card_security_code(),
                card_type=fake.random_element(elements=('visa', 'mastercard')),
                client_id=client.id
            )
            cards.append(card)

    db.session.add_all(transactions + cards)
    db.session.commit()
