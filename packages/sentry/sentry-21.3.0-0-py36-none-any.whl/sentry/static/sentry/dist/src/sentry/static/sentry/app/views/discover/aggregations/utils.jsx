import { __read } from "tslib";
/**
 * Returns true if an aggregation is valid and false if not
 *
 * @param aggregation Aggregation in external Snuba format
 * @param cols List of column objects
 * @param cols.name Column name
 * @param cols.type Type of column
 * @returns True if valid aggregation, false if not
 */
export function isValidAggregation(aggregation, cols) {
    var columns = new Set(cols.map(function (_a) {
        var name = _a.name;
        return name;
    }));
    var _a = __read(aggregation, 2), func = _a[0], col = _a[1];
    if (!func) {
        return false;
    }
    if (func === 'count()') {
        return !col;
    }
    if (func === 'uniq') {
        return columns.has(col || '');
    }
    if (func === 'avg' || func === 'sum') {
        var validCols = new Set(cols.filter(function (_a) {
            var type = _a.type;
            return type === 'number';
        }).map(function (_a) {
            var name = _a.name;
            return name;
        }));
        return validCols.has(col || '');
    }
    return false;
}
//# sourceMappingURL=utils.jsx.map