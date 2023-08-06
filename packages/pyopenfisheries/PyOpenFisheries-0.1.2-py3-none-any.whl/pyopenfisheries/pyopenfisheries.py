# -*- coding: utf-8 -*-
import requests


class PyOpenFisheries(object):

    """
    Base class for accessing the OpenFisheries API.
    Useful for gathering data for plots or analysis.

    Returns:
        instance: base OpenFisheries API wrapper
    Examples:
        >>> open_fish_conn = PyOpenFisheries()
        >>> skipjack_tuna = open_fish_conn.annual_landings(species="SKJ").filter_years(start_year=1970,end_year=1991)
        >>> print(skipjack_tuna.landings)
        [{'year': 1970, 'catch': 402166}...{'year': 1991, 'catch': 1575170}]
        >>> print(skipjack_tuna.summarize())
        Landings of SKJ globally from 1970 to 1991
    Attributes:
        landings: List of dictionaries containing the year and landing count.
        species: if present - three-letter ASFIS species code (i.e. "SKJ" - Skipjack Tuna).
        country: if present - ISO-3166 alpha 3 country code (i.e. "USA" - United States).
        start_year: if present - start year of filtered landings data.
        end_year : if present - end year of filtered landings data.
    """

    def __init__(self, **kwargs):
        self.landings = kwargs.get('landings')
        self.species = kwargs.get('species')
        self.country = kwargs.get('country')
        self.start_year = kwargs.get('start_year')
        self.end_year = kwargs.get('end_year')

    def annual_landings(self, species=None, country=None):
        """
        Gathers annual fishery landings filtered by either species or
        country. If neither fish nor country are specified, then this
        will return global aggregate landings data.

        Args:
            species: three-letter ASFIS species code (i.e. "SKJ" - Skipjack Tuna)
            country: ISO-3166 alpha 3 country code (i.e. "USA" - United States)

        Returns:
            instance: PyOpenFisheries instance with landings populated
        """

        url = 'http://openfisheries.org/api/'

        if (species is not None) & (country is not None):

            # HRK: this can probably be handled better

            raise ValueError('too many arguments.')
        elif (species is None) & (country is None):

            url += 'landings.json'
            try:
                r = requests.get(url)
            except exception:
                raise Exception(exception)

            return PyOpenFisheries(landings=r.json(), country=country,
                                   species=species)
        else:

            if species:
                url += 'landings/species/' + species.upper() + '.json'
            elif country:

                url += 'landings/countries/' + country.upper() + '.json'

            try:
                r = requests.get(url)
            except exception:
                raise Exception(exception)

            try:
                landings = r.json()
            except:
                landings = [{'year': 0, 'catch': 0}]

            return PyOpenFisheries(landings=landings, country=country,
                                   species=species)

    def filter_years(self, start_year=1950, end_year=2018):
        """
            Filters annual fishing data to within a time-frame.

            Args:
                start_year: 4 digit integer year (i.e. 1980)
                end_year: I 4 digit integer year (i.e. 2015)

            Returns:
                instance: PyOpenFisheries instance with years filtered.
        """

        try:
            filtered_landings = [landing for landing in self.landings
                                 if landing['year'] >= start_year
                                 and landing['year'] <= end_year]
        except:
            raise ValueError('No landings to filter.')

        return PyOpenFisheries(landings=filtered_landings,
                               species=self.species,
                               country=self.country,
                               start_year=start_year, end_year=end_year)

    def summarize(self):
        """ Summarizes what has been returned from OpenFisheries.

        """

        base_string = 'Landings '

        if self.landings:
            if self.species:
                base_string += 'of ' + self.species + ' globally'
            elif self.country:
                base_string += 'of all species in ' + self.country
            else:
                base_string += 'globally'
            base_string += ' from ' + str(self.start_year) + ' to ' \
                + str(self.end_year)
            return base_string
        else:

            return 'PyOpenFisheries API Wrapper'

    def label(self):
        """
            Useful as a legend / for plots.
        """

        if self.species:
            return self.species
        elif self.country:
            return self.country
        else:
            return 'Global'
