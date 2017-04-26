"""
Generally useful utilities

"""

class ExtractionUtils(object):

    @staticmethod
    def percentage_diff(v1, v2):
        """
        Calculates percentage of a whole.
        :param v1: one number
        :param v2: second number
        :return: prcentage difference
        """
        # cast to float
        v1 = float(v1)
        v2 = float(v2)

        return (abs(v1 - v2) / ((v1 + v2)/2.0)) * 100


    @staticmethod
    def parse_date(date):
        """
        Parses date in following formats:
            - DD/MM/YYYY, YYYY
        :param date: date string
        """
        year = None
        month = None
        day = None

        if ("/" in date):
            date_array = date.split("/")

            if (len(date_array) == 3):
                if (date_array[0].isdigit()):
                    day = date_array[0]
                if (date_array[1].isdigit()):
                    month = date_array[1]
                if (date_array[2].isdigit()):
                    year = date_array[2]

            elif (len(date_array) == 2):
                month = date_array[0]
                year = date_array[1]

        elif (date.isdigit()):
            year = date

        return {"day": day, "month": month, "year": year}

    @staticmethod
    def is_date1_equal_or_larger(year1, month1, day1, year2, month2, day2):
        """
        Compare two dates. If a value is missing in day and not in the other,
        the more detailed value wins.
        :param year1:
        :param month1:
        :param day1:
        :param year2:
        :param month2:
        :param day2:
        :return:
        """
        if (year1 > year2):
            return True
        elif (year1 < year2):
            return False
        elif (year1 == year2):
            if ((month1 != None) and (month2 == None)):     # 05/2001 vs. 2001
                return True
            elif ((month1 == None) and (month2 != None)):   # 2001 vs. 05/2001
                return False
            elif ((month1 == None) and (month2 == None)):   # 2001 vs. 2001
                return True
            elif (month1 > month2):
                return True
            elif (month1 < month2):
                return False
            elif (month1 == month2):
                if ((day1 != None) and (day2 == None)):     # 01/05/2001 vs. 05/2001
                    return True
                elif ((day1 == None) and (day2 != None)):   # 05/2001 vs. 01/05/2001
                    return False
                elif ((day1 == None) and (day2 == None)):
                    return True
                elif (day1 > day2):
                    return True
                elif (day1 < day2):
                    return False
                elif (day1 == day2):
                    return True

    @staticmethod
    def date_equals(year1, year2, tolerance_years=0):
        """
        Checks whether two temporal values match considering the tolerance rate.

        :param year1: integer
        :param year2: integer
        :param tolerance_years: time span in number of years that can be tolerated; if set to -1 they will always equal
        :return: money matches or not
        """
        if (tolerance_years == -1):
            return True

        if (tolerance_years > 0):
            min = int(year2) - tolerance_years
            max = int(year2) + tolerance_years
            year = int(year1)
            return ((min <= year) and (year <= max))
        else:
            # perfect match
            return (int(year1) == int(year2))

    @staticmethod
    def money_equals(value1, currency1, value2, currency2, tolerance_percent=0):
        """
        Checks whether two monetary values match considering tolerance rate.

        :param value1: integer
        :param value2: integer
        :param currency1: string
        :param currency2: string
        :param tolerance_percent: percentage of difference that can be tolerated; if set to -1 money will always equal
        :return: money matches or not
        """

        # no matter what the values are,
        # money will equal
        if (tolerance_percent == -1):
            return True

        if (currency1 != currency2):
            return False        # Currency isn't right
        else:
            p_diff = ExtractionUtils.percentage_diff(value1,value2)

            if (p_diff <= (tolerance_percent)):
                return True     # Money within range
            else:
                return False    # Money differs

    @staticmethod
    def dbpedia_uris_to_str(q_uris, delimit):
        """
        Replaces http://dbpedia.org/resource/ from DBpedia URIs and separates them by 'delim'
        :param q: e.g., q.getSubjectURIs()
        :return: uris as string separated by delimitor
        """
        list_d = set()
        for i in q_uris.get("dbpedia"):
            list_d.add(i.replace("http://dbpedia.org/resource/",""))

        return delimit.join(list_d)

    @staticmethod
    def freebase_uris_to_str(q_uris, delimit):
        """
        Represents Freebase URIs in format '/m/02_286' and separates them by 'delim'
        :param q: e.g., q.getSubjectURIs()
        :return: uris as string separated by delimitor
        """
        list_d = set()
        for i in q_uris.get("freebase"):
            list_d.add(ExtractionUtils.freebase_uri_to_id(i))

        return delimit.join(list_d)

    @staticmethod
    def freebase_id_to_uri(freebase_id):
        """Translate Freebase ID to (prefixed) Freebase URI.
        For example, '/m/02_286' => '<fb:m\\u002e02_286>'
        """
        if freebase_id.startswith("/m/"):
            return "<fb:m\\u002e" + freebase_id[3:] + ">"
        else:
            print "Invalid Freebase ID: " + freebase_id

    @staticmethod
    def freebase_uri_to_id(freebase_uri):
        """Translate (prefixed) Freebase URI to Freebase ID.
        For example, '<fb:m.02_286>' => '/m/02_286'
        """
        if freebase_uri.startswith("<fb:m\u002e"):
            return "/m/" + freebase_uri[11:-1]
        else:
            print Exception("Invalid Freebase URI")