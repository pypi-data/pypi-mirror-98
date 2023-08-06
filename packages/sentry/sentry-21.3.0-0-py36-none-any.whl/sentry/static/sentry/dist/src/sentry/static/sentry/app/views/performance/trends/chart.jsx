import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory, withRouter } from 'react-router';
import { withTheme } from 'emotion-theming';
import ChartZoom from 'app/components/charts/chartZoom';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import { decodeList, decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import { YAxis } from 'app/views/releases/detail/overview/chart/releaseChartControls';
import { generateTrendFunctionAsString, getCurrentTrendFunction, getCurrentTrendParameter, getUnselectedSeries, transformEventStatsSmoothed, trendToColor, } from './utils';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function transformEventStats(data, seriesName) {
    return [
        {
            seriesName: seriesName || 'Current',
            data: data.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return ({
                    name: timestamp * 1000,
                    value: countsForTimestamp.reduce(function (acc, _a) {
                        var count = _a.count;
                        return acc + count;
                    }, 0),
                });
            }),
        },
    ];
}
function getLegend(trendFunction) {
    return {
        right: 10,
        top: 0,
        itemGap: 12,
        align: 'left',
        data: [
            {
                name: 'Baseline',
                icon: 'path://M180 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z, M810 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40zm, M1440 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z',
            },
            {
                name: 'Releases',
                icon: 'line',
            },
            {
                name: trendFunction,
                icon: 'line',
            },
        ],
    };
}
function getIntervalLine(theme, series, intervalRatio, transaction) {
    if (!transaction || !series.length || !series[0].data || !series[0].data.length) {
        return [];
    }
    var seriesStart = parseInt(series[0].data[0].name, 0);
    var seriesEnd = parseInt(series[0].data.slice(-1)[0].name, 0);
    if (seriesEnd < seriesStart) {
        return [];
    }
    var periodLine = {
        data: [],
        color: theme.textColor,
        markLine: {
            data: [],
            label: {},
            lineStyle: {
                normal: {
                    color: theme.textColor,
                    type: 'dashed',
                    width: 1,
                },
            },
            symbol: ['none', 'none'],
            tooltip: {
                show: false,
            },
        },
        seriesName: 'Baseline',
    };
    var periodLineLabel = {
        fontSize: 11,
        show: true,
    };
    var previousPeriod = __assign(__assign({}, periodLine), { markLine: __assign({}, periodLine.markLine), seriesName: 'Baseline' });
    var currentPeriod = __assign(__assign({}, periodLine), { markLine: __assign({}, periodLine.markLine), seriesName: 'Baseline' });
    var periodDividingLine = __assign(__assign({}, periodLine), { markLine: __assign({}, periodLine.markLine), seriesName: 'Period split' });
    var seriesDiff = seriesEnd - seriesStart;
    var seriesLine = seriesDiff * intervalRatio + seriesStart;
    previousPeriod.markLine.data = [
        [
            { value: 'Past', coord: [seriesStart, transaction.aggregate_range_1] },
            { coord: [seriesLine, transaction.aggregate_range_1] },
        ],
    ];
    currentPeriod.markLine.data = [
        [
            { value: 'Present', coord: [seriesLine, transaction.aggregate_range_2] },
            { coord: [seriesEnd, transaction.aggregate_range_2] },
        ],
    ];
    periodDividingLine.markLine = {
        data: [
            {
                value: 'Previous Period / This Period',
                xAxis: seriesLine,
            },
        ],
        label: { show: false },
        lineStyle: {
            normal: {
                color: theme.textColor,
                type: 'solid',
                width: 2,
            },
        },
        symbol: ['none', 'none'],
        tooltip: {
            show: false,
        },
    };
    previousPeriod.markLine.label = __assign(__assign({}, periodLineLabel), { formatter: 'Past', position: 'insideStartBottom' });
    currentPeriod.markLine.label = __assign(__assign({}, periodLineLabel), { formatter: 'Present', position: 'insideEndBottom' });
    var additionalLineSeries = [previousPeriod, currentPeriod, periodDividingLine];
    return additionalLineSeries;
}
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var _a = _this.props, location = _a.location, trendChangeType = _a.trendChangeType;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var query = __assign({}, location.query);
            var queryKey = getUnselectedSeries(trendChangeType);
            query[queryKey] = unselected;
            var to = __assign(__assign({}, location), { query: query });
            browserHistory.push(to);
        };
        return _this;
    }
    Chart.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var props = this.props;
        var theme = props.theme, trendChangeType = props.trendChangeType, router = props.router, statsPeriod = props.statsPeriod, project = props.project, environment = props.environment, transaction = props.transaction, statsData = props.statsData, isLoading = props.isLoading, location = props.location, projects = props.projects;
        var lineColor = trendToColor[trendChangeType || ''];
        var events = statsData && (transaction === null || transaction === void 0 ? void 0 : transaction.project) && (transaction === null || transaction === void 0 ? void 0 : transaction.transaction)
            ? statsData[[transaction.project, transaction.transaction].join(',')]
            : undefined;
        var data = (_a = events === null || events === void 0 ? void 0 : events.data) !== null && _a !== void 0 ? _a : [];
        var trendFunction = getCurrentTrendFunction(location);
        var trendParameter = getCurrentTrendParameter(location);
        var chartLabel = generateTrendFunctionAsString(trendFunction.field, trendParameter.column);
        var results = transformEventStats(data, chartLabel);
        var _c = transformEventStatsSmoothed(results, chartLabel), smoothedResults = _c.smoothedResults, minValue = _c.minValue, maxValue = _c.maxValue;
        var start = props.start ? getUtcToLocalDateObject(props.start) : null;
        var end = props.end ? getUtcToLocalDateObject(props.end) : null;
        var utc = decodeScalar(router.location.query.utc) !== 'false';
        var seriesSelection = decodeList(location.query[getUnselectedSeries(trendChangeType)]).reduce(function (selection, metric) {
            selection[metric] = false;
            return selection;
        }, {});
        var legend = __assign(__assign({}, getLegend(chartLabel)), { selected: seriesSelection });
        var loading = isLoading;
        var reloading = isLoading;
        var transactionProject = parseInt(((_b = projects.find(function (_a) {
            var slug = _a.slug;
            return (transaction === null || transaction === void 0 ? void 0 : transaction.project) === slug;
        })) === null || _b === void 0 ? void 0 : _b.id) || '', 10);
        var yMax = Math.max(maxValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || 0, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || 0);
        var yMin = Math.min(minValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || Number.MAX_SAFE_INTEGER, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || Number.MAX_SAFE_INTEGER);
        var yDiff = yMax - yMin;
        var yMargin = yDiff * 0.1;
        var queryExtra = {
            showTransactions: trendChangeType,
            yAxis: YAxis.COUNT_DURATION,
        };
        var chartOptions = {
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return tooltipFormatter(value, seriesName);
                },
            },
            yAxis: {
                min: Math.max(0, yMin - yMargin),
                max: yMax + yMargin,
                axisLabel: {
                    color: theme.chartLabel,
                    // p50() coerces the axis to be time based
                    formatter: function (value) { return axisLabelFormatter(value, 'p50()'); },
                },
            },
        };
        return (<ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc}>
        {function (zoomRenderProps) {
            var smoothedSeries = smoothedResults
                ? smoothedResults.map(function (values) {
                    return __assign(__assign({}, values), { color: lineColor.default, lineStyle: {
                            opacity: 1,
                        } });
                })
                : [];
            var intervalSeries = getIntervalLine(theme, smoothedResults || [], 0.5, transaction);
            return (<ReleaseSeries start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc} projects={isNaN(transactionProject) ? project : [transactionProject]} environments={environment} memoized>
              {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return (<TransitionChart loading={loading} reloading={reloading}>
                  <TransparentLoadingMask visible={reloading}/>
                  {getDynamicText({
                    value: (<LineChart {...zoomRenderProps} {...chartOptions} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spread(smoothedSeries, releaseSeries, intervalSeries)} seriesOptions={{
                        showSymbol: false,
                    }} legend={legend} toolBox={{
                        show: false,
                    }} grid={{
                        left: '10px',
                        right: '10px',
                        top: '40px',
                        bottom: '0px',
                    }}/>),
                    fixed: 'Duration Chart',
                })}
                </TransitionChart>);
            }}
            </ReleaseSeries>);
        }}
      </ChartZoom>);
    };
    return Chart;
}(React.Component));
export default withTheme(withApi(withRouter(Chart)));
//# sourceMappingURL=chart.jsx.map