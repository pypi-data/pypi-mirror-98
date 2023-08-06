import React from 'react';
import { defined } from 'app/utils';
import Tag from './tag';
/**
 * Displays a number count. If `max` is specified, then give representation
 * of count, i.e. "1000+"
 *
 * Render nothing by default if `count` is falsy.
 */
var QueryCount = function (_a) {
    var count = _a.count, max = _a.max, _b = _a.hideIfEmpty, hideIfEmpty = _b === void 0 ? true : _b, _c = _a.hideParens, hideParens = _c === void 0 ? false : _c, _d = _a.isTag, isTag = _d === void 0 ? false : _d, _e = _a.tagProps, tagProps = _e === void 0 ? {} : _e;
    var countOrMax = defined(count) && defined(max) && count >= max ? max + "+" : count;
    if (hideIfEmpty && !count) {
        return null;
    }
    if (isTag) {
        return <Tag {...tagProps}>{countOrMax}</Tag>;
    }
    return (<span>
      {!hideParens && <span>(</span>}
      <span>{countOrMax}</span>
      {!hideParens && <span>)</span>}
    </span>);
};
export default QueryCount;
//# sourceMappingURL=queryCount.jsx.map