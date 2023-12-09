from flask_wtf import FlaskForm

class BaseForm(FlaskForm):
    
    @property
    def error_message(self):
        return self.errors
