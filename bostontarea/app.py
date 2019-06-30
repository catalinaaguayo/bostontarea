import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'model/bostontarea.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')
app = flask.Flask(__name__, static_url_path='/static')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        habitaciones = flask.request.form['habitaciones']
        propietarios = flask.request.form['propietarios']
        estudiantes = flask.request.form['estudiantes']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[habitaciones, propietarios, estudiantes]],
                                       columns=['RM', 'LSTAT', 'PTRATIO'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'habitaciones':habitaciones,
                                                     'propietarios':propietarios,
                                                     'estudiantes':estudiantes},
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()