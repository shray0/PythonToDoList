from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #initializing app framewor
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'  #attaches database to project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True) #holding column int value id, primary key keeps track of id
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/") #Indicating that it is homedirectory, if you add something to do forward slash, it will give different directory    
def home(): #First page, landing page of website
    todo_list = Todo.query.all() #searching for everything in class, query is search function
    return render_template("index.html",todo_list=todo_list) #output of function, rendering the index.html template to attach, attach the html definition of todolist to equal the python definition of todolist

@app.route("/add",methods=['POST']) #indicating the /add directory, post method posts new task to be done to the database
def add():
    new_title = request.form.get('title') #set title = to request to get the title of new task
    new_todo = Todo(title=new_title, complete = False) #setting the requested title of new task to equal to title from class Todo, when you create task, it cant be completed which is why its false
    db.session.add(new_todo) #adding the new entry into database log
    db.session.commit() #pushing the data entry into database
    return redirect(url_for("home")) #after you create todo, brings it back to home page

@app.route("/update/<int:todo_id>") #attaching route to specific id you are updating
def update(todo_id): #updating todo id, whenever we make changes id changes
    todo = Todo.query.filter_by(id=todo_id).first() #access todo class, search and filter databse by id, by first & lowest id
    todo.complete = not todo.complete #not means false, setting it to be not completed todo 
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>") 
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo) #deletes entry
    db.session.commit()
    return redirect(url_for("home"))

@app.before_first_request #attaching route to point to this code before pointing to main code
def create_tables(): #creating the tables before main does, to prevent any errors
    db.create_all()
    

if __name__ == "__main__": 
    db.create_all() #creating all database entries
    app.run(debug=True) #allow us to debug code


