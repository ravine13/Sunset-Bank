from flask import Flask, make_response, jsonify, request,Blueprint
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Client, Account, Transaction, Card, db


main_bp = Blueprint('main',__name__)

app = Flask(__name__)


api = Api(main_bp)
ma = Marshmallow(main_bp)


@main_bp.route('/')
def home():
    return 'welcome to sunset banking system'

class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client

client_schema = ClientSchema()

class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account

account_schema = AccountSchema()

class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction

transaction_schema = TransactionSchema()


class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Card

card_schema = CardSchema()


patch_args = reqparse.RequestParser(bundle_errors=True)
patch_args.add_argument('username', type=str, help='Username of the Client')
patch_args.add_argument('email', type=str, help='Email of the Client')
patch_args.add_argument('phone_number', type=str, help='Phone number of the Client')


client_post_args = reqparse.RequestParser(bundle_errors=True)
client_post_args.add_argument('username', type=str, required=True, help='Username of the Client is required')
client_post_args.add_argument('password', type=str, required=True, help='Password of the Client is required')
client_post_args.add_argument('email', type=str, required=True, help='Email of the Client is required')
client_post_args.add_argument('phone_number', type=str, help='Phone number of the Client')


transaction_post_args = reqparse.RequestParser(bundle_errors=True)
transaction_post_args.add_argument('amount', type=float, required=True, help='Amount of the Transaction is required')
transaction_post_args.add_argument('transaction_type', type=str, required=True, help='Type of the Transaction is required')
transaction_post_args.add_argument('description', type=str, help='Description of the Transaction')
transaction_post_args.add_argument('account_id', type=int, required=True, help='Account ID of the Transaction is required')

card_post_args = reqparse.RequestParser(bundle_errors=True)
card_post_args.add_argument('card_number', type=str, required=True, help='Card number is required')
card_post_args.add_argument('expiration_date', type=str, required=True, help='Expiration date of the Card is required')
card_post_args.add_argument('cvv', type=str, required=True, help='CVV of the Card is required')
card_post_args.add_argument('card_type', type=str, required=True, help='Type of the Card is required')
card_post_args.add_argument('client_id', type=int, required=True, help='Client ID of the Card is required')

card_patch_args = reqparse.RequestParser(bundle_errors=True)
card_patch_args.add_argument('card_number', type=str, help='New card number')
card_patch_args.add_argument('expiration_date', type=str, help='New expiration date of the Card')
card_patch_args.add_argument('cvv', type=str, help='New CVV of the Card')
card_patch_args.add_argument('card_type', type=str, help='New type of the Card')


class Clients(Resource):
    def get(self):
        clients = Client.query.all()
        res = client_schema.dump(clients,many = True)

        response = make_response(
            jsonify(res),
            200
        )

        return response
api.add_resource(Clients, '/clients')

class ClientByID(Resource):
    def get(self, id):
        client = Client.query.filter_by(id=id).first()

        if client is None:
            response = make_response(
                jsonify({"Error": "Client does not exist"}),
                404
            )
            return response
        else:
            client_data = client_schema.dump(client)
            transactions = Transaction.query.join(Account, Transaction.account_id == Account.id).filter(Account.client_id == id).all()
            client_data['transactions'] = transaction_schema.dump(transactions, many=True)
            response = make_response(
                jsonify(client_data),
                200
            )
            return response
    def patch(self, id):
        args = patch_args.parse_args()
        client = Client.query.get(id)
        if client is None:
            response = make_response(
                jsonify({"Error": "Client does not exist"}),
                404
            )
        else:
            if args['username']:
                client.username = args['username']
            if args['email']:
                client.email = args['email']
            if args['phone_number']:
                client.phone_number = args['phone_number']
            db.session.commit()

            response = make_response(
                jsonify({"Success": "Client updated"}),
                200
            )
        return response
    def delete(self, id):
        client = Client.query.get(id)
        if client is None:
            response = make_response(
                jsonify({"Error": "Client does not exist"}),
                404
            )
        else:
            transactions = Transaction.query.join(Account, Transaction.account_id == Account.id).filter(Account.client_id == id).all()
            for transaction in transactions:
                db.session.delete(transaction)

            db.session.delete(client)
            db.session.commit()

            response = make_response(
                jsonify({"Success": "Client and associated transactions deleted"}),
                200
            )
        return response

