import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import pick from 'lodash/pick';
import AsyncComponent from 'app/components/asyncComponent';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import TimeSince from 'app/components/timeSince';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconCheckmark, IconFire, IconOpen, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { IncidentStatus } from '../alerts/types';
import MissingAlertsButtons from './missingFeatureButtons/missingAlertsButtons';
import { SectionHeadingLink, SectionHeadingWrapper, SidebarSection } from './styles';
import { didProjectOrEnvironmentChange } from './utils';
var PLACEHOLDER_AND_EMPTY_HEIGHT = '172px';
var ProjectLatestAlerts = /** @class */ (function (_super) {
    __extends(ProjectLatestAlerts, _super);
    function ProjectLatestAlerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderAlertRow = function (alert) {
            var _a = _this.props, organization = _a.organization, theme = _a.theme;
            var status = alert.status, id = alert.id, identifier = alert.identifier, title = alert.title, dateClosed = alert.dateClosed, dateStarted = alert.dateStarted;
            var isResolved = status === IncidentStatus.CLOSED;
            var isWarning = status === IncidentStatus.WARNING;
            var color = isResolved
                ? theme.green300
                : isWarning
                    ? theme.yellow300
                    : theme.red300;
            var Icon = isResolved ? IconCheckmark : isWarning ? IconWarning : IconFire;
            return (<AlertRowLink to={"/organizations/" + organization.slug + "/alerts/" + identifier + "/"} key={id}>
        <AlertBadge color={color} icon={Icon}>
          <AlertIconWrapper>
            <Icon color="white"/>
          </AlertIconWrapper>
        </AlertBadge>
        <AlertDetails>
          <AlertTitle>{title}</AlertTitle>
          <AlertDate color={color}>
            {isResolved
                ? tct('Resolved [date]', {
                    date: dateClosed ? <TimeSince date={dateClosed}/> : null,
                })
                : tct('Triggered [date]', { date: <TimeSince date={dateStarted}/> })}
          </AlertDate>
        </AlertDetails>
      </AlertRowLink>);
        };
        return _this;
    }
    ProjectLatestAlerts.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        // TODO(project-detail): we temporarily removed refetching based on timeselector
        if (this.state !== nextState ||
            didProjectOrEnvironmentChange(location, nextProps.location) ||
            isProjectStabilized !== nextProps.isProjectStabilized) {
            return true;
        }
        return false;
    };
    ProjectLatestAlerts.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        if (didProjectOrEnvironmentChange(prevProps.location, location) ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectLatestAlerts.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, isProjectStabilized = _a.isProjectStabilized;
        if (!isProjectStabilized) {
            return [];
        }
        var query = __assign(__assign({}, pick(location.query, Object.values(URL_PARAM))), { per_page: 3 });
        // we are listing 3 alerts total, first unresolved and then we fill with resolved
        return [
            [
                'unresolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: __assign(__assign({}, query), { status: 'open' }) },
            ],
            [
                'resolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: __assign(__assign({}, query), { status: 'closed' }) },
            ],
        ];
    };
    /**
     * If our alerts are empty, determine if we've configured alert rules (empty message differs then)
     */
    ProjectLatestAlerts.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, unresolvedAlerts, resolvedAlerts, _b, location, organization, isProjectStabilized, alertRules;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.state, unresolvedAlerts = _a.unresolvedAlerts, resolvedAlerts = _a.resolvedAlerts;
                        _b = this.props, location = _b.location, organization = _b.organization, isProjectStabilized = _b.isProjectStabilized;
                        if (!isProjectStabilized) {
                            return [2 /*return*/];
                        }
                        if (__spread((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []), (resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : [])).length !== 0) {
                            this.setState({ hasAlertRule: true });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/alert-rules/", {
                                method: 'GET',
                                query: __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM)))), { per_page: 1 }),
                            })];
                    case 1:
                        alertRules = _c.sent();
                        this.setState({ hasAlertRule: alertRules.length > 0, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(ProjectLatestAlerts.prototype, "alertsLink", {
        get: function () {
            var organization = this.props.organization;
            // as this is a link to latest alerts, we want to only preserve project and environment
            return {
                pathname: "/organizations/" + organization.slug + "/alerts/",
                query: {
                    statsPeriod: undefined,
                    start: undefined,
                    end: undefined,
                    utc: undefined,
                },
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectLatestAlerts.prototype.renderInnerBody = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug, isProjectStabilized = _a.isProjectStabilized;
        var _b = this.state, loading = _b.loading, unresolvedAlerts = _b.unresolvedAlerts, resolvedAlerts = _b.resolvedAlerts, hasAlertRule = _b.hasAlertRule;
        var alertsUnresolvedAndResolved = __spread((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []), (resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : []));
        var checkingForAlertRules = alertsUnresolvedAndResolved.length === 0 && hasAlertRule === undefined;
        var showLoadingIndicator = loading || checkingForAlertRules || !isProjectStabilized;
        if (showLoadingIndicator) {
            return <Placeholder height={PLACEHOLDER_AND_EMPTY_HEIGHT}/>;
        }
        if (!hasAlertRule) {
            return (<MissingAlertsButtons organization={organization} projectSlug={projectSlug}/>);
        }
        if (alertsUnresolvedAndResolved.length === 0) {
            return (<StyledEmptyStateWarning small>{t('No alerts found')}</StyledEmptyStateWarning>);
        }
        return alertsUnresolvedAndResolved.slice(0, 3).map(this.renderAlertRow);
    };
    ProjectLatestAlerts.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectLatestAlerts.prototype.renderBody = function () {
        return (<SidebarSection>
        <SectionHeadingWrapper>
          <SectionHeading>{t('Latest Alerts')}</SectionHeading>
          <SectionHeadingLink to={this.alertsLink}>
            <IconOpen />
          </SectionHeadingLink>
        </SectionHeadingWrapper>

        <div>{this.renderInnerBody()}</div>
      </SidebarSection>);
    };
    return ProjectLatestAlerts;
}(AsyncComponent));
var AlertRowLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"])), space(3), space(0.5), space(1));
var AlertBadge = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.color; });
var AlertIconWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n"], ["\n  position: absolute;\n"])));
var AlertDetails = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-left: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  margin-left: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeMedium; }, space(2), overflowEllipsis);
var AlertTitle = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-weight: 400;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  font-weight: 400;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])));
var AlertDate = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.color; });
var StyledEmptyStateWarning = styled(EmptyStateWarning)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  height: ", ";\n  justify-content: center;\n"], ["\n  height: ", ";\n  justify-content: center;\n"])), PLACEHOLDER_AND_EMPTY_HEIGHT);
export default withTheme(ProjectLatestAlerts);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=projectLatestAlerts.jsx.map