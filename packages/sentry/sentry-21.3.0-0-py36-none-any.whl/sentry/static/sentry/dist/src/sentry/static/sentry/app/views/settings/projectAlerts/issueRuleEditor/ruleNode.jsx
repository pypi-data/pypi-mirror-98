import { __assign, __extends, __makeTemplateObject, __read, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import ExternalLink from 'app/components/links/externalLink';
import { IconDelete, IconSettings } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { AssigneeTargetType, MailActionTargetType, } from 'app/types/alerts';
import Input from 'app/views/settings/components/forms/controls/input';
import MemberTeamFields from './memberTeamFields';
import TicketRuleModal from './ticketRuleModal';
var RuleNode = /** @class */ (function (_super) {
    __extends(RuleNode, _super);
    function RuleNode() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            var _a = _this.props, index = _a.index, onDelete = _a.onDelete;
            onDelete(index);
        };
        _this.handleMemberTeamChange = function (data) {
            var _a = _this.props, index = _a.index, onPropertyChange = _a.onPropertyChange;
            onPropertyChange(index, 'targetType', "" + data.targetType);
            onPropertyChange(index, 'targetIdentifier', "" + data.targetIdentifier);
        };
        _this.getChoiceField = function (name, fieldConfig) {
            var _a = _this.props, data = _a.data, disabled = _a.disabled, index = _a.index, onPropertyChange = _a.onPropertyChange, onReset = _a.onReset;
            // Select the first item on this list
            // If it's not yet defined, call onPropertyChange to make sure the value is set on state
            var initialVal;
            if (data) {
                if (data[name] === undefined && !!fieldConfig.choices.length) {
                    if (fieldConfig.initial) {
                        initialVal = fieldConfig.initial;
                    }
                    else {
                        initialVal = fieldConfig.choices[0][0];
                    }
                }
                else {
                    initialVal = data[name];
                }
            }
            // Cast `key` to string, this problem pops up because of react-select v3 where
            // `value` requires the `option` object (e.g. {label, object}) - we have
            // helpers in `SelectControl` to filter `choices` to produce the value object
            //
            // However there are integrations that give the form field choices with the value as number, but
            // when the integration configuration gets saved, it gets saved and returned as a string
            var choices = fieldConfig.choices.map(function (_a) {
                var _b = __read(_a, 2), key = _b[0], value = _b[1];
                return ["" + key, value];
            });
            var handleChange = function (_a) {
                var value = _a.value;
                if (fieldConfig.resetsForm) {
                    onReset(index, name, value);
                }
                else {
                    onPropertyChange(index, name, value);
                }
            };
            return (<InlineSelectControl isClearable={false} name={name} value={initialVal} styles={{
                control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '28px', height: '28px' })); },
            }} disabled={disabled} choices={choices} onChange={handleChange}/>);
        };
        _this.getTextField = function (name, fieldConfig) {
            var _a;
            var _b = _this.props, data = _b.data, index = _b.index, onPropertyChange = _b.onPropertyChange, disabled = _b.disabled;
            return (<InlineInput type="text" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={"" + fieldConfig.placeholder} disabled={disabled} onChange={function (e) {
                return onPropertyChange(index, name, e.target.value);
            }}/>);
        };
        _this.getNumberField = function (name, fieldConfig) {
            var _a;
            var _b = _this.props, data = _b.data, index = _b.index, onPropertyChange = _b.onPropertyChange, disabled = _b.disabled;
            return (<InlineNumberInput type="number" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={"" + fieldConfig.placeholder} disabled={disabled} onChange={function (e) {
                return onPropertyChange(index, name, e.target.value);
            }}/>);
        };
        _this.getMailActionFields = function (_, __) {
            var _a = _this.props, data = _a.data, organization = _a.organization, project = _a.project, disabled = _a.disabled;
            var isInitialized = (data === null || data === void 0 ? void 0 : data.targetType) !== undefined && ("" + data.targetType).length > 0;
            return (<MemberTeamFields disabled={disabled} project={project} organization={organization} loading={!isInitialized} ruleData={data} onChange={_this.handleMemberTeamChange} options={[
                { value: MailActionTargetType.IssueOwners, label: t('Issue Owners') },
                { value: MailActionTargetType.Team, label: t('Team') },
                { value: MailActionTargetType.Member, label: t('Member') },
            ]} memberValue={MailActionTargetType.Member} teamValue={MailActionTargetType.Team}/>);
        };
        _this.getAssigneeFilterFields = function (_, __) {
            var _a = _this.props, data = _a.data, organization = _a.organization, project = _a.project, disabled = _a.disabled;
            var isInitialized = (data === null || data === void 0 ? void 0 : data.targetType) !== undefined && ("" + data.targetType).length > 0;
            return (<MemberTeamFields disabled={disabled} project={project} organization={organization} loading={!isInitialized} ruleData={data} onChange={_this.handleMemberTeamChange} options={[
                { value: AssigneeTargetType.Unassigned, label: t('No One') },
                { value: AssigneeTargetType.Team, label: t('Team') },
                { value: AssigneeTargetType.Member, label: t('Member') },
            ]} memberValue={AssigneeTargetType.Member} teamValue={AssigneeTargetType.Team}/>);
        };
        _this.getField = function (name, fieldConfig) {
            var getFieldTypes = {
                choice: _this.getChoiceField,
                number: _this.getNumberField,
                string: _this.getTextField,
                mailAction: _this.getMailActionFields,
                assignee: _this.getAssigneeFilterFields,
            };
            return getFieldTypes[fieldConfig.type](name, fieldConfig);
        };
        /**
         * Update all the AlertRuleAction's fields from the TicketRuleModal together
         * only after the user clicks "Apply Changes".
         * @param formData Form data
         * @param fetchedFieldOptionsCache Object
         */
        _this.updateParent = function (formData, fetchedFieldOptionsCache) {
            var e_1, _a;
            var _b = _this.props, index = _b.index, onPropertyChange = _b.onPropertyChange;
            // We only know the choices after the form loads.
            formData.dynamic_form_fields = (formData.dynamic_form_fields || []).map(function (field) {
                // Overwrite the choices because the user's pick is in this list.
                if (field.name in formData && (fetchedFieldOptionsCache === null || fetchedFieldOptionsCache === void 0 ? void 0 : fetchedFieldOptionsCache.hasOwnProperty(field.name))) {
                    field.choices = fetchedFieldOptionsCache[field.name];
                }
                return field;
            });
            try {
                for (var _c = __values(Object.entries(formData)), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var _e = __read(_d.value, 2), name_1 = _e[0], value = _e[1];
                    onPropertyChange(index, name_1, value);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                }
                finally { if (e_1) throw e_1.error; }
            }
        };
        return _this;
    }
    RuleNode.prototype.renderRow = function () {
        var _this = this;
        var _a = this.props, data = _a.data, node = _a.node;
        if (!node) {
            return (<Separator>
          This node failed to render. It may have migrated to another section of the alert
          conditions
        </Separator>);
        }
        var label = node.label, formFields = node.formFields;
        var parts = label.split(/({\w+})/).map(function (part, i) {
            if (!/^{\w+}$/.test(part)) {
                return <Separator key={i}>{part}</Separator>;
            }
            var key = part.slice(1, -1);
            // If matcher is "is set" or "is not set", then we do not want to show the value input
            // because it is not required
            if (key === 'value' && data && (data.match === 'is' || data.match === 'ns')) {
                return null;
            }
            return (<Separator key={key}>
          {formFields && formFields.hasOwnProperty(key)
                ? _this.getField(key, formFields[key])
                : part}
        </Separator>);
        });
        var _b = __read(parts), title = _b[0], inputs = _b.slice(1);
        // We return this so that it can be a grid
        return (<React.Fragment>
        {title}
        {inputs}
      </React.Fragment>);
    };
    RuleNode.prototype.conditionallyRenderHelpfulBanner = function () {
        var _a = this.props, data = _a.data, project = _a.project, organization = _a.organization;
        /**
         * Would prefer to check if data is of `IssueAlertRuleAction` type, however we can't do typechecking at runtime as
         * user defined types are erased through transpilation.
         * Instead, we apply duck typing semantics here.
         * See: https://stackoverflow.com/questions/51528780/typescript-check-typeof-against-custom-type
         */
        if (!(data === null || data === void 0 ? void 0 : data.targetType) || data.id !== 'sentry.mail.actions.NotifyEmailAction') {
            return null;
        }
        switch (data.targetType) {
            case MailActionTargetType.IssueOwners:
                return (<MarginlessAlert type="warning">
            {tct('If there are no matching [issueOwners], ownership is determined by the [ownershipSettings].', {
                    issueOwners: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/">
                    {t('issue owners')}
                  </ExternalLink>),
                    ownershipSettings: (<ExternalLink href={"/settings/" + organization.slug + "/projects/" + project.slug + "/ownership/"}>
                    {t('ownership settings')}
                  </ExternalLink>),
                })}
          </MarginlessAlert>);
            case MailActionTargetType.Team:
                return null;
            case MailActionTargetType.Member:
                return null;
            default:
                return null;
        }
    };
    RuleNode.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, disabled = _a.disabled, index = _a.index, node = _a.node, organization = _a.organization;
        var ticketRule = node === null || node === void 0 ? void 0 : node.hasOwnProperty('actionType');
        return (<RuleRowContainer>
        <RuleRow>
          <Rule>
            {data && <input type="hidden" name="id" value={data.id}/>}
            {this.renderRow()}
            {ticketRule && node && (<Button size="small" icon={<IconSettings size="xs"/>} type="button" onClick={function () {
            return openModal(function (deps) { return (<TicketRuleModal {...deps} formFields={node.formFields || {}} link={node.link} ticketType={node.ticketType} instance={data} index={index} onSubmitAction={_this.updateParent} organization={organization}/>); });
        }}>
                {t('Issue Link Settings')}
              </Button>)}
          </Rule>
          <DeleteButton disabled={disabled} label={t('Delete Node')} onClick={this.handleDelete} type="button" size="small" icon={<IconDelete />}/>
        </RuleRow>
        {this.conditionallyRenderHelpfulBanner()}
      </RuleRowContainer>);
    };
    return RuleNode;
}(React.Component));
export default RuleNode;
var InlineInput = styled(Input)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: auto;\n  height: 28px;\n"], ["\n  width: auto;\n  height: 28px;\n"])));
var InlineNumberInput = styled(Input)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 90px;\n  height: 28px;\n"], ["\n  width: 90px;\n  height: 28px;\n"])));
var InlineSelectControl = styled(SelectControl)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 180px;\n"], ["\n  width: 180px;\n"])));
var Separator = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"], ["\n  margin-right: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"])), space(1), space(0.5), space(0.5));
var RuleRow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space(1));
var RuleRowContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"], ["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.innerBorder; });
var Rule = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n  flex-wrap: wrap;\n"])));
var DeleteButton = styled(Button)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var MarginlessAlert = styled(Alert)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=ruleNode.jsx.map