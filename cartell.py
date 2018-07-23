# -*- coding: utf-8 -*-
import commands
import json
import os
import time
import urllib

import datetime
import requests


def submit(url, data, header):
    try:
        submit_url = url + 'problem/submit/'
        response = requests.post(url=submit_url, data=data, headers=header)
        return response.json()
    except Exception as e:
        response = '\nError at submit()'
        logger.write(response + '\n')
        logger.write(e + '\n')
        return -1


def generate_submit_data(problem_id, team_id, category):
    submit_data = {"problem": problem_id, "solution": {"category": category}, "team": team_id}
    print 'Submit data: ', submit_data
    submit_data = json.dumps(submit_data)

    submit_result = submit(base_url, submit_data, headers)
    print 'Submit response: ', submit_result, '\n'


def fetch_problem(url, header):
    try:
        response = requests.get(url, headers=header)
        return response.json()
    except Exception as e:
        response = '\nError at fetch_problem()'
        logger.write(response + '\n')
        logger.write(e + '\n')
        return -1


def problem_set(url, header):
    try:
        problem_set_url = url + 'problem-set/'
        response = requests.get(problem_set_url, headers=header)
        return response.json()
    except Exception as e:
        response = '\nError at problem_set()'
        logger.write(response + '\n')
        logger.write(e + '\n')
        return -1


def current_iteration(url, header):
    try:
        iteration_url = url + 'current-iteration/'
        response = requests.get(iteration_url, headers=header)
        return response.json()
    except Exception as e:
        response = '\nError at current_iteration()'
        logger.write(response + '\n')
        logger.write(e + '\n')
        return -1


def login(url):
    login_url = url + 'login/'
    login_data = {'name': 'T.H.A.N.O.S', 'token': 'nr8WgLBi73'}
    response = requests.post(url=login_url, data=login_data)
    return response.json()


if __name__ == "__main__":
    base_url = 'http://10.7.40.23/api/'
    index = ('mahindra', 'honda', 'toyota', 'suzuki', 'tata', 'ford', 'hyundai', 'volkswagen')

    date = str(datetime.datetime.now())
    log_date = date[:10] + '.log'
    logger = open(log_date, 'a+')

    login_response = login(base_url)
    team_id = login_response['team']['id']
    print 'Login response: ', login_response

    headers = {'Content-Type': 'application/json', 'TOKEN': login_response['auth_token']}

    while True:
        iteration_response = current_iteration(base_url, headers)
        iteration = iteration_response['current-iteration']
        print 'Current iteration: ', iteration_response
        if iteration != -1:
            break
        time.sleep(1)
    # time.sleep(4)
    iteration_name = 'iteration-' + str(iteration)

    problem_set = problem_set(base_url, headers)
    if problem_set != -1:
        print '\nFetched problem set successfully!\n'
        logger.write('\n------------------------------- ITERATION ' + str(iteration) + '-------------------------------\n')

    problem_url = 'problem/{id}/'
    problem_count = 1
    for problem in problem_set:
        print '\n-------------------------------', 'Problem: ', str(problem_count), '-------------------------------'
        problem_count += 1
        problem_id = problem['id']
        problem_fetch_url = base_url + problem_url.format(id=problem_id)

        problem_response = fetch_problem(problem_fetch_url, headers)
        if problem_response == -1:
            logger.write('Error while fetching problem: ' + problem_id + '\n')
            continue
        problem_details = problem_response['problem']
        problem_title = problem_details['title'].encode('utf-8')
        problem_description = problem_details['description'].encode('utf-8')
        ext = problem_description.split('.')[-1]

        image_name = "{}.{}".format(problem_id, ext)
        image_path = iteration_name + '/' + image_name
        try:
            urllib.urlretrieve(problem_description, image_path)
        except Exception as e:
            logger.write('Error while fetching url: ' + problem_description + '\n')

    cwd = os.getcwd()
    files = os.listdir(cwd + '/' + iteration_name)

    problem_count = 1
    for image in files:
        print '\n-------------------------------', 'Submission: ', str(problem_count), '-------------------------------'
        problem_count += 1
        command = "python label_image.py \
        --graph=output/output_graph.pb \
        --labels=output/output_labels.txt \
        --input_layer=Placeholder \
        --output_layer=final_result \
        --image={}/{}".format(iteration_name, image)

        status, result = commands.getstatusoutput(command)
        result_list = result.split('\n')

        #TODO Modify the format according to the new result
        for result in result_list:
            if result.startswith(index):
                brand = result.split(' ')
                result = brand[0] + '-' + brand[1]
                problem_id = image.split('.')[0]
                logger.write(problem_id + ' ' + result + '\n')
                generate_submit_data(problem_id, team_id, result)
                break

    logger.close()
