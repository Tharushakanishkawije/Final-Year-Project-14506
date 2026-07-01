from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/hostDiscovery', methods=['POST'])
def execute_host_discovery():
    command = "/home/rasp/Desktop/Monitoring_System/hostDiscovery/network_scan.sh"
    return execute_command(command)

@app.route('/toggleFWoff', methods=['POST'])
def execute_off_firewall():
    command = "/home/rasp/Desktop/Monitoring_System/firewall/Toggle_Off/offFW.sh"
    return execute_command(command)

@app.route('/toggleFWon', methods=['POST'])
def execute_on_firewall():
    command = "/home/rasp/Desktop/Monitoring_System/firewall/Toggle_On/onFW.sh"
    return execute_command(command)

@app.route('/updateRules', methods=['POST'])
def execute_update_rules():
    command = "/home/rasp/Desktop/Monitoring_System/firewall/Rules_Upload/fw_rules.sh"
    return execute_command(command)

@app.route('/toggleIdpsoff', methods=['POST'])
def execute_off_idps():
    command = "/home/rasp/Desktop/Monitoring_System/idps/Toggle_Off/offIdps.sh"
    return execute_command(command)

@app.route('/toggleIdpson', methods=['POST'])
def execute_on_idps():
    command = "/home/rasp/Desktop/Monitoring_System/idps/Toggle_On/onIdps.sh"
    return execute_command(command)

@app.route('/updateAlerts', methods=['POST'])
def execute_update_alerts():
    command = "/home/rasp/Desktop/Monitoring_System/idps/alerts.sh"
    return execute_command(command)

@app.route('/clearAlerts', methods=['POST'])
def execute_clear_alerts():
    command = "sudo /home/rasp/Desktop/Monitoring_System/idps/clearAlerts.sh"
    return execute_command(command)

def execute_command(command):
    try:
        output = os.popen(command).read()
        return "200"
    except Exception as e:
        return "500"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
