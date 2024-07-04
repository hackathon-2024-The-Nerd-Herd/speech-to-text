from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        if 'text' in data:
            text = data['text']
            with open('recognized_text.txt', 'w') as file:
                file.write(text)
            return jsonify({'message': 'File saved successfully'})
        else:
            return jsonify({'error': 'Text not found in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-file', methods=['GET'])
def get_file_contents():
    try:
        with open('recognized_text.txt', 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
