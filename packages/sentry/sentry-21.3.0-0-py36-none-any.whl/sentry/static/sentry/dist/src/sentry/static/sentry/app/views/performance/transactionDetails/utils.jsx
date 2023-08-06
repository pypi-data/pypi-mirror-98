import { __read, __spread } from "tslib";
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import EventView from 'app/utils/discover/eventView';
import { generateEventSlug } from 'app/utils/discover/urls';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { getTraceDetailsUrl } from '../traceDetails/utils';
import { getTransactionDetailsUrl } from '../utils';
export function generateSingleEventTarget(event, organization, location) {
    var eventSlug = generateEventSlug({
        id: event.event_id,
        project: event.project_slug,
    });
    return getTransactionDetailsUrl(organization, eventSlug, event.transaction, location.query);
}
export function generateMultiEventsTarget(currentEvent, events, organization, location, groupType) {
    if (events.length === 1) {
        return generateSingleEventTarget(events[0], organization, location);
    }
    var queryResults = new QueryResults([]);
    var eventIds = events.map(function (child) { return child.event_id; });
    for (var i = 0; i < eventIds.length; i++) {
        queryResults.addOp(i === 0 ? '(' : 'OR');
        queryResults.addQuery("id:" + eventIds[i]);
        if (i === eventIds.length - 1) {
            queryResults.addOp(')');
        }
    }
    var _a = getTraceDateTimeRange({
        start: currentEvent.startTimestamp,
        end: currentEvent.endTimestamp,
    }), start = _a.start, end = _a.end;
    var traceEventView = EventView.fromSavedQuery({
        id: undefined,
        name: groupType + " Transactions of Event ID " + currentEvent.id,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: stringifyQueryObject(queryResults),
        projects: __spread(new Set(events.map(function (child) { return child.project_id; }))),
        version: 2,
        start: start,
        end: end,
    });
    return traceEventView.getResultsViewUrlTarget(organization.slug);
}
export function generateTraceTarget(event, organization) {
    var _a, _b, _c;
    var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
    var _d = getTraceDateTimeRange({
        start: event.startTimestamp,
        end: event.endTimestamp,
    }), start = _d.start, end = _d.end;
    if (organization.features.includes('trace-view-summary')) {
        return getTraceDetailsUrl(organization, traceId, start, end, {});
    }
    var eventView = EventView.fromSavedQuery({
        id: undefined,
        name: "Transactions with Trace ID " + traceId,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: "event.type:transaction trace:" + traceId,
        projects: [ALL_ACCESS_PROJECTS],
        version: 2,
        start: start,
        end: end,
    });
    return eventView.getResultsViewUrlTarget(organization.slug);
}
//# sourceMappingURL=utils.jsx.map