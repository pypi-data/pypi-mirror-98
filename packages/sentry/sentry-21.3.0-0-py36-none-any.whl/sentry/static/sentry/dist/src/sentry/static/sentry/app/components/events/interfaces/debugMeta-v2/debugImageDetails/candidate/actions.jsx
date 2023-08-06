import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Role from 'app/components/acl/role';
import Button from 'app/components/actions/button';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import DropdownLink from 'app/components/dropdownLink';
import NotAvailable from 'app/components/notAvailable';
import Tooltip from 'app/components/tooltip';
import { IconDownload, IconEllipsis } from 'app/icons';
import { t } from 'app/locale';
import { CandidateDownloadStatus } from 'app/types/debugImage';
function Actions(_a) {
    var candidate = _a.candidate, organization = _a.organization, baseUrl = _a.baseUrl, projectId = _a.projectId, isInternalSource = _a.isInternalSource, onDelete = _a.onDelete;
    var download = candidate.download, debugFileId = candidate.location;
    if (!debugFileId || isInternalSource) {
        return <NotAvailable />;
    }
    var status = download.status;
    var deleted = status === CandidateDownloadStatus.DELETED;
    var actions = (<StyledDropdownLink caret={false} customTitle={<Button label={t('Actions')} disabled={deleted} icon={<IconEllipsis size="sm"/>}/>} anchorRight>
      <Role role={organization.debugFilesRole} organization={organization}>
        {function (_a) {
        var hasRole = _a.hasRole;
        return (<Tooltip disabled={hasRole} title={t('You do not have permission to download debug files.')} containerDisplayMode="block">
            <MenuItemActionLink shouldConfirm={false} icon={<IconDownload size="xs"/>} title={t('Download')} href={baseUrl + "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugFileId} onClick={function (event) {
            if (deleted) {
                event.preventDefault();
            }
        }} disabled={!hasRole || deleted}>
              {t('Download')}
            </MenuItemActionLink>
          </Tooltip>);
    }}
      </Role>
      <Access access={['project:write']} organization={organization}>
        {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Tooltip disabled={hasAccess} title={t('You do not have permission to delete debug files.')} containerDisplayMode="block">
            <MenuItemActionLink onAction={function () { return onDelete(debugFileId); }} message={t('Are you sure you wish to delete this file?')} title={t('Delete')} disabled={!hasAccess || deleted} shouldConfirm>
              {t('Delete')}
            </MenuItemActionLink>
          </Tooltip>);
    }}
      </Access>
    </StyledDropdownLink>);
    if (!deleted) {
        return actions;
    }
    return <Tooltip title={t('Actions not available.')}>{actions}</Tooltip>;
}
export default Actions;
var StyledDropdownLink = styled(DropdownLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
var templateObject_1;
//# sourceMappingURL=actions.jsx.map