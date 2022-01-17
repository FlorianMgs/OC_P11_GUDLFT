from utils import read, update_points, update_competition_dict_with_past_bool, check_points
from flask import Flask, render_template, request, redirect, flash, url_for

COMPETITIONS = read('competitions.json', 'competitions')
CLUBS = read('clubs.json', 'clubs')


def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)
    competitions = COMPETITIONS
    clubs = CLUBS

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def show_summary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]

            # Checking if competition is past or not, then render template
            _competitions = update_competition_dict_with_past_bool(competitions)
            return render_template('welcome.html', club=club, competitions=_competitions)

        except IndexError:
            flash("error: please enter a valid email")
            return redirect(url_for('index'))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]

            max_places = round(int(foundClub['points']) / 3)
            if max_places > 12:
                max_places = 12
            return render_template('booking.html', club=foundClub, competition=foundCompetition, max_places=max_places)

        except IndexError:
            flash("error: Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        try:
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            placesRequired = int(request.form['places'])

        except ValueError:
            """
            Occurs if user enter a non numeric value after modifying page/request in dev tools.
            """
            flash("error: please enter valid points")
            return redirect(url_for('book', club=club['name'], competition=competition['name']))

        except IndexError:
            """
            This error occurs only if user modify post request in dev tools. Redirects to index page.
            """
            flash("error: invalid club / competition")
            return redirect(url_for('index'))

        else:
            # checking if points are valid
            if not check_points(placesRequired, competition, club):
                flash("error: point amount is not valid or you already have reserved 12 places.")
                return redirect(url_for('book', club=club['name'], competition=competition['name']))

            else:
                # updating number of places available in competition, then deduct points from club balance
                # then update club reservations count
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - (placesRequired * 3)
                club['reservations'][competition['name']] = int(club['reservations'][competition['name']]) + placesRequired

                # updating points in clubs.json and competitions.json
                update_points(
                    points=str(club['points']),
                    places=str(competition['numberOfPlaces']),
                    resas=str(club['reservations'][competition['name']]),
                    club_idx=clubs.index(club),
                    comp_idx=competitions.index(competition),
                    comp_name=competition['name']
                )

                flash('Great-booking complete!')
                return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/pointsDisplay')
    def points_display():
        return render_template('clubs.html', clubs=clubs)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app

