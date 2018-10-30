"""
This file contains all the HTTP routes for basic pages (usually HTML)
"""
from flask import Blueprint, render_template


pages = Blueprint('controller', __name__)


@pages.route('/api/sample')
def index():
    """
    A basic landing page for this web service

    :return: HTTP Response (HTML page only)
    """
    return render_template(
        'samples_page_index.html'
    )


@pages.route('/api/sample/about')
def about():
    return render_template(
        'samples_page_about.html'
    )
