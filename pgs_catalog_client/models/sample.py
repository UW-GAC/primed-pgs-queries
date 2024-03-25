# coding: utf-8

"""
    PGS Catalog REST API

    Programmatic access to the PGS Catalog metadata. More information about the metadata and its structure can be found [here](/docs/).  <i class=\"fas fa-exclamation-circle pgs_color_1\"></i> Each PGS is provided as a scoring file (containing the variants, alleles, effect weights) on our <a href=\"http://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/\" target=\"_blank\">FTP site</a>. The variants are not distributed within this API; however, a link to the scoring file is provided in the<code>ftp_scoring_file</code>field for each result of the<code>/rest/score/</code>endpoints for ease of download.  ---  ###### REST API settings  * `pagination`: This REST API is using pagination for the endpoints returning more than 1 results. It is currently set to **50** results per page.   <a class=\"toggle_btn pgs_btn_plus\" id=\"pagination\">More information</a>   <div class=\"toggle_content\" id=\"content_pagination\" style=\"display:none\">      ###### **Pagination structure**      Here is an example of the pagination result structure in JSON:      ```       {         \"size\": 50,         \"count\": 137,         \"next\": \"https://www.pgscatalog.org/rest/score/all?limit=50&offset=50\",         \"previous\": null,         \"results\": [           < list the results 1 to 50 >         ]       }     ```     * **size**: is the number of results in the current page.     * **count**: is the overall number of results.     * **next**: is the URL to the following page of results.     * **previous**: is the URL to the preceding page of results (only present if you are not on the first page).     * **results**: contains the list of results of the current page.     <pre></pre>     ###### **Pagination parameters**     * **limit**: The number of results per page can be overwritten using this parameter, e.g:       * <code>.../rest/score/all/?limit=100</code>: returns the first 100 results.       * <code>.../rest/score/all/?limit=150</code>: returns all the results (the overall number of results is 137 in our example above).        The default value is **50**. The maximum value is **250**. Over this maximum value, the REST API returns an error 400.      * **offset**: This parameter indicates the starting position (0 based) of the query in relation to the complete set of results. It provides access to a desired range of results, e.g.:       * <code>.../rest/score/all/?offset=75</code> provides results from the number **76** to **125**, as the number of results per page is **50** by default (equivalent to \"limit=50\")       * <code>.../rest/score/all/?offset=75&limit=60</code> provides results from the number **76** to **135**    </div>   * `rate limit`: The limit number of queries is set to **100** queries per minute.   <a class=\"toggle_btn pgs_btn_plus\" id=\"rate_limit\">More information</a>   <div class=\"toggle_content\" id=\"content_rate_limit\" style=\"display:none\">     Here is an example of the JSON message returned if the rate limit is reached:      ```       {         \"message\": \"request limit exceeded\",         \"availableIn\": \"33 seconds\"       }     ```     * **message**: description of the error.     * **availableIn**: number of seconds before the rate limit is reset.   </div>  ---  <a class=\"toggle_btn pgs_btn_plus\" id=\"changelog\">REST API version changelog</a> <div class=\"toggle_content\" id=\"content_changelog\" style=\"display:none\">    * <span class=\"badge badge-pill badge-pgs\">1.8.6</span> - January 2023:     * New field **date_release** in the Score schemas (`/rest/score/` endpoints), containing the release date of the Score in the PGS Catalog.     * New field **date_release** in the Publication schemas (`/rest/publication/` endpoints), containing the release date of the Publication in the PGS Catalog.    * <span class=\"badge badge-pill badge-pgs\">1.8.5</span> - December 2022:     * Add deprecation message about the parameter 'pgs_ids' of the endpoint `/rest/score/search` as it is redundant with the parameter 'filter_ids'  of the endpoint `/rest/score/all`.     * Fix the parameter 'include_parents' for the endpoint `/rest/trait/all`.     * New parameter 'include_child_associated_pgs_ids' for the endpoint `/rest/trait/all` to display the list of PGS IDs associated with the children traits.    * <span class=\"badge badge-pill badge-pgs\">1.8.4</span> - August 2022:     * New field **ftp_harmonized_scoring_files** in the Score schemas (`/rest/score/` endpoints), listing the URLs to the different harmonized scoring files.     * New field **ensembl_version** in the `/rest/info/` endpoint: Ensembl version used to generate the harmonized scoring files.    * <span class=\"badge badge-pill badge-pgs\">1.8.3</span> - February 2022:     * New parameter 'filter_ids' to narrow down the results in the following endpoints:       * `/rest/score/all`       * `/rest/publication/all`       * `/rest/trait/all`       * `/rest/performance/all`       * `/rest/cohort/all`       * `/rest/sample_set/all`     * New field **name_others** in the Cohort schemas (`/rest/cohort/` endpoints).    * <span class=\"badge badge-pill badge-pgs\">1.8.2</span> - October 2021:     * New field **weight_type** in the Score schemas (`/rest/score/` endpoints).     * New parameters 'pgp_id' and 'pmid' for the endpoints `/rest/performance/search` and `/rest/sample_set/search`.     * New parameter 'pgp_id' for the endpoint `/rest/score/search`.    * <span class=\"badge badge-pill badge-pgs\">1.8.1</span> - July 2021:     * Change the data type of the field **source_PMID** to numeric in the Sample schemas     * New field **source_DOI** in the Sample schemas and move the DOI data from **source_PMID** to this new field.    * <span class=\"badge badge-pill badge-pgs\">1.8</span> - June 2021:     * New endpoint `/rest/api_versions` providing the list of all the REST API versions and their changelogs.     * Change the data type of the field **rest_api/version** in `/rest/info` to **string**.     * Change the data structure of the `/rest/ancestry_categories` endpoint by adding the new fields **display_category** and **categories**.    * <span class=\"badge badge-pill badge-pgs\">1.7</span> - April 2021:     * New data **ancestry_distribution** in the `/rest/score` endpoints, providing information about ancestry distribution on each stage of the PGS.     * New endpoint `/rest/ancestry_categories` providing the list of ancestry symbols and names.     * New data **PMID** (PubMed ID) in the `/rest/info` endpoint, under the **citation** category.    * <span class=\"badge badge-pill badge-pgs\">1.6</span> - March 2021:     * New endpoint `/rest/info` with data such as the REST API version, latest release date and counts, PGS citation, ...     * New endpoint `/rest/cohort/all` returning all the Cohorts and their associated PGS.     * New endpoint `/rest/sample_set/all` returning all the Sample Set data.    * <span class=\"badge badge-pill badge-pgs\">1.5</span> - February 2021:     * Split the array of the field **associated_pgs_ids** (from the `/rest/publication/` endpoint) in 2 arrays **development** and **evaluation**, e.g.:       ```         \"associated_pgs_ids\": {           \"development\": [               \"PGS000011\"           ],           \"evaluation\": [               \"PGS000010\",               \"PGS000011\"           ]         }       ```      * New flag parameter **include_parents** for the endpoint `/rest/trait/all` to display the traits in the catalog + their parent traits (default: 0)    * <span class=\"badge badge-pill badge-pgs\">1.4</span> - January 2021:     * Setup a maximum value for the `limit` parameter.     * Add a new field **size** at the top of the paginated results, to indicate the number of results visible in the page.     * Replace the fields **labels** and **value** under performance_metrics**&rarr;**effect_sizes**/**class_acc**/**othermetrics in the `/rest/performance` endpoints by new fields: **name_long**, **name_short**, **estimate**, **ci_lower**, **ci_upper** and **se**.        Now the content of the **labels** and **value** fields are structured like this, e.g.:       ```         {           \"name_long\": \"Odds Ratio\",           \"name_short\": \"OR\",           \"estimate\": 1.54,           \"ci_lower\": 1.51,           \"ci_upper\": 1.57,           \"se\": 0.0663         }       ```     * Restructure the **samples**&rarr;**sample_age**/**followup_time** JSON (used in several endpoints):       * Merge and replace the fields **mean** and **median** into generic fields **estimate_type** and **estimate**:         ```           \"estimate_type\": \"mean\",           \"estimate\": 53.0         ```       * Merge and replace the fields **se** and **sd** into generic fields **variability_type** and **variability**:         ```           \"variability_type\": \"sd\",           \"variability\": 16.0,         ```       * Merge and replace the fields **range** and **iqr** by a new structure **interval**:         ```           \"interval\": {             \"type\": \"range\",             \"lower\": 51.0,             \"upper\": 77.0           }         ```         Note: The field **type** can take the value 'range', 'iqr' or 'ci'.    * <span class=\"badge badge-pill badge-pgs\">1.3</span> - November 2020:     * New endpoint `/rest/performance/all`.     * New field **license** in the `/rest/score` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.2</span> - July 2020:     * Update `/rest/trait/search`:       * New parameters '*include_children*' and '*exact*'.       * New field **child_associated_pgs_ids**     * Update `/rest/trait/{trait_id}`:       * New parameter '*include_children*'.       * New field **child_associated_pgs_ids**       * New field **child_traits** present when the parameter '*include_children*' is set to 1.    * <span class=\"badge badge-pill badge-pgs\">1.1</span> - June 2020:     * New endpoint `/rest/trait_category/all`.     * New field **trait_categories** in the `/rest/trait` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.0</span> - May 2020:     * First version of the PGS Catalog REST API </div>  ---   # noqa: E501

    OpenAPI spec version: 1.8.6
    Contact: pgs-info@ebi.ac.uk
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Sample(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'sample_number': 'int',
        'sample_cases': 'int',
        'sample_controls': 'int',
        'sample_percent_male': 'float',
        'sample_age': 'Demographic',
        'phenotyping_free': 'str',
        'followup_time': 'Demographic',
        'ancestry_broad': 'str',
        'ancestry_free': 'str',
        'ancestry_country': 'str',
        'ancestry_additional': 'str',
        'source_gwas_catalog': 'str',
        'source_pmid': 'int',
        'source_doi': 'str',
        'cohorts': 'list[Cohort]',
        'cohorts_additional': 'str'
    }

    attribute_map = {
        'sample_number': 'sample_number',
        'sample_cases': 'sample_cases',
        'sample_controls': 'sample_controls',
        'sample_percent_male': 'sample_percent_male',
        'sample_age': 'sample_age',
        'phenotyping_free': 'phenotyping_free',
        'followup_time': 'followup_time',
        'ancestry_broad': 'ancestry_broad',
        'ancestry_free': 'ancestry_free',
        'ancestry_country': 'ancestry_country',
        'ancestry_additional': 'ancestry_additional',
        'source_gwas_catalog': 'source_GWAS_catalog',
        'source_pmid': 'source_PMID',
        'source_doi': 'source_DOI',
        'cohorts': 'cohorts',
        'cohorts_additional': 'cohorts_additional'
    }

    def __init__(self, sample_number=None, sample_cases=None, sample_controls=None, sample_percent_male=None, sample_age=None, phenotyping_free=None, followup_time=None, ancestry_broad=None, ancestry_free=None, ancestry_country=None, ancestry_additional=None, source_gwas_catalog=None, source_pmid=None, source_doi=None, cohorts=None, cohorts_additional=None):  # noqa: E501
        """Sample - a model defined in Swagger"""  # noqa: E501
        self._sample_number = None
        self._sample_cases = None
        self._sample_controls = None
        self._sample_percent_male = None
        self._sample_age = None
        self._phenotyping_free = None
        self._followup_time = None
        self._ancestry_broad = None
        self._ancestry_free = None
        self._ancestry_country = None
        self._ancestry_additional = None
        self._source_gwas_catalog = None
        self._source_pmid = None
        self._source_doi = None
        self._cohorts = None
        self._cohorts_additional = None
        self.discriminator = None
        if sample_number is not None:
            self.sample_number = sample_number
        if sample_cases is not None:
            self.sample_cases = sample_cases
        if sample_controls is not None:
            self.sample_controls = sample_controls
        if sample_percent_male is not None:
            self.sample_percent_male = sample_percent_male
        if sample_age is not None:
            self.sample_age = sample_age
        if phenotyping_free is not None:
            self.phenotyping_free = phenotyping_free
        if followup_time is not None:
            self.followup_time = followup_time
        if ancestry_broad is not None:
            self.ancestry_broad = ancestry_broad
        if ancestry_free is not None:
            self.ancestry_free = ancestry_free
        if ancestry_country is not None:
            self.ancestry_country = ancestry_country
        if ancestry_additional is not None:
            self.ancestry_additional = ancestry_additional
        if source_gwas_catalog is not None:
            self.source_gwas_catalog = source_gwas_catalog
        if source_pmid is not None:
            self.source_pmid = source_pmid
        if source_doi is not None:
            self.source_doi = source_doi
        if cohorts is not None:
            self.cohorts = cohorts
        if cohorts_additional is not None:
            self.cohorts_additional = cohorts_additional

    @property
    def sample_number(self):
        """Gets the sample_number of this Sample.  # noqa: E501

        Number of individuals included in the sample  # noqa: E501

        :return: The sample_number of this Sample.  # noqa: E501
        :rtype: int
        """
        return self._sample_number

    @sample_number.setter
    def sample_number(self, sample_number):
        """Sets the sample_number of this Sample.

        Number of individuals included in the sample  # noqa: E501

        :param sample_number: The sample_number of this Sample.  # noqa: E501
        :type: int
        """

        self._sample_number = sample_number

    @property
    def sample_cases(self):
        """Gets the sample_cases of this Sample.  # noqa: E501

        Number of cases  # noqa: E501

        :return: The sample_cases of this Sample.  # noqa: E501
        :rtype: int
        """
        return self._sample_cases

    @sample_cases.setter
    def sample_cases(self, sample_cases):
        """Sets the sample_cases of this Sample.

        Number of cases  # noqa: E501

        :param sample_cases: The sample_cases of this Sample.  # noqa: E501
        :type: int
        """

        self._sample_cases = sample_cases

    @property
    def sample_controls(self):
        """Gets the sample_controls of this Sample.  # noqa: E501

        Number of controls  # noqa: E501

        :return: The sample_controls of this Sample.  # noqa: E501
        :rtype: int
        """
        return self._sample_controls

    @sample_controls.setter
    def sample_controls(self, sample_controls):
        """Sets the sample_controls of this Sample.

        Number of controls  # noqa: E501

        :param sample_controls: The sample_controls of this Sample.  # noqa: E501
        :type: int
        """

        self._sample_controls = sample_controls

    @property
    def sample_percent_male(self):
        """Gets the sample_percent_male of this Sample.  # noqa: E501

        Percentage of male participants  # noqa: E501

        :return: The sample_percent_male of this Sample.  # noqa: E501
        :rtype: float
        """
        return self._sample_percent_male

    @sample_percent_male.setter
    def sample_percent_male(self, sample_percent_male):
        """Sets the sample_percent_male of this Sample.

        Percentage of male participants  # noqa: E501

        :param sample_percent_male: The sample_percent_male of this Sample.  # noqa: E501
        :type: float
        """

        self._sample_percent_male = sample_percent_male

    @property
    def sample_age(self):
        """Gets the sample_age of this Sample.  # noqa: E501


        :return: The sample_age of this Sample.  # noqa: E501
        :rtype: Demographic
        """
        return self._sample_age

    @sample_age.setter
    def sample_age(self, sample_age):
        """Sets the sample_age of this Sample.


        :param sample_age: The sample_age of this Sample.  # noqa: E501
        :type: Demographic
        """

        self._sample_age = sample_age

    @property
    def phenotyping_free(self):
        """Gets the phenotyping_free of this Sample.  # noqa: E501

        Detailed phenotype description  # noqa: E501

        :return: The phenotyping_free of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._phenotyping_free

    @phenotyping_free.setter
    def phenotyping_free(self, phenotyping_free):
        """Sets the phenotyping_free of this Sample.

        Detailed phenotype description  # noqa: E501

        :param phenotyping_free: The phenotyping_free of this Sample.  # noqa: E501
        :type: str
        """

        self._phenotyping_free = phenotyping_free

    @property
    def followup_time(self):
        """Gets the followup_time of this Sample.  # noqa: E501


        :return: The followup_time of this Sample.  # noqa: E501
        :rtype: Demographic
        """
        return self._followup_time

    @followup_time.setter
    def followup_time(self, followup_time):
        """Sets the followup_time of this Sample.


        :param followup_time: The followup_time of this Sample.  # noqa: E501
        :type: Demographic
        """

        self._followup_time = followup_time

    @property
    def ancestry_broad(self):
        """Gets the ancestry_broad of this Sample.  # noqa: E501

        Author reported ancestry is mapped to the best matching ancestry category from the NHGRI-EBI GWAS Catalog framework (Table 1, Morales et al. (2018)).  # noqa: E501

        :return: The ancestry_broad of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._ancestry_broad

    @ancestry_broad.setter
    def ancestry_broad(self, ancestry_broad):
        """Sets the ancestry_broad of this Sample.

        Author reported ancestry is mapped to the best matching ancestry category from the NHGRI-EBI GWAS Catalog framework (Table 1, Morales et al. (2018)).  # noqa: E501

        :param ancestry_broad: The ancestry_broad of this Sample.  # noqa: E501
        :type: str
        """

        self._ancestry_broad = ancestry_broad

    @property
    def ancestry_free(self):
        """Gets the ancestry_free of this Sample.  # noqa: E501

        A more detailed description of sample ancestry that usually matches the most specific description described by the authors (e.g. French, Chinese).  # noqa: E501

        :return: The ancestry_free of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._ancestry_free

    @ancestry_free.setter
    def ancestry_free(self, ancestry_free):
        """Sets the ancestry_free of this Sample.

        A more detailed description of sample ancestry that usually matches the most specific description described by the authors (e.g. French, Chinese).  # noqa: E501

        :param ancestry_free: The ancestry_free of this Sample.  # noqa: E501
        :type: str
        """

        self._ancestry_free = ancestry_free

    @property
    def ancestry_country(self):
        """Gets the ancestry_country of this Sample.  # noqa: E501

        Author reported countries of recruitment (if available).  # noqa: E501

        :return: The ancestry_country of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._ancestry_country

    @ancestry_country.setter
    def ancestry_country(self, ancestry_country):
        """Sets the ancestry_country of this Sample.

        Author reported countries of recruitment (if available).  # noqa: E501

        :param ancestry_country: The ancestry_country of this Sample.  # noqa: E501
        :type: str
        """

        self._ancestry_country = ancestry_country

    @property
    def ancestry_additional(self):
        """Gets the ancestry_additional of this Sample.  # noqa: E501

        Any additional description not captured in the structured data (e.g. founder or genetically isolated populations, or further description of admixed samples).  # noqa: E501

        :return: The ancestry_additional of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._ancestry_additional

    @ancestry_additional.setter
    def ancestry_additional(self, ancestry_additional):
        """Sets the ancestry_additional of this Sample.

        Any additional description not captured in the structured data (e.g. founder or genetically isolated populations, or further description of admixed samples).  # noqa: E501

        :param ancestry_additional: The ancestry_additional of this Sample.  # noqa: E501
        :type: str
        """

        self._ancestry_additional = ancestry_additional

    @property
    def source_gwas_catalog(self):
        """Gets the source_gwas_catalog of this Sample.  # noqa: E501

        Associated NHGRI-EBI GWAS Catalog study identifier  # noqa: E501

        :return: The source_gwas_catalog of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._source_gwas_catalog

    @source_gwas_catalog.setter
    def source_gwas_catalog(self, source_gwas_catalog):
        """Sets the source_gwas_catalog of this Sample.

        Associated NHGRI-EBI GWAS Catalog study identifier  # noqa: E501

        :param source_gwas_catalog: The source_gwas_catalog of this Sample.  # noqa: E501
        :type: str
        """

        self._source_gwas_catalog = source_gwas_catalog

    @property
    def source_pmid(self):
        """Gets the source_pmid of this Sample.  # noqa: E501

        Associated PubMed identifier  # noqa: E501

        :return: The source_pmid of this Sample.  # noqa: E501
        :rtype: int
        """
        return self._source_pmid

    @source_pmid.setter
    def source_pmid(self, source_pmid):
        """Sets the source_pmid of this Sample.

        Associated PubMed identifier  # noqa: E501

        :param source_pmid: The source_pmid of this Sample.  # noqa: E501
        :type: int
        """

        self._source_pmid = source_pmid

    @property
    def source_doi(self):
        """Gets the source_doi of this Sample.  # noqa: E501

        Associated Digital Object Identifier  # noqa: E501

        :return: The source_doi of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._source_doi

    @source_doi.setter
    def source_doi(self, source_doi):
        """Sets the source_doi of this Sample.

        Associated Digital Object Identifier  # noqa: E501

        :param source_doi: The source_doi of this Sample.  # noqa: E501
        :type: str
        """

        self._source_doi = source_doi

    @property
    def cohorts(self):
        """Gets the cohorts of this Sample.  # noqa: E501

        List of cohorts that collected the samples  # noqa: E501

        :return: The cohorts of this Sample.  # noqa: E501
        :rtype: list[Cohort]
        """
        return self._cohorts

    @cohorts.setter
    def cohorts(self, cohorts):
        """Sets the cohorts of this Sample.

        List of cohorts that collected the samples  # noqa: E501

        :param cohorts: The cohorts of this Sample.  # noqa: E501
        :type: list[Cohort]
        """

        self._cohorts = cohorts

    @property
    def cohorts_additional(self):
        """Gets the cohorts_additional of this Sample.  # noqa: E501

        Any additional description about the samples and what they were used for that is not captured by the structured categories (e.g. sub-cohort information).  # noqa: E501

        :return: The cohorts_additional of this Sample.  # noqa: E501
        :rtype: str
        """
        return self._cohorts_additional

    @cohorts_additional.setter
    def cohorts_additional(self, cohorts_additional):
        """Sets the cohorts_additional of this Sample.

        Any additional description about the samples and what they were used for that is not captured by the structured categories (e.g. sub-cohort information).  # noqa: E501

        :param cohorts_additional: The cohorts_additional of this Sample.  # noqa: E501
        :type: str
        """

        self._cohorts_additional = cohorts_additional

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Sample, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Sample):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
