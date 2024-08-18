from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, IPAddress

class SendPacketForm(FlaskForm):
    ip_address = StringField('IP Address/Host Name', validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired()])
    protocol = SelectField('Protocol', choices=[('TCP', 'TCP'), ('UDP', 'UDP'), ('ICMP', 'ICMP')], validators=[DataRequired()])
    submit = SubmitField('Send Packet')

class RespondPacketForm(FlaskForm):
    incoming_ip = StringField('Incoming IP Address', validators=[DataRequired(), IPAddress()])
    incoming_port = IntegerField('Incoming Port', validators=[DataRequired()])
    answer_port = IntegerField('Answer Port', validators=[DataRequired()])
    submit = SubmitField('Respond to Packet')
