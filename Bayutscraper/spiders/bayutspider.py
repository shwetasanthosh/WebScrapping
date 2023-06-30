import scrapy
import json

class BayutSpider(scrapy.Spider):
    name = "bayut"
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        # Extract property listings using XPath
        property_listings = response.xpath('//div[contains(@class, "list-item")]')

        for listing in property_listings:
            # Extract property details using XPath
            property_id = listing.xpath('./@data-listing_id').get()
            purpose = listing.xpath('.//p[contains(@class, "property-purpose")]/span/text()').get()
            property_type = listing.xpath('.//p[contains(@class, "property-type")]/span/text()').get()
            added_on = listing.xpath('.//p[contains(@class, "added-on")]/span/text()').get()
            furnishing = listing.xpath('.//p[contains(@class, "furnished")]/span/text()').get()
            price = listing.xpath('.//span[contains(@class, "price")]/text()').get().strip()
            location = listing.xpath('.//p[contains(@class, "value-location")]/span/text()').get().strip()
            bed_bath_size = listing.xpath('.//p[contains(@class, "value-size")]/span/text()').get()
            permit_number = listing.xpath('.//p[contains(text(), "Permit No")]/span/text()').get()
            agent_name = listing.xpath('.//h5/a/text()').get()
            image_url = listing.xpath('.//div[contains(@class, "image-wrap")]/a/img/@src').get()
            breadcrumbs = listing.xpath('.//div[@class="breadcrumbs"]//a/text()').getall()
            amenities = listing.xpath('.//div[contains(@class, "amenities-list")]//li/span/text()').getall()
            description = listing.xpath('.//div[contains(@class, "description")]/text()').get()

            # Clean and structure the data
            cleaned_property_id = self.clean_data(property_id)
            cleaned_purpose = self.clean_data(purpose)
            cleaned_property_type = self.clean_data(property_type)
            cleaned_added_on = self.clean_data(added_on)
            cleaned_furnishing = self.clean_data(furnishing)
            cleaned_price = self.clean_data(price)
            cleaned_location = self.clean_data(location)
            cleaned_bed_bath_size = self.clean_data(bed_bath_size)
            cleaned_permit_number = self.clean_data(permit_number)
            cleaned_agent_name = self.clean_data(agent_name)
            cleaned_image_url = self.clean_data(image_url)
            cleaned_breadcrumbs = [self.clean_data(crumb) for crumb in breadcrumbs]
            cleaned_amenities = [self.clean_data(amenity) for amenity in amenities]

            # Create a dictionary with the structured data
            data = {
                'Property ID': cleaned_property_id,
                'Purpose': cleaned_purpose,
                'Type': cleaned_property_type,
                'Added On': cleaned_added_on,
                'Furnishing': cleaned_furnishing,
                'Price': cleaned_price,
                'Location': cleaned_location,
                'Bed Bath Size': cleaned_bed_bath_size,
                'Permit Number': cleaned_permit_number,
                'Agent Name': cleaned_agent_name,
                'Image URL': cleaned_image_url,
                'Breadcrumbs': cleaned_breadcrumbs,
                'Amenities': cleaned_amenities,
                
            } 
            yield data
          
        filename = 'property_data.json'
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def clean_data(self, data):
        # Perform cleaning operations as required
        # Example: Remove unwanted characters, whitespace, etc.
        cleaned_data = data.strip()
        return cleaned_data
