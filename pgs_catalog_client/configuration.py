# coding: utf-8

"""
    PGS Catalog REST API

    Programmatic access to the PGS Catalog metadata. More information about the metadata and its structure can be found [here](/docs/).  <i class=\"fas fa-exclamation-circle pgs_color_1\"></i> Each PGS is provided as a scoring file (containing the variants, alleles, effect weights) on our <a href=\"http://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/\" target=\"_blank\">FTP site</a>. The variants are not distributed within this API; however, a link to the scoring file is provided in the<code>ftp_scoring_file</code>field for each result of the<code>/rest/score/</code>endpoints for ease of download.  ---  ###### REST API settings  * `pagination`: This REST API is using pagination for the endpoints returning more than 1 results. It is currently set to **50** results per page.   <a class=\"toggle_btn pgs_btn_plus\" id=\"pagination\">More information</a>   <div class=\"toggle_content\" id=\"content_pagination\" style=\"display:none\">      ###### **Pagination structure**      Here is an example of the pagination result structure in JSON:      ```       {         \"size\": 50,         \"count\": 137,         \"next\": \"https://www.pgscatalog.org/rest/score/all?limit=50&offset=50\",         \"previous\": null,         \"results\": [           < list the results 1 to 50 >         ]       }     ```     * **size**: is the number of results in the current page.     * **count**: is the overall number of results.     * **next**: is the URL to the following page of results.     * **previous**: is the URL to the preceding page of results (only present if you are not on the first page).     * **results**: contains the list of results of the current page.     <pre></pre>     ###### **Pagination parameters**     * **limit**: The number of results per page can be overwritten using this parameter, e.g:       * <code>.../rest/score/all/?limit=100</code>: returns the first 100 results.       * <code>.../rest/score/all/?limit=150</code>: returns all the results (the overall number of results is 137 in our example above).        The default value is **50**. The maximum value is **250**. Over this maximum value, the REST API returns an error 400.      * **offset**: This parameter indicates the starting position (0 based) of the query in relation to the complete set of results. It provides access to a desired range of results, e.g.:       * <code>.../rest/score/all/?offset=75</code> provides results from the number **76** to **125**, as the number of results per page is **50** by default (equivalent to \"limit=50\")       * <code>.../rest/score/all/?offset=75&limit=60</code> provides results from the number **76** to **135**    </div>   * `rate limit`: The limit number of queries is set to **100** queries per minute.   <a class=\"toggle_btn pgs_btn_plus\" id=\"rate_limit\">More information</a>   <div class=\"toggle_content\" id=\"content_rate_limit\" style=\"display:none\">     Here is an example of the JSON message returned if the rate limit is reached:      ```       {         \"message\": \"request limit exceeded\",         \"availableIn\": \"33 seconds\"       }     ```     * **message**: description of the error.     * **availableIn**: number of seconds before the rate limit is reset.   </div>  ---  <a class=\"toggle_btn pgs_btn_plus\" id=\"changelog\">REST API version changelog</a> <div class=\"toggle_content\" id=\"content_changelog\" style=\"display:none\">    * <span class=\"badge badge-pill badge-pgs\">1.8.6</span> - January 2023:     * New field **date_release** in the Score schemas (`/rest/score/` endpoints), containing the release date of the Score in the PGS Catalog.     * New field **date_release** in the Publication schemas (`/rest/publication/` endpoints), containing the release date of the Publication in the PGS Catalog.    * <span class=\"badge badge-pill badge-pgs\">1.8.5</span> - December 2022:     * Add deprecation message about the parameter 'pgs_ids' of the endpoint `/rest/score/search` as it is redundant with the parameter 'filter_ids'  of the endpoint `/rest/score/all`.     * Fix the parameter 'include_parents' for the endpoint `/rest/trait/all`.     * New parameter 'include_child_associated_pgs_ids' for the endpoint `/rest/trait/all` to display the list of PGS IDs associated with the children traits.    * <span class=\"badge badge-pill badge-pgs\">1.8.4</span> - August 2022:     * New field **ftp_harmonized_scoring_files** in the Score schemas (`/rest/score/` endpoints), listing the URLs to the different harmonized scoring files.     * New field **ensembl_version** in the `/rest/info/` endpoint: Ensembl version used to generate the harmonized scoring files.    * <span class=\"badge badge-pill badge-pgs\">1.8.3</span> - February 2022:     * New parameter 'filter_ids' to narrow down the results in the following endpoints:       * `/rest/score/all`       * `/rest/publication/all`       * `/rest/trait/all`       * `/rest/performance/all`       * `/rest/cohort/all`       * `/rest/sample_set/all`     * New field **name_others** in the Cohort schemas (`/rest/cohort/` endpoints).    * <span class=\"badge badge-pill badge-pgs\">1.8.2</span> - October 2021:     * New field **weight_type** in the Score schemas (`/rest/score/` endpoints).     * New parameters 'pgp_id' and 'pmid' for the endpoints `/rest/performance/search` and `/rest/sample_set/search`.     * New parameter 'pgp_id' for the endpoint `/rest/score/search`.    * <span class=\"badge badge-pill badge-pgs\">1.8.1</span> - July 2021:     * Change the data type of the field **source_PMID** to numeric in the Sample schemas     * New field **source_DOI** in the Sample schemas and move the DOI data from **source_PMID** to this new field.    * <span class=\"badge badge-pill badge-pgs\">1.8</span> - June 2021:     * New endpoint `/rest/api_versions` providing the list of all the REST API versions and their changelogs.     * Change the data type of the field **rest_api/version** in `/rest/info` to **string**.     * Change the data structure of the `/rest/ancestry_categories` endpoint by adding the new fields **display_category** and **categories**.    * <span class=\"badge badge-pill badge-pgs\">1.7</span> - April 2021:     * New data **ancestry_distribution** in the `/rest/score` endpoints, providing information about ancestry distribution on each stage of the PGS.     * New endpoint `/rest/ancestry_categories` providing the list of ancestry symbols and names.     * New data **PMID** (PubMed ID) in the `/rest/info` endpoint, under the **citation** category.    * <span class=\"badge badge-pill badge-pgs\">1.6</span> - March 2021:     * New endpoint `/rest/info` with data such as the REST API version, latest release date and counts, PGS citation, ...     * New endpoint `/rest/cohort/all` returning all the Cohorts and their associated PGS.     * New endpoint `/rest/sample_set/all` returning all the Sample Set data.    * <span class=\"badge badge-pill badge-pgs\">1.5</span> - February 2021:     * Split the array of the field **associated_pgs_ids** (from the `/rest/publication/` endpoint) in 2 arrays **development** and **evaluation**, e.g.:       ```         \"associated_pgs_ids\": {           \"development\": [               \"PGS000011\"           ],           \"evaluation\": [               \"PGS000010\",               \"PGS000011\"           ]         }       ```      * New flag parameter **include_parents** for the endpoint `/rest/trait/all` to display the traits in the catalog + their parent traits (default: 0)    * <span class=\"badge badge-pill badge-pgs\">1.4</span> - January 2021:     * Setup a maximum value for the `limit` parameter.     * Add a new field **size** at the top of the paginated results, to indicate the number of results visible in the page.     * Replace the fields **labels** and **value** under performance_metrics**&rarr;**effect_sizes**/**class_acc**/**othermetrics in the `/rest/performance` endpoints by new fields: **name_long**, **name_short**, **estimate**, **ci_lower**, **ci_upper** and **se**.        Now the content of the **labels** and **value** fields are structured like this, e.g.:       ```         {           \"name_long\": \"Odds Ratio\",           \"name_short\": \"OR\",           \"estimate\": 1.54,           \"ci_lower\": 1.51,           \"ci_upper\": 1.57,           \"se\": 0.0663         }       ```     * Restructure the **samples**&rarr;**sample_age**/**followup_time** JSON (used in several endpoints):       * Merge and replace the fields **mean** and **median** into generic fields **estimate_type** and **estimate**:         ```           \"estimate_type\": \"mean\",           \"estimate\": 53.0         ```       * Merge and replace the fields **se** and **sd** into generic fields **variability_type** and **variability**:         ```           \"variability_type\": \"sd\",           \"variability\": 16.0,         ```       * Merge and replace the fields **range** and **iqr** by a new structure **interval**:         ```           \"interval\": {             \"type\": \"range\",             \"lower\": 51.0,             \"upper\": 77.0           }         ```         Note: The field **type** can take the value 'range', 'iqr' or 'ci'.    * <span class=\"badge badge-pill badge-pgs\">1.3</span> - November 2020:     * New endpoint `/rest/performance/all`.     * New field **license** in the `/rest/score` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.2</span> - July 2020:     * Update `/rest/trait/search`:       * New parameters '*include_children*' and '*exact*'.       * New field **child_associated_pgs_ids**     * Update `/rest/trait/{trait_id}`:       * New parameter '*include_children*'.       * New field **child_associated_pgs_ids**       * New field **child_traits** present when the parameter '*include_children*' is set to 1.    * <span class=\"badge badge-pill badge-pgs\">1.1</span> - June 2020:     * New endpoint `/rest/trait_category/all`.     * New field **trait_categories** in the `/rest/trait` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.0</span> - May 2020:     * First version of the PGS Catalog REST API </div>  ---   # noqa: E501

    OpenAPI spec version: 1.8.6
    Contact: pgs-info@ebi.ac.uk
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import copy
import logging
import multiprocessing
import sys
import urllib3

import six
from six.moves import http_client as httplib


class TypeWithDefault(type):
    def __init__(cls, name, bases, dct):
        super(TypeWithDefault, cls).__init__(name, bases, dct)
        cls._default = None

    def __call__(cls):
        if cls._default is None:
            cls._default = type.__call__(cls)
        return copy.copy(cls._default)

    def set_default(cls, default):
        cls._default = copy.copy(default)


class Configuration(six.with_metaclass(TypeWithDefault, object)):
    """NOTE: This class is auto generated by the swagger code generator program.

    Ref: https://github.com/swagger-api/swagger-codegen
    Do not edit the class manually.
    """

    def __init__(self):
        """Constructor"""
        # Default Base url
        self.host = "https://www.pgscatalog.org/"
        # Temp file folder for downloading files
        self.temp_folder_path = None

        # Authentication Settings
        # dict to store API key(s)
        self.api_key = {}
        # dict to store API prefix (e.g. Bearer)
        self.api_key_prefix = {}
        # function to refresh API key if expired
        self.refresh_api_key_hook = None
        # Username for HTTP basic authentication
        self.username = ""
        # Password for HTTP basic authentication
        self.password = ""
        # Logging Settings
        self.logger = {}
        self.logger["package_logger"] = logging.getLogger("pgs_catalog_client")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        # Log format
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        # Log stream handler
        self.logger_stream_handler = None
        # Log file handler
        self.logger_file_handler = None
        # Debug file location
        self.logger_file = None
        # Debug switch
        self.debug = False

        # SSL/TLS verification
        # Set this to false to skip verifying SSL certificate when calling API
        # from https server.
        self.verify_ssl = True
        # Set this to customize the certificate file to verify the peer.
        self.ssl_ca_cert = None
        # client certificate file
        self.cert_file = None
        # client key file
        self.key_file = None
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None

        # urllib3 connection pool's maximum number of connections saved
        # per pool. urllib3 uses 1 connection as default value, but this is
        # not the best value when you are making a lot of possibly parallel
        # requests to the same host, which is often the case here.
        # cpu_count * 5 is used as default value to increase performance.
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5

        # Proxy URL
        self.proxy = None
        # Safe chars for path_param
        self.safe_chars_for_path_param = ''

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_file_handler)
                if self.logger_stream_handler:
                    logger.removeHandler(self.logger_stream_handler)
        else:
            # If not set logging file,
            # then add stream handler and remove file handler.
            self.logger_stream_handler = logging.StreamHandler()
            self.logger_stream_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_stream_handler)
                if self.logger_file_handler:
                    logger.removeHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.WARNING)
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :return: The token for api key authentication.
        """
        if self.refresh_api_key_hook:
            self.refresh_api_key_hook(self)

        key = self.api_key.get(identifier)
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return "%s %s" % (prefix, key)
            else:
                return key

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        return urllib3.util.make_headers(
            basic_auth=self.username + ':' + self.password
        ).get('authorization')

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        return {
        }

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 1.8.6\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)
