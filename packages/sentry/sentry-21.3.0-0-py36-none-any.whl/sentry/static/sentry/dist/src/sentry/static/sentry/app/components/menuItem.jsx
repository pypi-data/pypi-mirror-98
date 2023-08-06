import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Link from 'app/components/links/link';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
var MenuItem = /** @class */ (function (_super) {
    __extends(MenuItem, _super);
    function MenuItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function (e) {
            var _a = _this.props, onSelect = _a.onSelect, disabled = _a.disabled, eventKey = _a.eventKey;
            if (disabled) {
                return;
            }
            if (onSelect) {
                e.preventDefault();
                callIfFunction(onSelect, eventKey);
            }
        };
        _this.renderAnchor = function () {
            var _a = _this.props, to = _a.to, href = _a.href, title = _a.title, disabled = _a.disabled, isActive = _a.isActive, children = _a.children;
            if (to) {
                return (<MenuLink to={to} title={title} onClick={_this.handleClick} tabIndex={-1} isActive={isActive} disabled={disabled}>
          {children}
        </MenuLink>);
            }
            if (href) {
                return (<MenuAnchor href={href} onClick={_this.handleClick} tabIndex={-1} isActive={isActive} disabled={disabled}>
          {children}
        </MenuAnchor>);
            }
            return (<MenuTarget role="button" title={title} onClick={_this.handleClick} tabIndex={-1} isActive={isActive} disabled={disabled}>
        {_this.props.children}
      </MenuTarget>);
        };
        return _this;
    }
    MenuItem.prototype.render = function () {
        var _a = this.props, header = _a.header, divider = _a.divider, isActive = _a.isActive, noAnchor = _a.noAnchor, className = _a.className, children = _a.children, props = __rest(_a, ["header", "divider", "isActive", "noAnchor", "className", "children"]);
        var renderChildren = null;
        if (noAnchor) {
            renderChildren = children;
        }
        else if (header) {
            renderChildren = children;
        }
        else if (!divider) {
            renderChildren = this.renderAnchor();
        }
        return (<MenuListItem className={className} role="presentation" isActive={isActive} divider={divider} noAnchor={noAnchor} header={header} {...omit(props, ['href', 'title', 'onSelect', 'eventKey', 'to'])}>
        {renderChildren}
      </MenuListItem>);
    };
    return MenuItem;
}(React.Component));
function getListItemStyles(props) {
    var common = "\n    display: block;\n    padding: " + space(0.5) + " " + space(2) + ";\n    &:focus {\n      outline: none;\n    }\n  ";
    if (props.disabled) {
        return "\n      " + common + "\n      color: " + props.theme.disabled + ";\n      background: transparent;\n      cursor: not-allowed;\n    ";
    }
    if (props.isActive) {
        return "\n      " + common + "\n      color: " + props.theme.white + ";\n      background: " + props.theme.active + ";\n\n      &:hover {\n        color: " + props.theme.black + ";\n      }\n    ";
    }
    return "\n    " + common + "\n\n    &:hover {\n      background: " + props.theme.focus + ";\n    }\n  ";
}
function getChildStyles(props) {
    if (!props.noAnchor) {
        return '';
    }
    return "\n    & a {\n      " + getListItemStyles(props) + "\n    }\n  ";
}
var MenuAnchor = styled('a', {
    shouldForwardProp: function (p) { return ['isActive', 'disabled'].includes(p) === false; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getListItemStyles);
var MenuListItem = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n\n  ", "\n  ", "\n\n  ", "\n"], ["\n  display: block;\n\n  ",
    "\n  ",
    "\n\n  ", "\n"])), function (p) {
    return p.divider &&
        "\nheight: 1px;\nmargin: " + space(0.5) + " 0;\noverflow: hidden;\nbackground-color: " + p.theme.innerBorder + ";\n    ";
}, function (p) {
    return p.header &&
        "\n    padding: " + space(0.25) + " " + space(1) + ";\n    font-size: " + p.theme.fontSizeSmall + ";\n    line-height: 1.4;\n    color: " + p.theme.gray300 + ";\n  ";
}, getChildStyles);
var MenuTarget = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n  display: flex;\n"], ["\n  ", "\n  display: flex;\n"])), getListItemStyles);
var MenuLink = styled(Link, {
    shouldForwardProp: function (p) { return ['isActive', 'disabled'].includes(p) === false; },
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getListItemStyles);
export default MenuItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=menuItem.jsx.map