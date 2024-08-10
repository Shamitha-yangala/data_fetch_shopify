from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# In-memory storage for processed data as a dictionary
processed_data = {}

# Replace with your actual Printful API key
# PRINTFUL_API_KEY = 'printful_api_key'
PRINTFUL_API_KEY = 'RZ1f8r0fHnwS9nJ2mZkDH5WpKnnnyNdyjm8NVjwK'

# Set up headers for authentication
headers = {
    'Authorization': f'Bearer {PRINTFUL_API_KEY}'
}

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    try:
        # Send a request to the Printful API to fetch orders
        response = requests.get('https://api.printful.com/orders', headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        orders = response.json().get('result', [])
        
        # Process the fetched orders data
        global processed_data
        processed_data = process_data(orders)
        
        return render_template('display.html', data=processed_data)

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

def process_data(data):
    # Store data in a dictionary format
    result = {}
    for order in data:
        order_id = order['id']
        order_status = order['status']
        result[order_id] = order_status  # Store order status by order ID
    return result

@app.route('/get-processed-data', methods=['GET'])
def get_processed_data():
    return render_template('display.html', data=processed_data)

if __name__ == '__main__':
    app.run(debug=True)
