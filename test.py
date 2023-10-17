import slumber
from flask import Flask, render_template, request,redirect
import config

ENDPOINT = "https://modernizacaopublica.pulseway.com/api/v2/"

def get_api_results():
    try:
        api = slumber.API(ENDPOINT, auth=(config.USERNAME, config.PASSWORD))
        # use limit & offset parameters
        result = api.notifications.get(limit='100', offset='0')
        # if result['message'].startswith('')
        update = []
        critical = []
        #print(result['data'])
        newdict = result['data']
        for i in newdict:

            if i['priority'] == 'low' or 'normal':
                update.append(i)
                print(i)
        #    elif i['priority'] == 'elevated' or 'critical':
        #        critical.append(i)

        return update
    except Exception as e:
        print('GetNotifications raised an exception.')

def get_critical_results():
    try:
        api = slumber.API(ENDPOINT, auth=(config.USERNAME, config.PASSWORD))
        # use limit & offset parameters
        result = api.notifications.get(limit='100', offset='0')
        critical = []
        newdict = result['data']
        for i in newdict:

            if i['priority'] == 'elevated':
                critical.append(i)
                print(i)
            elif i['priority'] == 'critical':
                critical.append(i)

        return critical
    except Exception as e:
        print('GetNotifications raised an exception.')


app = Flask(__name__)

@app.route('/notifications')
def notifications():
    return render_template('pending_reboot.html', update=get_api_results())

@app.route('/critical')
def critical_notifications():
    return render_template('critical.html', critical=get_critical_results())

@app.route('/remove_item', methods=['POST'])
def delete_notification():
    try:
        api = slumber.API(ENDPOINT, auth=(config.USERNAME, config.PASSWORD))
        notification_id = request.form['notification_id']
        print(notification_id)
        result = api.notifications(notification_id).delete()
        print(result)
    except Exception as e:
        print('DeleteNotification raised an exception.')

    # Redirect back to the original page
    return redirect(request.referrer)

app.run("0.0.0.0",8130,False)
