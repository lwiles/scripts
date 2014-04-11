#!/usr/bin/env python

import xml.etree.ElementTree as ET

###############################################
# Travelocity Standard Client Feed Transformer
###############################################

# file definitions
source_file = 'travelocityfeed10-migrated.xml'
output_file = 'final10.xml'

#namespace declaration
namespace = '{http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6}'
ET.register_namespace('', 'http://www.bazaarvoice.com/xs/PRR/StandardClientFeed/5.6')

# parse the source standard client feed
tree = ET.parse(source_file)
root = tree.getroot()

# iterate through the reviews
for review in root.iter('{0}Review'.format(namespace)):
    if review.find('{0}Tags'.format(namespace)) is not None:
        # if a review has Tags but no "AdditionalFields" element, create one
        if review.find('{0}AdditionalFields'.format(namespace)) is None:
            AdditionalFields = ET.SubElement(review, '{0}AdditionalFields'.format(namespace))
            # grab the Pro Tags from the Travelocity feed
            pros = [pro.text for pro in review.findall('./{0}Tags/{0}TagDimension[@id="Pro"]/{0}Tags/{0}Tag/{0}Label'.format(namespace))]
            # transform the Pros into an additional field for the Expedia feed
            AdditionalFieldPro = ET.SubElement(AdditionalFields, '{0}AdditionalField'.format(namespace), attrib={'id': 'PositiveRemarks'})
            AdditionalFieldProDisplayLabel = ET.SubElement(AdditionalFieldPro, '{0}DisplayLabel'.format(namespace))
            AdditionalFieldProDisplayLabel.text = 'What were your &lt;strong&gt;favorite&lt;/strong&gt; things about this hotel?'
            AdditionalFieldProValue = ET.SubElement(AdditionalFieldPro, '{0}Value'.format(namespace))
            AdditionalFieldProValue.text = ', '.join(unicode(pro) for pro in pros)
            # grab the Con Tags from the Travelocity feed
            cons = [con.text for con in review.findall('./{0}Tags/{0}TagDimension[@id="Con"]/{0}Tags/{0}Tag/{0}Label'.format(namespace))]
            # transform the Pros into an additional field for the Expedia feed
            AdditionalFieldCon = ET.SubElement(AdditionalFields, '{0}AdditionalField'.format(namespace), attrib={'id': 'NegativeRemarks'})
            AdditionalFieldConDisplayLabel = ET.SubElement(AdditionalFieldCon, '{0}DisplayLabel'.format(namespace))
            AdditionalFieldConDisplayLabel.text = 'What were your &lt;strong&gt;least favorite&lt;/strong&gt; things about this hotel?'
            AdditionalFieldConValue = ET.SubElement(AdditionalFieldCon, '{0}Value'.format(namespace))
            AdditionalFieldConValue.text = ', '.join(unicode(con) for con in cons)
            # delete the Tags from the review
            tags = review.find('{0}Tags'.format(namespace))
            review.remove(tags)
        else:
            # if a review has Tags and also has Additional Fields, append to the existing Additional Fields
            AdditionalFields = review.find('{0}AdditionalFields'.format(namespace))
            pros = [pro.text for pro in review.findall('./{0}Tags/{0}TagDimension[@id="Pro"]/{0}Tags/{0}Tag/{0}Label'.format(namespace))]
            # transform the Pros into an additional field for the Expedia feed
            AdditionalFieldPro = ET.SubElement(AdditionalFields, '{0}AdditionalField'.format(namespace), attrib={'id': 'PositiveRemarks'})
            AdditionalFieldProDisplayLabel = ET.SubElement(AdditionalFieldPro, '{0}DisplayLabel'.format(namespace))
            AdditionalFieldProDisplayLabel.text = 'What were your &lt;strong&gt;favorite&lt;/strong&gt; things about this hotel?'
            AdditionalFieldProValue = ET.SubElement(AdditionalFieldPro, '{0}Value'.format(namespace))
            AdditionalFieldProValue.text = ', '.join(unicode(pro) for pro in pros)
            # grab the Con Tags from the Travelocity feed
            cons = [con.text for con in review.findall('./{0}Tags/{0}TagDimension[@id="Con"]/{0}Tags/{0}Tag/{0}Label'.format(namespace))]
            # transform the Pros into an additional field for the Expedia feed
            AdditionalFieldCon = ET.SubElement(AdditionalFields, '{0}AdditionalField'.format(namespace), attrib={'id': 'NegativeRemarks'})
            AdditionalFieldConDisplayLabel = ET.SubElement(AdditionalFieldCon, '{0}DisplayLabel'.format(namespace))
            AdditionalFieldConDisplayLabel.text = 'What were your &lt;strong&gt;least favorite&lt;/strong&gt; things about this hotel?'
            AdditionalFieldConValue = ET.SubElement(AdditionalFieldCon, '{0}Value'.format(namespace))
            AdditionalFieldConValue.text = ', '.join(unicode(con) for con in cons)
            # delete the Tags from the review
            tags = review.find('{0}Tags'.format(namespace))
            review.remove(tags)
    try:
        # search the review for the rating dimension "Cleanliness"
        # if found, transform IDs and text to "RoomCleanliness" and "Room Cleanliness" respectively 
        Cleanliness = review.find('./{0}RatingValues/{0}RatingValue/{0}RatingDimension[@id="Cleanliness"]'.format(namespace))
        Cleanliness.set('id', 'RoomCleanliness')
        ExternalId = Cleanliness.find('{0}ExternalId'.format(namespace))
        ExternalId.text = 'RoomCleanliness'
        Label = Cleanliness.find('{0}Label'.format(namespace))
        Label.text = 'Room Cleanliness'
        Label1 = Cleanliness.find('{0}Label1'.format(namespace))
        Label1.text = 'Room Cleanliness'
    except:
        pass
    try:
        # search the review for the rating dimension "StaffAndService"
        # if found, transform IDs and text to "Service" and "Service" respectively 
        StaffAndService = review.find('./{0}RatingValues/{0}RatingValue/{0}RatingDimension[@id="StaffAndService"]'.format(namespace))
        StaffAndService.set('id', 'Service')
        ExternalId = StaffAndService.find('{0}ExternalId'.format(namespace))
        ExternalId.text = 'Service'
        Label = StaffAndService.find('{0}Label'.format(namespace))
        Label.text = 'Service'
        Label1 = StaffAndService.find('{0}Label1'.format(namespace))
        Label1.text = 'Service'
    except:
        pass
    try:
        # search the review for the rating dimension "BedComfort"
        # if found, transform IDs and text to "RoomComfort" and "Room Comfort" respectively 
        BedComfort = review.find('./{0}RatingValues/{0}RatingValue/{0}RatingDimension[@id="BedComfort"]'.format(namespace))
        BedComfort.set('id', 'RoomComfort')
        ExternalId = BedComfort.find('{0}ExternalId'.format(namespace))
        ExternalId.text = 'RoomComfort'
        Label = BedComfort.find('{0}Label'.format(namespace))
        Label.text = 'Room Comfort'
        Label1 = BedComfort.find('{0}Label1'.format(namespace))
        Label1.text = 'Room Comfort'
    except:
        pass
    # If the review contains a "NumComments" or "Comments" tag, delete them
    if review.find('{0}NumComments'.format(namespace)) is not None:
        NumComments = review.find('{0}NumComments'.format(namespace))
        review.remove(NumComments)
    if review.find('{0}Comments'.format(namespace)) is not None:
        Comments = review.find('{0}Comments'.format(namespace))
        review.remove(Comments)

#output the transformed feed
tree.write(output_file, encoding="utf-8", xml_declaration=True, default_namespace='')