from flask import Flask, redirect
import search_jobs

app = Flask(__name__)

@app.route('/')
def main():
    return 'hi there'

@app.route('/job_search')
def search_jobs_():
    search_jobs.main()

@app.route('/view_jobs')
def view_jobs():
    return redirect("static/results.txt")

if __name__== '__main__':
    app.run()