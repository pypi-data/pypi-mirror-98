import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Alert from 'app/components/alert';
import AutoSelectText from 'app/components/autoSelectText';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import PluginList from 'app/components/pluginList';
import { IconFlag } from 'app/icons';
import { t, tct } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
import routeTitleGen from 'app/utils/routeTitle';
import withPlugins from 'app/utils/withPlugins';
import AsyncView from 'app/views/asyncView';
import Field from 'app/views/settings/components/forms/field';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var TOKEN_PLACEHOLDER = 'YOUR_TOKEN';
var WEBHOOK_PLACEHOLDER = 'YOUR_WEBHOOK_URL';
var placeholderData = {
    token: TOKEN_PLACEHOLDER,
    webhookUrl: WEBHOOK_PLACEHOLDER,
};
var ProjectReleaseTracking = /** @class */ (function (_super) {
    __extends(ProjectReleaseTracking, _super);
    function ProjectReleaseTracking() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRegenerateToken = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.api.request("/projects/" + orgId + "/" + projectId + "/releases/token/", {
                method: 'POST',
                data: { project: projectId },
                success: function (data) {
                    _this.setState({
                        data: {
                            token: data.token,
                            webhookUrl: data.webhookUrl,
                        },
                    });
                    addSuccessMessage(t('Your deploy token has been regenerated. You will need to update any existing deploy hooks.'));
                },
                error: function () {
                    addErrorMessage(t('Unable to regenerate deploy token, please try again'));
                },
            });
        };
        return _this;
    }
    ProjectReleaseTracking.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Releases'), projectId, false);
    };
    ProjectReleaseTracking.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        // Allow 403s
        return [
            [
                'data',
                "/projects/" + orgId + "/" + projectId + "/releases/token/",
                {},
                { allowError: function (err) { return err && err.status === 403; } },
            ],
        ];
    };
    ProjectReleaseTracking.prototype.getReleaseWebhookIntructions = function () {
        var webhookUrl = (this.state.data || placeholderData).webhookUrl;
        return ('curl ' +
            webhookUrl +
            ' \\' +
            '\n  ' +
            '-X POST \\' +
            '\n  ' +
            "-H 'Content-Type: application/json' \\" +
            '\n  ' +
            '-d \'{"version": "abcdefg"}\'');
    };
    ProjectReleaseTracking.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, plugins = _a.plugins;
        var hasWrite = organization.access.includes('project:write');
        if (plugins.loading) {
            return <LoadingIndicator />;
        }
        var pluginList = plugins.plugins.filter(function (p) { return p.type === 'release-tracking' && p.hasConfiguration; });
        var _b = this.state.data || placeholderData, token = _b.token, webhookUrl = _b.webhookUrl;
        token = getDynamicText({ value: token, fixed: '__TOKEN__' });
        webhookUrl = getDynamicText({ value: webhookUrl, fixed: '__WEBHOOK_URL__' });
        return (<div>
        <SettingsPageHeader title={t('Release Tracking')}/>
        {!hasWrite && (<Alert icon={<IconFlag size="md"/>} type="warning">
            {t('You do not have sufficient permissions to access Release tokens, placeholders are displayed below.')}
          </Alert>)}
        <p>
          {t('Configure release tracking for this project to automatically record new releases of your application.')}
        </p>

        <Panel>
          <PanelHeader>{t('Client Configuration')}</PanelHeader>
          <PanelBody flexible withPadding>
            <p>
              {tct('Start by binding the [release] attribute in your application, take a look at [link] to see how to configure this for the SDK you are using.', {
            link: (<a href="https://docs.sentry.io/platform-redirect/?next=/configuration/releases/">
                      our docs
                    </a>),
            release: <code>release</code>,
        })}
            </p>
            <p>
              {t("This will annotate each event with the version of your application, as well as automatically create a release entity in the system the first time it's seen.")}
            </p>
            <p>
              {t('In addition you may configure a release hook (or use our API) to push a release and include additional metadata with it.')}
            </p>
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader>{t('Deploy Token')}</PanelHeader>
          <PanelBody flexible>
            <Field label={t('Token')} help={t('A unique secret which is used to generate deploy hook URLs')}>
              <TextCopyInput>{token}</TextCopyInput>
            </Field>
            <Field label={t('Regenerate Token')} help={t('If a service becomes compromised, you should regenerate the token and re-configure any deploy hooks with the newly generated URL.')}>
              <div>
                <Confirm disabled={!hasWrite} priority="danger" onConfirm={this.handleRegenerateToken} message={t('Are you sure you want to regenerate your token? Your current token will no longer be usable.')}>
                  <Button type="button" priority="danger" disabled={!hasWrite}>
                    {t('Regenerate Token')}
                  </Button>
                </Confirm>
              </div>
            </Field>
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader>{t('Webhook')}</PanelHeader>
          <PanelBody flexible withPadding>
            <p>
              {t('If you simply want to integrate with an existing system, sometimes its easiest just to use a webhook.')}
            </p>

            <AutoSelectText>
              <pre>{webhookUrl}</pre>
            </AutoSelectText>

            <p>
              {t('The release webhook accepts the same parameters as the "Create a new Release" API endpoint.')}
            </p>

            {getDynamicText({
            value: (<AutoSelectText>
                  <pre>{this.getReleaseWebhookIntructions()}</pre>
                </AutoSelectText>),
            fixed: (<pre>
                  {"curl __WEBHOOK_URL__ \\\n  -X POST \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"version\": \"abcdefg\"}'"}
                </pre>),
        })}
          </PanelBody>
        </Panel>

        <PluginList organization={organization} project={project} pluginList={pluginList}/>

        <Panel>
          <PanelHeader>{t('API')}</PanelHeader>
          <PanelBody flexible withPadding>
            <p>
              {t('You can notify Sentry when you release new versions of your application via our HTTP API.')}
            </p>

            <p>
              {tct('See the [link:releases documentation] for more information.', {
            link: <a href="https://docs.sentry.io/workflow/releases/"/>,
        })}
            </p>
          </PanelBody>
        </Panel>
      </div>);
    };
    return ProjectReleaseTracking;
}(AsyncView));
export default withPlugins(ProjectReleaseTracking);
// Export for tests
export { ProjectReleaseTracking };
//# sourceMappingURL=projectReleaseTracking.jsx.map