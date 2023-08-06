import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getSortLabel } from './utils';
function SavedSearchMenu(_a) {
    var savedSearchList = _a.savedSearchList, onSavedSearchDelete = _a.onSavedSearchDelete, onSavedSearchSelect = _a.onSavedSearchSelect, organization = _a.organization, query = _a.query;
    if (savedSearchList.length === 0) {
        return <EmptyItem>{t("There don't seem to be any saved searches yet.")}</EmptyItem>;
    }
    return (<React.Fragment>
      {savedSearchList.map(function (search, index) { return (<Tooltip title={<React.Fragment>
              {search.name + " \u2022 "}
              <TooltipSearchQuery>{search.query}</TooltipSearchQuery>
              {" \u2022 "}
              {t('Sort: ')}
              {getSortLabel(search.sort)}
            </React.Fragment>} containerDisplayMode="block" delay={1000} key={search.id}>
          <StyledMenuItem isActive={search.query === query} last={index === savedSearchList.length - 1}>
            <MenuItemLink tabIndex={-1} onClick={function () { return onSavedSearchSelect(search); }}>
              <SearchTitle>{search.name}</SearchTitle>
              <SearchQuery>{search.query}</SearchQuery>
              <SearchSort>
                {t('Sort: ')}
                {getSortLabel(search.sort)}
              </SearchSort>
            </MenuItemLink>
            {search.isGlobal === false && search.isPinned === false && (<Access organization={organization} access={['org:write']} renderNoAccessMessage={false}>
                <Confirm onConfirm={function () { return onSavedSearchDelete(search); }} message={t('Are you sure you want to delete this saved search?')} stopPropagation>
                  <DeleteButton borderless title={t('Delete this saved search')} icon={<IconDelete />} label={t('delete')} size="zero"/>
                </Confirm>
              </Access>)}
          </StyledMenuItem>
        </Tooltip>); })}
    </React.Fragment>);
}
export default SavedSearchMenu;
var SearchTitle = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n\n  &:after {\n    content: ' \u2022 ';\n  }\n"], ["\n  color: ", ";\n\n  &:after {\n    content: ' \\u2022 ';\n  }\n"])), function (p) { return p.theme.textColor; });
var SearchQuery = styled('code')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n"], ["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n"])), function (p) { return p.theme.textColor; });
var SearchSort = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \u2022 ';\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \\u2022 ';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; });
var TooltipSearchQuery = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.text.familyMono; });
var DeleteButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, space(1), function (p) { return p.theme.blue300; });
var StyledMenuItem = styled(MenuItem)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  ", "\n"], ["\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  ",
    "\n"])), function (p) { return (!p.last ? "1px solid " + p.theme.innerBorder : null); }, function (p) { return p.theme.fontSizeMedium; }, function (p) {
    return p.isActive &&
        "\n  " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n    color: " + p.theme.white + ";\n  }\n  " + SearchSort + ":before {\n    color: " + p.theme.white + ";\n  }\n  &:hover {\n    " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n      color: " + p.theme.black + ";\n    }\n    " + SearchSort + ":before {\n      color: " + p.theme.black + ";\n    }\n  }\n  ";
});
var MenuItemLink = styled('a')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: block;\n  flex-grow: 1;\n  padding: ", " 0;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"], ["\n  display: block;\n  flex-grow: 1;\n  padding: ", " 0;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"])), space(0.5), overflowEllipsis);
var EmptyItem = styled('li')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding: 8px 10px 5px;\n  font-style: italic;\n"], ["\n  padding: 8px 10px 5px;\n  font-style: italic;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=savedSearchMenu.jsx.map