api.add_resource(ClientByID, '/client/<int:id>')

class ClientOnlyByID(Resource):
    def get(self, id):
        client = Client.query.get(id)

        if client is None:
            response = make_response(
                jsonify({"Error": "Client does not exist"}),
                404
            )
            return response
        else:
            response = make_response(
                jsonify(client_schema.dump(client)),
                200
            )
            return response

api.add_resource(ClientOnlyByID, '/Client/<int:id>')

class CardAll(Resource):
    def get(self):
        cards = Card.query.all()
        response = make_response(
            jsonify(card_schema.dump(cards, many=True)),
            200
        )
        return response

class CardOne(Resource):
    def get(self, id):
        card = Card.query.get(id)

        if card is None:
            response = make_response(
                jsonify({"Error": "Card does not exist"}),
                404
            )
            return response
        else:
            response = make_response(
                jsonify(card_schema.dump(card)),
                200
            )
            return response
    def patch(self, id):
        args = card_patch_args.parse_args()
        card = Card.query.get(id)
        if card is None:
            response = make_response(
                jsonify({"Error": "Card does not exist"}),
                404
            )
        else:
            if args['card_number']:
                card.card_number = args['card_number']
            if args['expiration_date']:
                card.expiration_date = args['expiration_date']
            if args['cvv']:
                card.cvv = args['cvv']
            if args['card_type']:
                card.card_type = args['card_type']
            db.session.commit()

            response = make_response(
                jsonify({"Success": "Card updated"}),
                200
            )
        return response
    def delete(self, id):
        card = Card.query.get(id)
        if card is None:
            response = make_response(
                jsonify({"Error": "Card does not exist"}),
                404
            )
        else:
            db.session.delete(card)
            db.session.commit()

            response = make_response(
                jsonify({"Success": "Card deleted"}),
                200
            )
        return response

api.add_resource(CardAll, '/cards')
api.add_resource(CardOne, '/card/<int:id>')

class AccountAll(Resource):
    def get(self):
        accounts = Account.query.all()
        response = make_response(
            jsonify(account_schema.dump(accounts, many=True)),
            200
        )
        return response

class AccountOne(Resource):
    def get(self, id):
        account = Account.query.get(id)

        if account is None:
            response = make_response(
                jsonify({"Error": "Account does not exist"}),
                404
            )
            return response
        else:
            response = make_response(
                jsonify(account_schema.dump(account)),
                200
            )
            return response
    def delete(self, id):
        account = Account.query.get(id)
        if account is None:
            response = make_response(
                jsonify({"Error": "Account does not exist"}),
                404
            )
        else:
            transactions = Transaction.query.filter_by(account_id=id).all()
            for transaction in transactions:
                db.session.delete(transaction)

            db.session.delete(account)
            db.session.commit()

            response = make_response(
                jsonify({"Success": "Account and associated transactions deleted"}),
                200
            )
        return response

api.add_resource(AccountAll, '/accounts')
api.add_resource(AccountOne, '/account/<int:id>')


class newUser(Resource):
    def post(self):
        args = client_post_args.parse_args()
        new_client = Client(username=args['username'], password=args['password'], email=args['email'], phone_number=args['phone_number'])
        db.session.add(new_client)
        db.session.commit()

        response = make_response(
            jsonify({"Success": "New client created"}),
            201
        )
        return response

api.add_resource(newUser, '/new_user')

class newTranscation(Resource):
    def post(self):
        args = transaction_post_args.parse_args()
        new_transaction = Transaction(amount=args['amount'], transaction_type=args['transaction_type'], description=args['description'], account_id=args['account_id'])
        db.session.add(new_transaction)
        db.session.commit()

        response = make_response(
            jsonify({"Success": "New transaction created"}),
            201
        )
        return response

api.add_resource(newTranscation, '/new_transactions')

class newCard(Resource):
    def post(self):
        args = card_post_args.parse_args()
        new_card = Card(card_number=args['card_number'], expiration_date=args['expiration_date'], cvv=args['cvv'], card_type=args['card_type'], client_id=args['client_id'])
        db.session.add(new_card)
        db.session.commit()

        response = make_response(
            jsonify({"Success": "New card created"}),
            201
        )
        return response

api.add_resource(newCard, '/new_card')