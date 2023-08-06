import { __assign, __rest } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import TraceFullQuery from 'app/utils/performance/quickTrace/traceFullQuery';
import TraceLiteQuery from 'app/utils/performance/quickTrace/traceLiteQuery';
import { flattenRelevantPaths, isTransaction, } from 'app/utils/performance/quickTrace/utils';
export default function QuickTraceQuery(_a) {
    var _b, _c;
    var children = _a.children, event = _a.event, props = __rest(_a, ["children", "event"]);
    var traceId = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    // non transaction events are currently unsupported
    if (!isTransaction(event) || !traceId) {
        return (<React.Fragment>
        {children({
            isLoading: false,
            error: null,
            trace: [],
            type: 'empty',
        })}
      </React.Fragment>);
    }
    var _d = getTraceDateTimeRange({
        start: event.startTimestamp,
        end: event.endTimestamp,
    }), start = _d.start, end = _d.end;
    return (<TraceLiteQuery eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
      {function (traceLiteResults) { return (<TraceFullQuery traceId={traceId} start={start} end={end} {...props}>
          {function (traceFullResults) {
        var _a;
        if (!traceFullResults.isLoading &&
            traceFullResults.error === null &&
            traceFullResults.trace !== null) {
            try {
                var trace = flattenRelevantPaths(event, traceFullResults.trace);
                return children(__assign(__assign({}, traceFullResults), { trace: trace }));
            }
            catch (error) {
                Sentry.setTag('current.trace_id', traceId);
                Sentry.captureException(error);
            }
        }
        if (!traceLiteResults.isLoading &&
            traceLiteResults.error === null &&
            traceLiteResults.trace !== null) {
            return children(traceLiteResults);
        }
        return children({
            isLoading: traceFullResults.isLoading || traceLiteResults.isLoading,
            error: (_a = traceFullResults.error) !== null && _a !== void 0 ? _a : traceLiteResults.error,
            trace: [],
            type: 'empty',
        });
    }}
        </TraceFullQuery>); }}
    </TraceLiteQuery>);
}
//# sourceMappingURL=quickTraceQuery.jsx.map