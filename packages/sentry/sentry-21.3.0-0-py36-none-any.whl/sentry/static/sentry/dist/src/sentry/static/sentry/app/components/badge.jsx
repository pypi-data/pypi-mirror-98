import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Badge = styled(function (_a) {
    var text = _a.text, props = __rest(_a, ["text"]);
    return <span {...props}>{text}</span>;
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  height: 20px;\n  min-width: 20px;\n  line-height: 20px;\n  border-radius: 20px;\n  padding: 0 5px;\n  margin-left: ", ";\n  font-size: 75%;\n  font-weight: 600;\n  text-align: center;\n  color: #fff;\n  background: ", ";\n  transition: background 100ms linear;\n\n  position: relative;\n  top: -1px;\n"], ["\n  display: inline-block;\n  height: 20px;\n  min-width: 20px;\n  line-height: 20px;\n  border-radius: 20px;\n  padding: 0 5px;\n  margin-left: ", ";\n  font-size: 75%;\n  font-weight: 600;\n  text-align: center;\n  color: #fff;\n  background: ", ";\n  transition: background 100ms linear;\n\n  position: relative;\n  top: -1px;\n"])), space(0.5), function (p) { return p.theme.badge.default.background; });
export default Badge;
var templateObject_1;
//# sourceMappingURL=badge.jsx.map