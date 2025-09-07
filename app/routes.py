from flask import Blueprint, render_template, request, jsonify, send_from_directory,current_app, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
import uuid
import os

from .dB import insert_sheet, get_safe_file_name, get_sheets_from_dB, db_load_user, db_check_user_exists, db_create_user, db_get_users, db_check_password,db_get_user, get_user_data
from .__init__ import loggin_manager
routes = Blueprint('routes', __name__)  

@routes.route('/', methods=['GET'])
def home():
    q = request.args.get('q', '')
    # Perform your query and pass `q` to the template.
    return render_template('home.html', show_search=True, q=q, sheets=get_sheets_from_dB(q=q))

@loggin_manager.user_loader
def load_user(user_id):
    data = db_load_user(user_id)
    if data:
        return data


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']

        password = request.form['password']

        if db_check_user_exists(username):
            return 'User alredy exists', 400
        
        db_create_user(username, password)

        return redirect(url_for('routes.login'))

    return render_template('register.html', show_search=False)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not db_check_user_exists(username) or not db_check_password(username, password):
            return 'Username or password incorrect', 404
        user = db_get_user(username)

        login_user(user)
        return redirect(url_for('routes.home', show_search=True))

    return render_template('login.html', show_search=False)


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out'

@routes.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! Logged in: {current_user.is_authenticated}'





@routes.route('/upload_file', methods=['GET','POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        ext = os.path.splitext(file.filename)[1] 
        safe_filename = f"{uuid.uuid4()}{ext}"
        song_name = request.form.get('song_name', '')

        authors = [author.strip() for author in request.form.get('authors', '').split(',') if author.strip()]

        categories = [category.strip() for category in request.form.get('categories', '').split(',') if category.strip()]

        instruments = [instrument.strip() for instrument in request.form.get('instruments', '').split(',') if instrument.strip()]

        os.makedirs('app/static/uploads',exist_ok=True)
        file.save(os.path.join('app/static/uploads', safe_filename))

        insert_sheet(safe_filename=safe_filename, song_name=song_name, authors=authors, categories=categories, instruments=instruments,user_id=current_user.id)
        
        return jsonify('x')
    return render_template('uploads.html', show_search=True)


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

    q = request.args.get('q', '').strip()

    return jsonify(get_sheets_from_dB(song_name,authors,categories,instruments,q))

@routes.route('/sheet/<safe_filename>', methods=['GET'])
def sheet(safe_filename):
    return render_template('sheet.html', safe_filename=safe_filename, show_search=True)

@routes.route('api/sheet/<safe_filename>', methods=['GET'])
def api_sheet(safe_filename):
    print(safe_filename)
    sheet = get_sheets_from_dB(safe_filename=safe_filename)
    print(sheet)
    if sheet:
        return jsonify(sheet)
    else:
        return jsonify({'error': 'Sheet not found'}), 404
    
@routes.route('/api/user/<user_id>', methods=['GET'])
def user_sheets(user_id):


    sheets, user_data = get_user_data(user_id)
    return jsonify({'sheets': sheets, 'user_data':user_data})

@routes.route('/user/<user_id>')
def user(user_id):
    print(user_id)
    return render_template('user.html',user_id=user_id, show_search=True)