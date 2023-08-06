import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { bulkDelete, bulkUpdate } from 'app/actionCreators/group';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import ResolveActions from 'app/components/actions/resolve';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import { IconEllipsis, IconIssues } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { ResolutionStatus } from 'app/types';
import Projects from 'app/utils/projects';
import withApi from 'app/utils/withApi';
import ActionButton from '../actions/button';
import MenuItemActionLink from '../actions/menuItemActionLink';
var GroupRowActions = /** @class */ (function (_super) {
    __extends(GroupRowActions, _super);
    function GroupRowActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdate = function (data, event) {
            event === null || event === void 0 ? void 0 : event.stopPropagation();
            var _a = _this.props, api = _a.api, group = _a.group, orgId = _a.orgId, query = _a.query, selection = _a.selection, onMarkReviewed = _a.onMarkReviewed;
            addLoadingMessage(t('Saving changes\u2026'));
            if (data.inbox === false) {
                onMarkReviewed === null || onMarkReviewed === void 0 ? void 0 : onMarkReviewed([group.id]);
            }
            bulkUpdate(api, __assign({ orgId: orgId, itemIds: [group.id], data: data,
                query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                complete: function () {
                    clearIndicators();
                },
            });
        };
        _this.handleDelete = function () {
            var _a = _this.props, api = _a.api, group = _a.group, orgId = _a.orgId, query = _a.query, selection = _a.selection;
            addLoadingMessage(t('Removing events\u2026'));
            bulkDelete(api, __assign({ orgId: orgId, itemIds: [group.id], query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                complete: function () {
                    clearIndicators();
                },
            });
        };
        return _this;
    }
    GroupRowActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, orgId = _a.orgId, group = _a.group;
        return (<Wrapper>
        <ActionButton type="button" disabled={!group.inbox} title={t('Mark Reviewed')} tooltipProps={{ disabled: !group.inbox }} icon={<IconIssues size="sm"/>} onClick={function (event) { return _this.handleUpdate({ inbox: false }, event); }}/>

        <StyledDropdownLink caret={false} customTitle={<ActionButton label={t('More issue actions')} icon={<IconEllipsis size="sm"/>}/>} anchorRight>
          <MenuItemActionLink onAction={function () { return _this.handleUpdate({ status: ResolutionStatus.RESOLVED }); }} shouldConfirm={false} title={t('Resolve')}>
            {t('Resolve')}
          </MenuItemActionLink>

          <StyledMenuItem noAnchor>
            <Projects orgId={orgId} slugs={[group.project.slug]}>
              {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
            var project = projects[0];
            return (<ResolveActions hasRelease={project.hasOwnProperty('features')
                ? project.features.includes('releases')
                : false} latestRelease={project.hasOwnProperty('latestRelease')
                ? project.latestRelease
                : undefined} orgId={orgId} projectId={group.project.id} onUpdate={_this.handleUpdate} shouldConfirm={false} hasInbox disabled={!!fetchError} disableDropdown={!initiallyLoaded || !!fetchError} projectFetchError={!!fetchError}/>);
        }}
            </Projects>
          </StyledMenuItem>

          <MenuItemActionLink onAction={this.handleDelete} shouldConfirm={false} title={t('Delete')}>
            {t('Delete')}
          </MenuItemActionLink>
        </StyledDropdownLink>
      </Wrapper>);
    };
    return GroupRowActions;
}(React.Component));
var StyledMenuItem = styled(MenuItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n\n  & .dropdown-submenu {\n    & > .dropdown {\n      & > .dropdown-menu-right.dropdown-toggle {\n        color: ", ";\n        padding: ", ";\n      }\n      .dropdown-menu {\n        left: -150%;\n      }\n    }\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n\n  & .dropdown-submenu {\n    & > .dropdown {\n      & > .dropdown-menu-right.dropdown-toggle {\n        color: ", ";\n        padding: ", ";\n      }\n      .dropdown-menu {\n        left: -150%;\n      }\n    }\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.textColor; }, space(1));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  justify-content: space-between;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
export default withApi(GroupRowActions);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=groupRowActions.jsx.map