import copy
import os
import shutil
import time
from io import BytesIO

from dateutil.parser import parse as parse_datetime
from flask import request, send_file
from flask_restx import Resource, abort
from flask import current_app as ca

from mindsdb.utilities.log import log
from mindsdb.api.http.namespaces.configs.predictors import ns_conf
from mindsdb.api.http.namespaces.entitites.predictor_metadata import (
    predictor_metadata,
    predictor_query_params,
    upload_predictor_params,
    put_predictor_params
)
from mindsdb.api.http.namespaces.entitites.predictor_status import predictor_status

def preparse_results(results, format_flag='explain'):
    response_arr = []
    for res in results:
        if format_flag == 'explain':
            response_arr.append(res.explain())
        elif format_flag == 'epitomize':
            response_arr.append(res.epitomize())
        elif format_flag == 'new_explain':
            response_arr.append(res.explanation)
        else:
            response_arr.append(res.explain())

    if len(response_arr) > 0:
        return response_arr
    else:
        abort(400, "")

def is_custom(name):
    if name in [x['name'] for x in ca.custom_models.get_models()]:
        return True
    return False

@ns_conf.route('/')
class PredictorList(Resource):
    @ns_conf.doc('list_predictors')
    @ns_conf.marshal_list_with(predictor_status, skip_none=True)
    def get(self):
        '''List all predictors'''

        return [*ca.mindsdb_native.get_models(),*ca.custom_models.get_models()]

@ns_conf.route('/custom/<name>')
@ns_conf.param('name', 'The predictor identifier')
@ns_conf.response(404, 'predictor not found')
class CustomPredictor(Resource):
    @ns_conf.doc('put_custom_predictor')
    def put(self, name):
        try:
            trained_status = request.json['trained_status']
        except:
            trained_status = 'untrained'

        predictor_file = request.files['file']
        fpath = os.path.join(ca.config_obj.paths['tmp'],  name + '.zip')
        with open(fpath, 'wb') as f:
            f.write(predictor_file.read())

        ca.custom_models.load_model(fpath, name, trained_status)

        return f'Uploaded custom model {name}'

@ns_conf.route('/<name>')
@ns_conf.param('name', 'The predictor identifier')
@ns_conf.response(404, 'predictor not found')
class Predictor(Resource):
    @ns_conf.doc('get_predictor')
    @ns_conf.marshal_with(predictor_metadata, skip_none=True)
    def get(self, name):
        try:
            if is_custom(name):
                model = ca.custom_models.get_model_data(name)
            else:
                model = ca.mindsdb_native.get_model_data(name, db_fix=False)
        except Exception as e:
            abort(404, "")

        for k in ['train_end_at', 'updated_at', 'created_at']:
            if k in model and model[k] is not None:
                model[k] = parse_datetime(model[k])

        return model

    @ns_conf.doc('delete_predictor')
    def delete(self, name):
        '''Remove predictor'''
        if is_custom(name):
            ca.custom_models.delete_model(name)
        else:
            ca.mindsdb_native.delete_model(name)

        return '', 200

    @ns_conf.doc('put_predictor', params=put_predictor_params)
    def put(self, name):
        '''Learning new predictor'''
        data = request.json
        to_predict = data.get('to_predict')

        try:
            kwargs = data.get('kwargs')
        except:
            kwargs = None

        if type(kwargs) != type({}):
            kwargs = {}

        if 'equal_accuracy_for_all_output_categories' not in kwargs:
            kwargs['equal_accuracy_for_all_output_categories'] = True

        if 'advanced_args' not in kwargs:
            kwargs['advanced_args'] = {}

        if 'use_selfaware_model' not in kwargs['advanced_args']:
            kwargs['advanced_args']['use_selfaware_model'] = False

        try:
            retrain = data.get('retrain')
            if retrain in ('true', 'True'):
                retrain = True
            else:
                retrain = False
        except Exception:
            retrain = None

        ds_name = data.get('data_source_name') if data.get('data_source_name') is not None else data.get('from_data')
        from_data = ca.default_store.get_datasource_obj(ds_name, raw=True)

        if from_data is None:
            return {'message': f'Can not find datasource: {ds_name}'}, 400

        if retrain is True:
            original_name = name
            name = name + '_retrained'

        ca.mindsdb_native.learn(name, from_data, to_predict, ca.default_store.get_datasource(ds_name)['id'], kwargs)
        for i in range(20):
            try:
                # Dirty hack, we should use a messaging queue between the predictor process and this bit of the code
                ca.mindsdb_native.get_model_data(name)
                break
            except Exception:
                time.sleep(1)

        if retrain is True:
            try:
                ca.mindsdb_native.delete_model(original_name)
                ca.mindsdb_native.rename_model(name, original_name)
            except:
                pass

        return '', 200

