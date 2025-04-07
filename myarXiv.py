from typing import Final

from bs4 import BeautifulSoup
import lxml
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, parse_qsl

from pprint import pprint
from icecream import ic

SUBJECT_ELEMENT = [
    'classification-physics_archives',
    'classification-q_finance',
    'classification-statistics',
    'classification-computer_science',
    'classification-economics',
    'classification-eess',
    'classification-mathematics',
    'classification-physics',
    'classification-q_biology',
    # 'classification-include_cross_list',
]

SUBJECT_INCLUDE_CROSS_LIST =[
    
]

PHYSICS_ARCHIVES_ELEMENT = [
    'all',
    'astro_ph',
    'cond_mat',
    'gr-pc',
    'hep-ex',
    'hep-lat',
    'hep-ph',
    'hep-th',
    'math-ph',
    'nlin',
    'nucl-ex',
    'nucl-th',
    'physics',
    'quant-ph'
]

DATE_FILTER_ELEMENT = [
    'date-filter_by', 
    'date-date_type', 
    'date-year', #YYYY
    'date-from_date', # YYYY[MM[DD]]
    'date-to_date', # YYYY[MM[DD]]
    'order'
]

OTHER_ELEMENT = [
    'abstracts',  # hide
    'size', # 25, 50 ,100, 200
    'include_order_version', # y
    'start'
]

SIMPLE_SEARCH_TYPE = [
    'all', # All fields
    'title', # Title
    'author', # Author(s)
    'abstract', # Abstract
    'comments', # Comments
    'journal_ref', # Journal reference
    'acm_class', # ACM classification
    'msc_class', # MSC classification
    'report_num', # Report number
    'paper_id', # arXiv identifier
    'doi', # DOI
    'orcid', # ORCID
    'license', # License (URI)
    'author_id', # arXiv author ID

]

SIMPLE_SEARCH_TYPE_SPECIAL = [
    'help', # Help pages
    'full_text' # Full text
]




class SimpleSearch:
    
    def __init__(self, query, type_):
        self.search_query = query,
        self.search_type = type_

        pass
    
    pass


class AdvancedSearch:
        
    _SUBMITTED_DATE = 0
    _SUBMITTED_DATE_FIRST = 1
    _ANNOUNCED_DATE_FIRST = 2
    
    def __init__(self, 
                 terms, subjects = 'all',
                 physics_archive = 'all',
                 has_cross_listed = True,
                 hits = 50, from_index = 0, order = _ANNOUNCED_DATE_FIRST,
                 date=(), date_type=_ANNOUNCED_DATE_FIRST,
                 ):
        """_summary_

        Parameters
        ----------
        terms : _type_
            {\n
                'field': terms-i-field,\n 
                'operator': terms-i-operator, \n
                'term': terms-i-term\n
            }\n
        subjects : list or str
            classifications. Defaults to 'all' that means all classifications will be included.
        physics_archive : str, optional
            set archives if you want. Defaults to 'all'.
        has_cross_listed : bool, optional
            whether hits include cross-listed papers. if True, hits include papers which have tagby default True
        hits : int, optional
            number of hits you get articles from arXiv. upper limit is 500
        from_index : int
            start index searched from results. Defaults to 0.
        order : str, optional
            _description_, by default 'first'
        date : tuple, optional
            Date range. Form (YYYY[-MM[-DD]], YYYY[-MM[-DD]]) such like (2023, 2025-11-01) or set `()` if you have no care about setting range, . Defaults to ().
        """
        
        self._terms = terms
        self._subjects = subjects
        self._physics_archive = physics_archive
        if has_cross_listed:
            self._cross_listed = 'include'
        else:
            self._cross_listed = 'exclude'
        self._hits = max(hits, 200)
        self._from_index = from_index
        if date == (): 
            self._date_filter = 'all_dates'
        elif date:
            self._date_filter = 'date_range'
        self._date = date
        if order == AdvancedSearch._ANNOUNCED_DATE_FIRST:
            self._order = '-announced_date_first'
        if date_type == AdvancedSearch._SUBMITTED_DATE:
            self._date_type = 'submitted_date'
        if date_type == AdvancedSearch._SUBMITTED_DATE_FIRST:
            self._date_type = 'submitted_date_first'
        if date_type == AdvancedSearch._ANNOUNCED_DATE_FIRST:
            self._date_type = 'announced_date_fist'
            
        
    def getUrls(self):
        
        search_query = 'https://arxiv.org/search/advanced?advanced=&'
        
        # terms
        for enum, term in enumerate(self._terms):
            if len(term) == 3:
                search_query += 'terms-'+ str(enum) + 'operator='+term['operator'] + '&'
                search_query += 'terms-' + str(enum) + 'term=' + term['term'] + '&'
                search_query += 'terms-' + str(enum) + 'field=' + term['field'] + '&'
            else:
                ic()
                raise Exception
        
        # subject
        for subject in self._subjects:
            search_query += subject +'=y&'
        
        # physics_archive 
        search_query += 'classification-physics_archives=' + self._physics_archive + '&'
        
        # cross_listed
        search_query += 'classification-include_cross_list=' + self._cross_listed + '&'
        
        # date'filter
        search_query += 'date-filter_by=' + self._date_filter +'&'
        if self._date == ():
            search_query += 'date-from_date=&date-to_date=&'
        elif len(self._date):
            search_query += 'date-from_date='+ self._date[0]+'&date-to_date=' + self._date[1] + '&'
        
        # date_type
        search_query += 'date-date_type=' + self._date_type + '&'
        
        # show abstract
        search_query += 'abstracts=hide&'
        
        # size
        search_query += 'size=100&'
        
        # order
        search_query += 'order=-announced_date_first&' 
        
        print(search_query)
        return search_query
            
            
            
        
        

        
    