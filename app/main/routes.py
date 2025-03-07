
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.main import bp
from app import db
from app.models import User, Note
from app.forms import EditProfileForm, MarkdownUploadForm, NoteForm
from datetime import datetime, timezone

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/')
@bp.route('/index')
def index():
  items = [
    {
    'topic': {'title': 'css and js in flask'},
    'body': 'css and js are usually in the static folder, unless configured otherwise'
    },
    {
    'topic': {'title': 'flask'},
    'body': 'Flask is nice and easy to get ideas up and running'
    }
  ]
  return render_template('index.html', title='Home', items=items)

@bp.route('/about')
def about():
    return render_template('index.html', content='Flask web app.')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)




@bp.route('/notes')
@login_required
def list_notes():
    notes = db.session.execute(db.select(Note).where(Note.user_id == current_user.id)).scalars()
    
    return render_template('notes_list.html', notes=notes)


@bp.route('/notes/new', methods=['GET', 'POST'])
@login_required
def upload():
    form = MarkdownUploadForm()
    if form.validate_on_submit():
        files = request.files.getlist('files')
        new_notes = []
        
        for file in files:
            if file:
                try:
                    content = file.read().decode('utf-8')
                except Exception as e:
                    flash(f"Error reading file {file.filename}: {e}")
                    continue
                
                title = file.filename.rsplit('.', 1)[0]
                
                note = Note(
                    title=title,
                    content=content,
                    filename=file.filename,
                    user_id=current_user.id
                )
                db.session.add(note)
        
        db.session.commit()
        flash('Files uploaded and saved to the database successfully.')
        return redirect(url_for('main.upload'))
    return render_template('upload.html', form=form)

@bp.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        abort(404)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!')
    return redirect(url_for('main.list_notes'))

@bp.route('/notes/<int:note_id>')
@login_required
def note_detail(note_id):
    note = db.session.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        abort(404)
    return render_template('note_detail.html', note=note)

@bp.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        abort(404)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.filename = f"{form.title.data.strip().replace(' ', '_')}.md"
        db.session.commit()
        flash('Note updated successfully!')
        return redirect(url_for('main.note_detail', note_id=note.id))
    return render_template('note_form.html', form=form, note=note)
