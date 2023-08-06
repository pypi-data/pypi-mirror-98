import { __assign, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import * as Layout from 'app/components/layouts/thirds';
import QueryCount from 'app/components/queryCount';
import Tooltip from 'app/components/tooltip';
import { IconPause, IconPlay } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withProjects from 'app/utils/withProjects';
import SavedSearchTab from './savedSearchTab';
import { getTabs, isForReviewQuery, IssueSortOptions, Query, TAB_MAX_COUNT, } from './utils';
function WrapGuideTabs(_a) {
    var children = _a.children, tabQuery = _a.tabQuery, query = _a.query, to = _a.to;
    if (isForReviewQuery(tabQuery)) {
        return (<GuideAnchor target="inbox_guide_tab" disabled={isForReviewQuery(query)} to={to}>
        <GuideAnchor target="for_review_guide_tab">{children}</GuideAnchor>
      </GuideAnchor>);
    }
    return children;
}
function IssueListHeader(_a) {
    var _b, _c;
    var organization = _a.organization, query = _a.query, queryCount = _a.queryCount, queryCounts = _a.queryCounts, realtimeActive = _a.realtimeActive, onRealtimeChange = _a.onRealtimeChange, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, savedSearchList = _a.savedSearchList, router = _a.router, displayReprocessingTab = _a.displayReprocessingTab;
    var tabs = getTabs(organization);
    var visibleTabs = displayReprocessingTab
        ? tabs
        : tabs.filter(function (_a) {
            var _b = __read(_a, 1), tab = _b[0];
            return tab !== Query.REPROCESSING;
        });
    var savedSearchTabActive = !visibleTabs.some(function (_a) {
        var _b = __read(_a, 1), tabQuery = _b[0];
        return tabQuery === query;
    });
    // Remove cursor and page when switching tabs
    var _d = (_c = (_b = router === null || router === void 0 ? void 0 : router.location) === null || _b === void 0 ? void 0 : _b.query) !== null && _c !== void 0 ? _c : {}, _ = _d.cursor, __ = _d.page, queryParms = __rest(_d, ["cursor", "page"]);
    var sortParam = queryParms.sort === IssueSortOptions.INBOX ? undefined : queryParms.sort;
    function trackTabClick(tabQuery) {
        // Clicking on inbox tab and currently another tab is active
        if (isForReviewQuery(tabQuery) && !isForReviewQuery(query)) {
            trackAnalyticsEvent({
                eventKey: 'inbox_tab.clicked',
                eventName: 'Clicked Inbox Tab',
                organization_id: organization.id,
            });
        }
    }
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{t('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <ButtonBar gap={1}>
            <Button title={t('Send us feedback via email')} size="small" href="mailto:workflow-feedback@sentry.io?subject=Issues Feedback">
              Give Feedback
            </Button>
            <Button size="small" title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))} onClick={function () { return onRealtimeChange(!realtimeActive); }}>
              {realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}
            </Button>
          </ButtonBar>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {visibleTabs.map(function (_a) {
        var _b = __read(_a, 2), tabQuery = _b[0], _c = _b[1], queryName = _c.name, tooltipTitle = _c.tooltipTitle, tooltipHoverable = _c.tooltipHoverable;
        var to = {
            query: __assign(__assign({}, queryParms), { query: tabQuery, sort: isForReviewQuery(tabQuery) ? IssueSortOptions.INBOX : sortParam }),
            pathname: "/organizations/" + organization.slug + "/issues/",
        };
        return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
                  <Link to={to} onClick={function () { return trackTabClick(tabQuery); }}>
                    <WrapGuideTabs query={query} tabQuery={tabQuery} to={to}>
                      <Tooltip title={tooltipTitle} position="bottom" isHoverable={tooltipHoverable} delay={1000}>
                        {queryName}{' '}
                        {queryCounts[tabQuery] && (<StyledQueryCount isTag tagProps={{
            type: isForReviewQuery(tabQuery) &&
                queryCounts[tabQuery].count > 0
                ? 'warning'
                : 'default',
        }} count={queryCounts[tabQuery].count} max={queryCounts[tabQuery].hasMore ? TAB_MAX_COUNT : 1000}/>)}
                      </Tooltip>
                    </WrapGuideTabs>
                  </Link>
                </li>);
    })}
          <SavedSearchTab organization={organization} query={query} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} isActive={savedSearchTabActive} queryCount={queryCount}/>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
export default withProjects(IssueListHeader);
var StyledLayoutTitle = styled(Layout.Title)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var BorderlessHeader = styled(Layout.Header)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var TabLayoutHeader = styled(Layout.Header)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"], ["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n  margin-right: ", ";\n"], ["\n  margin-bottom: 0;\n  margin-right: ", ";\n"])), space(2));
var StyledQueryCount = styled(QueryCount)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map