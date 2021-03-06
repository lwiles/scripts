#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import datetime, csv

###############################################
# TrendMicro Native Content Feed Builder
###############################################


# initialize variables
clientName = input('Input client name: ')
reviews = dict()
reviewCounter = 1
profileCounter = 1


# open the CSV file
with open('reviewsReport.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        # grab the ExternalId from each row
        externalid = row[1]
        # if the product already exists in the "reviews" dict, append the review to the list of reviews
        if externalid in reviews:
            reviews[externalid].append(row)
        # if the product does not yet exist in the "reviews" dict, use it to define a new product
        else:
            reviews[externalid] = list()
            reviews[externalid].append(row)


# etree namespace declaration
namespace = '{http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6}'
ET.register_namespace('', 'http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6')
# define the root "Feed" element and attributes
root = ET.Element('{0}Feed'.format(namespace), attrib={
    'name': clientName,
    'extractDate': datetime.datetime.now().isoformat()
})


# build out the feed with the "reviews" dict
for product in reviews:
    # build out the products
    ProductElement = ET.SubElement(root, '{0}Product'.format(namespace), attrib={'id': product})
    ProductExternalId = ET.SubElement(ProductElement, '{0}ExternalId'.format(namespace))
    ProductExternalId.text = product
    Reviews = ET.SubElement(ProductElement, '{0}Reviews'.format(namespace))
    # build out the reviews
    for review in reviews[product]:
        Review = ET.SubElement(Reviews, '{0}Review'.format(namespace), attrib={'id': str(reviewCounter)})
        reviewCounter += 1
        SubmissionTime = ET.SubElement(Review, '{0}SubmissionTime'.format(namespace))
        myDate = review[3].strip().split('/')
        # transform client m/d/yy into correct xs:dateTime format
        SubmissionTime.text = str(datetime.datetime(int(myDate[2]) + 2000, int(myDate[0]), int(myDate[1])).isoformat())
        Rating = ET.SubElement(Review, '{0}Rating'.format(namespace))
        Rating.text = review[2].strip()
        Title = ET.SubElement(Review, '{0}Title'.format(namespace))
        Title.text = review[0]
        ReviewText = ET.SubElement(Review, '{0}ReviewText'.format(namespace))
        ReviewText.text = review[4]
        # if a profile name is provided, build out the profile
        if review[5]:
            UserProfileReference = ET.SubElement(Review, '{0}UserProfileReference'.format(namespace), attrib={'id': str(profileCounter)})
            ProfileExternalId = ET.SubElement(UserProfileReference, '{0}ExternalId'.format(namespace))
            ProfileExternalId.text = str(profileCounter)
            profileCounter += 1
            DisplayName = ET.SubElement(UserProfileReference, '{0}DisplayName'.format(namespace))
            DisplayName.text = review[5].strip().replace(' ', '')
            Anonymous = ET.SubElement(UserProfileReference, '{0}Anonymous'.format(namespace))
            Anonymous.text = 'false'
            HyperlinkingEnabled = ET.SubElement(UserProfileReference, '{0}HyperlinkingEnabled'.format(namespace))
            HyperlinkingEnabled.text = 'false'

# wrap the feed in an ElementTree instance, and save as XML
tree = ET.ElementTree(root)
tree.write('output.xml', encoding="utf-8", xml_declaration=True, default_namespace='')