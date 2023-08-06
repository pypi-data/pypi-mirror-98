/**
 * A component to render a Field (i.e. label + help + form "control"),
 * generally inside of a Panel.
 *
 * This is unconnected to any Form state
 */
import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import QuestionTooltip from 'app/components/questionTooltip';
import ControlState from 'app/views/settings/components/forms/field/controlState';
import FieldControl from 'app/views/settings/components/forms/field/fieldControl';
import FieldDescription from 'app/views/settings/components/forms/field/fieldDescription';
import FieldErrorReason from 'app/views/settings/components/forms/field/fieldErrorReason';
import FieldHelp from 'app/views/settings/components/forms/field/fieldHelp';
import FieldLabel from 'app/views/settings/components/forms/field/fieldLabel';
import FieldRequiredBadge from 'app/views/settings/components/forms/field/fieldRequiredBadge';
import FieldWrapper from 'app/views/settings/components/forms/field/fieldWrapper';
import FieldQuestion from './fieldQuestion';
var Field = /** @class */ (function (_super) {
    __extends(Field, _super);
    function Field() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Field.prototype.render = function () {
        var _a = this.props, className = _a.className, otherProps = __rest(_a, ["className"]);
        var controlClassName = otherProps.controlClassName, alignRight = otherProps.alignRight, inline = otherProps.inline, highlighted = otherProps.highlighted, required = otherProps.required, visible = otherProps.visible, disabled = otherProps.disabled, disabledReason = otherProps.disabledReason, error = otherProps.error, flexibleControlStateSize = otherProps.flexibleControlStateSize, help = otherProps.help, id = otherProps.id, isSaving = otherProps.isSaving, isSaved = otherProps.isSaved, label = otherProps.label, hideLabel = otherProps.hideLabel, stacked = otherProps.stacked, children = otherProps.children, style = otherProps.style, showHelpInTooltip = otherProps.showHelpInTooltip;
        var isDisabled = typeof disabled === 'function' ? disabled(this.props) : disabled;
        var isVisible = typeof visible === 'function' ? visible(this.props) : visible;
        var Control;
        if (!isVisible) {
            return null;
        }
        var helpElement = typeof help === 'function' ? help(this.props) : help;
        var controlProps = {
            className: controlClassName,
            inline: inline,
            alignRight: alignRight,
            disabled: isDisabled,
            disabledReason: disabledReason,
            flexibleControlStateSize: flexibleControlStateSize,
            help: helpElement,
            errorState: error ? <FieldErrorReason>{error}</FieldErrorReason> : null,
            controlState: <ControlState error={error} isSaving={isSaving} isSaved={isSaved}/>,
        };
        // See comments in prop types
        if (children instanceof Function) {
            Control = children(__assign(__assign({}, otherProps), controlProps));
        }
        else {
            Control = <FieldControl {...controlProps}>{children}</FieldControl>;
        }
        return (<FieldWrapper className={className} inline={inline} stacked={stacked} highlighted={highlighted} hasControlState={!flexibleControlStateSize} style={style}>
        {((label && !hideLabel) || helpElement) && (<FieldDescription inline={inline} htmlFor={id}>
            {label && !hideLabel && (<FieldLabel disabled={isDisabled}>
                <span>
                  {label}
                  {required && <FieldRequiredBadge />}
                </span>
                {helpElement && showHelpInTooltip && (<FieldQuestion>
                    <QuestionTooltip position="top" size="sm" title={helpElement}/>
                  </FieldQuestion>)}
              </FieldLabel>)}
            {helpElement && !showHelpInTooltip && (<FieldHelp stacked={stacked} inline={inline}>
                {helpElement}
              </FieldHelp>)}
          </FieldDescription>)}

        {Control}
      </FieldWrapper>);
    };
    Field.defaultProps = {
        alignRight: false,
        inline: true,
        disabled: false,
        required: false,
        visible: true,
        showHelpInTooltip: false,
    };
    return Field;
}(React.Component));
export default Field;
//# sourceMappingURL=index.jsx.map