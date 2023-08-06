import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import MenuItem from 'app/components/menuItem';
import QuestionTooltip from 'app/components/questionTooltip';
import Tag, { Background } from 'app/components/tag';
import Truncate from 'app/components/truncate';
import space from 'app/styles/space';
import theme, { aliases } from 'app/utils/theme';
export function MetaData(_a) {
    var headingText = _a.headingText, tooltipText = _a.tooltipText, bodyText = _a.bodyText, subtext = _a.subtext;
    return (<HeaderInfo>
      <StyledSectionHeading>
        {headingText}
        <QuestionTooltip position="top" size="sm" containerDisplayMode="block" title={tooltipText}/>
      </StyledSectionHeading>
      <SectionBody>{bodyText}</SectionBody>
      <SectionSubtext>{subtext}</SectionSubtext>
    </HeaderInfo>);
}
var HeaderInfo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 78px;\n"], ["\n  height: 78px;\n"])));
var StyledSectionHeading = styled(SectionHeading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var SectionBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " 0;\n"], ["\n  font-size: ", ";\n  margin: ", " 0;\n"])), function (p) { return p.theme.headerFontSize; }, space(0.5));
export var SectionSubtext = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return (p.type === 'error' ? p.theme.error : p.theme.subText); }, function (p) { return p.theme.fontSizeMedium; });
var nodeColors = {
    error: {
        color: theme.white,
        background: theme.red300,
        border: theme.red300,
    },
    warning: {
        color: theme.red300,
        background: theme.white,
        border: theme.red300,
    },
    white: {
        color: theme.gray500,
        background: theme.white,
        border: theme.gray500,
    },
    black: {
        color: theme.white,
        background: theme.gray500,
        border: aliases.border,
    },
};
export var EventNode = styled(Tag)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  div {\n    color: ", ";\n  }\n  & ", " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"], ["\n  div {\n    color: ", ";\n  }\n  & " /* sc-selector */, " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"])), function (p) { return nodeColors[p.type || 'white'].color; }, /* sc-selector */ Background, function (p) { return nodeColors[p.type || 'white'].background; }, function (p) { return nodeColors[p.type || 'white'].border; });
export var TraceConnector = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  width: ", ";\n  border-top: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.border; });
export var QuickTraceContainer = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledMenuItem = styled(MenuItem)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  border-top: ", ";\n  width: 350px;\n"], ["\n  border-top: ", ";\n  width: 350px;\n"])), function (p) { return (!p.first ? "1px solid " + p.theme.innerBorder : null); });
var MenuItemContent = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"])));
export function DropdownItem(_a) {
    var children = _a.children, first = _a.first, onSelect = _a.onSelect, to = _a.to;
    return (<StyledMenuItem to={to} onSelect={onSelect} first={first}>
      <MenuItemContent>{children}</MenuItemContent>
    </StyledMenuItem>);
}
export var DropdownItemSubContainer = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
export var StyledTruncate = styled(Truncate)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=styles.jsx.map