import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import datetime

app = Flask(__name__)

def dump(obj):
    str = ''
    for attr in dir(obj):
        str = str + ("obj.%s = %r" % (attr, getattr(obj, attr))) + "\n"
    return str

def createNotionMeetingNote(token, collectionURL, data):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    
    row.title = data.get('title')
    
    person_str = data.get('person')
    if person_str:
        people_cv = client.get_collection_view('https://www.notion.so/brocoders/b4fee3350c234fa8a5a4a89677fb21c3?v=d6b07641b1f84e37863ad1ddde29d5f6')
        return people_cv.collection.get_rows(search=person_str)[0].id + ' -- ' + client.get_block('dce65ea3-eda4-4c9b-85d6-2086d2629ddd').id
        row.person = people_cv.collection.get_rows(search=person_str)
    
    str_date = data.get('date') #6/25/2020 22:35:33
    if str_date:
        row.date = datetime.datetime.strptime(str_date, '%m/%d/%Y').date()
    row.mood = data.get('mood').split(",")
    row.tags = data.get('tags').split(",")
    row.type = data.get('type')
    #row.interviewer = data.get('interviewer')

@app.route('/meeting_notes', methods=['POST'])
def create_meeting_note():
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    return createNotionMeetingNote(token_v2, url, request.form)
    #return f'added meeting note to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
