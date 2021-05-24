from time import time

from flask import Flask, session, render_template, request

import flask_session
from markupsafe import Markup

import constants
import web_requests
import db
import utilities
import logging

app = Flask(__name__)
app.secret_key = 'super secret key'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
flask_session.Session(app)


@app.route('/')
def home_page():
    logging.basicConfig()
    # logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
    logging.info('So should this')
    update_session_var()
    logging.info('So should this')
    con = db.create_connection("climbDash")
    db.create_tables_if_needed(con)
    logging.info('So should this')
    db.update_routes(constants.areas)
    logging.info('8', time())
    return render_my_template()


@app.route('/sort')
def sort():
    update_session_var(request.args.to_dict())
    if session['name_to_search'] != '' and session['name_selected'] == '':
        user_data = web_requests.get_user_data(session['name_to_search'])
        if len(user_data) == 1:
            session['name_selected'] = user_data[0]
            x, user_id = user_data[0]
            session['name_to_search'] = ''
            tick_url = web_requests.get_tick_url(user_data[0])
            reader = web_requests.get_csv_reader_from_url(tick_url)
            db.update_ticks(reader, user_id)
        else:
            print('zero or more than two names were selected and this code has not been written')
    return render_my_template()


def render_my_template():
    rows = db.get_rows(session['area'],
                       session['crag'],
                       session['grade'],
                       session['exact_match'],
                       session['view'])
    logging.info('9', time())
    return render_template('body.html',
                           form=Markup(render_template('form.html',
                                                       form_parameters=session)),
                           table=Markup(render_template('table.html',
                                                        header_row=constants.header_row,
                                                        data_rows=rows)
                                        ))


def update_session_var(input_dictionary=constants.default_param_dict):
    """Updates session variables.
    If view is present, it handles the toggling of the radio button.  To ensure that only one can be selected at a time.
    If reset has been pressed, it clears the user

    Parameters
    ----------
    input_dictionary : dict
        The dictionary used to update the session variable

    Returns
    -------
    None
    """
    for key, value in input_dictionary.items():
        if 'view' in key:
            utilities.toggle_view_buttons(key)

        if 'reset' in key:
            session['name_selected'] = ''

        session[key] = value


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
