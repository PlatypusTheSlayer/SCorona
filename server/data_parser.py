#!/usr/bin/env python3

import json
import numpy as np
import nltk

class DataParser:

    def __init__(self):
        nltkpath = 'resources/nltk/'
        nltk.download('punkt', download_dir=nltkpath)
        nltk.data.path.append(nltkpath)

        with open('resources/british-cities-to-counties.json') as f:
            cities_to_counties = json.load(f)

        self.counties = np.unique(np.array(list(cities_to_counties.values())))
        self.cities = np.array(list(cities_to_counties.keys()))
        self.cities_and_counties = np.concatenate((self.counties, self.cities))
        self.cities_and_counties_lower = np.char.lower(self.cities_and_counties)
        self.cities_to_counties = cities_to_counties

    def parse_text_for_location(self, article, map_to_counties=True):
        words = np.array(nltk.word_tokenize(article))
        words = np.char.lower(words)

        word_pairs = np.array([" ".join(bigram) for bigram in nltk.bigrams(words)])
        word_triplets = np.array([" ".join(trigram) for trigram in nltk.ngrams(words, 3)])

        three_word_locations = word_triplets[np.isin(word_triplets, self.cities_and_counties_lower)]
        two_word_locations = word_pairs[np.isin(word_pairs, self.cities_and_counties_lower)]
        single_word_locations = words[np.isin(words, self.cities_and_counties_lower)]

        all_locations = np.concatenate((three_word_locations, two_word_locations, single_word_locations))

        if map_to_counties:
            all_locations = np.array([self.map_location_to_county(location) for location in all_locations])

        unique_locations, counts = np.unique(all_locations, return_counts=True)

        try:
            # Find indices with most occurences
            indices = np.argwhere(counts == np.max(counts))
            if len(indices) > 4:
                return "NO_LOCATION"
            # Out of these filter the longest matching name
            location = max(unique_locations[indices].tolist())[0]
            # Find its index and return the correctly cased version
            location_index = np.argwhere(self.cities_and_counties_lower == location)
            return self.cities_and_counties[location_index].flatten()[0]
        except:
            return "NO_LOCATION"

    def map_location_to_county(self, location):
        location_index = np.argwhere(self.cities_and_counties_lower == location)
        try:
            city = self.cities_and_counties[location_index].flatten()[0]
            county = self.cities_to_counties[city]
            return county.lower()
        except:
            return location

