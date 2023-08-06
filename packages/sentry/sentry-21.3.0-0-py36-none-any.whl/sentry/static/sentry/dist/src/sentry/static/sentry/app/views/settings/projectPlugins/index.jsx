import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { disablePlugin, enablePlugin, fetchPlugins } from 'app/actionCreators/plugins';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import withPlugins from 'app/utils/withPlugins';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import ProjectPlugins from './projectPlugins';
var ProjectPluginsContainer = /** @class */ (function (_super) {
    __extends(ProjectPluginsContainer, _super);
    function ProjectPluginsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var plugins, installCount;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetchPlugins(this.props.params)];
                    case 1:
                        plugins = _a.sent();
                        installCount = plugins.filter(function (plugin) { return plugin.hasConfiguration && plugin.enabled; }).length;
                        trackIntegrationEvent('integrations.index_viewed', {
                            integrations_installed: installCount,
                            view: 'legacy_integrations',
                        }, this.props.organization, { startSession: true });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleChange = function (pluginId, shouldEnable) {
            var _a = _this.props.params, projectId = _a.projectId, orgId = _a.orgId;
            var actionCreator = shouldEnable ? enablePlugin : disablePlugin;
            actionCreator({ projectId: projectId, orgId: orgId, pluginId: pluginId });
        };
        return _this;
    }
    ProjectPluginsContainer.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectPluginsContainer.prototype.render = function () {
        var _a = this.props.plugins || {}, loading = _a.loading, error = _a.error, plugins = _a.plugins;
        var orgId = this.props.params.orgId;
        var title = t('Legacy Integrations');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} orgSlug={orgId}/>
        <SettingsPageHeader title={title}/>
        <PermissionAlert />

        <ProjectPlugins {...this.props} onChange={this.handleChange} loading={loading} error={error} plugins={plugins}/>
      </React.Fragment>);
    };
    return ProjectPluginsContainer;
}(React.Component));
export default withPlugins(ProjectPluginsContainer);
//# sourceMappingURL=index.jsx.map