import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import NarrowLayout from 'app/components/narrowLayout';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import SelectField from 'app/views/settings/components/forms/selectField';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var AcceptProjectTransfer = /** @class */ (function (_super) {
    __extends(AcceptProjectTransfer, _super);
    function AcceptProjectTransfer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (formData) {
            _this.api.request('/accept-transfer/', {
                method: 'POST',
                data: {
                    data: _this.props.location.query.data,
                    organization: formData.organization,
                },
                success: function () {
                    var orgSlug = formData.organization;
                    _this.props.router.push("/" + orgSlug);
                    addSuccessMessage(t('Project successfully transferred'));
                },
                error: function (error) {
                    var errorMsg = error && error.responseJSON && typeof error.responseJSON.detail === 'string'
                        ? error.responseJSON.detail
                        : '';
                    addErrorMessage(t('Unable to transfer project') + errorMsg ? ": " + errorMsg : '');
                },
            });
        };
        return _this;
    }
    AcceptProjectTransfer.prototype.getEndpoints = function () {
        var query = this.props.location.query;
        return [['transferDetails', '/accept-transfer/', { query: query }]];
    };
    AcceptProjectTransfer.prototype.getTitle = function () {
        return t('Accept Project Transfer');
    };
    AcceptProjectTransfer.prototype.renderError = function (error) {
        var disableLog = false;
        // Check if there is an error message with `transferDetails` endpoint
        // If so, show as toast and ignore, otherwise log to sentry
        if (error && error.responseJSON && typeof error.responseJSON.detail === 'string') {
            addErrorMessage(error.responseJSON.detail);
            disableLog = true;
        }
        return _super.prototype.renderError.call(this, error, disableLog);
    };
    AcceptProjectTransfer.prototype.renderBody = function () {
        var _a;
        var transferDetails = this.state.transferDetails;
        var options = transferDetails === null || transferDetails === void 0 ? void 0 : transferDetails.organizations.map(function (org) { return ({
            label: org.slug,
            value: org.slug,
        }); });
        var organization = (_a = options === null || options === void 0 ? void 0 : options[0]) === null || _a === void 0 ? void 0 : _a.value;
        return (<NarrowLayout>
        <SettingsPageHeader title={t('Approve Transfer Project Request')}/>
        <p>
          {tct('Projects must be transferred to a specific [organization]. ' +
            'You can grant specific teams access to the project later under the [projectSettings]. ' +
            '(Note that granting access to at least one team is necessary for the project to ' +
            'appear in all parts of the UI.)', {
            organization: <strong>{t('Organization')}</strong>,
            projectSettings: <strong>{t('Project Settings')}</strong>,
        })}
        </p>
        {transferDetails && (<p>
            {tct('Please select which [organization] you want for the project [project].', {
            organization: <strong>{t('Organization')}</strong>,
            project: transferDetails.project.slug,
        })}
          </p>)}
        <Form onSubmit={this.handleSubmit} submitLabel={t('Transfer Project')} submitPriority="danger" initialData={organization ? { organization: organization } : undefined}>
          <SelectField options={options} label={t('Organization')} name="organization" style={{ borderBottom: 'none' }}/>
        </Form>
      </NarrowLayout>);
    };
    return AcceptProjectTransfer;
}(AsyncView));
export default AcceptProjectTransfer;
//# sourceMappingURL=acceptProjectTransfer.jsx.map