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
        results = Sites.query.filter(db.and_(Sites.siteID.icontains(q) | Sites.siteName.icontains(
            q) | Sites.parish.icontains(q) | Sites.filters.icontains(q) | Sites.city.icontains(q), Sites.techID == g.user.id)).all()
    else:
        results = Sites.query.filter_by(techID=g.user.id).limit(10)
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
                             manufacturer=make, model=model, serial=serial, refrigerant=freon, controller=controller, type_of=typeOf, filters=filters, techID=g.user.id)
                db.session.add(site)
            except Exception as e:
                error = f"Error: {e}"
                db.session.rollback()
            else:
                return redirect(url_for('main.index'))
            finally:
                db.session.commit()
    return render_template('main/create.html')

@mainBP.route('/view/<id>', methods=('GET', 'POST'))
@login_required
def view(id):
    data = Sites.query.get(id)
    if request.method == 'POST':
        pass
    return render_template('main/view.html', data=data)






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
            return redirect(url_for('main.editor', id=data.siteID))
        except Exception as e:
            flash(f"Error: {e}")
            db.session.rollback()


    if not data:
        return redirect(url_for('main.found404'))

    return render_template('main/editor.html', data=data)


@mainBP.route('/map')
@login_required
def map():
    maps = {
        1: None, # admin
        2: None, # guest
        3: "https://www.google.com/maps/d/u/0/embed?mid=1iVn8SOtoD0SwNcKPWJknpFG1xACP9wM&ehbc=2E312F",
        4: "https://www.google.com/maps/d/u/0/embed?mid=1e1_2nvDkn4pnI7EZCqOQUxLHuKfew3M&ehbc=2E312F",
        5: "https://www.google.com/maps/d/u/0/embed?mid=17Lkvi1wpm7CJb8omsEeyhzuJWCi0aWE&ehbc=2E312F",
        6: "https://www.google.com/maps/d/u/0/embed?mid=1IF9KEHG6WMJE3gf_HrzTaG4VUDc2eh4&ehbc=2E312F",
        7: "https://www.google.com/maps/d/u/0/embed?mid=11Vw_6Pj1hSd-Y5iw5cnpmDFahnNiD7Q&ehbc=2E312F"
    }
    
    return render_template('main/map.html', mapObj=maps[g.user.id])


@mainBP.route("/view_user")
@login_required
def view_user():
    return render_template('main/view_user.html')




@mainBP.route('/found404')
def found404():
    return render_template('found404.html')