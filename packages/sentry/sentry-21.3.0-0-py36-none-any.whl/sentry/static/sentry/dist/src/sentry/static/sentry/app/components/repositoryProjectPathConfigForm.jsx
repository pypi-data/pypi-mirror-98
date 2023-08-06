import { __assign, __extends } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import { t } from 'app/locale';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import { FieldFromConfig } from 'app/views/settings/components/forms';
import Form from 'app/views/settings/components/forms/form';
var RepositoryProjectPathConfigForm = /** @class */ (function (_super) {
    __extends(RepositoryProjectPathConfigForm, _super);
    function RepositoryProjectPathConfigForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "initialData", {
        get: function () {
            var _a = this.props, existingConfig = _a.existingConfig, integration = _a.integration;
            return __assign({ defaultBranch: 'master', stackRoot: '', sourceRoot: '', repositoryId: existingConfig === null || existingConfig === void 0 ? void 0 : existingConfig.repoId, integrationId: integration.id }, pick(existingConfig, ['projectId', 'defaultBranch', 'stackRoot', 'sourceRoot']));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "formFields", {
        get: function () {
            var _a = this.props, projects = _a.projects, repos = _a.repos;
            var repoChoices = repos.map(function (_a) {
                var name = _a.name, id = _a.id;
                return ({ value: id, label: name });
            });
            return [
                {
                    name: 'projectId',
                    type: 'sentry_project_selector',
                    required: true,
                    label: t('Project'),
                    projects: projects,
                },
                {
                    name: 'repositoryId',
                    type: 'select',
                    required: true,
                    label: t('Repo'),
                    placeholder: t('Choose repo'),
                    options: repoChoices,
                    deprecatedSelectControl: false,
                },
                {
                    name: 'defaultBranch',
                    type: 'string',
                    required: true,
                    label: t('Branch'),
                    placeholder: t('Type your branch'),
                    showHelpInTooltip: true,
                    help: t('If an event does not have a release tied to a commit, we will use this branch when linking to your source code.'),
                },
                {
                    name: 'stackRoot',
                    type: 'string',
                    required: false,
                    label: t('Stack Trace Root'),
                    placeholder: t('Type root path of your stack traces'),
                    showHelpInTooltip: true,
                    help: t('Any stack trace starting with this path will be mapped with this rule. An empty string will match all paths.'),
                },
                {
                    name: 'sourceRoot',
                    type: 'string',
                    required: false,
                    label: t('Source Code Root'),
                    placeholder: t('Type root path of your source code, e.g. `src/`.'),
                    showHelpInTooltip: true,
                    help: t('When a rule matches, the stack trace root is replaced with this path to get the path in your repository. Leaving this empty means replacing the stack trace root with an empty string.'),
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    RepositoryProjectPathConfigForm.prototype.handlePreSubmit = function () {
        trackIntegrationEvent('integrations.stacktrace_submit_config', {
            setup_type: 'manual',
            view: 'integration_configuration_detail',
            provider: this.props.integration.provider.key,
        }, this.props.organization);
    };
    RepositoryProjectPathConfigForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, onSubmitSuccess = _a.onSubmitSuccess, onCancel = _a.onCancel, existingConfig = _a.existingConfig;
        // endpoint changes if we are making a new row or updating an existing one
        var baseEndpoint = "/organizations/" + organization.slug + "/repo-project-path-configs/";
        var endpoint = existingConfig
            ? "" + baseEndpoint + existingConfig.id + "/"
            : baseEndpoint;
        var apiMethod = existingConfig ? 'PUT' : 'POST';
        return (<Form onSubmitSuccess={onSubmitSuccess} onPreSubmit={function () { return _this.handlePreSubmit(); }} initialData={this.initialData} apiEndpoint={endpoint} apiMethod={apiMethod} onCancel={onCancel}>
        {this.formFields.map(function (field) { return (<FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>); })}
      </Form>);
    };
    return RepositoryProjectPathConfigForm;
}(React.Component));
export default RepositoryProjectPathConfigForm;
//# sourceMappingURL=repositoryProjectPathConfigForm.jsx.map