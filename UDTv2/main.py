from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from UDTv2.auth import login_required
from UDTv2.models import Users, Sites
from UDTv2 import db



mainBP = Blueprint('main', __name__)


@mainBP.route('/')
@login_required
def index():
    if not g.user:
        redirect(url_for('auth.login'))
    return render_template('main/index.html')


@mainBP.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        id = request.form['siteID']
        name = request.form['siteName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        parish = request.form['parish']
        coordinates = request.form['coordinates']
        typeOf = request.form['typeOf']
        owner = request.form['owner']
        make = request.form['make']
        model = request.form['model']
        serial = request.form['serial']
        freon = request.form['freon']
        controller = request.form['controller']
        filters = request.form['filters']
        error = None

        if not id:
            error = "site id required"
        elif not name:
            error = "site name required"

        if error is not None:
            flash(error)
        else:
            try:
                site = Sites(siteID=id, siteName=name, address=address, city=city, state=state, zip=zip, owner=owner, parish=parish, coordinates=coordinates, manufacturer=make, model=model, serial=serial, refrigerant=freon, controller=controller, type_of=typeOf, filters=filters)
                db.session.add(site)
            except Exception as e:
                error = f"Error: {e}"
                db.session.rollback()
            else:
                return redirect(url_for('main.index'))
            finally:
                db.session.commit()
    return render_template('main/create.html')


@mainBP.route("/read")
@login_required
def read():
    return render_template('search.html')