import { __makeTemplateObject } from "tslib";
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var shouldForwardProp = function (p) { return p !== 'disabled' && isPropValid(p); };
var FieldLabel = styled('div', { shouldForwardProp: shouldForwardProp })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"], ["\n  color: ", ";\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"])), function (p) { return (!p.disabled ? p.theme.textColor : p.theme.disabled); }, space(0.5));
export default FieldLabel;
var templateObject_1;
//# sourceMappingURL=fieldLabel.jsx.map