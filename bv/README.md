scripts
=======

### pid_migration.py & travelocity_transformer.py

pid_migration.py and travelocity_transformer.py go hand in hand.  They are intended to be run against Bazaarvoice's Standard Client Feed.

**pid_migration.py** is intended to perform a Product ID migration prior to a native content import. This is due to the fact that the client instance from which we were importing content and the destination client instance had overlapping Product ID's.

**travelocity_transformer.py** performs several actions to transform the C2013 "Travelocity" Standard Client Feed (SCF) into a format that can be ingested by a new "Travelocityapi" client instance that inherits, for the most part, directly from "ExpediaHosted":

* Transforms any "Pros" (Tags) into a comma separated string and places them into a single Additional Field ("PositiveRemarks")
* Transforms any "Cons" (Tags) into a comma separated string and places them into a single Additional Field ("NegativeRemarks")
* Transforms the ExternalId's of three Secondary Rating Dimensions
* Deletes comments

### target_transformer.py

**target_transformer.py** is intended to be run against Bazaarvoice's Product Feed.  It matches product IDs between two Product Feeds and then transfers any syndication-related elements (UPCs, EANs, ManufacturerPartNumbers, BrandExternalId) from the source feed to the destination feed.