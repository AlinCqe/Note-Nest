from flask import Blueprint, render_template, request, jsonify, send_from_directory,current_app
import uuid
import os

from .dB import insert_sheet, get_safe_file_name, get_sheets_from_dB

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return render_template('uploads.html')

@routes.route('/upload_file', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    ext = os.path.splitext(file.filename)[1] 
    safe_filename = f"{uuid.uuid4()}{ext}"
    song_name = request.form.get('song_name', '')

    authors = [author.strip() for author in request.form.get('authors', '').split(',') if author.strip()]

    categories = [category.strip() for category in request.form.get('categories', '').split(',') if category.strip()]

    instruments = [instrument.strip() for instrument in request.form.get('instruments', '').split(',') if instrument.strip()]

    os.makedirs('app/static/uploads',exist_ok=True)
    file.save(os.path.join('app/static/uploads', safe_filename))

    insert_sheet(safe_filename=safe_filename, song_name=song_name, authors=authors, categories=categories, instruments=instruments)
    
    return jsonify('x')

@routes.route('/download/<song_name>', methods=['GET'])
def download(song_name):
    full_path = os.path.join(current_app.root_path, 'static/uploads')

    safe_filename = get_safe_file_name(song_name)

    return send_from_directory(directory=full_path, path=safe_filename, as_attachment=True, download_name=song_name)


@routes.route('/get_sheets', methods=['GET'])
def get_sheets():

    song_name = request.args.get('song_name', '')

    authors = [author.strip() for author in request.args.get('authors', '').split(',') if author.strip()]

    categories = [category.strip() for category in request.args.get('categories', '').split(',') if category.strip()]

    instruments = [instrument.strip() for instrument in request.args.get('instruments', '').split(',') if instrument.strip()]

    return jsonify(get_sheets_from_dB(song_name,authors,categories,instruments))

