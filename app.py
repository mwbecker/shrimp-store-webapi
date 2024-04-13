# app.py
from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
import json
from searchHelper import fuzzy_search
app = Flask(__name__)
cors = CORS(app)

global shrimps_data
f = open('shrimps.json')
shrimps_data = json.load(f)
image_folder = 'assets/images'

@app.route('/shrimps', methods=["GET", "PUT", "POST"])
def index():
  if request.method == 'GET':
    return jsonify(shrimps_data)
  elif request.method == 'PUT':
    shrimp = request.json
    ind = next((index for index, d in enumerate(shrimps_data) if d.get('id') == shrimp['id']))
    shrimps_data.pop(ind)
    shrimps_data.insert(ind, shrimp)
    return Response(status=200)
  elif request.method == 'POST':
    shrimp_name = request.json['name']
    max_id = max(shrimps_data, key=lambda x: x["id"])["id"]      
    new_object = (
         {
           'id':max_id+1,
           'name': shrimp_name
         }
    )
    shrimps_data.append(new_object)
    return jsonify(new_object)
      

@app.route('/shrimps/<int:shrimp_id>', methods=['GET', 'DELETE'])
def get_shrimp_by_id(shrimp_id):
  if request.method == 'GET':
    shrimp = list(filter(lambda shrimp: shrimp['id'] == shrimp_id, shrimps_data))
    if shrimp:
        return jsonify(shrimp[0]), 200
    else:
        return jsonify({'error': 'User not found'}), 404
  elif request.method == 'DELETE':
    ind = next((index for index, d in enumerate(shrimps_data) if d.get('id') == shrimp_id))
    shrimps_data.pop(ind)
    return Response(status=200)

@app.route('/shrimps/', methods=["GET", "PUT", "POST"])
def search():
  search_name = request.args.get('name')
  if search_name is not None:
    return jsonify(fuzzy_search(shrimps_data, 'name', search_name))
  
@app.route('/imgs/<int:shrimp_id>')
def getImg(shrimp_id):
    shrimp = list(filter(lambda shrimp: shrimp['id'] == shrimp_id, shrimps_data))[0]

    image_path = image_folder + "/" + shrimp['imageUrl']
    
    # Set the MIME type to JPEG
    mime_type = 'image/jpeg'
    
    # Return the image file
    try:
      return send_file(image_path, mimetype=mime_type)
    except:
      return Response(status=500)

if __name__ == '__main__':
    app.run(debug=True)