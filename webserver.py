from flask import Flask, request,render_template,send_from_directory,Response
import json

keys = {"type":str,"id":int,"lon":float,"lat":float,"process":str,"state":str}

#instantiate the script as an app
app = Flask(__name__,template_folder='html')
log = 'log.txt'
p_data = []

###These variables are used only for debugging
#outfile = './json/test.out'
#open(outfile,'w').close()

#Processes the POST data, updates entities expected at a given time
#TODO add check for bad post request
def post(post_data):
    global p_data
    #open(log,'a').write(str(post_data))
    p_data.append(json.dumps(post_data))
    #copy_data(json.dumps(post_data))
    ##echo the post data back to the sender
    return str(post_data)
    
def post_gen():
    global p_data
    if len(p_data)>0:
        yield p_data.pop(0)
    # for i,p in enumerate(p_data):
        # if i == 0: yield "["+str(p)+","
        # elif i == len(data)-1: yield str(p)+"]"
        # else: yield str(p) +","

#a method used for debugging to write out data to a log
def copy_data(data):
    with open(outfile,'a') as f:
        f.write(data)

@app.route("/", methods = ['GET','POST'])
def index():
   #When you request the root path via GET, return the dashboard.html page, otherwise process the post data
   if request.form:
        return post(request.form)
   else: return render_template("dashboard.html")
   
@app.route("/data",methods = ['GET'])
def update(): 
    for x in p_data: print(x)
    return Response(post_gen(),mimetype='text/json')
    #return Response(p_data,mimetype='text/json')


########These routes are to allow loading of local files from javascript########
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
    
@app.route('/json/<path:path>')
def send_json(path):
    return send_from_directory('json', path)
#################################################################################


if __name__ == '__main__':
    app.run(debug=True)