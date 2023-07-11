"""
Output Formatting

This module provides a function to format response data in various formats
including csv, xlsx, html, xml, yaml and json.

It also adds the appropriate Content-Disposition header for csv and xlsx formats,
allowing these types of responses to be downloaded as files with the correct filename.

Proper Import: `from ..utils import format_output`
To use the output formatting, replace `return jsonify(results)` with:

.. code-block:: python

    output_format = request.args.get('format', 'json')
    return format_output(results, output_format, 'domain_summary')

"""

import os
import csv
from werkzeug.datastructures import Headers
import pandas as pd
import yaml
from dicttoxml import dicttoxml
from sqlalchemy import text
from flask import jsonify, send_file, Response, make_response
from app.logging import logger


def format_response_data(data, format, file_name):
    """
    Format response data in various formats and add appropriate headers.

    :param data: The response data to be formatted.
    :type data: dict or list of dicts
    :param format: The format to which to convert the data. Options are 'csv', 'xlsx', 'html', 'xml', 'yaml' and 'json'.
    :type format: str
    :param file_name: The base file name to use for downloadable formats.
    :type file_name: str
    :return: A Flask response object with the formatted data and appropriate headers and mimetype.
    :rtype: flask.wrappers.Response
    """
    df = pd.DataFrame(data)

    if format == 'csv':
        csv_file = f"{file_name}.csv"
        df.to_csv(csv_file, index=False)
        absolute_file_path = os.path.abspath(csv_file)
        logger.info('Responding with CSV')
        response = make_response(send_file(
            absolute_file_path,
            mimetype='text/csv',
            as_attachment=True,
        ))
        response.headers["Content-Disposition"] = f"attachment; filename={csv_file}"
        return response

    elif format == 'xlsx':
        excel_file = f"{file_name}.xlsx"
        df.to_excel(excel_file, index=False)
        absolute_file_path = os.path.abspath(excel_file)
        logger.info('Responding with Excel')
        response = make_response(send_file(
            absolute_file_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
        ))
        response.headers["Content-Disposition"] = f"attachment; filename={excel_file}"
        return response

    elif format == 'html':
        html_data = df.to_html()
        logger.info('Responding with HTML')
        return Response(html_data, mimetype='text/html')

    elif format == 'xml':
        xml_data = dicttoxml(data)
        logger.info('Responding with XML')
        return Response(xml_data, mimetype='application/xml')

    elif format == 'yaml':
        yaml_data = yaml.dump(data)
        logger.info('Responding with YAML')
        return Response(yaml_data, mimetype='application/x-yaml')

    else:  # Default to JSON
        logger.info('Responding with JSON')
        return jsonify(data)
