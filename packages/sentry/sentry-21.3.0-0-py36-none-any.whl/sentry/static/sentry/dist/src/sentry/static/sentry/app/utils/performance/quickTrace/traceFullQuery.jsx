import { __assign, __rest } from "tslib";
import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import { beforeFetch, getQuickTraceRequestPayload, makeEventView, } from 'app/utils/performance/quickTrace/utils';
import withApi from 'app/utils/withApi';
function EmptyTrace(_a) {
    var children = _a.children;
    return (<React.Fragment>
      {children({
        isLoading: false,
        error: null,
        trace: null,
        type: 'full',
    })}
    </React.Fragment>);
}
function TraceFullQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, children = _a.children, props = __rest(_a, ["traceId", "start", "end", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var eventView = makeEventView(start, end);
    return (<GenericDiscoverQuery route={"events-trace/" + traceId} getRequestPayload={getQuickTraceRequestPayload} beforeFetch={beforeFetch} eventView={eventView} {...props}>
      {function (_a) {
        var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
        return children(__assign({ 
            // This is using '||` instead of '??` here because
            // the client returns a empty string when the response
            // is 204. And we want the empty string, undefined and
            // null to be converted to null.
            trace: tableData || null, type: 'full' }, rest));
    }}
    </GenericDiscoverQuery>);
}
export default withApi(TraceFullQuery);
//# sourceMappingURL=traceFullQuery.jsx.map