import dateutil.parser
import requests
import dateutil
import io

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from generator import generate_docx

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

BASE_URL = 'https://lgv-cw-st.church.tools/api'
SESSION = requests.Session()

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    response = SESSION.post(f"{BASE_URL}/login", json=request.get_json())
    return response.json(), response.status_code

@app.route('/events', methods=['GET'])
def events():
    """Fetch and filter events."""
    response = SESSION.get(f"{BASE_URL}/events")
    if response.status_code == 200:
        events = [
            {
                "id": event['id'],
                "name": event['name'],
                "date": dateutil.parser.parse(event['startDate']).strftime("%d.%m.%Y")
            }
            for event in response.json().get('data', [])
            if event['name'] == 'Gottesdienst -FESN'
        ]
        return {'data': events}, 200
    return {'message': response.json().get('message', 'Something went wrong')}, response.status_code

@app.route('/events/<int:event_id>/agenda', methods=['GET'])
def event_agenda(event_id):
    """Generate and return the agenda document for a specific event."""

    # Requests for event and agenda data
    event_response = SESSION.get(BASE_URL + f'/events/{event_id}')
    agenda_response = SESSION.get(BASE_URL + f'/events/{event_id}/agenda')

    # Check if the requests were successful
    if (agenda_response.status_code != 200):
        return agenda_response.json(), agenda_response.status_code
    if (event_response.status_code != 200):
        return event_response.json(), event_response.status_code

    # Generate the agenda document
    doc = generate_docx(event_response.json(), agenda_response.json())

    # Save the document to a BytesIO object
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)

    # Set the appropriate headers for the response
    return send_file(
        bio,
        as_attachment=True,
        download_name='agenda.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


if __name__ == '__main__':
    app.run()