from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)


with open('RidgeModel2.pkl', 'rb') as file:
    model = pickle.load(file)

# The exact address categories the model was trained on.
# The pipeline's OneHotEncoder only recognizes these values -
# anything else is handled by handle_unknown='ignore', so we
# expose exactly these choices in the dropdown to keep predictions reliable.
ADDRESSES = [
    'other',
    'Huidekoperstraat 24 F, Amsterdam',
    'Uilengouw 2, Amsterdam',
    'Nieuwevaartweg, Amsterdam',
    'Quashibastraat, Amsterdam',
    'Ringdijk, Amsterdam',
]



@app.route('/')
def index():
    return render_template('index.html', addresses=ADDRESSES)



@app.route('/predict', methods=['POST'])
def predict():
    try:

        address = request.form.get('address')
        area = float(request.form.get('area'))
        rooms = int(request.form.get('rooms'))


        input_df = pd.DataFrame(
            [[address, area, rooms]],
            columns=['Address', 'Area', 'Room']
        )


        predicted_price = model.predict(input_df)[0]


        formatted_price = f"€ {predicted_price:,.2f}"


        return render_template(
            'index.html',
            addresses=ADDRESSES,
            prediction_text=formatted_price,
            form_values={'address': address, 'area': area, 'rooms': rooms}
        )

    except (TypeError, ValueError):

        return render_template(
            'index.html',
            addresses=ADDRESSES,
            error_text='Please enter a valid number for area and rooms.'
        )
    except Exception as e:
        return render_template(
            'index.html',
            addresses=ADDRESSES,
            error_text=f'Something went wrong: {e}'
        )


if __name__ == '__main__':
    app.run(debug=True)