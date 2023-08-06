import { __assign, __extends } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import NavTabs from 'app/components/navTabs';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import recreateRoute from 'app/utils/recreateRoute';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import GroupTombstones from 'app/views/settings/project/projectFilters/groupTombstones';
import ProjectFiltersChart from 'app/views/settings/project/projectFilters/projectFiltersChart';
import ProjectFiltersSettings from 'app/views/settings/project/projectFilters/projectFiltersSettings';
var ProjectFilters = /** @class */ (function (_super) {
    __extends(ProjectFilters, _super);
    function ProjectFilters() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectFilters.prototype.render = function () {
        var _a = this.props, project = _a.project, params = _a.params, location = _a.location;
        var orgId = params.orgId, projectId = params.projectId, filterType = params.filterType;
        if (!project) {
            return null;
        }
        var features = new Set(project.features);
        return (<React.Fragment>
        <SentryDocumentTitle title={t('Inbound Filters')} projectSlug={projectId}/>
        <SettingsPageHeader title={t('Inbound Data Filters')}/>
        <PermissionAlert />

        <TextBlock>
          {t('Filters allow you to prevent Sentry from storing events in certain situations. Filtered events are tracked separately from rate limits, and do not apply to any project quotas.')}
        </TextBlock>

        <div>
          <ProjectFiltersChart project={project} params={this.props.params}/>

          {features.has('discard-groups') && (<NavTabs underlined style={{ paddingTop: '30px' }}>
              <li className={filterType === 'data-filters' ? 'active' : ''}>
                <Link to={recreateRoute('data-filters/', __assign(__assign({}, this.props), { stepBack: -1 }))}>
                  {t('Data Filters')}
                </Link>
              </li>
              <li className={filterType === 'discarded-groups' ? 'active' : ''}>
                <Link to={recreateRoute('discarded-groups/', __assign(__assign({}, this.props), { stepBack: -1 }))}>
                  {t('Discarded Issues')}
                </Link>
              </li>
            </NavTabs>)}

          {filterType === 'discarded-groups' ? (<GroupTombstones orgId={orgId} projectId={project.slug} location={location}/>) : (<ProjectFiltersSettings project={project} params={this.props.params} features={features}/>)}
        </div>
      </React.Fragment>);
    };
    return ProjectFilters;
}(React.Component));
export default ProjectFilters;
//# sourceMappingURL=index.jsx.map