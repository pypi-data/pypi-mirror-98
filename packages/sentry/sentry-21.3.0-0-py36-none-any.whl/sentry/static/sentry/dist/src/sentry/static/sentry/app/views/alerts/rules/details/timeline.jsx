import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment-timezone';
import { fetchIncidentActivities } from 'app/actionCreators/incident';
import DateTime from 'app/components/dateTime';
import Duration from 'app/components/duration';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import NavTabs from 'app/components/navTabs';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SeenByList from 'app/components/seenByList';
import TimeSince from 'app/components/timeSince';
import { IconCheckmark, IconEllipse, IconFire, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { getTriggerName } from 'app/views/alerts/details/activity/statusItem';
import { IncidentActivityType, IncidentStatus, IncidentStatusMethod, } from 'app/views/alerts/types';
var TimelineIncident = /** @class */ (function (_super) {
    __extends(TimelineIncident, _super);
    function TimelineIncident() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            activities: null,
        };
        return _this;
    }
    TimelineIncident.prototype.componentDidMount = function () {
        this.fetchData();
    };
    TimelineIncident.prototype.componentDidUpdate = function (prevProps) {
        // Only refetch if incidentStatus changes.
        //
        // This component can mount before incident details is fully loaded.
        // In which case, `incidentStatus` is null and we will be fetching via `cDM`
        // There's no need to fetch this gets updated due to incident details being loaded
        if (prevProps.incident.status !== null &&
            prevProps.incident.status !== this.props.incident.status) {
            this.fetchData();
        }
    };
    TimelineIncident.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, orgId, incident, activities, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, incident = _a.incident;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchIncidentActivities(api, orgId, incident.identifier)];
                    case 2:
                        activities = _b.sent();
                        this.setState({ activities: activities, loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        this.setState({ loading: false, error: !!err_1 });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    TimelineIncident.prototype.renderActivity = function (activity, idx) {
        var _a, _b;
        var _c = this.props, incident = _c.incident, rule = _c.rule;
        var activities = this.state.activities;
        var last = this.state.activities && idx === this.state.activities.length - 1;
        var authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
        var isDetected = activity.type === IncidentActivityType.DETECTED;
        var isStarted = activity.type === IncidentActivityType.STARTED;
        var isClosed = activity.type === IncidentActivityType.STATUS_CHANGE &&
            activity.value === "" + IncidentStatus.CLOSED;
        var isTriggerChange = activity.type === IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if ((!isStarted && !isDetected && !isClosed && !isTriggerChange) ||
            !activities ||
            !activities.length) {
            return null;
        }
        var currentTrigger = getTriggerName(activity.value);
        var title;
        var subtext;
        if (isTriggerChange) {
            var nextActivity = activities.find(function (_a) {
                var previousValue = _a.previousValue;
                return previousValue === activity.value;
            }) ||
                (activity.value &&
                    activity.value === "" + IncidentStatus.OPENED &&
                    activities.find(function (_a) {
                        var type = _a.type;
                        return type === IncidentActivityType.DETECTED;
                    }));
            var activityDuration = (nextActivity
                ? moment(nextActivity.dateCreated)
                : moment()).diff(moment(activity.dateCreated), 'milliseconds');
            title = t('Alert status changed');
            subtext =
                activityDuration !== null &&
                    tct("[currentTrigger]: [duration]", {
                        currentTrigger: currentTrigger,
                        duration: <Duration abbreviation seconds={activityDuration / 1000}/>,
                    });
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === IncidentStatusMethod.RULE_UPDATED) {
            title = t('Alert auto-resolved');
            subtext = t('Alert rule has been modified or deleted');
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== IncidentStatusMethod.RULE_UPDATED) {
            title = t('Alert resolved');
            subtext = tct('by [authorName]', { authorName: authorName });
        }
        else if (isDetected) {
            title = (incident === null || incident === void 0 ? void 0 : incident.alertRule) ? t('Alert was created')
                : tct('[authorName] created an alert', { authorName: authorName });
            subtext = <DateTime timeOnly date={activity.dateCreated}/>;
        }
        else if (isStarted) {
            var dateEnded = moment(activity.dateCreated)
                .add(rule.timeWindow, 'minutes')
                .utc()
                .format();
            var timeOnly = Boolean(dateEnded && moment(activity.dateCreated).date() === moment(dateEnded).date());
            title = t('Trigger conditions were met');
            subtext = (<React.Fragment>
          <DateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={activity.dateCreated}/>
          {' — '}
          <DateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
        </React.Fragment>);
        }
        else {
            return null;
        }
        return (<Activity key={activity.id}>
        <ActivityTrack>
          <IconEllipse size="sm" color="gray300"/>
          {!last && <VerticalDivider />}
        </ActivityTrack>

        <ActivityBody>
          <ActivityTime>
            <StyledTimeSince date={activity.dateCreated} suffix={t('ago')}/>
            <HorizontalDivider />
          </ActivityTime>
          <ActivityText>
            {title}
            {subtext && <ActivitySubText>{subtext}</ActivitySubText>}
          </ActivityText>
        </ActivityBody>
      </Activity>);
    };
    TimelineIncident.prototype.render = function () {
        var _this = this;
        var incident = this.props.incident;
        var activities = this.state.activities;
        var Icon = IconCheckmark;
        var color = theme.green300;
        if (
        // incident was at max critical
        activities === null || 
        // incident was at max critical
        activities === void 0 ? void 0 : 
        // incident was at max critical
        activities.find(function (_a) {
            var type = _a.type, value = _a.value;
            return type === IncidentActivityType.STATUS_CHANGE &&
                value === "" + IncidentStatus.CRITICAL;
        })) {
            Icon = IconFire;
            color = theme.red300;
        }
        else if (
        // incident was at max warning
        activities === null || 
        // incident was at max warning
        activities === void 0 ? void 0 : 
        // incident was at max warning
        activities.find(function (_a) {
            var type = _a.type, value = _a.value;
            return type === IncidentActivityType.STATUS_CHANGE &&
                value === "" + IncidentStatus.WARNING;
        })) {
            Icon = IconWarning;
            color = theme.yellow300;
        }
        return (<StyledNavTabs key={incident.identifier}>
        <IncidentHeader>
          <AlertBadge color={color} icon={Icon}>
            <IconWrapper>
              <Icon color="white" size="xs"/>
            </IconWrapper>
          </AlertBadge>
          <li>{tct('Alert #[id]', { id: incident.identifier })}</li>
          <SeenByTab>
            {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={t('People who have viewed this alert')}/>)}
          </SeenByTab>
        </IncidentHeader>
        {activities && (<IncidentBody>
            {activities
            .filter(function (activity) { return activity.type !== IncidentActivityType.COMMENT; })
            .map(function (activity, idx) { return _this.renderActivity(activity, idx); })}
          </IncidentBody>)}
      </StyledNavTabs>);
    };
    return TimelineIncident;
}(React.Component));
var Timeline = /** @class */ (function (_super) {
    __extends(Timeline, _super);
    function Timeline() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<EmptyStateWarning small withIcon={false}>
        {t('No alerts have been triggered yet')}
      </EmptyStateWarning>);
        };
        return _this;
    }
    Timeline.prototype.render = function () {
        var _a = this.props, api = _a.api, incidents = _a.incidents, orgId = _a.orgId, rule = _a.rule;
        return (<Panel>
        <PanelHeader>{t('Timeline')}</PanelHeader>
        <PanelBody>
          {incidents && rule && incidents.length
            ? incidents.map(function (incident) { return (<TimelineIncident key={incident.identifier} api={api} orgId={orgId} incident={incident} rule={rule}/>); })
            : this.renderEmptyMessage()}
        </PanelBody>
      </Panel>);
    };
    return Timeline;
}(React.Component));
export default Timeline;
var StyledNavTabs = styled(NavTabs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  margin: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  margin: ", ";\n"])), space(2));
var IncidentHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var AlertBadge = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  margin-right: ", ";\n\n  &:before {\n    content: '';\n    width: 16px;\n    height: 16px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  margin-right: ", ";\n\n  &:before {\n    content: '';\n    width: 16px;\n    height: 16px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, space(1.5), function (p) { return p.theme.borderRadius; }, function (p) { return p.color; });
var IconWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n"], ["\n  position: absolute;\n"])));
var SeenByTab = styled('li')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"], ["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"])), space(2));
var StyledSeenByList = styled(SeenByList)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var IncidentBody = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Activity = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var ActivityTrack = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n"])), space(1.5));
var ActivityBody = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"], ["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"])));
var ActivityTime = styled('li')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; }, space(0.75));
var StyledTimeSince = styled(TimeSince)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ActivityText = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  flex-direction: row;\n  margin-bottom: ", ";\n"], ["\n  flex-direction: row;\n  margin-bottom: ", ";\n"])), space(1.5));
var ActivitySubText = styled('span')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5));
var HorizontalDivider = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"], ["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"])), function (p) { return p.theme.innerBorder; });
var VerticalDivider = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"], ["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"])), function (p) { return p.theme.innerBorder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=timeline.jsx.map