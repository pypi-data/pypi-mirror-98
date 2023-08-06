import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { update } from 'app/actionCreators/projects';
import { IconStar } from 'app/icons';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import withApi from 'app/utils/withApi';
var BookmarkStar = function (_a) {
    var api = _a.api, isBookmarkedProp = _a.isBookmarked, className = _a.className, organization = _a.organization, project = _a.project, onToggle = _a.onToggle;
    var isBookmarked = defined(isBookmarkedProp)
        ? isBookmarkedProp
        : project.isBookmarked;
    var toggleProjectBookmark = function (event) {
        update(api, {
            orgId: organization.slug,
            projectId: project.slug,
            data: { isBookmarked: !isBookmarked },
        }).catch(function () {
            addErrorMessage(t('Unable to toggle bookmark for %s', project.slug));
        });
        //needed to dismiss tooltip
        document.activeElement.blur();
        //prevent dropdowns from closing
        event.stopPropagation();
        if (onToggle) {
            onToggle(!isBookmarked);
        }
    };
    return (<Star isSolid isBookmarked={isBookmarked} onClick={toggleProjectBookmark} className={className}/>);
};
var Star = styled(IconStar, { shouldForwardProp: function (p) { return p !== 'isBookmarked'; } })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return (p.isBookmarked ? p.theme.yellow300 : p.theme.gray200); }, function (p) { return (p.isBookmarked ? p.theme.yellow200 : p.theme.gray300); });
export default withApi(BookmarkStar);
var templateObject_1;
//# sourceMappingURL=bookmarkStar.jsx.map