import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import EventAttachmentActions from 'app/components/events/eventAttachmentActions';
import FileSize from 'app/components/fileSize';
import Link from 'app/components/links/link';
import { t } from 'app/locale';
import AttachmentUrl from 'app/utils/attachmentUrl';
import { types } from 'app/views/organizationGroupDetails/groupEventAttachments/types';
var GroupEventAttachmentsTableRow = function (_a) {
    var attachment = _a.attachment, projectId = _a.projectId, onDelete = _a.onDelete, isDeleted = _a.isDeleted, orgId = _a.orgId, groupId = _a.groupId;
    return (<TableRow isDeleted={isDeleted}>
    <td>
      <h5>
        {attachment.name}
        <br />
        <small>
          <DateTime date={attachment.dateCreated}/> &middot;{' '}
          <Link to={"/organizations/" + orgId + "/issues/" + groupId + "/events/" + attachment.event_id + "/"}>
            {attachment.event_id}
          </Link>
        </small>
      </h5>
    </td>

    <td>{types[attachment.type] || t('Other')}</td>

    <td>
      <FileSize bytes={attachment.size}/>
    </td>

    <td>
      <ActionsWrapper>
        <AttachmentUrl projectId={projectId} eventId={attachment.event_id} attachment={attachment}>
          {function (url) {
        return !isDeleted && (<EventAttachmentActions url={url} onDelete={onDelete} attachmentId={attachment.id}/>);
    }}
        </AttachmentUrl>
      </ActionsWrapper>
    </td>
  </TableRow>);
};
var TableRow = styled('tr')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  opacity: ", ";\n  td {\n    text-decoration: ", ";\n  }\n"], ["\n  opacity: ", ";\n  td {\n    text-decoration: ", ";\n  }\n"])), function (p) { return (p.isDeleted ? 0.3 : 1); }, function (p) { return (p.isDeleted ? 'line-through' : 'normal'); });
var ActionsWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n"], ["\n  display: inline-block;\n"])));
export default GroupEventAttachmentsTableRow;
var templateObject_1, templateObject_2;
//# sourceMappingURL=groupEventAttachmentsTableRow.jsx.map