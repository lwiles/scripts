#!/usr/bin/env python

import xml.etree.ElementTree as ET

###############################################
# Travelocity Standard Client Feed Transformer
###############################################

# file definitions
source_file = 'travelocityfeed10.xml'
output_file = 'travelocityfeed10-migrated.xml'

#namespace declaration
namespace = '{http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6}'
ET.register_namespace('', 'http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6')

# parse the source standard client feed
tree = ET.parse(source_file)
root = tree.getroot()

# map the old product IDs to the new product IDs (truncated)
mapping = {
    '101036': '2856418',
    '116745': '3208251',
    '5169': '36445',
    '56350': '41428',
}

# initiate a list of the products we are eventually going to drop from the feed
# (products that are not matched in the mapping)
removeList = list()

# iterate through the products in the feed
for product in root.iter('{0}Product'.format(namespace)):
    # create a dictionary of the "Product" elements' attribute names and values
    attributes = product.items()
    try:
        # if an "attributes" "id" matches a key from the "mapping" dict,
        # replace that id's value with the value from the mapping dict
        product.set('id', mapping[attributes[2][1]])
        # replace the text within the "ExternalId" element of that Product as well
        externalid = product.find('{0}ExternalId'.format(namespace))
        externalid.text = mapping[attributes[2][1]]
    except:
        # if there is no match between the Product's id and the mapping dict,
        # add that Product to the "removeList"
        removeList.append(product)
        pass

# open or create a new file called "removed_ids.txt"
f = open('removed_ids.txt', 'w')

for product in removeList:
    # loop the through the Products in "removeList" and add their id's to "removed_ids.txt"
    # this allows us to track which Product id's were not included in the mapping
    externalid = product.find('{0}ExternalId'.format(namespace))
    str_id = str(externalid.text)
    f.write(str_id + '\n')
    # drop the Product from the feed, since it was not mapped
    root.remove(product)

# output the new feed
tree.write(output_file, encoding="utf-8", xml_declaration=True, default_namespace='')