if __name__ == "__main__":
    article = """Lorem Manchester dolor sit Staffordshire, Manchester London elit. Sed tristique Manchester augue, pulvinar sollicitudin enim tristique nec. Ut vitae egestas lorem, a dapibus nulla. Aenean et varius mauris, sit amet mollis augue. Integer neque sem, finibus non ullamcorper eget, sagittis nec odio. Etiam suscipit quam eleifend augue luctus, non posuere eros lobortis. Praesent elementum congue dui ultrices placerat. Vestibulum efficitur ante nec sem fermentum mattis. Maecenas et ante vel nisi volutpat tempus. Proin sed faucibus mi. Pellentesque Staffordshire elit odio, a efficitur nisi malesuada ac. Duis quam tortor, tincidunt eu cursus molestie, porttitor vel diam. Praesent tempus libero sit amet nisl accumsan egestas. Quisque egestas massa vel neque imperdiet convallis. Sed venenatis cursus magna, vel eleifend erat consectetur eget."""
    article2 = """Lorem Manchester dolor sit Staffordshire, Manchester Staffordshire elit. Sed Staffordshire Manchester augue, pulvinar Staffordshire enim tristique nec. Ut vitae egestas lorem, a dapibus nulla. Aenean et varius mauris, sit amet mollis augue. Integer neque sem, finibus non ullamcorper eget, sagittis nec odio. Etiam suscipit quam eleifend augue luctus, non posuere eros lobortis. Praesent elementum congue dui ultrices placerat. Vestibulum efficitur ante nec sem fermentum mattis. Maecenas et ante vel nisi volutpat Staffordshire. Proin sed faucibus mi. Pellentesque Staffordshire elit odio, a efficitur nisi malesuada ac. Duis quam tortor, tincidunt eu cursus molestie, porttitor vel diam. Praesent tempus libero sit amet nisl accumsan egestas. Quisque egestas massa vel neque imperdiet convallis. Sed venenatis cursus magna, vel eleifend erat consectetur eget."""
    article3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu aliquet lorem, nec placerat metus. Donec ornare felis in urna faucibus, eu euismod quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article4 = """Lorem ipsum dolor sit Manchester, London adipiscing elit. Maecenas eu Manchester lorem, Manchester London metus. Surrey Surrey Newcastle Newcastle urna faucibus, eu euismod quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article5 = """Lorem ipsum dolor sit Staffordshire, Staffordshire adipiscing elit. Maecenas eu aliquet lorem, nec Surrey metus. Staffordshire ornare felis in urna Surrey, eu Surrey quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article6 = """Lorem ipsum dolor sit Greater Manchester, Greater Manchester adipiscing elit. Maecenas eu aliquet Greater Manchester, nec Surrey metus. Greater Manchester ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article7 = """Lorem ipsum dolor sit East Sussex, East Sussex adipiscing elit. Maecenas eu aliquet East Sussex, nec Surrey metus. East Sussex ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. East Sussex ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article8 = """Lorem ipsum dolor sit Tyne and Wear, Tyne and Wear adipiscing elit. Maecenas eu aliquet Tyne and Wear, nec Surrey metus. Tyne and Wear ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Tyne and Wear sit amet dolor arcu. Sed convallis molestie placerat. Tyne and Wear ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article9 = """asdas asdasd sadfkjh adsfjh dsaf Newcastle upon Tyne shjd Newcastle upon Tyne sadkjh jskadh Newcastle upon Tyne Newcastle upon Tyne aksdf dsf, asfd Newcastle upon Tyne"""
    with open('resources/example-article.txt', 'r') as f:
        article10 = f.read()
    article11 = """Newcastle upon Tyne sdafasdf Tyne and Wear sadfdsaf Tyne and Wear asdfdsaf Tyne and Wear asdfasdf Manchester asdfsaf Greater Manchester  asdfasdf Greater Manchester asdfasfd Manchester asdfas Tyne and Wear asdf Tyne and Wear"""
    article12 = """London Manchester Newcastle upon Tyne Leeds"""


    data_parser = DataParser()

    print("Article single city, location: %s, county: %s." % (data_parser.parse_text_for_location(article, map_to_counties=False), data_parser.parse_text_for_location(article, map_to_counties=True)))
    print("Article single county, location: %s, county: %s." % (data_parser.parse_text_for_location(article2, map_to_counties=False), data_parser.parse_text_for_location(article2, map_to_counties=True)))
    print("Article no locations, location: %s, county: %s." % (data_parser.parse_text_for_location(article3, map_to_counties=False), data_parser.parse_text_for_location(article3, map_to_counties=True)))
    print("Article draw city, location: %s, county: %s." % (data_parser.parse_text_for_location(article4, map_to_counties=False), data_parser.parse_text_for_location(article4, map_to_counties=True)))
    print("Article draw county, location: %s, county: %s." % (data_parser.parse_text_for_location(article5, map_to_counties=False), data_parser.parse_text_for_location(article5, map_to_counties=True)))
    print("Article unique two word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article6, map_to_counties=False), data_parser.parse_text_for_location(article6, map_to_counties=True)))
    print("Article non-unique two word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article7, map_to_counties=False), data_parser.parse_text_for_location(article7, map_to_counties=True)))
    print("Article three word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article8, map_to_counties=False), data_parser.parse_text_for_location(article8, map_to_counties=True)))
    print("Article three word city, location: %s, county: %s." % (data_parser.parse_text_for_location(article9, map_to_counties=False), data_parser.parse_text_for_location(article9, map_to_counties=True)))
    print("Article long article check, location: %s, county: %s." % (data_parser.parse_text_for_location(article10, map_to_counties=False), data_parser.parse_text_for_location(article10, map_to_counties=True)))
    print("Article long article check, location: %s, county: %s." % (data_parser.parse_text_for_location(article11, map_to_counties=False), data_parser.parse_text_for_location(article11, map_to_counties=True)))
    print("Article long article check, location: %s, county: %s." % (data_parser.parse_text_for_location(article12, map_to_counties=False), data_parser.parse_text_for_location(article12, map_to_counties=True)))