import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import Duration from 'app/components/duration';
import ErrorBoundary from 'app/components/errorBoundary';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import { PanelItem } from 'app/components/panels';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getUtcDateString } from 'app/utils/dates';
import getDynamicText from 'app/utils/getDynamicText';
import theme from 'app/utils/theme';
import { API_INTERVAL_POINTS_LIMIT, API_INTERVAL_POINTS_MIN, } from '../rules/details/constants';
import { IncidentStatus } from '../types';
import { getIncidentMetricPreset, isIssueAlert } from '../utils';
import SparkLine from './sparkLine';
import { TableLayout, TitleAndSparkLine } from './styles';
/**
 * Retrieve the start/end for showing the graph of the metric
 * Will show at least 150 and no more than 10,000 data points
 */
export var makeRuleDetailsQuery = function (incident) {
    var timeWindow = incident.alertRule.timeWindow;
    var timeWindowMillis = timeWindow * 60 * 1000;
    var minRange = timeWindowMillis * API_INTERVAL_POINTS_MIN;
    var maxRange = timeWindowMillis * API_INTERVAL_POINTS_LIMIT;
    var now = moment.utc();
    var startDate = moment.utc(incident.dateStarted);
    // make a copy of now since we will modify endDate and use now for comparing
    var endDate = incident.dateClosed ? moment.utc(incident.dateClosed) : moment(now);
    var incidentRange = Math.max(endDate.diff(startDate), 3 * timeWindowMillis);
    var range = Math.min(maxRange, Math.max(minRange, incidentRange));
    var halfRange = moment.duration(range / 2);
    return {
        start: getUtcDateString(startDate.subtract(halfRange)),
        end: getUtcDateString(moment.min(endDate.add(halfRange), now)),
    };
};
var AlertListRow = /** @class */ (function (_super) {
    __extends(AlertListRow, _super);
    function AlertListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    Object.defineProperty(AlertListRow.prototype, "metricPreset", {
        get: function () {
            var incident = this.props.incident;
            return incident ? getIncidentMetricPreset(incident) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    AlertListRow.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, incident = _a.incident, filteredStatus = _a.filteredStatus;
        if (filteredStatus === 'open') {
            return [
                ['stats', "/organizations/" + orgId + "/incidents/" + incident.identifier + "/stats/"],
            ];
        }
        return [];
    };
    AlertListRow.prototype.renderLoading = function () {
        return this.renderBody();
    };
    AlertListRow.prototype.renderError = function () {
        return this.renderBody();
    };
    AlertListRow.prototype.renderTimeSince = function (date) {
        return (<CreatedResolvedTime>
        <TimeSince date={date}/>
      </CreatedResolvedTime>);
    };
    AlertListRow.prototype.renderStatusIndicator = function () {
        var status = this.props.incident.status;
        var isResolved = status === IncidentStatus.CLOSED;
        var isWarning = status === IncidentStatus.WARNING;
        var color = isResolved ? theme.gray200 : isWarning ? theme.orange300 : theme.red200;
        var text = isResolved ? t('Resolved') : isWarning ? t('Warning') : t('Critical');
        return (<Tooltip title={tct('Status: [text]', { text: text })}>
        <StatusIndicator color={color}/>
      </Tooltip>);
    };
    AlertListRow.prototype.renderBody = function () {
        var _a;
        var _b = this.props, incident = _b.incident, orgId = _b.orgId, projectsLoaded = _b.projectsLoaded, projects = _b.projects, filteredStatus = _b.filteredStatus, organization = _b.organization;
        var _c = this.state, error = _c.error, stats = _c.stats;
        var started = moment(incident.dateStarted);
        var duration = moment
            .duration(moment(incident.dateClosed || new Date()).diff(started))
            .as('seconds');
        var slug = incident.projects[0];
        var hasRedesign = incident.alertRule &&
            !isIssueAlert(incident.alertRule) &&
            organization.features.includes('alert-details-redesign');
        var alertLink = hasRedesign
            ? {
                pathname: "/organizations/" + orgId + "/alerts/rules/details/" + ((_a = incident.alertRule) === null || _a === void 0 ? void 0 : _a.id) + "/",
                query: makeRuleDetailsQuery(incident),
            }
            : {
                pathname: "/organizations/" + orgId + "/alerts/" + incident.identifier + "/",
            };
        return (<ErrorBoundary>
        <IncidentPanelItem>
          <TableLayout status={filteredStatus}>
            <TitleAndSparkLine status={filteredStatus}>
              <Title>
                {this.renderStatusIndicator()}
                <IncidentLink to={alertLink}>Alert #{incident.id}</IncidentLink>
                {incident.title}
              </Title>

              {filteredStatus === 'open' && (<SparkLine error={error && <ErrorLoadingStatsIcon />} eventStats={stats === null || stats === void 0 ? void 0 : stats.eventStats}/>)}
            </TitleAndSparkLine>

            <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>

            {this.renderTimeSince(incident.dateStarted)}

            {filteredStatus === 'closed' && (<Duration seconds={getDynamicText({ value: duration, fixed: 1200 })}/>)}

            {filteredStatus === 'closed' &&
            incident.dateClosed &&
            this.renderTimeSince(incident.dateClosed)}
          </TableLayout>
        </IncidentPanelItem>
      </ErrorBoundary>);
    };
    return AlertListRow;
}(AsyncComponent));
function ErrorLoadingStatsIcon() {
    return (<Tooltip title={t('Error loading alert stats')}>
      <IconWarning />
    </Tooltip>);
}
var CreatedResolvedTime = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n  line-height: 1.4;\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n  line-height: 1.4;\n  display: flex;\n  align-items: center;\n"])), overflowEllipsis);
var ProjectBadge = styled(IdBadge)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var StatusIndicator = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 10px;\n  height: 12px;\n  background: ", ";\n  display: inline-block;\n  border-top-right-radius: 40%;\n  border-bottom-right-radius: 40%;\n  margin-bottom: -1px;\n"], ["\n  width: 10px;\n  height: 12px;\n  background: ", ";\n  display: inline-block;\n  border-top-right-radius: 40%;\n  border-bottom-right-radius: 40%;\n  margin-bottom: -1px;\n"])), function (p) { return p.color; });
var Title = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var IncidentLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: 0 ", ";\n"], ["\n  padding: 0 ", ";\n"])), space(1));
var IncidentPanelItem = styled(PanelItem)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  padding: ", " ", " ", " 0;\n"], ["\n  font-size: ", ";\n  padding: ", " ", " ", " 0;\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1.5), space(2), space(1.5));
export default AlertListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=row.jsx.map