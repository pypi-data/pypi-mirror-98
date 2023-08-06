import json
import logging
import random
# Global variables
from concurrent.futures.thread import ThreadPoolExecutor
from json import JSONDecodeError

import requests

from enrich_pkg.custom_call_exception import CustomCallException

mappings = {}
enrichment_returned_data_dict = {}
user_data = {}
enrich_targets = {}


def log_with_tabs(depth, string_output):
    logging_str = ''
    for _ in range(0, depth):
        logging_str += '\t'
    logging_str += string_output
    logging.info(logging_str)


def get_value_from_mapping(which_one, param):
    incoming_user_data = ''
    if which_one in mappings and param in mappings[which_one]:
        incoming_var_name = mappings[which_one][param]
        if incoming_var_name in user_data.keys():
            incoming_user_data = user_data[incoming_var_name]
        else:
            if '_1_app_'+incoming_var_name in user_data.keys():
                incoming_user_data = user_data['_1_app_'+incoming_var_name]
    return incoming_user_data


def get_payload(which_one):
    request_params = {}
    params = enrich_targets.get(which_one).get('params')
    for param in params:
        incoming_user_data = get_value_from_mapping(which_one, param)
        request_params[param] = incoming_user_data

    return request_params


def get_body(which_one):
    body_shell = enrich_targets.get(which_one).get('body').copy()
    for key in body_shell:
        incoming_user_data = get_value_from_mapping(which_one, key)
        incoming_user_data_raw = incoming_user_data
        if isinstance(incoming_user_data, str) and isinstance(body_shell.get(key), bool):
            incoming_user_data = (incoming_user_data.lower() == 'true')
        if incoming_user_data_raw != '':
            if body_shell.__getitem__(key) != '':
                next_entry = body_shell.__getitem__(key)
                for subkey in next_entry:
                    body_shell[key][subkey] = incoming_user_data
            else:
                body_shell[key] = incoming_user_data
    return body_shell


def call_specific_enrichment(which_one):
    url = enrich_targets.get(which_one).get('url')
    mechanism = enrich_targets.get(which_one).get('mechanism')
    r = {}
    try:

        if mechanism == 'GET':
            payload = get_payload(which_one)
            if payload != '':
                r = requests.get(url, params=payload)
            else:
                r = requests.get(url)
        elif mechanism == 'POST':
            body = get_body(which_one)
            # NOTE - have to do the json.dumps, and the header -
            # otherwise we get back an offset in the return, making it not json!!
            payload = json.dumps(body)
            headers = {"Content-type": "application/json"}
            r = requests.post(url, data=payload, headers=headers)

    except requests.exceptions.HTTPError as errh:
        enrichment_returned_data_dict[which_one] = dict(result='failure', data={'http_error': errh})
        raise CustomCallException(errh)
    except requests.exceptions.ConnectionError as errc:
        enrichment_returned_data_dict[which_one] = dict(result='failure', data={'connection_error': errc})
        raise CustomCallException(errc)
    except requests.exceptions.Timeout as errt:
        enrichment_returned_data_dict[which_one] = dict(result='failure', data={'timeout_error': errt})
        raise CustomCallException(errt)
    except requests.exceptions.RequestException as err:
        logging.error('ERROR calling %s [%s]' % (which_one, err.args))
        enrichment_returned_data_dict[which_one] = dict(result='failure', data={'other_error': err.args})
        raise CustomCallException(err)

    return {'r': r, 'mechanism': mechanism, 'url': url}


def call_enrichment(which_one, depth):
    log_with_tabs(depth, 'calling enrichment %s' % which_one)
    if which_one in enrich_targets.keys():
        r_dict = call_specific_enrichment(which_one)

        try:
            enrichment_returned_data_dict[which_one] = dict(result='success',
                                                            data=r_dict['r'].json())
        except JSONDecodeError as err:
            logging.error("Json decode error on %s to %s: %s" % (r_dict['mechanism'], r_dict['url'], err))
            enrichment_returned_data_dict[which_one] = dict(result='failure',
                                                            data=(r_dict['mechanism'], r_dict['url'], err))
            raise Exception((r_dict['mechanism'], r_dict['url'], err))
    else:
        logging.error('No such target for enrichment %s' % which_one)
        raise Exception('No such target for enrichment %s' % which_one)


def serial_enrich_with_failover(serial_steps, failover_steps, depth):
    log_with_tabs(depth, 'in serialEnrichWithFailover %s %s' % (serial_steps, failover_steps))
    # Serially run those in serialSteps.  If any exceptions arise, switch and call those in failoverSteps
    on_which_step = ''
    try:
        for on_which_step in serial_steps:
            call_enrichment(on_which_step, depth + 1)
    except CustomCallException:
        logging.error("Exception raised in serial steps %s, failed on %s. Calling failover steps %s" %
                      (serial_steps, on_which_step, failover_steps))
        try:
            for on_which_step in failover_steps:
                call_enrichment(on_which_step, depth + 1)
        except CustomCallException:
            logging.error('Failed on fail-over calls - enrichment data will be lost %s' % on_which_step)


def run_single_step(a_step, depth, ran=100):
    lower = a_step.get('stepBoundsLower', 0)
    upper = a_step.get('stepBoundsUpper', 100)
    what = a_step.get('what', 'missing')

    if lower <= ran <= upper:
        log_with_tabs(depth, 'What %s, LowerBound %s, Upperbound %s' % (what, lower, upper))

        if 'serialsteps' in a_step.keys():
            # failoversteps are optional, will show as 'missing' in method
            serial_enrich_with_failover(a_step.get('serialsteps'), a_step.get('failoversteps', 'missing'), depth + 1)
        elif what.find(';') < 0:
            # At the end of the path, call the enrichment
            try:
                call_enrichment(what, depth)
            except CustomCallException as cce:
                logging.error('Failed on enrichment step %s\n\t%s' % (what, cce.message.args[0].reason))
        else:
            zstep = a_step.get('steps')
            run_single_step(zstep, depth + 1, ran)


def run_steps(steptuple):
    ran = steptuple[0]
    step_map = steptuple[1]
    for step in step_map['steps']:
        run_single_step(step, 1, ran)


def decide_with_json(enrich_targets_provided, enrich_step_definitions, incoming_mappings, json_user_data):
    """
    enrich_step_definitions:  step definitions in json format, describing how to call which enrichment tool
    incoming_mappings: get dictionary describing how data is mapped from ID to enrichment, and from enrichment to ID
    json_user_data: json data representing data coming from Intelligent Decisioning

    returns: tuple, value_dictionary
    """
    global mappings, user_data, enrichment_returned_data_dict, enrich_targets
    mappings = incoming_mappings
    user_data = json_user_data
    enrichment_returned_data_dict = {}
    enrich_targets = enrich_targets_provided
    concurrent_steps = []

    for a_step in enrich_step_definitions['steps']:
        ran = random.randint(0, 100)
        if 'steps' in a_step:
            concurrent_steps.append((ran, a_step))

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_steps, concurrent_steps)

    return enrichment_returned_data_dict
