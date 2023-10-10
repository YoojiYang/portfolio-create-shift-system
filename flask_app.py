from flask import Flask, render_template
app = Flask(__name__)

from .assign_system.assign_system import assign_system

@app.route('/')

def index():
  return render_template (
    'index.html'
  )


@app.route('/run_script', methods=['POST'])
def run_script():
  try:
    assign_system()
    return "Script executed", 200
  except Exception as e:
    return f"Error: {str(e)}", 500