import dimod
from jijcloud.client import JijCloudClient
from logging import getLogger
from typing import Type, TypeVar, Dict, Any
from jijcloud.response import APIStatus, BaseResponse
import time

logger = getLogger(__name__)

def post_instance_and_query(
        ResponseType: Type[TypeVar('ResponseType', bound='BaseResponse')],
        client: JijCloudClient,
        instance_type: str, instance: Dict[str, Any], solver: str, parameters: dict,
        sync: bool = True):
    
    # Instance を投げる
    logger.info("uploading instance ...")
    instance_id = client.post_instance(instance_type, instance)

    # Solverにqueryをなげる
    logger.info("submitting query ...")
    solver_res = client.submit_solve_query(solver, parameters, instance_id)

    # 同期モードで解を取得
    status = 'PENDING'
    if sync:
        logger.info("polling...")
        while status == APIStatus.PENDING.value:
            response = client.fetch_result(solver_res['solution_id'])
            status = response['status']
            if response['status'] == APIStatus.SUCCESS.value:
                break
            elif response['status'] == APIStatus.FAILED.value:
                return  ResponseType.empty_response(
                            APIStatus.FAILED,
                            client.url, client.token,
                            solver_res['solution_id'],
                            err_dict=response['solution'])

            elif response['status'] == APIStatus.UNKNOWNERROR.value:
                return ResponseType.empty_response(
                            APIStatus.UNKNOWNERROR,
                            client.url, client.token,
                            solver_res['solution_id'])

            time.sleep(2)

    else:
        return ResponseType.empty_response(
                    APIStatus.PENDING,
                    client.url, client.token,
                    solver_res['solution_id'])

    res_obj = ResponseType.from_json_obj(response['solution'])
    res_obj.set_status(APIStatus.SUCCESS)
    return res_obj
