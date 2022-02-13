from __main__ import app, mongo
from utils.login_required import login_required
from flask import render_template, session, request
from bson import ObjectId


@app.route('/')
@app.route('/home')
def index():
    user = session.get('username')
    return render_template('index.html')


@app.route('/notifications')
@login_required
def notifications():
    notifications = list(mongo.db.notifications.find(
        {'user_id': session['user_id']}))
    return render_template('notifications.html', notifications=notifications)


@app.route('/delete_notification', methods=["POST"])
@login_required
def delete_notification():
    """  mongo.db.notifications.delete_one({
         "user_id": session["user_id"],
         "_id": request.
     }) """
    print(request.form["notification_id"])

    mongo.db.notifications.delete_one({
        "user_id": session["user_id"],
        "_id": ObjectId(request.form["notification_id"])
    })
    return "success"
