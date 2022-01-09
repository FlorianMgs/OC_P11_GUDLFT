from helpers import read, update_points, update_competition_dict_with_past_bool
from flask import Flask, render_template, request, redirect, flash, url_for


def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)

    competitions = read('competitions.json', 'competitions')
    clubs = read('clubs.json', 'clubs')

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
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        # checking if points are valid
        if not 0 < placesRequired <= 12 or placesRequired > int(club['points']) or placesRequired > int(competition['numberOfPlaces']):
            flash("error: please enter a valid amount of points")
            return redirect(url_for('book', club=club['name'], competition=competition['name']))

        else:
            # updating number of places available in competition, then deduct points from club balance
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired

            # updating points in clubs.json and competitions.json
            update_points(
                points=str(club['points']),
                places=str(competition['numberOfPlaces']),
                club_idx=clubs.index(club),
                comp_idx=competitions.index(competition)
            )

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app

