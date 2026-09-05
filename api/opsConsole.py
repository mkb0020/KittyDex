# api/opsConsole.py
import os
from flask import Blueprint, request, session, redirect, send_from_directory

opsconsole_bp = Blueprint('opsconsole', __name__)

@opsconsole_bp.route('/ops-console', methods=['GET'])
def ops_console_page():
    if not session.get('ops_console_authed'):
        return '''
            <form method="POST" action="/ops-console/login" style="font-family:monospace;padding:40px;">
                <input type="password" name="password" placeholder="Password" autofocus>
                <button type="submit">Enter</button>
            </form>
        '''
    return send_from_directory('forms', 'ops-console.html')

@opsconsole_bp.route('/ops-console/login', methods=['POST'])
def ops_console_login():
    if request.form.get('password') == os.environ.get('OPS_CONSOLE_PASSWORD'):
        session['ops_console_authed'] = True
    return redirect('/ops-console')