# coding: utf-8

"""
    PGS Catalog REST API

    Programmatic access to the PGS Catalog metadata. More information about the metadata and its structure can be found [here](/docs/).  <i class=\"fas fa-exclamation-circle pgs_color_1\"></i> Each PGS is provided as a scoring file (containing the variants, alleles, effect weights) on our <a href=\"http://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/\" target=\"_blank\">FTP site</a>. The variants are not distributed within this API; however, a link to the scoring file is provided in the<code>ftp_scoring_file</code>field for each result of the<code>/rest/score/</code>endpoints for ease of download.  ---  ###### REST API settings  * `pagination`: This REST API is using pagination for the endpoints returning more than 1 results. It is currently set to **50** results per page.   <a class=\"toggle_btn pgs_btn_plus\" id=\"pagination\">More information</a>   <div class=\"toggle_content\" id=\"content_pagination\" style=\"display:none\">      ###### **Pagination structure**      Here is an example of the pagination result structure in JSON:      ```       {         \"size\": 50,         \"count\": 137,         \"next\": \"https://www.pgscatalog.org/rest/score/all?limit=50&offset=50\",         \"previous\": null,         \"results\": [           < list the results 1 to 50 >         ]       }     ```     * **size**: is the number of results in the current page.     * **count**: is the overall number of results.     * **next**: is the URL to the following page of results.     * **previous**: is the URL to the preceding page of results (only present if you are not on the first page).     * **results**: contains the list of results of the current page.     <pre></pre>     ###### **Pagination parameters**     * **limit**: The number of results per page can be overwritten using this parameter, e.g:       * <code>.../rest/score/all/?limit=100</code>: returns the first 100 results.       * <code>.../rest/score/all/?limit=150</code>: returns all the results (the overall number of results is 137 in our example above).        The default value is **50**. The maximum value is **250**. Over this maximum value, the REST API returns an error 400.      * **offset**: This parameter indicates the starting position (0 based) of the query in relation to the complete set of results. It provides access to a desired range of results, e.g.:       * <code>.../rest/score/all/?offset=75</code> provides results from the number **76** to **125**, as the number of results per page is **50** by default (equivalent to \"limit=50\")       * <code>.../rest/score/all/?offset=75&limit=60</code> provides results from the number **76** to **135**    </div>   * `rate limit`: The limit number of queries is set to **100** queries per minute.   <a class=\"toggle_btn pgs_btn_plus\" id=\"rate_limit\">More information</a>   <div class=\"toggle_content\" id=\"content_rate_limit\" style=\"display:none\">     Here is an example of the JSON message returned if the rate limit is reached:      ```       {         \"message\": \"request limit exceeded\",         \"availableIn\": \"33 seconds\"       }     ```     * **message**: description of the error.     * **availableIn**: number of seconds before the rate limit is reset.   </div>  ---  <a class=\"toggle_btn pgs_btn_plus\" id=\"changelog\">REST API version changelog</a> <div class=\"toggle_content\" id=\"content_changelog\" style=\"display:none\">    * <span class=\"badge badge-pill badge-pgs\">1.8.6</span> - January 2023:     * New field **date_release** in the Score schemas (`/rest/score/` endpoints), containing the release date of the Score in the PGS Catalog.     * New field **date_release** in the Publication schemas (`/rest/publication/` endpoints), containing the release date of the Publication in the PGS Catalog.    * <span class=\"badge badge-pill badge-pgs\">1.8.5</span> - December 2022:     * Add deprecation message about the parameter 'pgs_ids' of the endpoint `/rest/score/search` as it is redundant with the parameter 'filter_ids'  of the endpoint `/rest/score/all`.     * Fix the parameter 'include_parents' for the endpoint `/rest/trait/all`.     * New parameter 'include_child_associated_pgs_ids' for the endpoint `/rest/trait/all` to display the list of PGS IDs associated with the children traits.    * <span class=\"badge badge-pill badge-pgs\">1.8.4</span> - August 2022:     * New field **ftp_harmonized_scoring_files** in the Score schemas (`/rest/score/` endpoints), listing the URLs to the different harmonized scoring files.     * New field **ensembl_version** in the `/rest/info/` endpoint: Ensembl version used to generate the harmonized scoring files.    * <span class=\"badge badge-pill badge-pgs\">1.8.3</span> - February 2022:     * New parameter 'filter_ids' to narrow down the results in the following endpoints:       * `/rest/score/all`       * `/rest/publication/all`       * `/rest/trait/all`       * `/rest/performance/all`       * `/rest/cohort/all`       * `/rest/sample_set/all`     * New field **name_others** in the Cohort schemas (`/rest/cohort/` endpoints).    * <span class=\"badge badge-pill badge-pgs\">1.8.2</span> - October 2021:     * New field **weight_type** in the Score schemas (`/rest/score/` endpoints).     * New parameters 'pgp_id' and 'pmid' for the endpoints `/rest/performance/search` and `/rest/sample_set/search`.     * New parameter 'pgp_id' for the endpoint `/rest/score/search`.    * <span class=\"badge badge-pill badge-pgs\">1.8.1</span> - July 2021:     * Change the data type of the field **source_PMID** to numeric in the Sample schemas     * New field **source_DOI** in the Sample schemas and move the DOI data from **source_PMID** to this new field.    * <span class=\"badge badge-pill badge-pgs\">1.8</span> - June 2021:     * New endpoint `/rest/api_versions` providing the list of all the REST API versions and their changelogs.     * Change the data type of the field **rest_api/version** in `/rest/info` to **string**.     * Change the data structure of the `/rest/ancestry_categories` endpoint by adding the new fields **display_category** and **categories**.    * <span class=\"badge badge-pill badge-pgs\">1.7</span> - April 2021:     * New data **ancestry_distribution** in the `/rest/score` endpoints, providing information about ancestry distribution on each stage of the PGS.     * New endpoint `/rest/ancestry_categories` providing the list of ancestry symbols and names.     * New data **PMID** (PubMed ID) in the `/rest/info` endpoint, under the **citation** category.    * <span class=\"badge badge-pill badge-pgs\">1.6</span> - March 2021:     * New endpoint `/rest/info` with data such as the REST API version, latest release date and counts, PGS citation, ...     * New endpoint `/rest/cohort/all` returning all the Cohorts and their associated PGS.     * New endpoint `/rest/sample_set/all` returning all the Sample Set data.    * <span class=\"badge badge-pill badge-pgs\">1.5</span> - February 2021:     * Split the array of the field **associated_pgs_ids** (from the `/rest/publication/` endpoint) in 2 arrays **development** and **evaluation**, e.g.:       ```         \"associated_pgs_ids\": {           \"development\": [               \"PGS000011\"           ],           \"evaluation\": [               \"PGS000010\",               \"PGS000011\"           ]         }       ```      * New flag parameter **include_parents** for the endpoint `/rest/trait/all` to display the traits in the catalog + their parent traits (default: 0)    * <span class=\"badge badge-pill badge-pgs\">1.4</span> - January 2021:     * Setup a maximum value for the `limit` parameter.     * Add a new field **size** at the top of the paginated results, to indicate the number of results visible in the page.     * Replace the fields **labels** and **value** under performance_metrics**&rarr;**effect_sizes**/**class_acc**/**othermetrics in the `/rest/performance` endpoints by new fields: **name_long**, **name_short**, **estimate**, **ci_lower**, **ci_upper** and **se**.        Now the content of the **labels** and **value** fields are structured like this, e.g.:       ```         {           \"name_long\": \"Odds Ratio\",           \"name_short\": \"OR\",           \"estimate\": 1.54,           \"ci_lower\": 1.51,           \"ci_upper\": 1.57,           \"se\": 0.0663         }       ```     * Restructure the **samples**&rarr;**sample_age**/**followup_time** JSON (used in several endpoints):       * Merge and replace the fields **mean** and **median** into generic fields **estimate_type** and **estimate**:         ```           \"estimate_type\": \"mean\",           \"estimate\": 53.0         ```       * Merge and replace the fields **se** and **sd** into generic fields **variability_type** and **variability**:         ```           \"variability_type\": \"sd\",           \"variability\": 16.0,         ```       * Merge and replace the fields **range** and **iqr** by a new structure **interval**:         ```           \"interval\": {             \"type\": \"range\",             \"lower\": 51.0,             \"upper\": 77.0           }         ```         Note: The field **type** can take the value 'range', 'iqr' or 'ci'.    * <span class=\"badge badge-pill badge-pgs\">1.3</span> - November 2020:     * New endpoint `/rest/performance/all`.     * New field **license** in the `/rest/score` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.2</span> - July 2020:     * Update `/rest/trait/search`:       * New parameters '*include_children*' and '*exact*'.       * New field **child_associated_pgs_ids**     * Update `/rest/trait/{trait_id}`:       * New parameter '*include_children*'.       * New field **child_associated_pgs_ids**       * New field **child_traits** present when the parameter '*include_children*' is set to 1.    * <span class=\"badge badge-pill badge-pgs\">1.1</span> - June 2020:     * New endpoint `/rest/trait_category/all`.     * New field **trait_categories** in the `/rest/trait` endpoints.    * <span class=\"badge badge-pill badge-pgs\">1.0</span> - May 2020:     * First version of the PGS Catalog REST API </div>  ---   # noqa: E501

    OpenAPI spec version: 1.8.6
    Contact: pgs-info@ebi.ac.uk
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pgs_catalog_client.api_client import ApiClient


class ScoreEndpointsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_scores(self, **kwargs):  # noqa: E501
        """get_all_scores  # noqa: E501

        Retrieve all the Polygenic Scores, including for each of them:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses  Example of request: ``` https://www.pgscatalog.org/rest/score/all ``` --- ###### **Filtering**  You can choose to filter the results of this endpoint to a specified list of polygenic scores by providing a list of PGS IDs in one of two ways: 1. A comma-seperated list of scores in the request URL (this will not work for larger queries), e.g.: ``` https://www.pgscatalog.org/rest/score/all?filter_ids=PGS000001,PGS000002 ``` 2. A json-formatted list of IDs, e.g.: `{ \"filter_ids\" : [\"PGS000001\",\"PGS000002\"] }`. Example with curl: ``` curl -X GET 'https://www.pgscatalog.org/rest/score/all' -H 'Content-type:application/json' -d '{ \"filter_ids\" : [\"PGS000001\", \"PGS000002\"] }' ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_scores(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter_ids: Comma-separated list of PGS IDs or JSON object with an array of PGS IDs
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_scores_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_scores_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_scores_with_http_info(self, **kwargs):  # noqa: E501
        """get_all_scores  # noqa: E501

        Retrieve all the Polygenic Scores, including for each of them:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses  Example of request: ``` https://www.pgscatalog.org/rest/score/all ``` --- ###### **Filtering**  You can choose to filter the results of this endpoint to a specified list of polygenic scores by providing a list of PGS IDs in one of two ways: 1. A comma-seperated list of scores in the request URL (this will not work for larger queries), e.g.: ``` https://www.pgscatalog.org/rest/score/all?filter_ids=PGS000001,PGS000002 ``` 2. A json-formatted list of IDs, e.g.: `{ \"filter_ids\" : [\"PGS000001\",\"PGS000002\"] }`. Example with curl: ``` curl -X GET 'https://www.pgscatalog.org/rest/score/all' -H 'Content-type:application/json' -d '{ \"filter_ids\" : [\"PGS000001\", \"PGS000002\"] }' ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_scores_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter_ids: Comma-separated list of PGS IDs or JSON object with an array of PGS IDs
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['filter_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_scores" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'filter_ids' in params:
            query_params.append(('filter_ids', params['filter_ids']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rest/score/all', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2007',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_score(self, pgs_id, **kwargs):  # noqa: E501
        """get_score  # noqa: E501

        Retrieve a Polygenic Score, including:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses  Example of request: ``` https://www.pgscatalog.org/rest/score/PGS000001 ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_score(pgs_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pgs_id: Polygenic Score ID (required)
        :return: Score
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_score_with_http_info(pgs_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_score_with_http_info(pgs_id, **kwargs)  # noqa: E501
            return data

    def get_score_with_http_info(self, pgs_id, **kwargs):  # noqa: E501
        """get_score  # noqa: E501

        Retrieve a Polygenic Score, including:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses  Example of request: ``` https://www.pgscatalog.org/rest/score/PGS000001 ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_score_with_http_info(pgs_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pgs_id: Polygenic Score ID (required)
        :return: Score
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['pgs_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_score" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'pgs_id' is set
        if ('pgs_id' not in params or
                params['pgs_id'] is None):
            raise ValueError("Missing the required parameter `pgs_id` when calling `get_score`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'pgs_id' in params:
            path_params['pgs_id'] = params['pgs_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rest/score/{pgs_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Score',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def search_scores(self, **kwargs):  # noqa: E501
        """search_scores  # noqa: E501

        Search Polygenic Scores using defined parameters (cf. \"Parameters\" section below).<br /> The parameters can be used directly in the request URL, e.g.: ``` https://www.pgscatalog.org/rest/score/search?trait_id=EFO_1000649 ``` This returns a list of Polygenic Scores, including for each of them:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_scores(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pgp_id: PGS Catalog Publication ID (PGP) - optional
        :param int pmid: PubMed ID (without the prefix \"PMID:\") - *optional*
        :param str trait_id: Ontology ID (e.g. from EFO, HP or MONDO) with the format \"EFO_XXXX\" - *optional*
        :param str pgs_ids: Comma-separated list of PGS IDs - <span style=\"color:red\">**DEPRECATED!</span>** Please use the endpoint <code>/rest/score/all?filter_ids=<pgs_ids></code> instead - *optional*
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.search_scores_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.search_scores_with_http_info(**kwargs)  # noqa: E501
            return data

    def search_scores_with_http_info(self, **kwargs):  # noqa: E501
        """search_scores  # noqa: E501

        Search Polygenic Scores using defined parameters (cf. \"Parameters\" section below).<br /> The parameters can be used directly in the request URL, e.g.: ``` https://www.pgscatalog.org/rest/score/search?trait_id=EFO_1000649 ``` This returns a list of Polygenic Scores, including for each of them:   * The URL to the scoring file   * Publication information   * Associated trait(s) (and mapped ontology trait(s))   * The different samples used during the PGS, with ancestry information and cohort(s):     * **samples_variants**: samples used to define the variant associations/effect-sizes used in the PGS. These data are extracted from the NHGRI-EBI GWAS Catalog when a study ID (GCST) is available.     * **samples_training**: samples used to develop or train the score (e.g. not used for variant discovery, and non-overlapping with the samples used to evaluate the PGS predictive ability).   * The ancestry distribution   * The Terms/Licenses   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_scores_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str pgp_id: PGS Catalog Publication ID (PGP) - optional
        :param int pmid: PubMed ID (without the prefix \"PMID:\") - *optional*
        :param str trait_id: Ontology ID (e.g. from EFO, HP or MONDO) with the format \"EFO_XXXX\" - *optional*
        :param str pgs_ids: Comma-separated list of PGS IDs - <span style=\"color:red\">**DEPRECATED!</span>** Please use the endpoint <code>/rest/score/all?filter_ids=<pgs_ids></code> instead - *optional*
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['pgp_id', 'pmid', 'trait_id', 'pgs_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_scores" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'pgp_id' in params:
            query_params.append(('pgp_id', params['pgp_id']))  # noqa: E501
        if 'pmid' in params:
            query_params.append(('pmid', params['pmid']))  # noqa: E501
        if 'trait_id' in params:
            query_params.append(('trait_id', params['trait_id']))  # noqa: E501
        if 'pgs_ids' in params:
            query_params.append(('pgs_ids', params['pgs_ids']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/rest/score/search', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2007',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
