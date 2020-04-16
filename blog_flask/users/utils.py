import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog_flask import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                   sender='info.sameerpashikanti@gmail.com',
                   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, kindly ignore this email. ''' 
    mail.send(msg)

