# -*- coding: utf-8 -*-
"""Dataflow_batch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Xxs7GLiSiswXzqwfBU-rbGiSrD5eTRD
"""

import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from sys import argv

PROJECT_ID = 'learn-gcp-337405'

SCHEMA = 'Branch:STRING,Gender:STRING,Product_line:STRING,Unit_price:FLOAT,Quantity:INTEGER,Total:FLOAT,Date:STRING,Payment:STRING'	

def discard_incomplete(data):
    """Filters out records that don't have an information."""
    return len(data['Invoice ID']) > 0 and len(data['Date']) > 0 and len(data['Product line']) > 0 and len(data['Time']) > 0

def convert_types(data):
    """Converts string values to their appropriate type."""
    data['Invoice ID'] = str(data['Invoice ID']) if 'Invoice ID' in data else None
    data['Branch'] = str(data['Branch']) if 'Branch' in data else None
    data['City'] = str(data['City']) if 'City' in data else None
    data['Customer type'] = str(data['Customer type']) if 'Customer type' in data else None
    data['Gender'] = str(data['Gender']) if 'Gender' in data else None

    data['Product line'] = str(data['Product line']) if 'Product line' in data else None
    data['Unit price'] = float(data['Unit price']) if 'Unit price' in data else None
    data['Quantity'] = int(data['Quantity']) if 'Quantity' in data else None
    data['Tax 5%'] = float(data['Tax 5%']) if 'Tax 5%' in data else None

    data['Total'] = float(data['Total']) if 'Total' in data else None
    data['Date'] = str(data['Date']) if 'Date' in data else None
    data['Time'] = str(data['Time']) if 'Time' in data else None
    data['Payment'] = str(data['Payment']) if 'Payment' in data else None
    data['cogs'] = float(data['cogs']) if 'cogs' in data else None
    data['gross margin percentage'] = float(data['gross margin percentage']) if 'gross margin percentage' in data else None
    data['gross income'] = float(data['gross income']) if 'gross income' in data else None
    data['Rating'] = float(data['Rating']) if 'Rating' in data else None

    return data

def del_unwanted_cols(data):
    """Delete the unwanted columns"""
    del data['Invoice ID']
    del data['City']
    del data['Customer type']
    del data['Tax 5%']
    del data['Time']
    del data['cogs']
    del data['gross margin percentage']
    del data['Rating']
    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    known_args = parser.parse_known_args(argv)

    p = beam.Pipeline(options=PipelineOptions())

    (p | 'ReadData' >> beam.io.ReadFromText('gs://dataflow_8787/supermarket_sales .csv', skip_header_lines =1)
       | 'SplitData' >> beam.Map(lambda x: x.split(','))
       | 'FormatToDict' >> beam.Map(lambda x: {"Invoice ID": x[0], "Branch": x[1], "City": x[2], "Customer type": x[3], "Gender": x[4], "Product line": x[5], "Unit price": x[6], "Quantity": x[7], "Tax 5%": x[8], "Total": x[9], "Date": x[10], "Time": x[11], "Payment": x[12], "cogs": x[13], "gross margin percentage": x[14], "gross income": x[15], "Rating": x[16] }) 
       | 'DeleteIncompleteData' >> beam.Filter(discard_incomplete)
       | 'ChangeDataType' >> beam.Map(convert_types)
       | 'DeleteUnwantedData' >> beam.Map(del_unwanted_cols)
       | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
           '{0}:beer.sales_data'.format(PROJECT_ID),
           schema=SCHEMA,
           write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))
    result = p.run()