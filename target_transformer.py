#!/usr/bin/env python


import xml.etree.ElementTree as ET

######################################
# Syndication Elements Transfer
######################################

# file definitions
source_file = 'syndication_feed.xml'
target_file = 'product_feed.xml'
output_file = 'final.xml'

#namespace declaration
namespace = 'http://www.bazaarvoice.com/xs/PRR/ProductFeed/5.6'
namespaces = {'', namespace}
ET.register_namespace('', namespace)

# parse the source product feed
tree = ET.parse(source_file)
root = tree.getroot()

# declare the product dictionary object
productDict = {}

# iterate through the products in the source feed, creating a dictionary of product IDs,
# each matched with a list of UPC/EAN/ManufacturerPartNumber/BrandExternalId values
for product in root.iter('{' + namespace + '}Product'):
    # set productDict top level key to product's ExternalId
    key = product.find('{' + namespace + '}ExternalId').text
    # initialize second level dictionary keyed against each product ExternalId
    productDict[key] = {}
    # if the product contains "UPCs" assign them as a list to the productDict's "UPCs" dictionary sub-element
    if product.find('{' + namespace + '}UPCs') is not None:
        productDict[key]['UPCs'] = [ upc.text for upc in product.iter('{' + namespace + '}UPC') ]
    # repeat process for "EANs"
    if product.find('{' + namespace + '}EANs') is not None:
        productDict[key]['EANs'] = [ ean.text for ean in product.iter('{' + namespace + '}EAN') ]
    # repeat process for "ManufacturerPartNumbers"
    if product.find('{' + namespace + '}ManufacturerPartNumbers') is not None:
        productDict[key]['ManufacturerPartNumbers'] = [ mpn.text for mpn in product.iter('{' + namespace + '}ManufacturerPartNumber') ]
    # repeat process for "BrandExternalId" (no list)
    if product.find('{' + namespace + '}BrandExternalId') is not None:
        productDict[key]['BrandExternalId'] = product.find('{' + namespace + '}BrandExternalId').text

print('finished reading')

# parse the target product feed
tree = ET.parse(target_file)
root = tree.getroot()
matchedProducts = 0

# iterate through the products in the target feed
for product in root.iter('{' + namespace + '}Product'):
    # set key to the current product "ExternalId"
    key = product.find('{' + namespace + '}ExternalId').text
    if key in productDict:
        matchedProducts += 1
        # if "UPCs" key is in productDict[key], create a "UPCs" SubElement
        if 'UPCs' in productDict[key]:
            UPCsSub = ET.SubElement(product, '{' + namespace + '}UPCs')
            # once the "UPCs" element is created, loop through list returned by productDict, creating "UPC" SubElements within "UPCs"
            for upc in productDict[key]['UPCs']:
                UPCSub = ET.SubElement(UPCsSub, '{' + namespace + '}UPC')
                UPCSub.text = upc
        # repeat process for "EANs"
        if 'EANs' in productDict[key]:
            EANsSub = ET.SubElement(product, '{' + namespace + '}EANs')
            for ean in productDict[key]['EANs']:
                EANSub = ET.SubElement(EANsSub, '{' + namespace + '}EAN')
                EANSub.text = ean
        # repeat process for "ManufacturerPartNumbers"
        if 'ManufacturerPartNumbers' in productDict[key]:
            MPNsSub = ET.SubElement(product, '{' + namespace + '}ManufacturerPartNumbers')
            for mpn in productDict[key]['ManufacturerPartNumbers']:
                MPNSub = ET.SubElement(MPNsSub, '{' + namespace + '}ManufacturerPartNumber')
                MPNSub.text = mpn
        # repeat process for "BrandExternalId" (no loop)
        if 'BrandExternalId' in productDict[key]:
            BEISub = ET.SubElement(product, '{' + namespace + '}BrandExternalId')
            BEISub.text = productDict[key]['BrandExternalId']

print('finished writing')
print('Matched Products:' + str(matchedProducts))

# output the final feed
tree.write(output_file, encoding="utf-8", xml_declaration=True, default_namespace='')

print('finished outputting')