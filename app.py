# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import json
import bot
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
SQLALCHEMY_TRACK_MODIFICATIONS = False


pyBot = bot.Bot()
slack = pyBot.client
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

holding_upper_limit = 100 

##### Models 
class users(db.Model):
    __tablename__ = 'user'
    name = db.Column(db.String(255), primary_key = True)
    holding = db.Column(db.Integer(), default = holding_upper_limit, nullable = False)
    stage = db.Column(db.Integer(), default = 0 )
    slot_id = db.Column(db.Integer())

    # 0 Before Start 
    # 1 Given 'bid' command 
    # 2 Selected Type 
    # 3 Selected Slot 
    # 4 Amount Given 
    # -> leave 
    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self.name)

class bidInfo(db.Model):
    __tablename__ = 'infoBid'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.Integer(), nullable = False)
    slot_id = db.Column(db.Integer(), nullable = False)

class slots(db.Model):
    __tablename__ = 'slotsInfo'
    slot_id = db.Column(db.Integer(), primary_key = True)
    start_time = db.Column(db.DateTime)
    slot_type = db.Column(db.String(255))
    duration = db.Column(db.Integer(), default = 20)
    highestBid = db.Column(db.Integer(), default =0)
    highestBidder = db.Column(db.String(255))
#######




def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event

    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error

    """    
    team_id = slack_event["team_id"]
    event = slack_event['event']
    print slack_event
    # if event_type == 'app_mention':
        
    #     return make_response('App mention', 200,)
    if (event_type == "message" or event_type == "app_mention"):
        print("entered")
        if "subtype" in event and event["subtype"] == "message_changed":
            msg_text = event["message"]["text"]
            user = event["message"]["user"]
        else:
            msg_text = event["text"]
            user = event["user"]

        existing_users=users.query.filter_by(name=user).all()
        if len(existing_users) == 0 :
            newUser = users(name = user)
            db.session.add(newUser)
            db.session.commit()
            userObj = newUser
        else:
            userObj = existing_users[0]

        if msg_text == 'bid' and userObj.stage == 0:
            userObj.stage = 1
            # Send dropdown for types
        elif userObj.stage == 4 and msg_text.isdigit():
            amount = int(msg_text)
            if userObj.holding < amount:
                userObj.stage = 0
                text="Current holding({}) less than bid amount({})".format(userObj.holding,amount)
            else:
                # TODO : check if bid can be placed now 
                userObj.holding -= amount
                userObj.stage = 0
                newBid = bidInfo(name=user,slot_id=userObj.slot_id)
                db.session.add(newBid)
                text="Bid placed. Holding remaining - {}".format(userObj.holding)
            pyBot.post_message(channel=event["channel"],text=text)
        else:
            userObj.stage = 0
            text="Sorry! Unknown message"
            pyBot.post_message(channel=event["channel"],text=text)


        if "<@UBH8PG5U6>" in msg_text:
            print("yayyy")
            channel=event["channel"]
            print("authed_teams:",bot.authed_teams)
            # token = bot.authed_teams[team_id]["bot_token"]xoxb-390491814181-390574586821-GaRdPD3hY2fr4iueUAGOiUfQ
            pyBot.post_secret_message(user=user,channel=channel,text="Hurray")
            #print(slack_event["event"]["text"])
            return make_response("Done",200,)
    
    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
    redirect_uri = pyBot.oauth["redirect_uri"]
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope, redirect_uri=redirect_uri)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    slack_event = json.loads(request.data)
    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })

    # ============ Slack Token Verification =========== #
    # We can verify the request is coming from Slack by checking that the
    # verification token in the request matches our app's settings
    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subcribed to
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
