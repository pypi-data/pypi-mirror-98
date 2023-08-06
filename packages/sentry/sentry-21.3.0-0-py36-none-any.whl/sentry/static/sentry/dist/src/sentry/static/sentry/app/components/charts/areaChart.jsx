import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import AreaSeries from './series/areaSeries';
import BaseChart from './baseChart';
var AreaChart = /** @class */ (function (_super) {
    __extends(AreaChart, _super);
    function AreaChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AreaChart.prototype.render = function () {
        var _a = this.props, series = _a.series, stacked = _a.stacked, colors = _a.colors, props = __rest(_a, ["series", "stacked", "colors"]);
        return (<BaseChart {...props} colors={colors} series={series.map(function (_a, i) {
            var seriesName = _a.seriesName, data = _a.data, otherSeriesProps = __rest(_a, ["seriesName", "data"]);
            return AreaSeries(__assign({ stack: stacked ? 'area' : undefined, name: seriesName, data: data.map(function (_a) {
                    var name = _a.name, value = _a.value;
                    return [name, value];
                }), lineStyle: {
                    color: colors === null || colors === void 0 ? void 0 : colors[i],
                    opacity: 1,
                    width: 0.4,
                }, areaStyle: {
                    color: colors === null || colors === void 0 ? void 0 : colors[i],
                    opacity: 1.0,
                }, animation: false, animationThreshold: 1, animationDuration: 0 }, otherSeriesProps));
        })}/>);
    };
    return AreaChart;
}(React.Component));
export default AreaChart;
//# sourceMappingURL=areaChart.jsx.map