@ns_conf.route('/<name>/learn')
@ns_conf.param('name', 'The predictor identifier')
class PredictorLearn(Resource):
    def post(self, name):
        data = request.json
        to_predict = data.get('to_predict')
        kwargs = data.get('kwargs', None)

        if type(kwargs) != type({}):
            kwargs = {}

        if 'advanced_args' not in kwargs:
            kwargs['advanced_args'] = {}


        ds_name = data.get('data_source_name') if data.get('data_source_name') is not None else data.get('from_data')
        from_data = ca.default_store.get_datasource_obj(ds_name, raw=True)

        ca.custom_models.learn(name, from_data, to_predict, ca.default_store.get_datasource(ds_name)['id'], kwargs)

        return '', 200


@ns_conf.route('/<name>/predict')
@ns_conf.param('name', 'The predictor identifier')
class PredictorPredict(Resource):
    @ns_conf.doc('post_predictor_predict', params=predictor_query_params)
    def post(self, name):
        '''Queries predictor'''

        data = request.json

        when = data.get('when') or {}
        try:
            format_flag = data.get('format_flag')
        except:
            format_flag = 'explain'

        try:
            kwargs = data.get('kwargs')
        except:
            kwargs = {}

        if type(kwargs) != type({}):
            kwargs = {}

        if is_custom(name):
            return ca.custom_models.predict(name, when_data=when, **kwargs)
        else:
            results = ca.mindsdb_native.predict(name, when_data=when, **kwargs)

        return preparse_results(results, format_flag)


@ns_conf.route('/<name>/predict_datasource')
@ns_conf.param('name', 'The predictor identifier')
class PredictorPredictFromDataSource(Resource):
    @ns_conf.doc('post_predictor_predict', params=predictor_query_params)
    def post(self, name):
        data = request.json

        from_data = ca.default_store.get_datasource_obj(data.get('data_source_name'))
        if from_data is None:
            abort(400, 'No valid datasource given')

        try:
            format_flag = data.get('format_flag')
        except Exception:
            format_flag = 'explain'

        try:
            kwargs = data.get('kwargs')
        except Exception:
            kwargs = {}

        if not isinstance(kwargs, dict):
            kwargs = {}

        if is_custom(name):
            return ca.custom_models.predict(name, from_data=from_data, **kwargs)

        results = ca.mindsdb_native.predict(name, when_data=from_data, **kwargs)
        return preparse_results(results, format_flag)

@ns_conf.route('/<name>/rename')
@ns_conf.param('name', 'The predictor identifier')
class PredictorDownload(Resource):
    @ns_conf.doc('get_predictor_download')
    def get(self, name):
        '''Export predictor to file'''
        try:
            new_name = request.args.get('new_name')
            if is_custom(name):
                ca.custom_models.rename_model(name, new_name)
            else:
                ca.mindsdb_native.rename_model(name, new_name)
        except Exception as e:
            return str(e), 400

        return f'Renamed model to {new_name}', 200
