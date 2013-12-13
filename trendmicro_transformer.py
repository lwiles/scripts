import csv
import xml.etree.ElementTree as ET
import datetime

###############################################
# TrendMicro Native Content Feed Builder
###############################################

# file definitions
source_file = 'blank.xml'
output_file = 'native_content.xml'

#namespace declaration
namespace = '{http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6}'
ET.register_namespace('', 'http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6')

# parse the source standard client feed
tree = ET.parse(source_file)
root = tree.getroot()

reviews = dict()
reviewCounter = 1
profileCounter = 1

with open('reviewsReport.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        externalid = row[1]
        if externalid in reviews:
            reviews[externalid].append(row)
        else:
            reviews[externalid] = list()
            reviews[externalid].append(row)

for product in reviews:
    ProductElement = ET.SubElement(root, '{0}Product'.format(namespace), attrib={'id': product})
    ProductExternalId = ET.SubElement(ProductElement, '{0}ExternalId'.format(namespace))
    ProductExternalId.text = product
    Reviews = ET.SubElement(ProductElement, '{0}Reviews'.format(namespace))
    for review in reviews[product]:
        Review = ET.SubElement(Reviews, '{0}Review'.format(namespace), attrib={'id': str(reviewCounter)})
        reviewCounter += 1
        SubmissionTime = ET.SubElement(Review, '{0}SubmissionTime'.format(namespace))
        myDate = review[3].strip().split('/')
        SubmissionTime.text = str(datetime.datetime(int(myDate[2]) + 2000, int(myDate[0]), int(myDate[1])).isoformat())
        Rating = ET.SubElement(Review, '{0}Rating'.format(namespace))
        Rating.text = review[2].strip()
        Title = ET.SubElement(Review, '{0}Title'.format(namespace))
        Title.text = review[0].decode('utf-8')
        ReviewText = ET.SubElement(Review, '{0}ReviewText'.format(namespace))
        ReviewText.text = review[4].decode('utf-8')
        if review[5]:
            # print(review[5].strip().replace(' ', ''))
            UserProfileReference = ET.SubElement(Review, '{0}UserProfileReference'.format(namespace), attrib={'id': str(profileCounter)})
            ProfileExternalId = ET.SubElement(UserProfileReference, '{0}ExternalId'.format(namespace))
            ProfileExternalId.text = str(profileCounter)
            profileCounter += 1
            DisplayName = ET.SubElement(UserProfileReference, '{0}DisplayName'.format(namespace))
            DisplayName.text = review[5].strip().replace(' ', '').decode('utf-8')
            Anonymous = ET.SubElement(UserProfileReference, '{0}Anonymous'.format(namespace))
            Anonymous.text = 'false'
            HyperlinkingEnabled = ET.SubElement(UserProfileReference, '{0}HyperlinkingEnabled'.format(namespace))
            HyperlinkingEnabled.text = 'false'
        else:
            print('false')



tree.write(output_file, encoding="utf-8", xml_declaration=True, default_namespace='')