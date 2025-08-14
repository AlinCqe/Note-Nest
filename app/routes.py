from flask import Blueprint, render_template, request, jsonify, send_from_directory,current_app
import uuid
import os

from .dB import insert_sheet, get_safe_file_name, get_sheets_from_dB

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return render_template('uploads.html')

#use get in case user doenst know on of those params, also in sql make it emptyable
@routes.route('/upload_file', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    safe_filename = f'{uuid.uuid4()}.{file.filename}'
    song_name = request.form.get('song_name', '')
    author = request.form.get('author', '')
    category = request.form.get('category', '')
    instrument = request.form.get('instrument', '')


    os.makedirs('app/static/uploads',exist_ok=True)

    if os.path.exists(os.path.join('app/static/uploads', file.filename)):
        return jsonify({'error': 'File already exists'}), 400
    
    file.save(os.path.join('app/static/uploads', safe_filename))
    

    insert_sheet(safe_filename=safe_filename, song_name=song_name, author=author, category=category, instrument=instrument)
    
    return jsonify('x')

@routes.route('/download/<song_name>', methods=['GET'])
def download(song_name):
    full_path = os.path.join(current_app.root_path, 'static/uploads')

    print('asdsad')
    safe_filename = get_safe_file_name(song_name)
    print(safe_filename)
    return send_from_directory(directory=full_path, path=safe_filename, as_attachment=True, download_name=song_name)


@routes.route('/get_sheets', methods=['GET'])
def get_sheets():

    song_name = request.args.get('song_name', '')
    author = request.args.get('author', '')
    category = request.args.get('category', '')
    instrument = request.args.get('instrument', '')


    return get_sheets_from_dB(song_name,author,category,instrument)

