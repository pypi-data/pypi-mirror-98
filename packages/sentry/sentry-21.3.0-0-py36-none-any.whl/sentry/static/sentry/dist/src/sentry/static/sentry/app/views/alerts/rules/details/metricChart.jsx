import { __extends, __read, __spread } from "tslib";
import React from 'react';
import color from 'color';
import moment from 'moment';
import Graphic from 'app/components/charts/components/graphic';
import MarkLine from 'app/components/charts/components/markLine';
import LineChart from 'app/components/charts/lineChart';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var X_AXIS_BOUNDARY_GAP = 15;
var VERTICAL_PADDING = 22;
function createThresholdSeries(lineColor, threshold) {
    return {
        seriesName: 'Threshold Line',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: lineColor, type: 'dashed', width: 1 },
            data: [{ yAxis: threshold }],
        }),
        data: [],
    };
}
var MetricChart = /** @class */ (function (_super) {
    __extends(MetricChart, _super);
    function MetricChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
        };
        _this.ref = null;
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function () {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            if (ref && !_this.ref) {
                _this.ref = ref;
                _this.updateDimensions();
            }
            if (!ref) {
                _this.ref = null;
            }
        };
        _this.getRuleCreatedThresholdElements = function () {
            var _a = _this.state, height = _a.height, width = _a.width;
            var _b = _this.props, data = _b.data, ruleChangeThreshold = _b.ruleChangeThreshold;
            if (!data.length || !data[0].data.length) {
                return [];
            }
            var seriesData = data[0].data;
            var seriesStart = seriesData[0].name;
            var seriesEnd = seriesData[seriesData.length - 1].name;
            var ruleChanged = moment(ruleChangeThreshold).valueOf();
            if (ruleChanged < seriesStart) {
                return [];
            }
            var chartWidth = width - X_AXIS_BOUNDARY_GAP;
            var position = X_AXIS_BOUNDARY_GAP +
                Math.round((chartWidth * (ruleChanged - seriesStart)) / (seriesEnd - seriesStart));
            return [
                {
                    type: 'line',
                    draggable: false,
                    position: [position, 0],
                    shape: { y1: 0, y2: height - VERTICAL_PADDING, x1: 1, x2: 1 },
                    style: {
                        stroke: theme.gray200,
                    },
                },
                {
                    type: 'rect',
                    draggable: false,
                    position: [X_AXIS_BOUNDARY_GAP, 0],
                    shape: {
                        // +1 makes the gray area go midway onto the dashed line above
                        width: position - X_AXIS_BOUNDARY_GAP + 1,
                        height: height - VERTICAL_PADDING,
                    },
                    style: {
                        fill: color(theme.gray100).alpha(0.42).rgb().string(),
                    },
                    z: 100,
                },
            ];
        };
        return _this;
    }
    MetricChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, incidents = _a.incidents, warningTrigger = _a.warningTrigger, criticalTrigger = _a.criticalTrigger;
        var series = __spread(data);
        // Ensure series data appears above incident lines
        series[0].z = 100;
        var dataArr = data[0].data;
        var maxSeriesValue = dataArr.reduce(function (currMax, coord) { return Math.max(currMax, coord.value); }, 0);
        var firstPoint = Number(dataArr[0].name);
        var lastPoint = dataArr[dataArr.length - 1].name;
        var resolvedArea = {
            seriesName: 'Resolved Area',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.green300, type: 'solid', width: 4 },
                data: [[{ coord: [firstPoint, 0] }, { coord: [lastPoint, 0] }]],
            }),
            data: [],
        };
        series.push(resolvedArea);
        if (incidents) {
            // select incidents that fall within the graph range
            var periodStart_1 = moment.utc(firstPoint);
            var filteredIncidents = incidents.filter(function (incident) {
                return !incident.dateClosed || moment(incident.dateClosed).isAfter(periodStart_1);
            });
            var criticalLines = filteredIncidents.map(function (incident) {
                var detectTime = Math.max(moment(incident.dateStarted).valueOf(), firstPoint);
                var resolveTime;
                if (incident.dateClosed) {
                    resolveTime = moment(incident.dateClosed).valueOf();
                }
                else {
                    resolveTime = lastPoint;
                }
                return [{ coord: [detectTime, 0] }, { coord: [resolveTime, 0] }];
            });
            var criticalArea = {
                seriesName: 'Critical Area',
                type: 'line',
                markLine: MarkLine({
                    silent: true,
                    lineStyle: { color: theme.red300, type: 'solid', width: 4 },
                    data: criticalLines,
                }),
                data: [],
            };
            series.push(criticalArea);
            var incidentValueMap_1 = {};
            var incidentLines = filteredIncidents.map(function (_a) {
                var dateStarted = _a.dateStarted, identifier = _a.identifier;
                var incidentStart = moment(dateStarted).valueOf();
                incidentValueMap_1[incidentStart] = identifier;
                return { xAxis: incidentStart };
            });
            var incidentLinesSeries = {
                seriesName: 'Incident Line',
                type: 'line',
                markLine: MarkLine({
                    silent: true,
                    lineStyle: { color: theme.red300, type: 'solid' },
                    data: incidentLines,
                    label: {
                        show: true,
                        position: 'insideEndBottom',
                        formatter: function (_a) {
                            var _b;
                            var value = _a.value;
                            return (_b = incidentValueMap_1[value]) !== null && _b !== void 0 ? _b : '-';
                        },
                        color: theme.red300,
                        fontSize: 10,
                    },
                }),
                data: [],
            };
            series.push(incidentLinesSeries);
        }
        var maxThresholdValue = 0;
        if (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) {
            var alertThreshold = warningTrigger.alertThreshold;
            var warningThresholdLine = createThresholdSeries(theme.yellow300, alertThreshold);
            series.push(warningThresholdLine);
            maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
        }
        if (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) {
            var alertThreshold = criticalTrigger.alertThreshold;
            var criticalThresholdLine = createThresholdSeries(theme.red300, alertThreshold);
            series.push(criticalThresholdLine);
            maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
        }
        return (<LineChart isGroupedByDate showTimeInTooltip forwardedRef={this.handleRef} grid={{
            left: 0,
            right: 0,
            top: space(2),
            bottom: 0,
        }} yAxis={maxThresholdValue > maxSeriesValue ? { max: maxThresholdValue } : undefined} series={series} graphic={Graphic({
            elements: this.getRuleCreatedThresholdElements(),
        })} onFinished={function () {
            // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
            // any graphics related to the triggers (e.g. the threshold areas + boundaries)
            _this.updateDimensions();
        }}/>);
    };
    return MetricChart;
}(React.PureComponent));
export default MetricChart;
//# sourceMappingURL=metricChart.jsx.map