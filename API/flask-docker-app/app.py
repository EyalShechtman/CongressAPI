from flask import Flask, jsonify, request
import pandas as pd

class CongressAPI:
    def __init__(self, bills_file, people_file, votes_file):
        self.app = Flask(__name__)
        self.bills_file = bills_file
        self.peoples_file = people_file
        self.votes_file = votes_file

        self.bills_data = self.read_csv_with_pandas(self.bills_file)
        self.peoples_data = self.read_csv_with_pandas(self.peoples_file)
        self.votes_data = self.read_csv_with_pandas(self.votes_file)

        self.setup_routes()

    def read_csv_with_pandas(self, file_path):
        return pd.read_csv(file_path)

    def setup_routes(self):
        @self.app.route('/bills', methods=['GET'])
        def get_bills():
            return jsonify(self.bills_data.to_dict(orient='records'))

        @self.app.route('/bills/filter', methods=['GET'])
        def filter_bills():
            column = request.args.get('column')
            value = request.args.get('value')
            if column and value:
                filtered_data = self.bills_data[self.bills_data[column] == value]
                return jsonify(filtered_data.to_dict(orient='records'))
            else:
                return jsonify({'error': 'Please provide both column and value query parameters'}), 400

        @self.app.route('/bills/<int:bill_id>', methods=['GET'])
        def get_bill(bill_id):
            bill = self.bills_data[self.bills_data['bill_id'] == bill_id]
            if not bill.empty:
                return jsonify(bill.to_dict(orient='records')[0])
            else:
                return jsonify({'error': 'Bill not found'}), 404
        
        @self.app.route('/bills/keywords', methods=['GET'])
        def get_bill_keywords():
            keywords = request.args.getlist('keyword')
            if not keywords:
                return jsonify({'error': 'Please provide at least one keyword as a query parameter'}), 400

            bills = self.bills_data
            relevant_bills = bills[bills['description'].str.contains('|'.join(keywords), case=False, na=False)]

            if not relevant_bills.empty:
                return jsonify(relevant_bills.to_dict(orient='records'))
            else:
                return jsonify({'error': f'No bills found containing the keywords: {", ".join(keywords)}'}), 404
            
        @self.app.route('/people', methods = ['GET'])
        def get_peoples():
            return jsonify(self.peoples_data.to_dict(orient = 'records'))

        @self.app.route('/people/<int:person_id>', methods = ['GET'])
        def people_name(person_id):
            person = self.peoples_data[self.peoples_data['people_id'] == person_id]
            if not person.empty:
                return jsonify(person.to_dict(orient='records')[0])
            else:
                return jsonify({'error': 'Person not found'}), 404
            
        @self.app.route('/votes', methods = ['GET'])
        def get_votes():
            return jsonify(self.votes_data.to_dict(orient='records'))

        @self.app.route('/votes/<int:person_id>', methods = ['GET'])
        def get_people_votes(person_id):
            votes = self.votes_data[self.votes_data['people_id'] == person_id]

            if not votes.empty:
                return jsonify(votes.to_dict(orient='records')[0])
            else:
                return jsonify({'error': 'person not found'}), 404



    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == '__main__':
    bill_api = CongressAPI('csv/bills.csv','csv/votes.csv', 'csv/people.csv')
    bill_api.run()
