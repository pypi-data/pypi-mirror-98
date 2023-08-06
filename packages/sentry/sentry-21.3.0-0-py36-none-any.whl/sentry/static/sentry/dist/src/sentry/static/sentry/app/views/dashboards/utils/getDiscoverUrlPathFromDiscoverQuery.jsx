import { __read, __spread } from "tslib";
import * as qs from 'query-string';
export function getDiscover2UrlPathFromDiscoverQuery(_a) {
    var _b;
    var organization = _a.organization, selection = _a.selection, d1Query = _a.query;
    var d2Query = {
        name: d1Query.name,
        field: __spread(['title'], d1Query.fields),
        sort: d1Query.orderby,
        statsPeriod: (_b = selection === null || selection === void 0 ? void 0 : selection.datetime) === null || _b === void 0 ? void 0 : _b.period,
        query: '',
    };
    var queryQueries = (d1Query.conditions || []).map(function (c) {
        var tag = c[0] || '';
        var val = c[2] || '';
        var operator = c[1] || '';
        var isNot = operator.includes('!') || operator.includes('NOT');
        var isNull = operator.includes('NULL');
        var isLike = operator.includes('LIKE') || operator.includes('*');
        var hasSpace = val.includes(' ');
        // Put condition into the columns
        if (!d2Query.field.includes(tag)) {
            d2Query.field.push(tag);
        }
        // Build the query
        var q = [];
        if (isNot) {
            q.push('!');
        }
        q.push(tag);
        q.push(':');
        // Quote open
        if (isNull || hasSpace) {
            q.push('"');
        }
        // Wildcard open
        if (isLike) {
            q.push('*');
        }
        q.push(val);
        // Wildcard close
        if (isLike) {
            q.push('*');
        }
        // Quote close
        if (isNull || hasSpace) {
            q.push('"');
        }
        return q.join('');
    });
    d2Query.field.push('count()');
    d2Query.query = queryQueries.join(' ');
    return "/organizations/" + organization.slug + "/discover/results/?" + qs.stringify(d2Query);
}
//# sourceMappingURL=getDiscoverUrlPathFromDiscoverQuery.jsx.map