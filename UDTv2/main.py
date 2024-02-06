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
    sites = Sites.query.all()


    if not g.user:
        redirect(url_for('auth.login'))
    return render_template('main/index.html', sites=sites)

@mainBP.route('/home-results')
def home_results():
    q = request.args.get("q")
    if q:
        results = Sites.query.filter(Sites.siteID.icontains(q) | Sites.siteName.icontains(
            q) | Sites.parish.icontains(q) | Sites.filters.icontains(q) | Sites.city.icontains(q)).all()
    else:
        results = Sites.query.limit(15)
    return render_template('main/search-results-home.html', results=results)


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
                site = Sites(siteID=id, siteName=name, address=address, city=city, state=state, zip=zip, owner=owner, parish=parish, coordinates=coordinates,
                             manufacturer=make, model=model, serial=serial, refrigerant=freon, controller=controller, type_of=typeOf, filters=filters)
                db.session.add(site)
            except Exception as e:
                error = f"Error: {e}"
                db.session.rollback()
            else:
                return redirect(url_for('main.index'))
            finally:
                db.session.commit()
    return render_template('main/create.html')


@mainBP.route('/search')
@login_required
def search():
    return render_template('main/search.html')


@mainBP.route('/results')
@login_required
def results():
    q = request.args.get("q")
    if q:
        results = Sites.query.filter(Sites.siteID.icontains(q) | Sites.siteName.icontains(
            q) | Sites.parish.icontains(q) | Sites.filters.icontains(q) | Sites.city.icontains(q)).all()
    else:
        results = []
    return render_template('main/search-results.html', results=results)


@mainBP.route('/editor/<id>', methods=('GET', 'POST'))
@login_required
def editor(id):
    data = Sites.query.get(id)
    if request.method == 'POST':
        try:
            data.siteID = request.form['siteID']
            data.siteName = request.form['siteName']
            data.address = request.form['address']
            data.city = request.form['city']
            data.state = request.form['state']
            data.parish = request.form['parish']
            data.coordinates = request.form['coordinates']
            data.type_of = request.form['typeOf']
            data.owner = request.form['owner']

            data.manufacturer = request.form['manufacturer']
            data.model = request.form['model']
            data.serial = request.form['serial']
            data.filters = request.form['filters']
            data.refrigerant = request.form['freon']
            data.controller = request.form['controller']

            db.session.commit()
            return redirect(url_for('main.search'))
        except Exception as e:
            flash(f"Error: {e}")
            db.session.rollback()


    if not data:
        return redirect(url_for('main.found404'))

    return render_template('main/editor.html', data=data)


@mainBP.route('/map')
@login_required
def map():
    return render_template('main/map.html')


@mainBP.route('/found404')
def found404():
    return render_template('found404.html')