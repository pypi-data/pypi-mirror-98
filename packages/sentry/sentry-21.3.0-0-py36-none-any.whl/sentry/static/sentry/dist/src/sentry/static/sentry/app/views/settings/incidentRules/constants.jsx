var _a, _b;
import { __assign } from "tslib";
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import { DATA_SOURCE_TO_SET_AND_EVENT_TYPES, getQueryDatasource, } from 'app/views/alerts/utils';
import { AlertRuleThresholdType, Dataset, Datasource, EventTypes, } from 'app/views/settings/incidentRules/types';
export var DEFAULT_AGGREGATE = 'count()';
export var DATASET_EVENT_TYPE_FILTERS = (_a = {},
    _a[Dataset.ERRORS] = 'event.type:error',
    _a[Dataset.TRANSACTIONS] = 'event.type:transaction',
    _a);
export var DATASOURCE_EVENT_TYPE_FILTERS = (_b = {},
    _b[Datasource.ERROR_DEFAULT] = '(event.type:error OR event.type:default)',
    _b[Datasource.ERROR] = 'event.type:error',
    _b[Datasource.DEFAULT] = 'event.type:default',
    _b[Datasource.TRANSACTION] = 'event.type:transaction',
    _b);
/**
 * Allowed error aggregations for alerts
 */
export var errorFieldConfig = {
    aggregations: ['count', 'count_unique'],
    fields: ['user'],
};
/**
 * Allowed transaction aggregations for alerts
 */
export var transactionFieldConfig = {
    aggregations: [
        'avg',
        'percentile',
        'failure_rate',
        'apdex',
        'count',
        'p50',
        'p75',
        'p95',
        'p99',
        'p100',
    ],
    fields: ['transaction.duration'],
    measurementKeys: Object.keys(WEB_VITAL_DETAILS),
};
export function createDefaultTrigger(label) {
    return {
        label: label,
        alertThreshold: '',
        actions: [],
    };
}
export function createDefaultRule() {
    return {
        dataset: Dataset.ERRORS,
        eventTypes: [EventTypes.ERROR],
        aggregate: DEFAULT_AGGREGATE,
        query: '',
        timeWindow: 1,
        triggers: [createDefaultTrigger('critical'), createDefaultTrigger('warning')],
        projects: [],
        environment: null,
        resolveThreshold: '',
        thresholdType: AlertRuleThresholdType.ABOVE,
    };
}
/**
 * Create an unsaved alert from a discover EventView object
 */
export function createRuleFromEventView(eventView) {
    var _a;
    var parsedQuery = getQueryDatasource(eventView.query);
    var datasetAndEventtypes = parsedQuery
        ? DATA_SOURCE_TO_SET_AND_EVENT_TYPES[parsedQuery.source]
        : DATA_SOURCE_TO_SET_AND_EVENT_TYPES.error;
    return __assign(__assign(__assign({}, createDefaultRule()), datasetAndEventtypes), { query: (_a = parsedQuery === null || parsedQuery === void 0 ? void 0 : parsedQuery.query) !== null && _a !== void 0 ? _a : eventView.query, aggregate: eventView.getYAxis(), environment: eventView.environment.length ? eventView.environment[0] : null });
}
//# sourceMappingURL=constants.jsx.map