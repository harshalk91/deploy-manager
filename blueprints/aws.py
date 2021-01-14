from flask import Flask, render_template, Blueprint, Response, request
from services.AWSService import AWSService
import os
import json

bp = Blueprint('aws', __name__)

@bp.route('/api/aws/deployments', methods=['GET'])
def aws_deployments():
    aws_service = AWSService()
    provider_id = request.args.get('query')
    response = json.dumps(aws_service.get_all_aws_deployments(provider_id=provider_id))
    return response