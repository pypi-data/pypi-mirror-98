""" This module contains general utulity functions """

import math
from .utilities import get_field_name_from_reference_property
from .utilities import get_class_name_from_reference_property


def get_classification_configuration(client):
    """ get the classification configuration from Weaviate """

    # initialize the return value
    ccuuid = None

    # prepare the query to get the uuid of the classification configuration
    query = """ { Get { ClassificationConfiguration { _additional { id } } } } """

    if client is not None:
        # query Weaviate
        result = client.query.raw(query)

        # check if there were any errors, if not set the return value
        if result is not None and result['errors'] is None:
            if len(result['data']['Get']["ClassificationConfiguration"]) > 0:
                ccuuid = result['data']['Get']["ClassificationConfiguration"][0]["_additional"]["id"]

    return ccuuid


def count_number_of_unvalidated_datapoints(client, classname):
    """ Count the number of datapoints in Weaviate """

    # initialize the return value
    count = 0

    # prepare the aggregate query to Weaviate: insert the name of the main class
    template = """ { Aggregate { %s (where: { operator:Equal path:["validated"] valueBoolean:false }) { meta { count } } } }"""
    query = template % (classname)

    # query Weaviate
    result = client.query.raw(query)

    # check if there were any errors, if not set the return value
    if result is not None:
        if result['errors'] is None:
            count = result['data']['Aggregate'][classname][0]["meta"]["count"]
        else:
            print(result['errors'])
    return count


def count_number_of_datapoints(client, classname):
    """ Count the number of datapoints in Weaviate """

    # initialize the return value
    count = 0

    # prepare the aggregate query to Weaviate: insert the name of the main class
    template = """ { Aggregate { %s { meta { count } } } } """
    query = template % (classname)

    # query Weaviate
    result = client.query.raw(query)

    # check if there were any errors, if not set the return value
    if result is not None:
        if result['errors'] is None:
            count = result['data']['Aggregate'][classname][0]["meta"]["count"]
        else:
            print(result['errors'])
    return count


def _create_base_whereclause_row_numbers(minrow, maxrow):

    # initialize the return value
    whereclause = {}

    # the basic clause includes a number of operands that all need to be True.
    whereclause = {}
    whereclause['operator'] = "And"
    whereclause['operands'] = []

    # add the operand that selects only those data points that have not yet been verified
    operand = {}
    operand["path"] = ["validated"]
    operand["operator"] = "Equal"
    operand["valueBoolean"] = False
    whereclause['operands'].append(operand)

    # add the operand that selects data points from a row higher than (or equal to) minrow
    operand = {}
    operand["path"] = ["row"]
    operand["operator"] = "GreaterThanEqual"
    operand["valueInt"] = minrow
    whereclause['operands'].append(operand)

    # add the operand that selects data points from a row lower than maxrow
    operand = {}
    operand["path"] = ["row"]
    operand["operator"] = "LessThan"
    operand["valueInt"] = maxrow
    whereclause['operands'].append(operand)

    return whereclause


def create_get_query_row_numbers(client, config, dataconfig, minrow, maxrow):
    """ create get query """

    if client is not None and config is not None and dataconfig is not None:

        # Get the name of the thing we are classifying
        thingname = dataconfig['classname']

        # Get the names of the properties that we are classifying
        properties = ['row', 'validated', 'batchNumber']
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                field = get_field_name_from_reference_property(prop)
                properties.append(field)

                classname = get_class_name_from_reference_property(prop)
                properties.append("""%s { ...on %s { name } }""" % (prop, classname))

        # Create the where clause in case we do a dynamic selection of training data
        whereclause = _create_base_whereclause_row_numbers(minrow, maxrow)

        query = client.query\
            .get(thingname, properties)\
            .with_limit(10000)\
            .with_where(whereclause)\
            .build()

    return query


def _create_base_whereclause_batch_number(batch):

    # initialize the return value
    whereclause = {}

    # the basic clause includes a number of operands that all need to be True.
    whereclause['operator'] = "And"
    whereclause['operands'] = []

    # add the operand that selects only those data points that have not yet been verified
    operand = {}
    operand["path"] = ["validated"]
    operand["operator"] = "Equal"
    operand["valueBoolean"] = False
    whereclause['operands'].append(operand)

    # add the operand that selects the right batch number
    operand = {}
    operand["path"] = ["batchNumber"]
    operand["operator"] = "Equal"
    operand["valueInt"] = batch
    whereclause['operands'].append(operand)

    return whereclause


def create_get_query_batch_number(client, config, dataconfig, batch):
    """ create get query """

    if client is not None and config is not None and dataconfig is not None:

        # Get the name of the thing we are classifying
        thingname = config['classification']['classify_class']

        # Get the names of the properties that we are classifying
        properties = ['_additional { id }', 'row', 'validated', 'batchNumber', 'preClassified']
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                field = get_field_name_from_reference_property(prop)
                properties.append(field)

                classname = get_class_name_from_reference_property(prop)
                properties.append("""%s { ...on %s { name } }""" % (prop, classname))

        # Create the where clause in case we do a dynamic selection of training data
        whereclause = _create_base_whereclause_batch_number(batch)

        query = client.query\
            .get(thingname, properties)\
            .with_limit(10000)\
            .with_where(whereclause)\
            .build()

    return query


def get_all_classified_datapoints(client, config, dataconfig):
    """ pulls all points that have been classified from Weaviate """

    # initialize the return value
    datapoints = []

    if client is not None and config is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # get the maximum batch size from the config file
        maxbatch = 10000
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_unvalidated_datapoints(client, classname)

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            result = client.query.raw(query)
            if result is not None and 'data' in result:
                datapoints += result['data']['Get'][classname]

    return datapoints
