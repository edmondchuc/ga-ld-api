"""
This file contains all the HTTP routes for classes from the IGSN model, such as Samples and the Sample Register
"""
from flask import Blueprint, render_template, request, Response
import _config as conf
from model.sample_register_renderer import SampleRegisterRenderer
from model.sample_renderer import SampleRenderer
import pyldapi
import requests
from io import BytesIO
from lxml import etree

classes = Blueprint('classes', __name__)


@classes.route('/api/sample/<string:igsn>')
def sample(igsn):
    """
    A single Sample

    :return: HTTP Response
    """
    s = SampleRenderer(request, conf.URI_SAMPLE_INSTANCE_BASE + igsn, igsn)
    return s.render()


@classes.route('/api/sample/<string:igsn>/pingback', methods=['GET', 'POST'])
def sample_pingback(igsn):
    if request.method == 'GET':
        return Response(
            'This endpoint is the individual PROV "pingback" endpoint for Sample {}. It is expected to be used in '
            'accordance with the PROV-AQ Working Group Note (https://www.w3.org/TR/prov-aq/).'.format(igsn),
            mimetype='text/plain'
        )

    # TODO: validate the pingback
    valid = True
    if valid:
        return Response(
            'This is a test response, no action has been taken with the pingback information',
            status=204,
            mimetype='text/plain'
        )
    else:
        return Response(
            'The pingback message submitted is not valid',
            status=400,
            mimetype='text/plain'
        )


@classes.route('/api/sample/register')
def samples():
    """
    The Register of Samples

    :return: HTTP Response
    """

    # get the total register count from the XML API
    try:
        r = requests.get(conf.XML_API_URL_TOTAL_COUNT)
        no_of_samples = int(r.content.decode('utf-8').split('<RECORD_COUNT>')[1].split('</RECORD_COUNT>')[0])

        page = request.values.get('page') if request.values.get('page') is not None else 1
        per_page = request.values.get('per_page') if request.values.get('per_page') is not None else 15
        items = _get_samples_items(page, per_page)

    except Exception as e:
        print(e)
        return Response('The Samples Register is offline', mimetype='text/plain', status=500)

    r = pyldapi.RegisterRenderer(
        request,
        request.url,
        'Sample Register',
        'A register of Samples',
        items,
        ['http://pid.geoscience.gov.au/def/ont/igsn#Sample'],
        no_of_samples
    )

    return r.render()


def _get_samples_items(page, per_page):
    items = []
    r = requests.get(conf.XML_API_URL_SAMPLESET.format(page, per_page), timeout=3)
    xml = r.content

    parser = etree.XMLParser(dtd_validation=False)

    try:
        etree.fromstring(xml, parser)
        xml = BytesIO(xml)

        for event, elem in etree.iterparse(xml):
            if elem.tag == "IGSN":
                items.append(elem.text)

        return items
    except Exception:
        print('not valid xml')
        return None
