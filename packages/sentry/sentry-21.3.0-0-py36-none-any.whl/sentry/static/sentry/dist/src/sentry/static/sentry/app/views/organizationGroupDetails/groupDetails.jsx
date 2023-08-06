import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import * as ReactRouter from 'react-router';
import * as Sentry from '@sentry/react';
import PropTypes from 'prop-types';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import MissingProjectMembership from 'app/components/projects/missingProjectMembership';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import GroupStore from 'app/stores/groupStore';
import { PageContent } from 'app/styles/organization';
import { callIfFunction } from 'app/utils/callIfFunction';
import { getMessage, getTitle } from 'app/utils/events';
import Projects from 'app/utils/projects';
import recreateRoute from 'app/utils/recreateRoute';
import withApi from 'app/utils/withApi';
import { ERROR_TYPES } from './constants';
import GroupHeader, { TAB } from './header';
import { fetchGroupEvent, getGroupReprocessingStatus, markEventSeen, ReprocessingStatus, } from './utils';
var GroupDetails = /** @class */ (function (_super) {
    __extends(GroupDetails, _super);
    function GroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.remountComponent = function () {
            _this.setState(_this.initialState);
            _this.fetchData();
        };
        _this.listener = GroupStore.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        return _this;
    }
    GroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
            location: this.props.location,
        };
    };
    GroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b;
        if (prevProps.isGlobalSelectionReady !== this.props.isGlobalSelectionReady) {
            this.fetchData();
        }
        if ((!this.canLoadEventEarly(prevProps) && !(prevState === null || prevState === void 0 ? void 0 : prevState.group) && this.state.group) ||
            (((_a = prevProps.params) === null || _a === void 0 ? void 0 : _a.eventId) !== ((_b = this.props.params) === null || _b === void 0 ? void 0 : _b.eventId) && this.state.group)) {
            this.getEvent(this.state.group);
        }
    };
    GroupDetails.prototype.componentWillUnmount = function () {
        GroupStore.reset();
        callIfFunction(this.listener);
    };
    Object.defineProperty(GroupDetails.prototype, "initialState", {
        get: function () {
            return {
                group: null,
                loading: true,
                loadingEvent: true,
                error: false,
                eventError: false,
                errorType: null,
                project: null,
            };
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.canLoadEventEarly = function (props) {
        return !props.params.eventId || ['oldest', 'latest'].includes(props.params.eventId);
    };
    Object.defineProperty(GroupDetails.prototype, "groupDetailsEndpoint", {
        get: function () {
            return "/issues/" + this.props.params.groupId + "/";
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.getEvent = function (group) {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var _b, params, environments, api, orgSlug, groupId, eventId, projectId, event_1, err_1;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (group) {
                            this.setState({ loadingEvent: true, eventError: false });
                        }
                        _b = this.props, params = _b.params, environments = _b.environments, api = _b.api;
                        orgSlug = params.orgId;
                        groupId = params.groupId;
                        eventId = (params === null || params === void 0 ? void 0 : params.eventId) || 'latest';
                        projectId = (_a = group === null || group === void 0 ? void 0 : group.project) === null || _a === void 0 ? void 0 : _a.slug;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchGroupEvent(api, orgSlug, groupId, eventId, environments, projectId)];
                    case 2:
                        event_1 = _c.sent();
                        this.setState({ event: event_1, loading: false, eventError: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        // This is an expected error, capture to Sentry so that it is not considered as an unhandled error
                        Sentry.captureException(err_1);
                        this.setState({ eventError: true, loading: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.getCurrentRouteInfo = function (group) {
        var _a = this.props, routes = _a.routes, organization = _a.organization;
        var event = this.state.event;
        // All the routes under /organizations/:orgId/issues/:groupId have a defined props
        var _b = routes[routes.length - 1].props, currentTab = _b.currentTab, isEventRoute = _b.isEventRoute;
        var baseUrl = isEventRoute && event
            ? "/organizations/" + organization.slug + "/issues/" + group.id + "/events/" + event.id + "/"
            : "/organizations/" + organization.slug + "/issues/" + group.id + "/";
        return { currentTab: currentTab, baseUrl: baseUrl };
    };
    GroupDetails.prototype.checkRedirectRoute = function () { };
    GroupDetails.prototype.fetchData = function () {
        var _a, _b, _c;
        return __awaiter(this, void 0, void 0, function () {
            var _d, environments, api, isGlobalSelectionReady, params, routes, location, organization, eventPromise, queryParams, groupPromise, _e, data, projects, projectId_1, features, hasReprocessingV2Feature, reprocessingStatus, _f, currentTab, baseUrl, project, locationWithProject, err_2, errorType;
            return __generator(this, function (_g) {
                switch (_g.label) {
                    case 0:
                        _d = this.props, environments = _d.environments, api = _d.api, isGlobalSelectionReady = _d.isGlobalSelectionReady, params = _d.params, routes = _d.routes, location = _d.location, organization = _d.organization;
                        // Need to wait for global selection store to be ready before making request
                        if (!isGlobalSelectionReady) {
                            return [2 /*return*/];
                        }
                        _g.label = 1;
                    case 1:
                        _g.trys.push([1, 4, , 5]);
                        eventPromise = void 0;
                        if (this.canLoadEventEarly(this.props)) {
                            eventPromise = this.getEvent();
                        }
                        queryParams = __assign({}, (environments ? { environment: environments } : {}));
                        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('inbox')) {
                            queryParams.expand = 'inbox';
                        }
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: queryParams,
                            })];
                    case 2:
                        groupPromise = _g.sent();
                        return [4 /*yield*/, Promise.all([groupPromise, eventPromise])];
                    case 3:
                        _e = __read.apply(void 0, [_g.sent(), 1]), data = _e[0];
                        projects = organization.projects;
                        projectId_1 = data.project.id;
                        features = (_c = (_b = projects === null || projects === void 0 ? void 0 : projects.find(function (proj) { return proj.id === projectId_1; })) === null || _b === void 0 ? void 0 : _b.features) !== null && _c !== void 0 ? _c : [];
                        hasReprocessingV2Feature = features.includes('reprocessing-v2');
                        reprocessingStatus = getGroupReprocessingStatus(data);
                        _f = this.getCurrentRouteInfo(data), currentTab = _f.currentTab, baseUrl = _f.baseUrl;
                        if (this.props.params.groupId !== data.id) {
                            if (hasReprocessingV2Feature) {
                                // Redirects to the Activities tab
                                if (reprocessingStatus === ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                                    currentTab !== TAB.ACTIVITY) {
                                    ReactRouter.browserHistory.push({
                                        pathname: "" + baseUrl + TAB.ACTIVITY + "/",
                                        query: __assign(__assign({}, params), { groupId: data.id }),
                                    });
                                    return [2 /*return*/];
                                }
                            }
                            ReactRouter.browserHistory.push(recreateRoute('', {
                                routes: routes,
                                location: location,
                                params: __assign(__assign({}, params), { groupId: data.id }),
                            }));
                            return [2 /*return*/];
                        }
                        if (hasReprocessingV2Feature) {
                            if (reprocessingStatus === ReprocessingStatus.REPROCESSING &&
                                currentTab !== TAB.DETAILS) {
                                ReactRouter.browserHistory.push({
                                    pathname: baseUrl,
                                    query: params,
                                });
                            }
                            if (reprocessingStatus === ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                                (currentTab !== TAB.ACTIVITY || currentTab !== TAB.USER_FEEDBACK)) {
                                ReactRouter.browserHistory.push({
                                    pathname: "" + baseUrl + TAB.ACTIVITY + "/",
                                    query: params,
                                });
                            }
                        }
                        project = data.project;
                        markEventSeen(api, params.orgId, project.slug, params.groupId);
                        if (!project) {
                            Sentry.withScope(function () {
                                Sentry.captureException(new Error('Project not found'));
                            });
                        }
                        else {
                            locationWithProject = __assign({}, this.props.location);
                            if (locationWithProject.query.project === undefined &&
                                locationWithProject.query._allp === undefined) {
                                //We use _allp as a temporary measure to know they came from the issue list page with no project selected (all projects included in filter).
                                //If it is not defined, we add the locked project id to the URL (this is because if someone navigates directly to an issue on single-project priveleges, then goes back - they were getting assigned to the first project).
                                //If it is defined, we do not so that our back button will bring us to the issue list page with no project selected instead of the locked project.
                                locationWithProject.query.project = project.id;
                            }
                            delete locationWithProject.query._allp; //We delete _allp from the URL to keep the hack a bit cleaner, but this is not an ideal solution and will ultimately be replaced with something smarter.
                            ReactRouter.browserHistory.replace(locationWithProject);
                        }
                        this.setState({ project: project });
                        GroupStore.loadInitialData([data]);
                        return [3 /*break*/, 5];
                    case 4:
                        err_2 = _g.sent();
                        Sentry.captureException(err_2);
                        errorType = null;
                        switch (err_2 === null || err_2 === void 0 ? void 0 : err_2.status) {
                            case 404:
                                errorType = ERROR_TYPES.GROUP_NOT_FOUND;
                                break;
                            case 403:
                                errorType = ERROR_TYPES.MISSING_MEMBERSHIP;
                                break;
                            default:
                        }
                        this.setState({
                            error: true,
                            errorType: errorType,
                            loading: false,
                        });
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.onGroupChange = function (itemIds) {
        var id = this.props.params.groupId;
        if (itemIds.has(id)) {
            var group = GroupStore.get(id);
            if (group) {
                // TODO(ts) This needs a better approach. issueActions is splicing attributes onto
                // group objects to cheat here.
                if (group.stale) {
                    this.fetchData();
                    return;
                }
                this.setState({
                    group: group,
                });
            }
        }
    };
    GroupDetails.prototype.getTitle = function () {
        var organization = this.props.organization;
        var group = this.state.group;
        var defaultTitle = 'Sentry';
        if (!group) {
            return defaultTitle;
        }
        var title = getTitle(group, organization).title;
        var message = getMessage(group);
        var project = group.project;
        var eventDetails = organization.slug + " - " + project.slug;
        if (title && message) {
            return title + ": " + message + " - " + eventDetails;
        }
        return (title || message || defaultTitle) + " - " + eventDetails;
    };
    GroupDetails.prototype.renderError = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, location = _c.location;
        var projects = (_a = organization.projects) !== null && _a !== void 0 ? _a : [];
        var projectId = location.query.project;
        var projectSlug = (_b = projects.find(function (proj) { return proj.id === projectId; })) === null || _b === void 0 ? void 0 : _b.slug;
        switch (this.state.errorType) {
            case ERROR_TYPES.GROUP_NOT_FOUND:
                return (<LoadingError message={t('The issue you were looking for was not found.')}/>);
            case ERROR_TYPES.MISSING_MEMBERSHIP:
                return (<MissingProjectMembership organization={this.props.organization} projectSlug={projectSlug}/>);
            default:
                return <LoadingError onRetry={this.remountComponent}/>;
        }
    };
    GroupDetails.prototype.renderContent = function (project) {
        var _this = this;
        var _a = this.props, children = _a.children, environments = _a.environments;
        var _b = this.state, loadingEvent = _b.loadingEvent, eventError = _b.eventError;
        // At this point group and event have to be defined
        var group = this.state.group;
        var event = this.state.event;
        var _c = this.getCurrentRouteInfo(group), currentTab = _c.currentTab, baseUrl = _c.baseUrl;
        var childProps = {
            environments: environments,
            group: group,
            project: project,
        };
        if (currentTab === TAB.DETAILS) {
            childProps = __assign(__assign({}, childProps), { event: event,
                loadingEvent: loadingEvent,
                eventError: eventError, onRetry: function () { return _this.remountComponent(); } });
        }
        if (currentTab === TAB.TAGS) {
            childProps = __assign(__assign({}, childProps), { event: event, baseUrl: baseUrl });
        }
        return (<React.Fragment>
        <GroupHeader project={project} event={event} group={group} currentTab={currentTab} baseUrl={baseUrl}/>
        {React.isValidElement(children)
            ? React.cloneElement(children, childProps)
            : children}
      </React.Fragment>);
    };
    GroupDetails.prototype.render = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var _b = this.state, isError = _b.error, group = _b.group, project = _b.project, loading = _b.loading;
        var isLoading = loading || (!group && !isError);
        return (<DocumentTitle title={this.getTitle()}>
        <GlobalSelectionHeader skipLoadLastUsed forceProject={project} showDateSelector={false} shouldForceProject lockedMessageSubject={t('issue')} showIssueStreamLink showProjectSettingsLink>
          <PageContent>
            {isLoading ? (<LoadingIndicator />) : isError ? (this.renderError()) : (<Projects orgId={organization.slug} slugs={[(_a = project === null || project === void 0 ? void 0 : project.slug) !== null && _a !== void 0 ? _a : '']} data-test-id="group-projects-container">
                {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
            return initiallyLoaded ? (fetchError ? (<LoadingError message={t('Error loading the specified project')}/>) : (_this.renderContent(projects[0]))) : (<LoadingIndicator />);
        }}
              </Projects>)}
          </PageContent>
        </GlobalSelectionHeader>
      </DocumentTitle>);
    };
    GroupDetails.childContextTypes = {
        group: SentryTypes.Group,
        location: PropTypes.object,
    };
    return GroupDetails;
}(React.Component));
export default withApi(Sentry.withProfiler(GroupDetails));
//# sourceMappingURL=groupDetails.jsx.map