import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getShortEventId } from 'app/utils/events';
import { getDuration } from 'app/utils/formatters';
import { isTransaction } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import QuickTrace from './quickTrace';
import { MetaData } from './styles';
function EventMetas(_a) {
    var _b, _c, _d;
    var event = _a.event, organization = _a.organization, projectId = _a.projectId, location = _a.location, quickTrace = _a.quickTrace;
    if (!isTransaction(event)) {
        return null;
    }
    var projectBadge = (<Projects orgId={organization.slug} slugs={[projectId]}>
      {function (_a) {
        var projects = _a.projects;
        var project = projects.find(function (p) { return p.slug === projectId; });
        return (<ProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>);
    }}
    </Projects>);
    var timestamp = (<TimeSince date={event.dateCreated || (event.endTimestamp || 0) * 1000}/>);
    var httpStatus = <HttpStatus event={event}/>;
    return (<EventDetailHeader>
      <MetaData headingText={t('Event ID')} tooltipText={t('The unique ID assigned to this transaction.')} bodyText={getShortEventId(event.eventID)} subtext={projectBadge}/>
      <MetaData headingText={t('Total Duration')} tooltipText={t('The total time elapsed between the start and end of this transaction.')} bodyText={getDuration(event.endTimestamp - event.startTimestamp, 2, true)} subtext={timestamp}/>
      <MetaData headingText={t('Status')} tooltipText={t('The status of this transaction indicating if it succeeded or otherwise.')} bodyText={(_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.status) !== null && _d !== void 0 ? _d : '\u2014'} subtext={httpStatus}/>
      <QuickTraceContainer>
        <QuickTrace event={event} organization={organization} location={location} quickTrace={quickTrace}/>
      </QuickTraceContainer>
    </EventDetailHeader>);
}
var EventDetailHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n    margin-bottom: 0;\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[1]; });
var QuickTraceContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"], ["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
function HttpStatus(_a) {
    var event = _a.event;
    var tags = event.tags;
    var emptyStatus = <React.Fragment>{'\u2014'}</React.Fragment>;
    if (!Array.isArray(tags)) {
        return emptyStatus;
    }
    var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
    if (!tag) {
        return emptyStatus;
    }
    return <React.Fragment>HTTP {tag.value}</React.Fragment>;
}
export default EventMetas;
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventMetas.jsx.map