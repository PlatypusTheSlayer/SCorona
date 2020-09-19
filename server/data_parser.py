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

        self.cities = np.array(list(cities_to_counties.keys()))
        self.counties = np.unique(np.array(list(cities_to_counties.values())))
        self.cities_and_counties = np.concatenate((self.cities, self.counties))
        self.cities_to_counties = cities_to_counties

    def parse_text_for_location(self, article):
        words = np.array(nltk.word_tokenize(article))
        word_pairs = np.array([" ".join(bigram) for bigram in nltk.bigrams(words)])
        word_triplets = np.array([" ".join(trigram) for trigram in nltk.ngrams(words, 3)])

        three_word_locations = word_triplets[np.isin(word_triplets, self.cities_and_counties)]
        two_word_locations = word_pairs[np.isin(word_pairs, self.cities_and_counties)]
        single_word_locations = words[np.isin(words, self.cities_and_counties)]

        filtered_locations = np.concatenate((three_word_locations, two_word_locations, single_word_locations))
        locations, counts = np.unique(filtered_locations, return_counts=True)

        try:
            return locations[np.argmax(counts)]
        except:
            return "NO_LOCATION"

    def parse_text_for_county(self, article):
        location = self.parse_text_for_location(article)

        try:
            return self.cities_to_counties[location]
        except:
            return location

if __name__ == "__main__":
    article = """Lorem Manchester dolor sit Staffordshire, Manchester London elit. Sed tristique Manchester augue, pulvinar sollicitudin enim tristique nec. Ut vitae egestas lorem, a dapibus nulla. Aenean et varius mauris, sit amet mollis augue. Integer neque sem, finibus non ullamcorper eget, sagittis nec odio. Etiam suscipit quam eleifend augue luctus, non posuere eros lobortis. Praesent elementum congue dui ultrices placerat. Vestibulum efficitur ante nec sem fermentum mattis. Maecenas et ante vel nisi volutpat tempus. Proin sed faucibus mi. Pellentesque Staffordshire elit odio, a efficitur nisi malesuada ac. Duis quam tortor, tincidunt eu cursus molestie, porttitor vel diam. Praesent tempus libero sit amet nisl accumsan egestas. Quisque egestas massa vel neque imperdiet convallis. Sed venenatis cursus magna, vel eleifend erat consectetur eget."""
    article2 = """Lorem Manchester dolor sit Staffordshire, Manchester Staffordshire elit. Sed Staffordshire Manchester augue, pulvinar Staffordshire enim tristique nec. Ut vitae egestas lorem, a dapibus nulla. Aenean et varius mauris, sit amet mollis augue. Integer neque sem, finibus non ullamcorper eget, sagittis nec odio. Etiam suscipit quam eleifend augue luctus, non posuere eros lobortis. Praesent elementum congue dui ultrices placerat. Vestibulum efficitur ante nec sem fermentum mattis. Maecenas et ante vel nisi volutpat Staffordshire. Proin sed faucibus mi. Pellentesque Staffordshire elit odio, a efficitur nisi malesuada ac. Duis quam tortor, tincidunt eu cursus molestie, porttitor vel diam. Praesent tempus libero sit amet nisl accumsan egestas. Quisque egestas massa vel neque imperdiet convallis. Sed venenatis cursus magna, vel eleifend erat consectetur eget."""
    article3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu aliquet lorem, nec placerat metus. Donec ornare felis in urna faucibus, eu euismod quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article4 = """Lorem ipsum dolor sit Manchester, London adipiscing elit. Maecenas eu Manchester lorem, nec London metus. Donec ornare felis in urna faucibus, eu euismod quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article5 = """Lorem ipsum dolor sit Staffordshire, Staffordshire adipiscing elit. Maecenas eu aliquet lorem, nec Surrey metus. Staffordshire ornare felis in urna Surrey, eu Surrey quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article6 = """Lorem ipsum dolor sit Greater Manchester, Greater Manchester adipiscing elit. Maecenas eu aliquet Greater Manchester, nec Surrey metus. Greater Manchester ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. Cras ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article7 = """Lorem ipsum dolor sit East Sussex, East Sussex adipiscing elit. Maecenas eu aliquet East Sussex, nec Surrey metus. East Sussex ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Nunc sit amet dolor arcu. Sed convallis molestie placerat. East Sussex ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article8 = """Lorem ipsum dolor sit Tyne and Wear, Tyne and Wear adipiscing elit. Maecenas eu aliquet Tyne and Wear, nec Surrey metus. Tyne and Wear ornare felis in urna Surrey, eu Greater London quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Tyne and Wear sit amet dolor arcu. Sed convallis molestie placerat. Tyne and Wear ut mauris elementum, accumsan mauris accumsan, consectetur turpis."""
    article9 = """Lorem ipsum dolor sit Newcastle, Newcastle adipiscing elit. Maecenas eu aliquet Newcastle, nec Surrey metus. Newcastle ornare felis in urna Surrey, eu Newcastle quam malesuada. Aenean facilisis nibh ut enim blandit, ac hendrerit libero placerat. Tyne and Wear sit amet dolor arcu. Sed Newcastle molestie placerat. Tyne and Wear ut mauris Newcastle, accumsan mauris accumsan, consectetur turpis."""
    with open('resources/example-article.txt', 'r') as f:
        article10 = f.read()


    data_parser = DataParser()

    print("Article single city, location: %s, county: %s." % (data_parser.parse_text_for_location(article), data_parser.parse_text_for_county(article)))
    print("Article single county, location: %s, county: %s." % (data_parser.parse_text_for_location(article2), data_parser.parse_text_for_county(article2)))
    print("Article no locations, location: %s, county: %s." % (data_parser.parse_text_for_location(article3), data_parser.parse_text_for_county(article3)))
    print("Article draw city, location: %s, county: %s." % (data_parser.parse_text_for_location(article4), data_parser.parse_text_for_county(article4)))
    print("Article draw county, location: %s, county: %s." % (data_parser.parse_text_for_location(article5), data_parser.parse_text_for_county(article5)))
    print("Article unique two word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article6), data_parser.parse_text_for_county(article6)))
    print("Article non-unique two word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article7), data_parser.parse_text_for_county(article7)))
    print("Article three word county, location: %s, county: %s." % (data_parser.parse_text_for_location(article8), data_parser.parse_text_for_county(article8)))
    print("Article Newcastle check, location: %s, county: %s." % (data_parser.parse_text_for_location(article9), data_parser.parse_text_for_county(article9)))
    print("Article long article check, location: %s, county: %s." % (data_parser.parse_text_for_location(article10), data_parser.parse_text_for_county(article10)))