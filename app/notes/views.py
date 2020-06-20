from flask_login import login_required, current_user
from flask import flash, redirect, render_template, url_for, request, redirect
from . import notes
from ..models import User, Minutes
from app import db
from datetime import datetime
from .edit_form import EditForm

@notes.route('/note/<int:n_id>', methods=["GET"])
@login_required
def view_note(n_id):
    note = Minutes.query.join(User).add_columns(Minutes.created_by,Minutes.body,Minutes.title, Minutes.purpose, Minutes.minute_id, Minutes.name_of_org, Minutes.attendees, Minutes.date_created, Minutes.date_modified, User.full_name).filter(Minutes.minute_id == n_id).first()
    user = User.query.add_column(User.full_name).filter_by(id=note.created_by)
    create = note.date_created.strftime("%d of %B %Y on %A at %I:%M %p")
    if note.date_created != note.date_modified:
        modified = note.date_created.strftime("%d of %B %Y on %A at %I:%M %p")
        return modified
    else: 
        modified = "Minute has not been edited" 
    return render_template("note.html", note = note, modified = modified, user=user,create = create)

@notes.route('/delete/<int:d_id>', methods=['GET'])
@login_required
def delete_note(d_id):
    minute = Minutes.query.filter_by(minute_id=d_id).first()
    db.session.delete(minute)
    db.session.commit()
    flash('You have successfully deleted a note')

    # redirect to the departments page
    return redirect(url_for('home.dashboard'))

@notes.route("/edit/<int:e_id>", methods=["GET", "POST"])
@login_required
def edit_note(e_id):
    note = Minutes.query.join(User).add_columns(Minutes.created_by,Minutes.body,Minutes.title, Minutes.purpose, Minutes.minute_id, Minutes.name_of_org, Minutes.attendees).filter(Minutes.minute_id==e_id).all()
    user = current_user.get_id()
    #if user == note.created_by:
    form = EditForm(formdata = request.form,obj=note)
    
    if note:
        if request.method == "POST":
            note.title = form.title.data
            note.purpose = form.purpose.data
            note.name_of_org = form.name_of_org.data
            note.attendees = form.attendees.data
            note.body = form.body.data
            
            #form.populate_obj(note)
            db.session.commit()
            db.session.refresh(note)
            return redirect(url_for('home.dashboard'))
    return render_template("edit_form.html",form=form, note=note,user=user)

