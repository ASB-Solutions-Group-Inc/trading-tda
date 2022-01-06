from flask import Flask
from flask import request 
import random  
import string

app = Flask(__name__)

@app.route("/")
def index():
    if not request.args.get("alpha"):           
        l = 8
    else:
        l = int(request.args.get("alpha", ""))
    if not request.args.get("digits"):
        d=4
    else:
        d =int(request.args.get("digits",""))
    random_string_out = random_string(l,d)
    return """<form action="" method="get">
        <h1> Password Generator </h1>
        <p> Number of letters </p>
        <input type="text" name="alpha" />
        <p> number of digits </p>
        <input type="int" name="digits"/>
        <input type="submit" value="password" />
        </form>""" + random_string_out

def random_string(letter_count, digit_count): 
    try: 
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    
        sam_list = list(str1) # it converts the string to list.  
        random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
        final_string = ''.join(sam_list)  
        return final_string 
    except ValueError:
        return "invalid input" 