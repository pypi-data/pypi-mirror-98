""" This module calculates the confidence score from classification by Weaviate """

from .utilities import get_weaviate_client
from .utilities import get_conf_score_field_name_from_ref_prop
from .utilities import get_conf_bucket_field_name_from_ref_prop
from .query import get_all_classified_datapoints


def _extract_classification_scores(config, dataconfig, point):

    # initialize the return value
    score = {}

    if config is not None and dataconfig is not None and point is not None:

        # check if the point is pre-classified. If so, all scores should be 1.0
        preclass = False
        if 'preClassified' in point['properties'] and point['properties']['preClassified']:
            preclass = True

        for prop in config['classification']['classify_properties']:
            if 'properties' in point and prop in point['properties'] and len(point['properties'][prop]) > 0:
                if preclass:
                    score[prop] = 1.0
                elif 'classification' in point['properties'][prop][0]:
                    outcome = point['properties'][prop][0]['classification']
                    score[prop] = outcome['winningCount'] / outcome['overallCount']

    return score


def get_bucket_id(buckets, score):
    """ returns the right bucket identifier for the argument score """

    # initialize the return value
    result = 0
    if score > 0.0:
        for bid in buckets:
            if buckets[bid]['lower'] < score <= buckets[bid]['upper']:
                result = bid

    return result


def get_confidence_buckets(config):
    """ reads the confidence buckets from the file indicated by argument config """

    # initialize the return value
    buckets = {}

    # get the confidence score intervals from the config file (if present). Default = [0.0, 1.0]
    if config is not None and 'classification' in config and 'confidence_buckets' in config['classification']:
        intervals = config['classification']['confidence_buckets']
    else:
        intervals = [0.0, 1.0]

    length = len(intervals)
    for count in range(length-1):
        buckets[count] = {}
        buckets[count]['lower'] = intervals[count]
        buckets[count]['upper'] = intervals[count+1]
        buckets[count]['correct'] = 0
        buckets[count]['incorrect'] = 0
        buckets[count]['count'] = 0

    return buckets


def calculate_confidence_scores(client, config, dataconfig):
    """ calculate the confidence scores for datapoints """
    # pylint: disable=protected-access

    # first get the confidence buckets from the config file
    buckets = get_confidence_buckets(config)

    count = 0
    datapoints = get_all_classified_datapoints(client, config, dataconfig)
    for point in datapoints:
        if '_additional' in point and 'id' in point['_additional']:
            count += 1
            puuid = point['_additional']['id']
            path = "/objects/" + puuid + "?include=classification"
            result = client._connection.run_rest(path, 0)
            score = _extract_classification_scores(config, dataconfig, result.json())
            for prop in score:

                # initialize the update
                update = {}

                # calculate the confidence score
                scoreprop = get_conf_score_field_name_from_ref_prop(prop)
                update[scoreprop] = score[prop]

                # calculate the confidence bucket
                bucketprop = get_conf_bucket_field_name_from_ref_prop(prop)
                update[bucketprop] = get_bucket_id(buckets, score[prop])

                # do the actual update
                client.data_object.update(update, "Component", puuid)

                print("Number of data points scored ----------:", count, end="\r")
    print("Number of data points scored ----------:", count)


def calculate_confidence_score_for_point(config, dataconfig, puuid):
    """ calculate the confidence score for a datapoint """
    # pylint: disable=protected-access

    # initialize the return value
    score = None

    # get the Weaviate client
    client = get_weaviate_client(config)

    if client is not None and dataconfig is not None:
        path = "/objects/" + puuid + "?include=classification"
        result = client._connection.run_rest(path, 0)
        score = _extract_classification_scores(config, dataconfig, result.json())

    return score
