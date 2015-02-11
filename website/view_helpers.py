from app import app

@app.template_filter("datetimeformat")
def datetimeformat(value, format='%b %d, %Y'):
    return value.strftime(format)