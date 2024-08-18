from flask import Flask, render_template, redirect, url_for
from models import db, PacketLog
from forms import SendPacketForm, RespondPacketForm
from scapy.all import IP, TCP, UDP, ICMP, send, sniff
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

def setup():
    with app.app_context():
        db.create_all()

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%H:%M:%S')

@app.route('/', methods=['GET', 'POST'])
def index():
    send_form = SendPacketForm()
    respond_form = RespondPacketForm()

    if send_form.validate_on_submit():
        ip = send_form.ip_address.data
        port = send_form.port.data
        protocol = send_form.protocol.data

        send_packet(ip, port, protocol)
        log_packet(datetime.now(), 'localhost', ip, 0, port, protocol, False)

        return redirect(url_for('index'))

    if respond_form.validate_on_submit():
        incoming_ip = respond_form.incoming_ip.data
        incoming_port = respond_form.incoming_port.data
        answer_port = respond_form.answer_port.data

        log_packet(datetime.now(), incoming_ip, 'localhost', incoming_port, answer_port, "TCP", True)

        return redirect(url_for('index'))

    return render_template('index.html', send_form=send_form, respond_form=respond_form)

@app.route('/logs', methods=['GET'])
def logs():
    logs = PacketLog.query.all()
    return render_template('logs.html', logs=logs)

def log_packet(timestamp, src_ip, dest_ip, src_port, dest_port, protocol, ping_back):
    log_entry = PacketLog(timestamp=int(timestamp.timestamp()), src_ip=src_ip, dest_ip=dest_ip,
                          src_port=src_port, dest_port=dest_port, protocol=protocol, ping_back=ping_back)
    db.session.add(log_entry)
    db.session.commit()

def send_packet(ip, port, protocol):
    if protocol == 'TCP':
        packet = IP(dst=ip) / TCP(dport=port)
    elif protocol == 'UDP':
        packet = IP(dst=ip) / UDP(dport=port)
    elif protocol == 'ICMP':
        packet = IP(dst=ip) / ICMP()

    send(packet)

def packet_listener():
    def handle_packet(packet):
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        src_port = packet[TCP].sport if TCP in packet else packet[UDP].sport
        dest_port = packet[TCP].dport if TCP in packet else packet[UDP].dport
        protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "ICMP"
        
        log_packet(datetime.now(), src_ip, dest_ip, src_port, dest_port, protocol, False)

        # Check if a ping-back is needed
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        ping_back_entry = PacketLog.query.filter_by(src_ip=src_ip, dest_ip=dest_ip, src_port=src_port, dest_port=dest_port, ping_back=True)\
                                         .filter(PacketLog.timestamp >= int(five_minutes_ago.timestamp()))\
                                         .first()
        if ping_back_entry:
            send_packet(src_ip, ping_back_entry.dest_port, protocol)

    sniff(prn=handle_packet)

if __name__ == '__main__':
    setup()  # Run setup before starting the app
    listener_thread = threading.Thread(target=packet_listener, daemon=True)
    listener_thread.start()
    app.run(debug=True, host='0.0.0.0')

