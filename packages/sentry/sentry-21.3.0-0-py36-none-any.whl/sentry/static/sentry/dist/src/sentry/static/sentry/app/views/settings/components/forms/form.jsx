import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Observer } from 'mobx-react';
import PropTypes from 'prop-types';
import Button from 'app/components/button';
import Panel from 'app/components/panels/panel';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isRenderFunc } from 'app/utils/isRenderFunc';
import FormModel from 'app/views/settings/components/forms/model';
var Form = /** @class */ (function (_super) {
    __extends(Form, _super);
    function Form(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.model = _this.props.model || new FormModel();
        _this.onSubmit = function (e) {
            var _a, _b;
            !_this.props.skipPreventDefault && e.preventDefault();
            if (_this.model.isSaving) {
                return;
            }
            (_b = (_a = _this.props).onPreSubmit) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (_this.props.onSubmit) {
                _this.props.onSubmit(_this.model.getData(), _this.onSubmitSuccess, _this.onSubmitError, e, _this.model);
            }
            else {
                _this.model.saveForm();
            }
        };
        _this.onSubmitSuccess = function (data) {
            var onSubmitSuccess = _this.props.onSubmitSuccess;
            _this.model.submitSuccess(data);
            if (onSubmitSuccess) {
                onSubmitSuccess(data, _this.model);
            }
        };
        _this.onSubmitError = function (error) {
            var onSubmitError = _this.props.onSubmitError;
            _this.model.submitError(error);
            if (onSubmitError) {
                onSubmitError(error, _this.model);
            }
        };
        var saveOnBlur = props.saveOnBlur, apiEndpoint = props.apiEndpoint, apiMethod = props.apiMethod, resetOnError = props.resetOnError, onSubmitSuccess = props.onSubmitSuccess, onSubmitError = props.onSubmitError, onFieldChange = props.onFieldChange, initialData = props.initialData, allowUndo = props.allowUndo;
        _this.model.setInitialData(initialData);
        _this.model.setFormOptions({
            resetOnError: resetOnError,
            allowUndo: allowUndo,
            onFieldChange: onFieldChange,
            onSubmitSuccess: onSubmitSuccess,
            onSubmitError: onSubmitError,
            saveOnBlur: saveOnBlur,
            apiEndpoint: apiEndpoint,
            apiMethod: apiMethod,
        });
        return _this;
    }
    Form.prototype.getChildContext = function () {
        return {
            saveOnBlur: this.props.saveOnBlur,
            form: this.model,
        };
    };
    Form.prototype.componentWillUnmount = function () {
        this.model.reset();
    };
    Form.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, children = _a.children, footerClass = _a.footerClass, footerStyle = _a.footerStyle, submitDisabled = _a.submitDisabled, submitLabel = _a.submitLabel, submitPriority = _a.submitPriority, cancelLabel = _a.cancelLabel, onCancel = _a.onCancel, extraButton = _a.extraButton, requireChanges = _a.requireChanges, saveOnBlur = _a.saveOnBlur, hideFooter = _a.hideFooter;
        var shouldShowFooter = typeof hideFooter !== 'undefined' ? !hideFooter : !saveOnBlur;
        return (<form onSubmit={this.onSubmit} className={className !== null && className !== void 0 ? className : 'form-stacked'} data-test-id={this.props['data-test-id']}>
        <div>
          {isRenderFunc(children) ? children({ model: this.model }) : children}
        </div>

        {shouldShowFooter && (<StyledFooter className={footerClass} style={footerStyle} saveOnBlur={saveOnBlur}>
            {extraButton}
            <DefaultButtons>
              {onCancel && (<Observer>
                  {function () { return (<Button type="button" disabled={_this.model.isSaving} onClick={onCancel} style={{ marginLeft: 5 }}>
                      {cancelLabel !== null && cancelLabel !== void 0 ? cancelLabel : t('Cancel')}
                    </Button>); }}
                </Observer>)}

              <Observer>
                {function () { return (<Button data-test-id="form-submit" priority={submitPriority !== null && submitPriority !== void 0 ? submitPriority : 'primary'} disabled={_this.model.isError ||
            _this.model.isSaving ||
            submitDisabled ||
            (requireChanges ? !_this.model.formChanged : false)} type="submit">
                    {submitLabel !== null && submitLabel !== void 0 ? submitLabel : t('Save Changes')}
                  </Button>); }}
              </Observer>
            </DefaultButtons>
          </StyledFooter>)}
      </form>);
    };
    Form.childContextTypes = {
        saveOnBlur: PropTypes.bool,
        form: PropTypes.object,
    };
    return Form;
}(React.Component));
export default Form;
var StyledFooter = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 25px;\n  border-top: 1px solid #e9ebec;\n  background: none;\n  padding: 16px 0 0;\n  margin-bottom: 16px;\n\n  ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 25px;\n  border-top: 1px solid #e9ebec;\n  background: none;\n  padding: 16px 0 0;\n  margin-bottom: 16px;\n\n  ",
    ";\n"])), function (p) {
    return !p.saveOnBlur &&
        "\n  " + Panel + " & {\n    margin-top: 0;\n    padding-right: 36px;\n  }\n\n  /* Better padding with form inside of a modal */\n  .modal-content & {\n    padding-right: 30px;\n    margin-left: -30px;\n    margin-right: -30px;\n    margin-bottom: -30px;\n    margin-top: 16px;\n    padding-bottom: 16px;\n  }\n  ";
});
var DefaultButtons = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  flex: 1;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  flex: 1;\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=form.jsx.map