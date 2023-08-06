import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { updateProjects } from 'app/actionCreators/globalSelection';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import IdBadge from 'app/components/idBadge';
import * as Layout from 'app/components/layouts/thirds';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import TextOverflow from 'app/components/textOverflow';
import { IconSettings, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import { defined } from 'app/utils';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withProjects from 'app/utils/withProjects';
import AsyncView from 'app/views/asyncView';
import ProjectScoreCards from './projectScoreCards/projectScoreCards';
import ProjectCharts from './projectCharts';
import ProjectIssues from './projectIssues';
import ProjectLatestAlerts from './projectLatestAlerts';
import ProjectLatestReleases from './projectLatestReleases';
import ProjectQuickLinks from './projectQuickLinks';
import ProjectTeamAccess from './projectTeamAccess';
var ProjectDetail = /** @class */ (function (_super) {
    __extends(ProjectDetail, _super);
    function ProjectDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleProjectChange = function (selectedProjects) {
            var _a = _this.props, projects = _a.projects, router = _a.router, location = _a.location, organization = _a.organization;
            var newlySelectedProject = projects.find(function (p) { return p.id === String(selectedProjects[0]); });
            // if we change project in global header, we need to sync the project slug in the URL
            if (newlySelectedProject === null || newlySelectedProject === void 0 ? void 0 : newlySelectedProject.id) {
                router.replace({
                    pathname: "/organizations/" + organization.slug + "/projects/" + newlySelectedProject.slug + "/",
                    query: __assign(__assign({}, location.query), { project: newlySelectedProject.id, environment: undefined }),
                });
            }
        };
        return _this;
    }
    ProjectDetail.prototype.getTitle = function () {
        var params = this.props.params;
        return routeTitleGen(t('Project %s', params.projectId), params.orgId, false);
    };
    ProjectDetail.prototype.componentDidMount = function () {
        this.syncProjectWithSlug();
    };
    ProjectDetail.prototype.componentDidUpdate = function () {
        this.syncProjectWithSlug();
    };
    Object.defineProperty(ProjectDetail.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, params = _a.params;
            return projects.find(function (p) { return p.slug === params.projectId; });
        },
        enumerable: false,
        configurable: true
    });
    ProjectDetail.prototype.syncProjectWithSlug = function () {
        var _a;
        var _b = this.props, router = _b.router, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        if (projectId && projectId !== location.query.project) {
            // if someone visits /organizations/sentry/projects/javascript/ (without ?project=XXX) we need to update URL and globalSelection with the right project ID
            updateProjects([Number(projectId)], router);
        }
    };
    ProjectDetail.prototype.isProjectStabilized = function () {
        var _a;
        var _b = this.props, selection = _b.selection, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        return (defined(projectId) &&
            projectId === location.query.project &&
            projectId === String(selection.projects[0]));
    };
    ProjectDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDetail.prototype.renderProjectNotFound = function () {
        return (<PageContent>
        <Alert type="error" icon={<IconWarning />}>
          {t('This project could not be found.')}
        </Alert>
      </PageContent>);
    };
    ProjectDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, router = _a.router, loadingProjects = _a.loadingProjects, selection = _a.selection;
        var project = this.project;
        var isProjectStabilized = this.isProjectStabilized();
        if (!loadingProjects && !project) {
            return this.renderProjectNotFound();
        }
        return (<GlobalSelectionHeader disableMultipleProjectSelection skipLoadLastUsed onUpdateProjects={this.handleProjectChange}>
        <LightWeightNoProjectMessage organization={organization}>
          <StyledPageContent>
            <Layout.Header>
              <Layout.HeaderContent>
                <Breadcrumbs crumbs={[
            {
                to: "/organizations/" + params.orgId + "/projects/",
                label: t('Projects'),
            },
            { label: t('Project Details') },
        ]}/>
                <Layout.Title>
                  <TextOverflow>
                    {project && (<IdBadge project={project} avatarSize={28} displayName={params.projectId}/>)}
                  </TextOverflow>
                </Layout.Title>
              </Layout.HeaderContent>

              <Layout.HeaderActions>
                <ButtonBar gap={1}>
                  <Button title={t('You’re seeing the new project details page because you’ve opted to be an early adopter of new features. Send us feedback via email.')} href="mailto:project-feedback@sentry.io?subject=Project Details Feedback">
                    {t('Give Feedback')}
                  </Button>
                  <Button to={
        // if we are still fetching project, we can use project slug to build issue stream url and let the redirect handle it
        (project === null || project === void 0 ? void 0 : project.id) ? "/organizations/" + params.orgId + "/issues/?project=" + project.id
            : "/" + params.orgId + "/" + params.projectId}>
                    {t('View All Issues')}
                  </Button>
                  <CreateAlertButton organization={organization} projectSlug={params.projectId}/>
                  <Button icon={<IconSettings />} label={t('Settings')} to={"/settings/" + params.orgId + "/projects/" + params.projectId + "/"}/>
                </ButtonBar>
              </Layout.HeaderActions>
            </Layout.Header>

            <Layout.Body>
              <StyledSdkUpdatesAlert />
              <Layout.Main>
                <ProjectScoreCards organization={organization} isProjectStabilized={isProjectStabilized} selection={selection}/>
                {isProjectStabilized && (<React.Fragment>
                    {[0, 1].map(function (id) { return (<ProjectCharts location={location} organization={organization} router={router} key={"project-charts-" + id} index={id}/>); })}
                    <ProjectIssues organization={organization} location={location}/>
                  </React.Fragment>)}
              </Layout.Main>
              <Layout.Side>
                <ProjectTeamAccess organization={organization} project={project}/>
                <Feature features={['incidents']}>
                  <ProjectLatestAlerts organization={organization} projectSlug={params.projectId} location={location} isProjectStabilized={isProjectStabilized}/>
                </Feature>
                <ProjectLatestReleases organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id} location={location} isProjectStabilized={isProjectStabilized}/>
                <ProjectQuickLinks organization={organization} project={project} location={location}/>
              </Layout.Side>
            </Layout.Body>
          </StyledPageContent>
        </LightWeightNoProjectMessage>
      </GlobalSelectionHeader>);
    };
    return ProjectDetail;
}(AsyncView));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledSdkUpdatesAlert = styled(GlobalSdkUpdateAlert)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
export default withProjects(withGlobalSelection(ProjectDetail));
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectDetail.jsx.map