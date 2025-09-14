from flask import Flask, request, redirect
import re

app = Flask(__name__)


@app.route('/remove_user', methods=['POST'])
def remove_user():
    redirect_url = request.form.get('user_management_url')
    # watfel.com/remove
    if not re.match('https?://www.watfel.com/remove', redirect_url):
        redirect_url = '/user_management'

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(redirect_url, code=302)