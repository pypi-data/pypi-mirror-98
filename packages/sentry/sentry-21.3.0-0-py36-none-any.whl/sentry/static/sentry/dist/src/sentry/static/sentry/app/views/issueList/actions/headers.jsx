import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ToolbarHeader from 'app/components/toolbarHeader';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function Headers(_a) {
    var anySelected = _a.anySelected, selection = _a.selection, statsPeriod = _a.statsPeriod, displayCount = _a.displayCount, onSelectStatsPeriod = _a.onSelectStatsPeriod, isReprocessingQuery = _a.isReprocessingQuery, hasInbox = _a.hasInbox;
    return (<React.Fragment>
      {hasInbox && !anySelected && (<ActionSetPlaceholder>
          {tct('Select [displayCount]', {
        displayCount: displayCount,
    })}
        </ActionSetPlaceholder>)}
      {isReprocessingQuery ? (<React.Fragment>
          <StartedColumn>{t('Started')}</StartedColumn>
          <EventsReprocessedColumn>{t('Events Reprocessed')}</EventsReprocessedColumn>
          <ProgressColumn>{t('Progress')}</ProgressColumn>
        </React.Fragment>) : (<React.Fragment>
          <GraphHeaderWrapper className={"hidden-xs hidden-sm " + (hasInbox ? 'hidden-md' : '')}>
            <GraphHeader>
              <StyledToolbarHeader>{t('Graph:')}</StyledToolbarHeader>
              {selection.datetime.period !== '24h' && (<GraphToggle active={statsPeriod === '24h'} onClick={function () { return onSelectStatsPeriod('24h'); }}>
                  {t('24h')}
                </GraphToggle>)}
              <GraphToggle active={statsPeriod === 'auto'} onClick={function () { return onSelectStatsPeriod('auto'); }}>
                {selection.datetime.period || t('Custom')}
              </GraphToggle>
            </GraphHeader>
          </GraphHeaderWrapper>
          <EventsOrUsersLabel>{t('Events')}</EventsOrUsersLabel>
          <EventsOrUsersLabel>{t('Users')}</EventsOrUsersLabel>
          <AssigneesLabel className="hidden-xs hidden-sm">
            <IssueToolbarHeader>{t('Assignee')}</IssueToolbarHeader>
          </AssigneesLabel>
          {hasInbox && (<ActionsLabel>
              <IssueToolbarHeader>{t('Actions')}</IssueToolbarHeader>
            </ActionsLabel>)}
        </React.Fragment>)}
    </React.Fragment>);
}
export default Headers;
var IssueToolbarHeader = styled(ToolbarHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  animation: 0.3s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"], ["\n  animation: 0.3s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"])));
var ActionSetPlaceholder = styled(IssueToolbarHeader)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (min-width: 800px) {\n    width: 66.66666666666666%;\n  }\n  @media (min-width: 992px) {\n    width: 50%;\n  }\n\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  overflow: hidden;\n  min-width: 0;\n  white-space: nowrap;\n"], ["\n  @media (min-width: 800px) {\n    width: 66.66666666666666%;\n  }\n  @media (min-width: 992px) {\n    width: 50%;\n  }\n\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  overflow: hidden;\n  min-width: 0;\n  white-space: nowrap;\n"])), space(1), space(1));
var GraphHeaderWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"], ["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"])), space(2), space(2));
var GraphHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledToolbarHeader = styled(IssueToolbarHeader)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var GraphToggle = styled('a')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: 13px;\n  padding-left: ", ";\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: 13px;\n  padding-left: ", ";\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), space(1), function (p) { return (p.active ? p.theme.textColor : p.theme.disabled); });
var EventsOrUsersLabel = styled(IssueToolbarHeader)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; });
var AssigneesLabel = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space(2), space(2));
var ActionsLabel = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin: 0 ", ";\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin: 0 ", ";\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; });
// Reprocessing
var StartedColumn = styled(IssueToolbarHeader)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin: 0 ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  margin: 0 ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space(2), overflowEllipsis, function (p) { return p.theme.breakpoints[0]; });
var EventsReprocessedColumn = styled(IssueToolbarHeader)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin: 0 ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  margin: 0 ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space(2), overflowEllipsis, function (p) { return p.theme.breakpoints[0]; });
var ProgressColumn = styled(IssueToolbarHeader)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin: 0 ", ";\n\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"], ["\n  margin: 0 ", ";\n\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=headers.jsx.map