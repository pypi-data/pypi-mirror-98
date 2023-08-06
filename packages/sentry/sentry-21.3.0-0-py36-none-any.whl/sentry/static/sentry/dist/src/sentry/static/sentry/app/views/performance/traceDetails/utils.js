import { __assign } from "tslib";
import { reduceTrace } from 'app/utils/performance/quickTrace/utils';
export function getTraceDetailsUrl(organization, traceSlug, start, end, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/trace/" + traceSlug + "/",
        query: __assign(__assign({}, query), { start: start, end: end }),
    };
}
function traceVisitor() {
    var projectIds = new Set();
    var eventIds = new Set();
    return function (accumulator, event) {
        if (!projectIds.has(event.project_id)) {
            projectIds.add(event.project_id);
            accumulator.totalProjects += 1;
            // No user conditions yet, so all projects are relevant.
            accumulator.relevantProjects += 1;
        }
        if (!eventIds.has(event.event_id)) {
            eventIds.add(event.event_id);
            accumulator.totalTransactions += 1;
            // No user conditions yet, so all transactions are relevant.
            accumulator.relevantTransactions += 1;
        }
        if (accumulator.startTimestamp > event.start_timestamp) {
            accumulator.startTimestamp = event.start_timestamp;
        }
        if (accumulator.endTimestamp < event.timestamp) {
            accumulator.endTimestamp = event.timestamp;
        }
        if (accumulator.maxGeneration < event.generation) {
            accumulator.maxGeneration = event.generation;
        }
        return accumulator;
    };
}
export function getTraceInfo(trace) {
    return reduceTrace(trace, traceVisitor(), {
        totalProjects: 0,
        relevantProjects: 0,
        totalTransactions: 0,
        relevantTransactions: 0,
        startTimestamp: Number.MAX_SAFE_INTEGER,
        endTimestamp: 0,
        maxGeneration: 0,
    });
}
export { getDurationDisplay } from 'app/components/events/interfaces/spans/spanBar';
export { getHumanDuration, toPercent } from 'app/components/events/interfaces/spans/utils';
//# sourceMappingURL=utils.js.map