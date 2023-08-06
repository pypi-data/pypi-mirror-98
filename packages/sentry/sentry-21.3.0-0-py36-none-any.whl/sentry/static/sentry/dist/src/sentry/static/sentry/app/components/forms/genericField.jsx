import { __assign, __rest } from "tslib";
import React from 'react';
import BooleanField from 'app/components/forms/booleanField';
import EmailField from 'app/components/forms/emailField';
import NumberField from 'app/components/forms/numberField';
import PasswordField from 'app/components/forms/passwordField';
import SelectAsyncField from 'app/components/forms/selectAsyncField';
import SelectCreatableField from 'app/components/forms/selectCreatableField';
import SelectField from 'app/components/forms/selectField';
import TextareaField from 'app/components/forms/textareaField';
import TextField from 'app/components/forms/textField';
import { defined } from 'app/utils';
var GenericField = function (_a) {
    var config = _a.config, _b = _a.formData, formData = _b === void 0 ? {} : _b, _c = _a.formErrors, formErrors = _c === void 0 ? {} : _c, formState = _a.formState, onChange = _a.onChange;
    var required = defined(config.required) ? config.required : true;
    var fieldProps = __assign(__assign({}, config), { value: formData[config.name], onChange: onChange, label: config.label + (required ? '*' : ''), placeholder: config.placeholder, required: required, name: config.name, error: (formErrors || {})[config.name], defaultValue: config.default, disabled: config.readonly, key: config.name, formState: formState, help: defined(config.help) && config.help !== '' ? (<span dangerouslySetInnerHTML={{ __html: config.help }}/>) : null });
    switch (config.type) {
        case 'secret':
            return <PasswordField {...fieldProps}/>;
        case 'bool':
            return <BooleanField {...fieldProps}/>;
        case 'email':
            return <EmailField {...fieldProps}/>;
        case 'string':
        case 'text':
        case 'url':
            if (fieldProps.choices) {
                return <SelectCreatableField deprecatedSelectControl {...fieldProps}/>;
            }
            return <TextField {...fieldProps}/>;
        case 'number':
            return <NumberField {...fieldProps}/>;
        case 'textarea':
            return <TextareaField {...fieldProps}/>;
        case 'choice':
        case 'select':
            // the chrome required tip winds up in weird places
            // for select elements, so just make it look like
            // it's required (with *) and rely on server validation
            var _1 = fieldProps.required, selectProps = __rest(fieldProps, ["required"]);
            if (config.has_autocomplete) {
                // Redeclaring field props here as config has been narrowed to include the correct options for SelectAsyncField
                var selectFieldProps = __assign(__assign({}, config), selectProps);
                return <SelectAsyncField deprecatedSelectControl {...selectFieldProps}/>;
            }
            return <SelectField deprecatedSelectControl {...selectProps}/>;
        default:
            return null;
    }
};
export default GenericField;
//# sourceMappingURL=genericField.jsx.map