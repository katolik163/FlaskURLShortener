from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import URLForm, PasswordForm
from app.generators import generate_short_url
from app.models import Link

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        original_url = form.original_url.data
        custom_short_url = form.custom_short_url.data
        deletion_date = form.deletion_date.data
        max_visits = form.max_visits.data
        password = form.password.data

        short_url = custom_short_url if custom_short_url else generate_short_url()
        deletion_date_utc = deletion_date.astimezone(timezone.utc) if deletion_date else None
        password_hash = generate_password_hash(password) if password else None

        if max_visits is not None and max_visits < 1:
            max_visits = None
        
        new_link = Link(original_url=original_url, short_url=short_url, deletion_date=deletion_date_utc, max_visits=max_visits, password=password_hash)
        db.session.add(new_link)
        db.session.commit()

        return redirect(url_for('shortened_url', short_url=short_url))
    return render_template('index.html', form=form)

@app.route('/shortened/<short_url>')
def shortened_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    return render_template('shortened.html', link=link)

@app.route('/<short_url>', methods=['GET', 'POST'])
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    form = PasswordForm()
    incorrect_password = False # error flag for password

    if link.deletion_date and link.deletion_date.tzinfo is None:
        link.deletion_date = link.deletion_date.replace(tzinfo=timezone.utc)

    if link.deletion_date and datetime.now(timezone.utc) > link.deletion_date:
        db.session.delete(link)
        db.session.commit()
        flash('This link has expired.')
        return render_template('errors/404.html')
    
    if link.max_visits and link.visit_count >= link.max_visits:
        db.session.delete(link)
        db.session.commit()
        flash('This link has reached its maximum number of visits.')
        return render_template('errors/404.html')

    if link.password:
        if form.validate_on_submit():
            if check_password_hash(link.password, form.password.data):
                link.visit_count += 1
                db.session.commit()
                return redirect(link.original_url)
            else:
                incorrect_password = True
        return render_template('protected.html', form=form, link=link, incorrect_password=incorrect_password)
    else:
        link.visit_count += 1
        db.session.commit()
        return redirect(link.original_url)

@app.route('/<short_url>+')
def url_stats(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    if link.deletion_date and link.deletion_date.tzinfo is None:
        link.deletion_date = link.deletion_date.replace(tzinfo=timezone.utc)

    if link.deletion_date and datetime.now(timezone.utc) > link.deletion_date:
        db.session.delete(link)
        db.session.commit()
        flash('This link has expired.')
        return render_template('errors/404.html')
    
    if link.max_visits and link.visit_count >= link.max_visits:
        db.session.delete(link)
        db.session.commit()
        flash('This link has reached its maximum number of visits.')
        return render_template('errors/404.html')
    return render_template('stats.html', link=link)