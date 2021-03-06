# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""


import json
import bot
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
import buildDropDown

pyBot = bot.Bot()
slack = pyBot.client
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

holding_upper_limit = 100 
##### Models 
class users(db.Model):
    __tablename__ = 'user_'
    name = db.Column(db.String(255), primary_key = True)
    fullname = db.Column(db.String(255))
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
        return str(self.name + ': ' + self.fullname + '; ')
    def __repr__(self):
        return str(self.name + ': ' + self.fullname + '; ')

class bidInfo(db.Model):
    __tablename__ = 'infoBid_'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.Integer(), nullable = False)
    amt = db.Column(db.Integer())
    slot_id = db.Column(db.Integer(), nullable = False)
    amt = db.Column(db.Integer())

class slots(db.Model):
    __tablename__ = 'slotsInfooo'
    slot_id = db.Column(db.Integer(), primary_key = True)
    start_time = db.Column(db.DateTime)
    slot_type = db.Column(db.String(255))
    duration = db.Column(db.Integer(), default = 20)
    highestBid = db.Column(db.Integer(), default =0)
    highestBidder = db.Column(db.String(255), default='')
    status = db.Column(db.String(255), default = 'open')
#######



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

    # print request.data
    # print 'request'
    # print request
    # print dir(request)
    # print 'data'
    # print request.data
    # print 'form'
    if len(request.form):
        data = request.form.to_dict(flat = False)
    else:
        data = json.loads(request.data)
    
    slack_event = data
    # print 'data is ', slack_event
    # print 'payload' in slack_event
    # print 'event' in slack_event
    # slack_event = json.loads(request.data)
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
    if 'payload' in slack_event:
        token = json.loads(slack_event['payload'][0]).get('token')
    else:
        token = slack_event.get('token')
    if pyBot.verification != token:
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (token, pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subcribed to

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)
    elif 'payload' in slack_event:
        print 'Two'
        return attachment_handler(json.loads(slack_event['payload'][0]))
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

def attachment_handler(payload):
    print payload
    user = payload['user']['id']
    name = payload['user']['name']
    callback_id = payload['callback_id']
    userObj = users.query.filter_by(name=user).first()
    if callback_id == 'dd_bidtype_select':

        userObj.stage = 2
        userObj.fullname = name
        selected_type = payload['actions'][0]['selected_options'][0]['value']

        open_slots = slots.query.filter_by(slot_type = selected_type, status = 'open').all()
        att = buildDropDown.slotDD(open_slots)
        response = pyBot.post_secret_message(user=user,channel=payload["channel"]["id"],text="Here are the available slots:", att=att)
    elif callback_id == 'dd_bidslot_select':

        selected_slot_id = payload['actions'][0]['selected_options'][0]['value']
        rebid = len(bidInfo.query.filter_by(name=user, slot_id = selected_slot_id).all()) > 0
        if rebid:
            userObj.stage = 0
            db.session.commit()
            return make_response('You\'ve already placed bid for this slot.')
        userObj.slot_id = selected_slot_id
        userObj.stage = 3
        response = pyBot.post_secret_message(user=user, channel=payload['channel']['id'],text="Enter bid amount",att="[]")
    db.session.commit()
    return make_response("Done",200,)

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
    try: 
        msg = slack_event['message']['text']
        if msg == 'Done':
            return make_response("Done",200)
    except:
        pass
    team_id = slack_event["team_id"]
    event = slack_event['event']
    # print slack_event
    # if event_type == 'app_mention':
        
    #     return make_response('App mention', 200,)
    print 'et: ', event
    if (event_type == "message" or event_type == "app_mention"):
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
            userObj = newUser
        else:
            userObj = existing_users[0]

        db.session.commit()
        print 'isdigit', msg_text.isdigit(), userObj.stage
        if msg_text == 'bid' and userObj.stage == 0:
            att=buildDropDown.msg_at
            userObj.stage = 1
            db.session.commit()
            # print att
            response = pyBot.post_secret_message(user=user,channel=event["channel"],text="Choose category", att=att)
            # print response
            #print(slack_event["event"]["text"])
            return make_response("Done",200,)

            # Send dropdown for types
        elif userObj.stage == 3 and msg_text.isdigit():
            amount = int(msg_text)
            if userObj.holding < amount:
                userObj.stage = 0
                text="Current holding({}) less than bid amount({})".format(userObj.holding,amount)
            else:
                # TODO : check if bid can be placed now 
                userObj.holding -= amount
                userObj.stage = 0
                newBid = bidInfo(name=user,slot_id=userObj.slot_id,amt=amount)
                db.session.add(newBid)
                text="Bid placed. Holding remaining - {}".format(userObj.holding)
            db.session.commit()
            pyBot.post_message(channel=event["channel"],text=text)
        else:
            userObj.stage = 0
            text="Sorry! Unknown message"
            pyBot.post_message(channel=event["channel"],text=text)
            db.session.commit()


        if "<@UBH8PG5U6>" in msg_text:
            # print("yayyy")
            channel=event["channel"]
            # print("authed_teams:",bot.authed_teams)
            # token = bot.authed_teams[team_id]["bot_token"]xoxb-390491814181-390574586821-GaRdPD3hY2fr4iueUAGOiUfQ
            pyBot.post_secret_message(user=user,channel=channel,text="Hurray")
            #print(slack_event["event"]["text"])
            return make_response("Done",200,)

    
    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
