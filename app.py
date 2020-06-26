
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)


def createNotionMeetingNote(token, collectionURL, data):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    
    row.title = data.get('title')
    #row.person = data.get('person')
    #row.date = data.get('date')
    #row.mood = data.get('mood')
    #row.tags = data.get('tags')
    #row.type = data.get('type')
    #row.interviewer = data.get('interviewer')

@app.route('/meeting_notes', methods=['POST'])
def create_meeting_note():
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionMeetingNote(token_v2, url, request.form)
    return f'added meeting note to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
