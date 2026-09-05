import os
import secrets
import time
from flask import Blueprint, request, session, redirect, send_from_directory

opsconsole_bp = Blueprint('opsconsole', __name__)

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 300  # 5 minutes

@opsconsole_bp.route('/ops-console', methods=['GET'])
def ops_console_page():
    if not session.get('ops_console_authed'):
        locked_until = session.get('ops_console_locked_until', 0)
        if time.time() < locked_until:
            remaining = int(locked_until - time.time())
            return f'<p style="font-family:monospace;padding:40px;">Too many attempts. Try again in {remaining}s.</p>'
        return '''
            <form method="POST" action="/ops-console/login" style="font-family:monospace;padding:40px;">
                <input type="password" name="password" placeholder="Password" autofocus>
                <button type="submit">Enter</button>
            </form>
        '''
    return send_from_directory('forms', 'ops-console.html')

@opsconsole_bp.route('/ops-console/login', methods=['POST'])
def ops_console_login():
    locked_until = session.get('ops_console_locked_until', 0)
    if time.time() < locked_until:
        return redirect('/ops-console')

    submitted = request.form.get('password', '')
    correct = os.environ.get('OPS_CONSOLE_PASSWORD', '')

    if secrets.compare_digest(submitted, correct):
        session['ops_console_authed'] = True
        session.pop('ops_console_attempts', None)
        session.pop('ops_console_locked_until', None)
    else:
        attempts = session.get('ops_console_attempts', 0) + 1
        session['ops_console_attempts'] = attempts
        if attempts >= MAX_ATTEMPTS:
            session['ops_console_locked_until'] = time.time() + LOCKOUT_SECONDS
            session['ops_console_attempts'] = 0

    return redirect('/ops-console')