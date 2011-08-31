#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail


class TestSearchForIdOrSignature:

    def test_that_when_item_not_available(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        results = csp.search_for_crash("this won't exist")
        Assert.true(results.can_find_text('No results were found.'))

    def test_that_search_for_valid_signature(self, mozwebqa):
        '''
            This is a test for 
                https://bugzilla.mozilla.org/show_bug.cgi?id=609070
        '''
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        reportlist = csp.click_first_product_top_crashers_link()
        signature = reportlist.first_report_with_valid_signature.signature
        result = csp.search_for_crash(signature)
        Assert.false(result.can_find_text('No results were found.'))

    @xfail(reason="Disabled till Bug 652880 is fixed")
    def test_that_advanced_search_for_firefox_can_be_filtered(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.true(cs_advanced.can_find_text('product is one of Firefox'))

    def test_that_advanced_search_for_thunderbird_can_be_filtered(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Thunderbird')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.true(cs_advanced.can_find_text('product is one of Thunderbird'))

    def test_that_advanced_search_for_fennec_can_be_filtered(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Fennec')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.true(cs_advanced.can_find_text('product is one of Fennec'))

    def test_that_advanced_search_for_camino_can_be_filtered(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Camino')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.true(cs_advanced.can_find_text('product is one of Camino'))
    
    def test_that_advanced_search_for_seamonkey_can_be_filtered(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('SeaMonkey')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.true(cs_advanced.can_find_text('product is one of SeaMonkey'))  

    def test_that_advanced_search_drilldown_results_are_correct(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=679310
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.click_advanced_search()
        
        cs_advanced.adv_select_product("Firefox")
        cs_advanced.adv_select_version("All")
        cs_advanced.filter_reports()
        
        results_page_count = cs_advanced.first_signature_number_of_results
        cssr = cs_advanced.click_first_signature()
        Assert.equal(results_page_count, cssr.total_items_label)
