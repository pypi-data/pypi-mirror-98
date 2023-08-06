import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import omit from 'lodash/omit';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconCheckmark } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import withOrganization from 'app/utils/withOrganization';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import AlertHeader from './header';
import Onboarding from './onboarding';
import AlertListRow from './row';
import { TableLayout, TitleAndSparkLine } from './styles';
var DEFAULT_QUERY_STATUS = 'open';
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
function getQueryStatus(status) {
    return ['open', 'closed'].includes(status) ? status : DEFAULT_QUERY_STATUS;
}
var IncidentsList = /** @class */ (function (_super) {
    __extends(IncidentsList, _super);
    function IncidentsList() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var query = location.query;
        var status = getQueryStatus(query.status);
        return [
            [
                'incidentList',
                "/organizations/" + (params && params.orgId) + "/incidents/",
                { query: __assign(__assign({}, query), { status: status }) },
            ],
        ];
    };
    /**
     * If our incidentList is empty, determine if we've configured alert rules or
     * if the user has seen the welcome prompt.
     */
    IncidentsList.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var incidentList, _a, params, location, organization, alertRules, hasAlertRule, prompt, firstVisitShown;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        incidentList = this.state.incidentList;
                        if (!incidentList || incidentList.length !== 0) {
                            this.setState({ hasAlertRule: true, firstVisitShown: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/alert-rules/", {
                                method: 'GET',
                                query: location.query,
                            })];
                    case 1:
                        alertRules = _b.sent();
                        hasAlertRule = alertRules.length > 0;
                        // We've already configured alert rules, no need to check if we should show
                        // the "first time welcome" prompt
                        if (hasAlertRule) {
                            this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: false, loading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, promptsCheck(this.api, {
                                organizationId: organization.id,
                                feature: 'alert_stream',
                            })];
                    case 2:
                        prompt = _b.sent();
                        firstVisitShown = !(prompt === null || prompt === void 0 ? void 0 : prompt.dismissedTime);
                        if (firstVisitShown) {
                            // Prompt has not been seen, mark the prompt as seen immediately so they
                            // don't see it again
                            promptsUpdate(this.api, {
                                feature: 'alert_stream',
                                organizationId: organization.id,
                                status: 'dismissed',
                            });
                        }
                        this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: firstVisitShown, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    IncidentsList.prototype.tryRenderOnboarding = function () {
        var firstVisitShown = this.state.firstVisitShown;
        var organization = this.props.organization;
        if (!firstVisitShown) {
            return null;
        }
        var actions = (<React.Fragment>
        <Button size="small" external href={DOCS_URL}>
          {t('View Features')}
        </Button>
        <CreateAlertButton organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="alert_stream">
          {t('Create Alert Rule')}
        </CreateAlertButton>
      </React.Fragment>);
        return <Onboarding actions={actions}/>;
    };
    IncidentsList.prototype.tryRenderEmpty = function () {
        var _a = this.state, hasAlertRule = _a.hasAlertRule, incidentList = _a.incidentList;
        var status = getQueryStatus(this.props.location.query.status);
        if (!incidentList || incidentList.length > 0) {
            return null;
        }
        return (<EmptyMessage size="medium" icon={<IconCheckmark isCircled size="48"/>} title={!hasAlertRule
            ? t('No metric alert rules exist for the selected projects.')
            : status === 'open'
                ? t('No unresolved metric alerts in the selected projects.')
                : t('No resolved metric alerts in the selected projects.')} description={tct('Learn more about [link:Metric Alerts]', {
            link: <ExternalLink href={DOCS_URL}/>,
        })}/>);
    };
    IncidentsList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentsList.prototype.renderList = function () {
        var _a, _b;
        var _c = this.state, loading = _c.loading, incidentList = _c.incidentList, incidentListPageLinks = _c.incidentListPageLinks, hasAlertRule = _c.hasAlertRule;
        var _d = this.props, orgId = _d.params.orgId, organization = _d.organization;
        var allProjectsFromIncidents = new Set(flatten(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        var showLoadingIndicator = loading || checkingForAlertRules;
        var status = getQueryStatus(this.props.location.query.status);
        return (<React.Fragment>
        {(_a = this.tryRenderOnboarding()) !== null && _a !== void 0 ? _a : (<Panel>
            {!loading && (<StyledPanelHeader>
                <TableLayout status={status}>
                  <PaddedTitleAndSparkLine status={status}>
                    <div>{t('Alert')}</div>
                    {status === 'open' && <div>{t('Graph')}</div>}
                  </PaddedTitleAndSparkLine>
                  <div>{t('Project')}</div>
                  <div>{t('Triggered')}</div>
                  {status === 'closed' && <div>{t('Duration')}</div>}
                  {status === 'closed' && <div>{t('Resolved')}</div>}
                </TableLayout>
              </StyledPanelHeader>)}
            {showLoadingIndicator ? (<LoadingIndicator />) : ((_b = this.tryRenderEmpty()) !== null && _b !== void 0 ? _b : (<PanelBody>
                  <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
                    {function (_a) {
            var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
            return incidentList.map(function (incident) { return (<AlertListRow key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} filteredStatus={status} organization={organization}/>); });
        }}
                  </Projects>
                </PanelBody>))}
          </Panel>)}
        <Pagination pageLinks={incidentListPageLinks}/>
      </React.Fragment>);
    };
    IncidentsList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization, router = _a.router;
        var pathname = location.pathname, query = location.query;
        var orgId = params.orgId;
        var openIncidentsQuery = omit(__assign(__assign({}, query), { status: 'open' }), 'cursor');
        var closedIncidentsQuery = omit(__assign(__assign({}, query), { status: 'closed' }), 'cursor');
        var status = getQueryStatus(query.status);
        return (<SentryDocumentTitle title={t('Alerts')} orgSlug={orgId}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false}>
          <AlertHeader organization={organization} router={router} activeTab="stream"/>
          <Layout.Body>
            <Layout.Main fullWidth>
              {!this.tryRenderOnboarding() && (<StyledButtonBar merged active={status}>
                  <Button to={{ pathname: pathname, query: openIncidentsQuery }} barId="open" size="small">
                    {t('Unresolved')}
                  </Button>
                  <Button to={{ pathname: pathname, query: closedIncidentsQuery }} barId="closed" size="small">
                    {t('Resolved')}
                  </Button>
                </StyledButtonBar>)}
              {this.renderList()}
            </Layout.Main>
          </Layout.Body>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return IncidentsList;
}(AsyncComponent));
var IncidentsListContainer = /** @class */ (function (_super) {
    __extends(IncidentsListContainer, _super);
    function IncidentsListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    IncidentsListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    };
    IncidentsListContainer.prototype.trackView = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var status = getQueryStatus(location.query.status);
        trackAnalyticsEvent({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
            status: status,
        });
    };
    IncidentsListContainer.prototype.renderNoAccess = function () {
        return (<Layout.Body>
        <Layout.Main fullWidth>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </Layout.Main>
      </Layout.Body>);
    };
    IncidentsListContainer.prototype.render = function () {
        var organization = this.props.organization;
        return (<Feature features={['organizations:incidents']} organization={organization} hookName="feature-disabled:alerts-page" renderDisabled={this.renderNoAccess}>
        <IncidentsList {...this.props}/>
      </Feature>);
    };
    return IncidentsListContainer;
}(React.Component));
var StyledButtonBar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100px;\n  margin-bottom: ", ";\n"], ["\n  width: 100px;\n  margin-bottom: ", ";\n"])), space(1));
var PaddedTitleAndSparkLine = styled(TitleAndSparkLine)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: ", ";\n"], ["\n  padding-left: ", ";\n"])), space(2));
var StyledPanelHeader = styled(PanelHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"], ["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"])), space(1.5), space(2), space(1.5));
export default withOrganization(IncidentsListContainer);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map