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

class Score(object):
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
        'id': 'str',
        'name': 'str',
        'ftp_scoring_file': 'str',
        'ftp_harmonized_scoring_files': 'ScoreFtpHarmonizedScoringFiles',
        'publication': 'Publication',
        'matches_publication': 'bool',
        'samples_variants': 'list[Sample]',
        'samples_training': 'list[Sample]',
        'trait_reported': 'str',
        'trait_additional': 'str',
        'trait_efo': 'list[EFOTrait]',
        'method_name': 'str',
        'method_params': 'str',
        'variants_number': 'int',
        'variants_interactions': 'int',
        'variants_genomebuild': 'str',
        'weight_type': 'str',
        'ancestry_distribution': 'ScoreAncestryDistribution',
        'date_release': 'date',
        'license': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'ftp_scoring_file': 'ftp_scoring_file',
        'ftp_harmonized_scoring_files': 'ftp_harmonized_scoring_files',
        'publication': 'publication',
        'matches_publication': 'matches_publication',
        'samples_variants': 'samples_variants',
        'samples_training': 'samples_training',
        'trait_reported': 'trait_reported',
        'trait_additional': 'trait_additional',
        'trait_efo': 'trait_efo',
        'method_name': 'method_name',
        'method_params': 'method_params',
        'variants_number': 'variants_number',
        'variants_interactions': 'variants_interactions',
        'variants_genomebuild': 'variants_genomebuild',
        'weight_type': 'weight_type',
        'ancestry_distribution': 'ancestry_distribution',
        'date_release': 'date_release',
        'license': 'license'
    }

    def __init__(self, id=None, name=None, ftp_scoring_file=None, ftp_harmonized_scoring_files=None, publication=None, matches_publication=None, samples_variants=None, samples_training=None, trait_reported=None, trait_additional=None, trait_efo=None, method_name=None, method_params=None, variants_number=None, variants_interactions=None, variants_genomebuild=None, weight_type=None, ancestry_distribution=None, date_release=None, license=None):  # noqa: E501
        """Score - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._ftp_scoring_file = None
        self._ftp_harmonized_scoring_files = None
        self._publication = None
        self._matches_publication = None
        self._samples_variants = None
        self._samples_training = None
        self._trait_reported = None
        self._trait_additional = None
        self._trait_efo = None
        self._method_name = None
        self._method_params = None
        self._variants_number = None
        self._variants_interactions = None
        self._variants_genomebuild = None
        self._weight_type = None
        self._ancestry_distribution = None
        self._date_release = None
        self._license = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if ftp_scoring_file is not None:
            self.ftp_scoring_file = ftp_scoring_file
        if ftp_harmonized_scoring_files is not None:
            self.ftp_harmonized_scoring_files = ftp_harmonized_scoring_files
        if publication is not None:
            self.publication = publication
        if matches_publication is not None:
            self.matches_publication = matches_publication
        if samples_variants is not None:
            self.samples_variants = samples_variants
        if samples_training is not None:
            self.samples_training = samples_training
        if trait_reported is not None:
            self.trait_reported = trait_reported
        if trait_additional is not None:
            self.trait_additional = trait_additional
        if trait_efo is not None:
            self.trait_efo = trait_efo
        if method_name is not None:
            self.method_name = method_name
        if method_params is not None:
            self.method_params = method_params
        if variants_number is not None:
            self.variants_number = variants_number
        if variants_interactions is not None:
            self.variants_interactions = variants_interactions
        if variants_genomebuild is not None:
            self.variants_genomebuild = variants_genomebuild
        if weight_type is not None:
            self.weight_type = weight_type
        if ancestry_distribution is not None:
            self.ancestry_distribution = ancestry_distribution
        if date_release is not None:
            self.date_release = date_release
        if license is not None:
            self.license = license

    @property
    def id(self):
        """Gets the id of this Score.  # noqa: E501

        Polygenic Score identifier  # noqa: E501

        :return: The id of this Score.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Score.

        Polygenic Score identifier  # noqa: E501

        :param id: The id of this Score.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Score.  # noqa: E501

        This may be the name that the authors describe the PGS with in the source publication, or a name that a curator has assigned to identify the score during the curation process (before a PGS ID has been given)  # noqa: E501

        :return: The name of this Score.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Score.

        This may be the name that the authors describe the PGS with in the source publication, or a name that a curator has assigned to identify the score during the curation process (before a PGS ID has been given)  # noqa: E501

        :param name: The name of this Score.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def ftp_scoring_file(self):
        """Gets the ftp_scoring_file of this Score.  # noqa: E501

        URL to the scoring file on the PGS FTP  # noqa: E501

        :return: The ftp_scoring_file of this Score.  # noqa: E501
        :rtype: str
        """
        return self._ftp_scoring_file

    @ftp_scoring_file.setter
    def ftp_scoring_file(self, ftp_scoring_file):
        """Sets the ftp_scoring_file of this Score.

        URL to the scoring file on the PGS FTP  # noqa: E501

        :param ftp_scoring_file: The ftp_scoring_file of this Score.  # noqa: E501
        :type: str
        """

        self._ftp_scoring_file = ftp_scoring_file

    @property
    def ftp_harmonized_scoring_files(self):
        """Gets the ftp_harmonized_scoring_files of this Score.  # noqa: E501


        :return: The ftp_harmonized_scoring_files of this Score.  # noqa: E501
        :rtype: ScoreFtpHarmonizedScoringFiles
        """
        return self._ftp_harmonized_scoring_files

    @ftp_harmonized_scoring_files.setter
    def ftp_harmonized_scoring_files(self, ftp_harmonized_scoring_files):
        """Sets the ftp_harmonized_scoring_files of this Score.


        :param ftp_harmonized_scoring_files: The ftp_harmonized_scoring_files of this Score.  # noqa: E501
        :type: ScoreFtpHarmonizedScoringFiles
        """

        self._ftp_harmonized_scoring_files = ftp_harmonized_scoring_files

    @property
    def publication(self):
        """Gets the publication of this Score.  # noqa: E501


        :return: The publication of this Score.  # noqa: E501
        :rtype: Publication
        """
        return self._publication

    @publication.setter
    def publication(self, publication):
        """Sets the publication of this Score.


        :param publication: The publication of this Score.  # noqa: E501
        :type: Publication
        """

        self._publication = publication

    @property
    def matches_publication(self):
        """Gets the matches_publication of this Score.  # noqa: E501

        Indicate if the PGS data matches the published polygenic score. If not, the authors have provided an alternative polygenic for the Catalog and some other data, such as performance metrics, may differ from the publication.  # noqa: E501

        :return: The matches_publication of this Score.  # noqa: E501
        :rtype: bool
        """
        return self._matches_publication

    @matches_publication.setter
    def matches_publication(self, matches_publication):
        """Sets the matches_publication of this Score.

        Indicate if the PGS data matches the published polygenic score. If not, the authors have provided an alternative polygenic for the Catalog and some other data, such as performance metrics, may differ from the publication.  # noqa: E501

        :param matches_publication: The matches_publication of this Score.  # noqa: E501
        :type: bool
        """

        self._matches_publication = matches_publication

    @property
    def samples_variants(self):
        """Gets the samples_variants of this Score.  # noqa: E501

        List of samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.  # noqa: E501

        :return: The samples_variants of this Score.  # noqa: E501
        :rtype: list[Sample]
        """
        return self._samples_variants

    @samples_variants.setter
    def samples_variants(self, samples_variants):
        """Sets the samples_variants of this Score.

        List of samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.  # noqa: E501

        :param samples_variants: The samples_variants of this Score.  # noqa: E501
        :type: list[Sample]
        """

        self._samples_variants = samples_variants

    @property
    def samples_training(self):
        """Gets the samples_training of this Score.  # noqa: E501

        List of samples used to develop/train the Polygenic Score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).  # noqa: E501

        :return: The samples_training of this Score.  # noqa: E501
        :rtype: list[Sample]
        """
        return self._samples_training

    @samples_training.setter
    def samples_training(self, samples_training):
        """Sets the samples_training of this Score.

        List of samples used to develop/train the Polygenic Score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).  # noqa: E501

        :param samples_training: The samples_training of this Score.  # noqa: E501
        :type: list[Sample]
        """

        self._samples_training = samples_training

    @property
    def trait_reported(self):
        """Gets the trait_reported of this Score.  # noqa: E501

        The author-reported trait that the PGS has been developed to predict.  # noqa: E501

        :return: The trait_reported of this Score.  # noqa: E501
        :rtype: str
        """
        return self._trait_reported

    @trait_reported.setter
    def trait_reported(self, trait_reported):
        """Sets the trait_reported of this Score.

        The author-reported trait that the PGS has been developed to predict.  # noqa: E501

        :param trait_reported: The trait_reported of this Score.  # noqa: E501
        :type: str
        """

        self._trait_reported = trait_reported

    @property
    def trait_additional(self):
        """Gets the trait_additional of this Score.  # noqa: E501

        Any additional description not captured in the structured data  # noqa: E501

        :return: The trait_additional of this Score.  # noqa: E501
        :rtype: str
        """
        return self._trait_additional

    @trait_additional.setter
    def trait_additional(self, trait_additional):
        """Sets the trait_additional of this Score.

        Any additional description not captured in the structured data  # noqa: E501

        :param trait_additional: The trait_additional of this Score.  # noqa: E501
        :type: str
        """

        self._trait_additional = trait_additional

    @property
    def trait_efo(self):
        """Gets the trait_efo of this Score.  # noqa: E501

        The Reported Trait is mapped to Experimental Factor Ontology (EFO) terms and their respective identifiers.  # noqa: E501

        :return: The trait_efo of this Score.  # noqa: E501
        :rtype: list[EFOTrait]
        """
        return self._trait_efo

    @trait_efo.setter
    def trait_efo(self, trait_efo):
        """Sets the trait_efo of this Score.

        The Reported Trait is mapped to Experimental Factor Ontology (EFO) terms and their respective identifiers.  # noqa: E501

        :param trait_efo: The trait_efo of this Score.  # noqa: E501
        :type: list[EFOTrait]
        """

        self._trait_efo = trait_efo

    @property
    def method_name(self):
        """Gets the method_name of this Score.  # noqa: E501

        The name or description of the method or computational algorithm used to develop the PGS.  # noqa: E501

        :return: The method_name of this Score.  # noqa: E501
        :rtype: str
        """
        return self._method_name

    @method_name.setter
    def method_name(self, method_name):
        """Sets the method_name of this Score.

        The name or description of the method or computational algorithm used to develop the PGS.  # noqa: E501

        :param method_name: The method_name of this Score.  # noqa: E501
        :type: str
        """

        self._method_name = method_name

    @property
    def method_params(self):
        """Gets the method_params of this Score.  # noqa: E501

        A description of the relevant inputs and parameters relevant to the PGS development method/process.  # noqa: E501

        :return: The method_params of this Score.  # noqa: E501
        :rtype: str
        """
        return self._method_params

    @method_params.setter
    def method_params(self, method_params):
        """Sets the method_params of this Score.

        A description of the relevant inputs and parameters relevant to the PGS development method/process.  # noqa: E501

        :param method_params: The method_params of this Score.  # noqa: E501
        :type: str
        """

        self._method_params = method_params

    @property
    def variants_number(self):
        """Gets the variants_number of this Score.  # noqa: E501

        Number of variants used to calculate the PGS. In the future this will include a more detailed description of the types of variants present.  # noqa: E501

        :return: The variants_number of this Score.  # noqa: E501
        :rtype: int
        """
        return self._variants_number

    @variants_number.setter
    def variants_number(self, variants_number):
        """Sets the variants_number of this Score.

        Number of variants used to calculate the PGS. In the future this will include a more detailed description of the types of variants present.  # noqa: E501

        :param variants_number: The variants_number of this Score.  # noqa: E501
        :type: int
        """

        self._variants_number = variants_number

    @property
    def variants_interactions(self):
        """Gets the variants_interactions of this Score.  # noqa: E501

        Number of higher-order variant interactions included in the PGS.  # noqa: E501

        :return: The variants_interactions of this Score.  # noqa: E501
        :rtype: int
        """
        return self._variants_interactions

    @variants_interactions.setter
    def variants_interactions(self, variants_interactions):
        """Sets the variants_interactions of this Score.

        Number of higher-order variant interactions included in the PGS.  # noqa: E501

        :param variants_interactions: The variants_interactions of this Score.  # noqa: E501
        :type: int
        """

        self._variants_interactions = variants_interactions

    @property
    def variants_genomebuild(self):
        """Gets the variants_genomebuild of this Score.  # noqa: E501

        The version of the genome assembly that the variants present in the PGS are associated with. Listed as NR (Not Reported) if unknown.  # noqa: E501

        :return: The variants_genomebuild of this Score.  # noqa: E501
        :rtype: str
        """
        return self._variants_genomebuild

    @variants_genomebuild.setter
    def variants_genomebuild(self, variants_genomebuild):
        """Sets the variants_genomebuild of this Score.

        The version of the genome assembly that the variants present in the PGS are associated with. Listed as NR (Not Reported) if unknown.  # noqa: E501

        :param variants_genomebuild: The variants_genomebuild of this Score.  # noqa: E501
        :type: str
        """

        self._variants_genomebuild = variants_genomebuild

    @property
    def weight_type(self):
        """Gets the weight_type of this Score.  # noqa: E501

        Variant Weight supplied by the author: beta (effect size), or something like an OR/HR (odds/hazard ratio).  # noqa: E501

        :return: The weight_type of this Score.  # noqa: E501
        :rtype: str
        """
        return self._weight_type

    @weight_type.setter
    def weight_type(self, weight_type):
        """Sets the weight_type of this Score.

        Variant Weight supplied by the author: beta (effect size), or something like an OR/HR (odds/hazard ratio).  # noqa: E501

        :param weight_type: The weight_type of this Score.  # noqa: E501
        :type: str
        """

        self._weight_type = weight_type

    @property
    def ancestry_distribution(self):
        """Gets the ancestry_distribution of this Score.  # noqa: E501


        :return: The ancestry_distribution of this Score.  # noqa: E501
        :rtype: ScoreAncestryDistribution
        """
        return self._ancestry_distribution

    @ancestry_distribution.setter
    def ancestry_distribution(self, ancestry_distribution):
        """Sets the ancestry_distribution of this Score.


        :param ancestry_distribution: The ancestry_distribution of this Score.  # noqa: E501
        :type: ScoreAncestryDistribution
        """

        self._ancestry_distribution = ancestry_distribution

    @property
    def date_release(self):
        """Gets the date_release of this Score.  # noqa: E501

        Release date in PGS Catalog (format YYYY-MM-DD)  # noqa: E501

        :return: The date_release of this Score.  # noqa: E501
        :rtype: date
        """
        return self._date_release

    @date_release.setter
    def date_release(self, date_release):
        """Sets the date_release of this Score.

        Release date in PGS Catalog (format YYYY-MM-DD)  # noqa: E501

        :param date_release: The date_release of this Score.  # noqa: E501
        :type: date
        """

        self._date_release = date_release

    @property
    def license(self):
        """Gets the license of this Score.  # noqa: E501

        The PGS Catalog distributes its data according to EBI’s standard Terms of Use. Some PGS have specific terms, licenses, or restrictions (e.g. non-commercial use) that we highlight in this field, if known.  # noqa: E501

        :return: The license of this Score.  # noqa: E501
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """Sets the license of this Score.

        The PGS Catalog distributes its data according to EBI’s standard Terms of Use. Some PGS have specific terms, licenses, or restrictions (e.g. non-commercial use) that we highlight in this field, if known.  # noqa: E501

        :param license: The license of this Score.  # noqa: E501
        :type: str
        """

        self._license = license

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
        if issubclass(Score, dict):
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
        if not isinstance(other, Score):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
