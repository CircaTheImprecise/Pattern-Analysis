from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Predefined patterns to look for in the Excel sheet
value_patterns = {
    'Pattern1': ['A', 'B', 'C'],
    'Pattern2': [1, 2, 3],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_excel(file)

        # Check for predefined patterns
        matched_patterns = check_for_patterns(df)

        return render_template('result.html', patterns=matched_patterns)

    return redirect(request.url)

def check_for_patterns(data_frame):
    matched_patterns = {}

    for pattern_name, pattern_values in value_patterns.items():
        if set(pattern_values).issubset(set(data_frame.values.flatten())):
            matched_patterns[pattern_name] = True
        else:
            matched_patterns[pattern_name] = False

    return matched_patterns

if __name__ == '__main__':
    app.run(debug=True)
