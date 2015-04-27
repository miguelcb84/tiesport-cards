# -*- coding: utf-8 -*-
from jinja2 import meta
from unidecode import unidecode
import argparse
import csv
import jinja2
import os
import sys

# Handle encoding
reload(sys)
sys.setdefaultencoding('utf-8')


# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument("csvfile", help="relative path to csv file")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
parser.add_argument("-t", "--template", help="relative path to template used to generate the output (default: template.jinja",
                    type=str, default="template.html")
parser.add_argument("-o", "--output", help="name of the output file (default: output.html)",
                    type=str, default="output.html")
parser.add_argument("-of", "--ofolder", help="name of the output folder (default: output)",
                    type=str, default="output")
args = parser.parse_args()


if args.output:
    o_filename = args.output
else:
    o_filename = 'output.html'

if args.ofolder:
    out_folder = args.ofolder
else:
    out_folder = 'output'


#env = Environment(loader=PackageLoader('yourapplication', 'templates'))
templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"

# Load template
try:
    if args and args.template:
        template = templateEnv.get_template(args.template)
        template_source = templateEnv.loader.get_source(templateEnv, args.template)[0]
    else:
        template = templateEnv.get_template(TEMPLATE_FILE)
        template_source = templateEnv.loader.get_source(templateEnv, TEMPLATE_FILE)[0]
# except NameError:
#     template = templateEnv.get_template(TEMPLATE_FILE)
#     template_source = templateEnv.loader.get_source(templateEnv, TEMPLATE_FILE)[0]
except TemplateNotFound:    
    sys.exit("Template not found")
except TemplateNotFound:
    sys.exit("Syntax error at template")
except Exception as e:
    sys.exit("Could not load template")


# extract required fields
parsed_content = templateEnv.parse(template_source)
REQUIRED_FIELDS = meta.find_undeclared_variables(parsed_content)

# Read csv
input_csv = open(args.csvfile, 'rb')
reader = csv.DictReader(input_csv)

# for field in REQUIRED_FIELDS:
#     #assert field in reader.fieldsnames
#     if field not in reader.fieldnames:
#         print "WARNING: required field {} is missing".format(field)


# counters
user_count = 0

context = []
# iterate over the rows
for row in reader:

    # which required fields are empty in this row
    for k in [k for k,v in row.iteritems() if k in REQUIRED_FIELDS and not v]:
        print "WARNING: field {} for user {} is empty".format(k, name)

    context.append(row)
    user_count = user_count + 1


# render template
output_path = "{}/{}".format(out_folder, o_filename)
outputText = template.render( {'yellowpages' : context} )
with open(output_path, 'wb') as out:
    out.write(outputText)

if args.verbosity:
    print "Processed user {}".format(name)

print "Completed ({} users processed)".format(user_count)