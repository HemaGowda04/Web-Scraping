from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Connect to the SQLite database
engine = create_engine('sqlite:///reviews.db')

@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.json
    review = data.get('review', '')
    # Assume there's some sentiment analysis logic here
    return jsonify({"sentiment": "Positive"})

@app.route('/reviews', methods=['GET'])
def reviews():
    color = request.args.get('color', '')
    style = request.args.get('style', '')
    
    # Load the data from the database
    df = pd.read_sql('SELECT * FROM reviews', con=engine)
    
    # Filter data based on query parameters
    if color != 'N/A':
        df = df[df['Color'].str.contains(color, na=False)]
    if style != 'N/A':
        df = df[df['Style'].str.contains(style, na=False)]
    
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)

