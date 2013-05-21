import webapp2
# import jinja2
# import os

# from google.appengine.ext import debug

# template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
#                                autoescape = True)

# def render_str(template, **params):
#     t = jinja_env.get_template(template)
#     return t.render(params)

# class BaseHandler(webapp2.RequestHandler):
#     def render(self, template, **kw):
#         self.response.out.write(render_str(template, **kw))

#     def write(self, *a, **kw):
#         self.response.out.write(*a, **kw)
 
form="""
<form method="post">
    What is your birthday?
    <br>
    <label> Month
    <input type="text" name="month" value="%(month)s">
    </label>
   
    <label> Day
    <input type="text" name="day" value="%(day)s">
    </label>
   
    <label> Year
    <input type="text" name="year" value="%(year)s">       
    </label>
    <div style="color: red">%(error)s</div>
   
    <br>
    <br>
   
    <input type="submit">
</form>
"""
 
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
 
months_abbvs = dict((m[:3].lower(),m) for m in months)
         
def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return months_abbvs.get(short_month)
               
def valid_day(day):
	if day and day.isdigit():
		day = int(day)
        if day>0 and day <=31:
            return day
           
def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year <= 2020:
            return year

def escape_html(s):
    for (i, o) in (("&", "&amp;"), (">", "&gt;"), 
                    ("<", "&lt;"),('"', "&quot;")):
        s = s.replace(i, o)

    return s
 
class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year="",):
		self.response.out.write(form % { "error": error, 
			                             "month": escape_html(month), 
                                         "day": escape_html(day), 
                                         "year": escape_html(year)})
 
	def get(self):
		self.write_form()
               
	def post(self):
	        user_month = self.request.get("month")
	        user_day = self.request.get("day")
	        user_year = self.request.get("year")

	        month = valid_month(user_month)
	        day = valid_day(user_day)
	        year = valid_year(user_year)

	        if not (month and day and year):
	            self.write_form("That doesn't look valid to me", 
	                user_month, user_day, user_year)
	        else:
	            self.redirect("/thanks")
               

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thank you, that's a vaild day")

# Unit 2 HW 1
unit2_rot13_form ="""
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>

    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(textarea_text)s</textarea>
      <br>
      <input type="submit">
    </form>

  </body>

</html>
"""

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self, textarea_text = ""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(unit2_rot13_form 
                                % {'textarea_text' : escape_html(textarea_text)})

    def rot13(self, s):
        return s.encode('rot13')

    def get(self):
        self.write_form()

    def post(self):
        user_text = self.request.get("text")
        encode_text = self.rot13(user_text)

        self.write_form(encode_text)



# class Rot13Handler(BaseHandler):
#     def get(self):
#         self.render('rot13-form.html')

#     def post(self):
#         rot13 = ''
#         text = self.request.get('text')
#         if text:
#             rot13 = text.encode('rot13')

#         self.render('rot13-form.html', text = rot13)

# Unit 2 HW 2


app = webapp2.WSGIApplication([('/', MainPage), 
                               ('/thanks', ThanksHandler), 
                               ('/unit2/rot13', Rot13Handler)], 
                                debug=True)