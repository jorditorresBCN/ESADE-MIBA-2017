import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello(name=None):
    return render_template('template1.html', name=name)


@app.route('/predict', methods=['POST'])
def predict(name=None):
    from grpc.beta import implementations
    import tensorflow as tf
    from tensorflow_serving.apis import predict_pb2
    from tensorflow_serving.apis import prediction_service_pb2
    print request
    file = request.files['file']
    file_root = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_root)
    host = "localhost"
    port = "8888"
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    # Send request
    try:
        with open(file_root, 'rb') as f:
            # See prediction_service.proto for gRPC request/response details.
            data = f.read()
            request_tf = predict_pb2.PredictRequest()
            request_tf.model_spec.name = 'inception'
            request_tf.model_spec.signature_name = 'predict_images'
            request_tf.inputs['images'].CopyFrom(
                tf.contrib.util.make_tensor_proto(data, shape=[1]))
            result_tf = stub.Predict(request_tf, 10.0)  # 10 secs timeout
            result = []
            for v in result_tf.outputs['classes'].string_val:
                result.append(v)
    except:
        result = ["error",]

    return jsonify(result)
