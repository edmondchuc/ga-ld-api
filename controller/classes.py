"""
This file contains all the HTTP routes for classes from the IGSN model, such as Samples and the Sample Register
"""
from flask import Blueprint, render_template, request, Response
import _config as conf
from model.sample_register_renderer import SampleRegisterRenderer
from model.sample_renderer import SampleRenderer

classes = Blueprint('classes', __name__)


@classes.route('/sample/<string:igsn>')
def sample(igsn):
    """
    A single Sample

    :return: HTTP Response
    """
    s = SampleRenderer(request, conf.URI_SAMPLE_INSTANCE_BASE + igsn, igsn)
    return s.render()


@classes.route('/sample/<string:igsn>/pingback', methods=['GET', 'POST'])
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


@classes.route('/sample/')
def samples():
    """
    The Register of Samples

    :return: HTTP Response
    """

    class_uri_of_register_items = 'http://pid.geoscience.gov.au/def/ont/igsn#Sample'

    r = SampleRegisterRenderer(request,
                         class_uri_of_register_items,
                         'Sample Register',
                         'A register of Samples',
                         None,
                         class_uri_of_register_items,
                         len(class_uri_of_register_items), #TODO: (Edmond) - not sure if this parameter affects anything? since this parameter is clearly wrong (it's not the total number of items in the dataset)
                         conf.REGISTER_BASE_URI
    )

    return r.render()
