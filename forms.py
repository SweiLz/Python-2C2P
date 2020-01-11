
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length


class PaymentInfoForm(FlaskForm):
    description = StringField('Payment description', [DataRequired()])
    currency = SelectField('Currency', choices=[
                           ('THB', 'THB'), ('HKD', 'HKD'), ('PHP', 'PHP'), ('IDR', 'IDR'), ('MYR', 'MYR')])
    amount = FloatField('Amount', [DataRequired()], default=0.00)
    # recaptcha = RecaptchaField()
    submit = SubmitField('Pay Now')

    def json(self):
        data = {"description": self.description.data,
                "currency": self.currency.data, "amount": self.amount.data}
        return data


# class ContactForm(FlaskForm):
#     """Contact form."""

#     name = StringField('Name', [
#         DataRequired()])
#     email = StringField('Email', [
#         Email(message='Not a valid email address.'),
#         DataRequired()])
#     body = TextAreaField('Message', [
#         DataRequired(),
#         Length(min=4, message='Your message is too short.')])
#     submit = SubmitField('Submit')


# class SignupForm(FlaskForm):
#     """Sign up for a user account."""

#     email = StringField('Email', [
#         Email(message='Not a valid email address.'),
#         DataRequired()])
#     password = PasswordField('Password', [
#         DataRequired(message="Please enter a password."),
#     ])
#     confirmPassword = PasswordField('Repeat Password', [
#             EqualTo(password, message='Passwords must match.')
#             ])
#     title = SelectField('Title', [DataRequired()],
#                         choices=[('Farmer', 'farmer'),
#                                  ('Corrupt Politician', 'politician'),
#                                  ('No-nonsense City Cop', 'cop'),
#                                  ('Professional Rocket League Player', 'rocket'),
#                                  ('Lonely Guy At A Diner', 'lonely'),
#                                  ('Pokemon Trainer', 'pokemon')])
#     website = StringField('Website', validators=[URL()])
#     birthday = DateField('Your Birthday')
#     recaptcha = RecaptchaField()
#     submit = SubmitField('Submit')
