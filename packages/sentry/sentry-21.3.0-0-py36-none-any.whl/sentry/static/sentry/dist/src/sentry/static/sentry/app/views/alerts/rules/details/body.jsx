import { __extends, __makeTemplateObject, __rest, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import moment from 'moment';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import EventsRequest from 'app/components/charts/eventsRequest';
import { SectionHeading } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import DateTime from 'app/components/dateTime';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Duration from 'app/components/duration';
import * as Layout from 'app/components/layouts/thirds';
import { Panel, PanelBody, PanelFooter } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import TimeSince from 'app/components/timeSince';
import { IconCheckmark } from 'app/icons/iconCheckmark';
import { IconFire } from 'app/icons/iconFire';
import { IconWarning } from 'app/icons/iconWarning';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import Projects from 'app/utils/projects';
import Timeline from 'app/views/alerts/rules/details/timeline';
import { DATASET_EVENT_TYPE_FILTERS } from 'app/views/settings/incidentRules/constants';
import { makeDefaultCta } from 'app/views/settings/incidentRules/incidentRulePresets';
import { AlertRuleThresholdType, Dataset, } from 'app/views/settings/incidentRules/types';
import { extractEventTypeFilterFromRule } from 'app/views/settings/incidentRules/utils/getEventTypeFilter';
import { IncidentStatus } from '../../types';
import { DATA_SOURCE_LABELS, getIncidentRuleMetricPreset } from '../../utils';
import { API_INTERVAL_POINTS_LIMIT, TIME_OPTIONS } from './constants';
import MetricChart from './metricChart';
import RelatedIssues from './relatedIssues';
import RelatedTransactions from './relatedTransactions';
var DetailsBody = /** @class */ (function (_super) {
    __extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(DetailsBody.prototype, "metricPreset", {
        get: function () {
            var rule = this.props.rule;
            return rule ? getIncidentRuleMetricPreset(rule) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Return a string describing the threshold based on the threshold and the type
     */
    DetailsBody.prototype.getThresholdText = function (value, thresholdType, isAlert) {
        if (isAlert === void 0) { isAlert = false; }
        if (!defined(value) || !defined(thresholdType)) {
            return '';
        }
        var isAbove = thresholdType === AlertRuleThresholdType.ABOVE;
        var direction = isAbove === isAlert ? '>' : '<';
        return direction + " " + value;
    };
    DetailsBody.prototype.getInterval = function () {
        var _a = this.props, _b = _a.timePeriod, start = _b.start, end = _b.end, rule = _a.rule;
        var startDate = moment.utc(start);
        var endDate = moment.utc(end);
        var timeWindow = rule === null || rule === void 0 ? void 0 : rule.timeWindow;
        if (timeWindow &&
            endDate.diff(startDate) < API_INTERVAL_POINTS_LIMIT * timeWindow * 60 * 1000) {
            return timeWindow + "m";
        }
        return getInterval({ start: start, end: end }, true);
    };
    DetailsBody.prototype.calculateSummaryPercentages = function (incidents, startTime, endTime) {
        var e_1, _a;
        var startDate = moment.utc(startTime);
        var endDate = moment.utc(endTime);
        var totalTime = endDate.diff(startDate);
        var criticalPercent = '0';
        var warningPercent = '0';
        if (incidents) {
            var filteredIncidents = incidents.filter(function (incident) {
                return !incident.dateClosed || moment(incident.dateClosed).isAfter(startDate);
            });
            var criticalDuration = 0;
            var warningDuration = 0;
            try {
                for (var filteredIncidents_1 = __values(filteredIncidents), filteredIncidents_1_1 = filteredIncidents_1.next(); !filteredIncidents_1_1.done; filteredIncidents_1_1 = filteredIncidents_1.next()) {
                    var incident = filteredIncidents_1_1.value;
                    // use the larger of the start of the incident or the start of the time period
                    var incidentStart = moment.max(moment(incident.dateStarted), startDate);
                    var incidentClose = incident.dateClosed ? moment(incident.dateClosed) : endDate;
                    criticalDuration += incidentClose.diff(incidentStart);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (filteredIncidents_1_1 && !filteredIncidents_1_1.done && (_a = filteredIncidents_1.return)) _a.call(filteredIncidents_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            criticalPercent = ((criticalDuration / totalTime) * 100).toFixed(2);
            warningPercent = ((warningDuration / totalTime) * 100).toFixed(2);
        }
        var resolvedPercent = (100 -
            (Number(criticalPercent) + Number(warningPercent))).toFixed(2);
        return { criticalPercent: criticalPercent, warningPercent: warningPercent, resolvedPercent: resolvedPercent };
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var rule = this.props.rule;
        if (rule === undefined) {
            return <Placeholder height="200px"/>;
        }
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        return (<RuleDetails>
        <span>{t('Data Source')}</span>
        <span>{(rule === null || rule === void 0 ? void 0 : rule.dataset) && DATA_SOURCE_LABELS[rule === null || rule === void 0 ? void 0 : rule.dataset]}</span>

        <span>{t('Metric')}</span>
        <span>{rule === null || rule === void 0 ? void 0 : rule.aggregate}</span>

        <span>{t('Time Window')}</span>
        <span>{(rule === null || rule === void 0 ? void 0 : rule.timeWindow) && <Duration seconds={(rule === null || rule === void 0 ? void 0 : rule.timeWindow) * 60}/>}</span>

        {((rule === null || rule === void 0 ? void 0 : rule.dataset) || (rule === null || rule === void 0 ? void 0 : rule.query)) && (<React.Fragment>
            <span>{t('Filter')}</span>
            <span>
              {(rule === null || rule === void 0 ? void 0 : rule.dataset) && <code>{DATASET_EVENT_TYPE_FILTERS[rule.dataset]}</code>}
              {rule === null || rule === void 0 ? void 0 : rule.query}
            </span>
          </React.Fragment>)}

        <span>{t('Critical Trigger')}</span>
        <span>
          {this.getThresholdText(criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold, rule === null || rule === void 0 ? void 0 : rule.thresholdType, true)}
        </span>

        {defined(warningTrigger) && (<React.Fragment>
            <span>{t('Warning Trigger')}</span>
            <span>
              {this.getThresholdText(warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold, rule === null || rule === void 0 ? void 0 : rule.thresholdType, true)}
            </span>
          </React.Fragment>)}

        {defined(rule === null || rule === void 0 ? void 0 : rule.resolveThreshold) && (<React.Fragment>
            <span>{t('Resolution')}</span>
            <span>
              {this.getThresholdText(rule === null || rule === void 0 ? void 0 : rule.resolveThreshold, rule === null || rule === void 0 ? void 0 : rule.thresholdType)}
            </span>
          </React.Fragment>)}
      </RuleDetails>);
    };
    DetailsBody.prototype.renderSummaryStatItems = function (_a) {
        var criticalPercent = _a.criticalPercent, warningPercent = _a.warningPercent, resolvedPercent = _a.resolvedPercent;
        return (<React.Fragment>
        <StatItem>
          <IconCheckmark color="green300" isCircled/>
          <StatCount>{resolvedPercent}%</StatCount>
        </StatItem>
        <StatItem>
          <IconWarning color="yellow300"/>
          <StatCount>{warningPercent}%</StatCount>
        </StatItem>
        <StatItem>
          <IconFire color="red300"/>
          <StatCount>{criticalPercent}%</StatCount>
        </StatItem>
      </React.Fragment>);
    };
    DetailsBody.prototype.renderChartActions = function (projects) {
        var _a = this.props, rule = _a.rule, params = _a.params, incidents = _a.incidents, timePeriod = _a.timePeriod;
        var preset = this.metricPreset;
        var ctaOpts = {
            orgSlug: params.orgId,
            projects: projects,
            rule: rule,
            start: timePeriod.start,
            end: timePeriod.end,
        };
        var _b = preset
            ? preset.makeCtaParams(ctaOpts)
            : makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = __rest(_b, ["buttonText"]);
        var percentages = this.calculateSummaryPercentages(incidents, timePeriod.start, timePeriod.end);
        return (<ChartActions>
        <ChartSummary>
          <SummaryText>{t('SUMMARY')}</SummaryText>
          <SummaryStats>{this.renderSummaryStatItems(percentages)}</SummaryStats>
        </ChartSummary>
        <Feature features={['discover-basic']}>
          <Button size="small" disabled={!rule} {...props}>
            {buttonText}
          </Button>
        </Feature>
      </ChartActions>);
    };
    DetailsBody.prototype.renderMetricStatus = function () {
        var _a = this.props, incidents = _a.incidents, theme = _a.theme;
        // get current status
        var activeIncident = incidents === null || incidents === void 0 ? void 0 : incidents.find(function (_a) {
            var dateClosed = _a.dateClosed;
            return !dateClosed;
        });
        var status = activeIncident ? activeIncident.status : IncidentStatus.CLOSED;
        var statusText = t('Okay');
        var Icon = IconCheckmark;
        var color = theme.green300;
        if (status === IncidentStatus.CRITICAL) {
            statusText = t('Critical');
            Icon = IconFire;
            color = theme.red300;
        }
        else if (status === IncidentStatus.WARNING) {
            statusText = t('Warning');
            Icon = IconWarning;
            color = theme.yellow300;
        }
        var latestIncident = (incidents === null || incidents === void 0 ? void 0 : incidents.length) ? incidents[0] : null;
        // The date at which the alert was triggered or resolved
        var activityDate = activeIncident
            ? activeIncident.dateStarted
            : latestIncident
                ? latestIncident.dateClosed
                : null;
        return (<GroupedHeaderItems>
        <SidebarHeading>{t('Status')}</SidebarHeading>
        <SidebarHeading>
          {activeIncident ? t('Last Triggered') : t('Last Resolved')}
        </SidebarHeading>
        <ItemValue>
          <AlertBadge color={color} icon={Icon}>
            <AlertIconWrapper>
              <Icon color="white"/>
            </AlertIconWrapper>
          </AlertBadge>
          <IncidentStatusValue color={color}>{statusText}</IncidentStatusValue>
        </ItemValue>
        <ItemValue>{activityDate ? <TimeSince date={activityDate}/> : '-'}</ItemValue>
      </GroupedHeaderItems>);
    };
    DetailsBody.prototype.renderLoading = function () {
        return (<Layout.Body>
        <Layout.Main>
          <Placeholder height="38px"/>
          <ChartPanel>
            <PanelBody withPadding>
              <Placeholder height="200px"/>
            </PanelBody>
          </ChartPanel>
        </Layout.Main>
        <Layout.Side>
          <SidebarHeading>
            <span>{t('Alert Rule')}</span>
          </SidebarHeading>
          {this.renderRuleDetails()}
        </Layout.Side>
      </Layout.Body>);
    };
    DetailsBody.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, rule = _a.rule, incidents = _a.incidents, location = _a.location, organization = _a.organization, timePeriod = _a.timePeriod, orgId = _a.params.orgId;
        if (!rule) {
            return this.renderLoading();
        }
        var query = rule.query, environment = rule.environment, aggregate = rule.aggregate, projectSlugs = rule.projects, timeWindow = rule.timeWindow, triggers = rule.triggers;
        var criticalTrigger = triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var queryWithTypeFilter = (query + " " + extractEventTypeFilterFromRule(rule)).trim();
        return (<Projects orgId={orgId} slugs={projectSlugs}>
        {function (_a) {
            var _b, _c;
            var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
            return initiallyLoaded ? (<Layout.Body>
              <Layout.Main>
                <ChartControls>
                  <DropdownControl label={timePeriod.label}>
                    {TIME_OPTIONS.map(function (_a) {
                var label = _a.label, value = _a.value;
                return (<DropdownItem key={value} eventKey={value} onSelect={_this.props.handleTimePeriodChange}>
                        {label}
                      </DropdownItem>);
            })}
                  </DropdownControl>
                  {timePeriod.custom && (<StyledTimeRange>
                      <DateTime date={moment.utc(timePeriod.start)} timeAndDate/>
                      {' — '}
                      <DateTime date={moment.utc(timePeriod.end)} timeAndDate/>
                    </StyledTimeRange>)}
                </ChartControls>
                <ChartPanel>
                  <PanelBody withPadding>
                    <ChartHeader>
                      <PresetName>
                        {(_c = (_b = _this.metricPreset) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : t('Custom metric')}
                      </PresetName>
                      {tct(' [metric] over [window]', {
                metric: aggregate,
                window: <Duration seconds={timeWindow * 60}/>,
            })}
                    </ChartHeader>
                    <EventsRequest api={api} organization={organization} query={queryWithTypeFilter} environment={environment ? [environment] : undefined} project={projects.map(function (project) { return Number(project.id); })} interval={_this.getInterval()} start={timePeriod.start} end={timePeriod.end} yAxis={aggregate} includePrevious={false} currentSeriesName={aggregate}>
                      {function (_a) {
                var loading = _a.loading, timeseriesData = _a.timeseriesData;
                return !loading && timeseriesData ? (<MetricChart data={timeseriesData} ruleChangeThreshold={rule === null || rule === void 0 ? void 0 : rule.dateModified} incidents={incidents} criticalTrigger={criticalTrigger} warningTrigger={warningTrigger}/>) : (<Placeholder height="200px"/>);
            }}
                    </EventsRequest>
                  </PanelBody>
                  {_this.renderChartActions(projects)}
                </ChartPanel>
                <DetailWrapper>
                  <ActivityWrapper>
                    {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.ERRORS && (<RelatedIssues organization={organization} rule={rule} projects={(projects || []).filter(function (project) {
                return rule.projects.includes(project.slug);
            })} start={timePeriod.start} end={timePeriod.end} filter={queryWithTypeFilter}/>)}
                    {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.TRANSACTIONS && (<RelatedTransactions organization={organization} location={location} rule={rule} projects={(projects || []).filter(function (project) {
                return rule.projects.includes(project.slug);
            })} start={timePeriod.start} end={timePeriod.end} filter={DATASET_EVENT_TYPE_FILTERS[rule.dataset]}/>)}
                    <Timeline api={api} orgId={orgId} rule={rule} incidents={incidents}/>
                  </ActivityWrapper>
                </DetailWrapper>
              </Layout.Main>
              <Layout.Side>
                {_this.renderMetricStatus()}
                <SidebarHeading>
                  <span>{t('Alert Rule')}</span>
                </SidebarHeading>
                {_this.renderRuleDetails()}
              </Layout.Side>
            </Layout.Body>) : (<Placeholder height="200px"/>);
        }}
      </Projects>);
    };
    return DetailsBody;
}(React.Component));
var DetailWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ActivityWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"])));
var GroupedHeaderItems = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(1), space(4), space(1), space(4));
var ItemValue = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var IncidentStatusValue = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space(1.5), function (p) { return p.color; });
var AlertBadge = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.color; });
var AlertIconWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: absolute;\n"], ["\n  position: absolute;\n"])));
var SidebarHeading = styled(SectionHeading)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var ChartControls = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"])));
var StyledTimeRange = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(2));
var ChartPanel = styled(Panel)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var ChartHeader = styled('header')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  display: flex;\n  flex-direction: row;\n"], ["\n  margin-bottom: ", ";\n  display: flex;\n  flex-direction: row;\n"])), space(1));
var PresetName = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  text-transform: capitalize;\n  margin-right: ", ";\n"], ["\n  text-transform: capitalize;\n  margin-right: ", ";\n"])), space(0.5));
var ChartActions = styled(PanelFooter)(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"])), space(1));
var ChartSummary = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: flex;\n  margin-right: auto;\n"], ["\n  display: flex;\n  margin-right: auto;\n"])));
var SummaryText = styled('span')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  margin-top: ", ";\n  font-weight: bold;\n  font-size: ", ";\n"], ["\n  margin-top: ", ";\n  font-weight: bold;\n  font-size: ", ";\n"])), space(0.25), function (p) { return p.theme.fontSizeSmall; });
var SummaryStats = styled('div')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"])), space(2));
var StatItem = styled('div')(templateObject_18 || (templateObject_18 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"])), space(2));
var StatCount = styled('span')(templateObject_19 || (templateObject_19 = __makeTemplateObject(["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: black;\n"], ["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: black;\n"])), space(0.5), space(0.25));
var RuleDetails = styled('div')(templateObject_20 || (templateObject_20 = __makeTemplateObject(["\n  display: grid;\n  font-size: ", ";\n  grid-template-columns: auto max-content;\n  margin-bottom: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  & > span:nth-child(2n + 1) {\n    width: 125px;\n  }\n\n  & > span:nth-child(2n + 2) {\n    text-align: right;\n    width: 215px;\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n  }\n\n  & > span:nth-child(4n + 1),\n  & > span:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"], ["\n  display: grid;\n  font-size: ", ";\n  grid-template-columns: auto max-content;\n  margin-bottom: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  & > span:nth-child(2n + 1) {\n    width: 125px;\n  }\n\n  & > span:nth-child(2n + 2) {\n    text-align: right;\n    width: 215px;\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n  }\n\n  & > span:nth-child(4n + 1),\n  & > span:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space(2), space(0.5), space(1), function (p) { return p.theme.rowBackground; });
export default withTheme(DetailsBody);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19, templateObject_20;
//# sourceMappingURL=body.jsx.map