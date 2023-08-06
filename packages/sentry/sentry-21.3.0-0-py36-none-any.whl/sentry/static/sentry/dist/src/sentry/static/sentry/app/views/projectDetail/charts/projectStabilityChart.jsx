import { __extends, __read, __spread } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { RELEASE_LINES_THRESHOLD } from 'app/components/charts/utils';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { displayCrashFreePercent } from 'app/views/releases/utils';
import { getSessionTermDescription, SessionTerm, } from 'app/views/releases/utils/sessionTerm';
import SessionsRequest from './sessionsRequest';
function ProjectStabilityChart(_a) {
    var theme = _a.theme, organization = _a.organization, router = _a.router, selection = _a.selection, api = _a.api, onTotalValuesChange = _a.onTotalValuesChange;
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
    return (<React.Fragment>
      {getDynamicText({
        value: (<ChartZoom router={router} period={period} start={start} end={end} utc={utc}>
            {function (zoomRenderProps) { return (<SessionsRequest api={api} selection={selection} organization={organization}>
                {function (_a) {
            var errored = _a.errored, loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData, totalSessions = _a.totalSessions;
            return (<ReleaseSeries utc={utc} period={period} start={start} end={end} projects={projects} environments={environments}>
                    {function (_a) {
                var releaseSeries = _a.releaseSeries;
                if (errored) {
                    return (<ErrorPanel>
                            <IconWarning color="gray300" size="lg"/>
                          </ErrorPanel>);
                }
                onTotalValuesChange(totalSessions);
                return (<TransitionChart loading={loading} reloading={reloading}>
                          <TransparentLoadingMask visible={reloading}/>

                          <HeaderTitleLegend>
                            {t('Crash Free Sessions')}
                            <QuestionTooltip size="sm" position="top" title={getSessionTermDescription(SessionTerm.STABILITY, null)}/>
                          </HeaderTitleLegend>

                          <Chart theme={theme} zoomRenderProps={zoomRenderProps} reloading={reloading} timeSeries={timeseriesData} previousTimeSeries={previousTimeseriesData
                    ? [previousTimeseriesData]
                    : undefined} releaseSeries={releaseSeries}/>
                        </TransitionChart>);
            }}
                  </ReleaseSeries>);
        }}
              </SessionsRequest>); }}
          </ChartZoom>),
        fixed: t('Crash Free Sessions Chart'),
    })}
    </React.Fragment>);
}
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        // inspired by app/components/charts/eventsChart.tsx@handleLegendSelectChanged
        _this.handleLegendSelectChanged = function (_a) {
            var selected = _a.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                state[key] = selected[key];
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.releaseSeries !== this.props.releaseSeries &&
            !nextProps.reloading &&
            !this.props.reloading) {
            return true;
        }
        if (this.props.reloading && !nextProps.reloading) {
            return true;
        }
        if (nextProps.timeSeries !== this.props.timeSeries) {
            return true;
        }
        return false;
    };
    Object.defineProperty(Chart.prototype, "legend", {
        get: function () {
            var _a;
            var _b, _c;
            var _d = this.props, theme = _d.theme, releaseSeries = _d.releaseSeries;
            var seriesSelection = this.state.seriesSelection;
            var hideReleasesByDefault = ((_c = (_b = releaseSeries[0]) === null || _b === void 0 ? void 0 : _b.markLine) === null || _c === void 0 ? void 0 : _c.data.length) >= RELEASE_LINES_THRESHOLD;
            var selected = Object.keys(seriesSelection).length === 0 && hideReleasesByDefault
                ? (_a = {}, _a[t('Releases')] = false, _a) : seriesSelection;
            return {
                right: 10,
                top: 0,
                icon: 'circle',
                itemHeight: 8,
                itemWidth: 8,
                itemGap: 12,
                align: 'left',
                textStyle: {
                    color: theme.textColor,
                    verticalAlign: 'top',
                    fontSize: 11,
                    fontFamily: theme.text.family,
                },
                data: [t('This Period'), t('Previous Period'), t('Releases')],
                selected: selected,
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Chart.prototype, "chartOptions", {
        get: function () {
            var theme = this.props.theme;
            return {
                colors: [theme.green300, theme.purple200],
                grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                seriesOptions: {
                    showSymbol: false,
                },
                tooltip: {
                    trigger: 'axis',
                    truncate: 80,
                    valueFormatter: function (value) {
                        if (value === null) {
                            return '\u2014';
                        }
                        return displayCrashFreePercent(value, 0, 3);
                    },
                },
                yAxis: {
                    axisLabel: {
                        color: theme.gray200,
                        formatter: function (value) { return displayCrashFreePercent(value); },
                    },
                    scale: true,
                    max: 100,
                },
            };
        },
        enumerable: false,
        configurable: true
    });
    Chart.prototype.render = function () {
        var _a = this.props, zoomRenderProps = _a.zoomRenderProps, timeSeries = _a.timeSeries, previousTimeSeries = _a.previousTimeSeries, releaseSeries = _a.releaseSeries;
        return (<LineChart {...zoomRenderProps} {...this.chartOptions} legend={this.legend} series={Array.isArray(releaseSeries) ? __spread(timeSeries, releaseSeries) : timeSeries} previousPeriod={previousTimeSeries} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>);
    };
    return Chart;
}(React.Component));
export default withGlobalSelection(withTheme(ProjectStabilityChart));
//# sourceMappingURL=projectStabilityChart.jsx.map